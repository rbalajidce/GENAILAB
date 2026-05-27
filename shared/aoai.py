import json
import os
from typing import Any, Dict

import openai

# ✅ Configure Azure OpenAI (OLD SDK STYLE)
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")


# ✅ CALL FUNCTION (FIXED)
def _call_aoai(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_DEPLOYMENT,  # ✅ IMPORTANT (not model)
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Always return strict JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response["choices"][0]["message"]["content"]


def _parse_json(raw: str) -> Dict[str, Any]:
    cleaned = raw.replace("```", "").strip()
    if cleaned.lower().startswith("json"):
        cleaned = cleaned[4:].strip()
    return json.loads(cleaned)


# ✅ CLASSIFICATION
def classify(text: str) -> Dict[str, str]:
    prompt = f"""
    Classify the supplier query into one category:
    [payment, delivery, onboarding, complaint]

    Return JSON only:
    {{"category": "...", "priority": "low/medium/high"}}

    Query: {text}
    """
    result = _call_aoai(prompt)
    return _parse_json(result)


# ✅ SUMMARIZATION
def summarize(text: str) -> Dict[str, str]:
    prompt = f"""
    Summarize this supplier query in 1-2 lines.

    Return JSON:
    {{"summary": "..."}}

    Query: {text}
    """
    result = _call_aoai(prompt)
    return _parse_json(result)


# ✅ RESPONSE
def generate_response(text: str, category: str, priority: str, summary: str) -> Dict[str, str]:
    prompt = f"""
    Generate a professional reply to the supplier.

    Category: {category}
    Priority: {priority}
    Summary: {summary}

    Original query: {text}

    Return JSON:
    {{"response": "..."}}
    """
    result = _call_aoai(prompt)
    return _parse_json(result)


# ✅ ORCHESTRATOR
def orchestrate(query: str) -> Dict[str, Any]:
    classification = classify(query)
    summary = summarize(query)
    response = generate_response(
        query,
        classification.get("category", "general"),
        classification.get("priority", "low"),
        summary.get("summary", ""),
    )

    return {
        "classification": classification,
        "summary": summary,
        "response": response,
    }