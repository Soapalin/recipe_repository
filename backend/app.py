
import os
from typing import Any
from dotenv import load_dotenv
load_dotenv()


from flask import Flask, jsonify, request
from recipe_api import recipe_api
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from schema.db import init_db

import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(recipe_api)
init_db()

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],  # Example: 100 requests per hour per IP
)
limiter.limit("30 per hour")(recipe_api)

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")
CORS(
    app,
    resources={r"/": {"origins": [FRONTEND_ORIGIN]}},
    supports_credentials=False,
)


@app.get("/health")
def health() -> Any:
    return jsonify(status="ok")

@app.route("/test", methods=["POST"])
def test() -> Any:
    logger.info(request.json)
    return jsonify(status="ok")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "9998")))
