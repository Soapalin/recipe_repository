from urllib.parse import urlparse
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
import requests
import hmac
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# from schema.recipe import RecipeSchema
load_dotenv()
import os

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")
N8N_WEBHOOK_URL = os.getenv("N8N_URL")
SHORTCUTS_API_TOKEN = os.getenv("SHORTCUTS_API_TOKEN")


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


recipe_api = Blueprint("recipe", __name__, url_prefix="/recipe")

from schema.db import SessionLocal
from schema.recipe import Recipe

def _collect_payload() -> Dict[str, Any]:
    logger.info("request.is_json: %s", request.is_json)
    logger.info("request.form: %s", request.form)
    logger.info("request.data: %s", request.data)
    if request.is_json:
        data = request.get_json(silent=True) or {}
        if isinstance(data, dict):
            return data
        return {"payload": data}

    if request.form:
        return request.form.to_dict(flat=True)

    if request.data:
        return {"raw": request.data.decode("utf-8", errors="replace")}

    return {}

def _is_allowed_origin(value: str) -> bool:
    try:
        parsed = urlparse(value)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        return origin == FRONTEND_ORIGIN
    except Exception:
        return False

def _enforce_origin() -> None:
    origin = request.headers.get("Origin")
    print(f"origin: {origin}")
    referer = request.headers.get("Referer")

    if origin:
        if not _is_allowed_origin(origin):
            raise PermissionError("Origin not allowed")
        return

    if referer:
        if not _is_allowed_origin(referer):
            raise PermissionError("Referer not allowed")
        return
    raise PermissionError("Missing Origin/Referer")


def _require_bearer_token() -> None:
    if not SHORTCUTS_API_TOKEN:
        raise RuntimeError("SHORTCUTS_API_TOKEN is not configured")

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise PermissionError("Missing Bearer token")

    token = auth_header.removeprefix("Bearer ").strip()
    if not hmac.compare_digest(token, SHORTCUTS_API_TOKEN):
        raise PermissionError("Invalid Bearer token")


def _serialize_recipe(recipe: Recipe) -> Dict[str, Any]:
    return {
        "id": recipe.id,
        "title": recipe.title,
        "url": recipe.url,
        "author": recipe.author,
        "description": recipe.description,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "created_at": recipe.created_at.isoformat() if recipe.created_at else None,
        "updated_at": recipe.updated_at.isoformat() if recipe.updated_at else None,
    }




def _apply_recipe_updates(recipe: Recipe, payload: Dict[str, Any]) -> None:
    for field in ("title", "url", "author", "description", "ingredients", "instructions"):
        if field in payload:
            setattr(recipe, field, payload.get(field))


@recipe_api.route("/share", methods=["POST"])
def share() -> Any:
    try:
        _require_bearer_token()
    except PermissionError as exc:
        return jsonify(ok=False, error=str(exc)), 401
    except RuntimeError as exc:
        return jsonify(ok=False, error=str(exc)), 500

    payload = _collect_payload()
    logging.info("Received payload: %s, %s", payload, type(payload))

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
    except requests.RequestException as exc:
        return jsonify(ok=False, error=str(exc)), 502
    
    logger.info(response.text)
    return jsonify(ok=response.ok, status=response.status_code)


@recipe_api.route("", methods=["POST"])
def create_recipe() -> Any:
    payload = _collect_payload()
    print(payload)
    title = payload.get("title")
    if not title:
        return jsonify(ok=False, error="title is required"), 400

    session: Session = SessionLocal()
    try:
        recipe = Recipe(
            title=title,
            url=payload.get("url"),
            author=payload.get("author"),
            description=payload.get("description"),
            ingredients=payload.get("ingredients"),
            instructions=payload.get("instructions"),
        )
        session.add(recipe)
        session.commit()
        session.refresh(recipe)
        return jsonify(ok=True, recipe=_serialize_recipe(recipe)), 201
    except SQLAlchemyError as exc:
        session.rollback()
        logger.exception("Failed to create recipe")
        return jsonify(ok=False, error=str(exc)), 500
    finally:
        session.close()


@recipe_api.route("", methods=["GET"])
def list_recipes() -> Any:
    session: Session = SessionLocal()
    try:
        recipes = session.query(Recipe).order_by(Recipe.created_at.desc()).all()
        return jsonify(ok=True, recipes=[_serialize_recipe(r) for r in recipes])
    except SQLAlchemyError as exc:
        logger.exception("Failed to list recipes")
        return jsonify(ok=False, error=str(exc)), 500
    finally:
        session.close()


@recipe_api.route("/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id: int) -> Any:
    session: Session = SessionLocal()
    try:
        recipe = session.get(Recipe, recipe_id)
        if not recipe:
            return jsonify(ok=False, error="Recipe not found"), 404
        return jsonify(ok=True, recipe=_serialize_recipe(recipe))
    except SQLAlchemyError as exc:
        logger.exception("Failed to fetch recipe")
        return jsonify(ok=False, error=str(exc)), 500
    finally:
        session.close()


@recipe_api.route("/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id: int) -> Any:
    payload = _collect_payload()
    if not payload:
        return jsonify(ok=False, error="No updates provided"), 400

    session: Session = SessionLocal()
    try:
        recipe = session.get(Recipe, recipe_id)
        if not recipe:
            return jsonify(ok=False, error="Recipe not found"), 404
        _apply_recipe_updates(recipe, payload)
        session.commit()
        session.refresh(recipe)
        return jsonify(ok=True, recipe=_serialize_recipe(recipe))
    except SQLAlchemyError as exc:
        session.rollback()
        logger.exception("Failed to update recipe")
        return jsonify(ok=False, error=str(exc)), 500
    finally:
        session.close()


@recipe_api.route("/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id: int) -> Any:
    session: Session = SessionLocal()
    try:
        recipe = session.get(Recipe, recipe_id)
        if not recipe:
            return jsonify(ok=False, error="Recipe not found"), 404
        session.delete(recipe)
        session.commit()
        return jsonify(ok=True)
    except SQLAlchemyError as exc:
        session.rollback()
        logger.exception("Failed to delete recipe")
        return jsonify(ok=False, error=str(exc)), 500
    finally:
        session.close()
