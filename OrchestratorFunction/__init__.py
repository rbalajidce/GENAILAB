import json
import logging
import azure.functions as func

from shared.aoai import classify, summarize, generate_response

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:

    logger.info("Orchestrator function triggered")

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
        # ✅ Step 1: Classification
        classification = classify(query)

        # ✅ Step 2: Summarization
        summary = summarize(query)

        # ✅ Step 3: Extract values safely
        category = classification.get("category", "general")
        priority = classification.get("priority", "low")
        summary_text = summary.get("summary", "No summary")

        # ✅ Step 4: Response generation
        response = generate_response(
            query,
            category,
            priority,
            summary_text
        )

        result = {
            "classification": classification,
            "summary": summary,
            "response": response
        }

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json"
        )

    except Exception as e:
        logger.error("Orchestrator error: " + str(e))

        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )