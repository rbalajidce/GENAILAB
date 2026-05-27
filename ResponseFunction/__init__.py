import json
import logging
import azure.functions as func

from shared.aoai import generate_response

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:   # ✅ FIX arrow also

    logger.info("Response generation function triggered")

    try:
        body = req.get_json()
    except:
        body = {}

    query = body.get("query", "")

    if not query:
        return func.HttpResponse(
            json.dumps({"error": "Missing 'query'"}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        result = generate_response(
            text=query,
            category="general",
            priority="low",
            summary="User request"
        )

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json"
        )

    except Exception as e:
        logger.error("Response generation error: " + str(e))

        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )