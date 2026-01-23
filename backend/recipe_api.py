from urllib.parse import urlparse
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
import requests
import hmac
from typing import Any, Dict
from dotenv import load_dotenv

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
