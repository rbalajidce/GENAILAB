import json
import logging
import azure.functions as func

from shared.aoai import summarize   # ✅ ONLY THIS (same style)

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:

    logger.info("Summarization function triggered")

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
        # ✅ USE SHARED LOGIC
        result = summarize(query)

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json"
        )

    except Exception as e:
        logger.error("Summarization error: " + str(e))

        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )