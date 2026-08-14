import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from src.utils import (
    build_context,
    detect_intent,
    has_enough_context,
    build_comparison_response,
    refusal_response,
)

from src.retriever import retrieve_assessments


# =========================================
# FASTAPI APP
# =========================================

app = FastAPI(
    title="SHL AI Assessment Recommender",
    version="1.0"
)


# =========================================
# REQUEST SCHEMA
# =========================================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# =========================================
# HEALTH ENDPOINT
# =========================================

@app.get("/health")
def health():
    return {"status": "ok"}


# =========================================
# CHAT ENDPOINT
# =========================================

@app.post("/chat")
def chat(request: ChatRequest):

    messages = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in request.messages
    ]

    # =====================================
    # BUILD CONTEXT
    # =====================================

    context = build_context(messages)

    # =====================================
    # DETECT INTENT
    # =====================================

    intent = detect_intent(context)

    # =====================================
    # REFUSAL
    # =====================================

    if intent == "refusal":

        return {
            "reply": refusal_response(),
            "recommendations": [],
            "end_of_conversation": True
        }

    # =====================================
    # COMPARISON
    # =====================================

    elif intent == "comparison":

        return {
            "reply": build_comparison_response(),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =====================================
    # CLARIFICATION
    # =====================================

    elif not has_enough_context(context):

        return {
            "reply": (
                "Could you share more details "
                "about the role, required skills, "
                "seniority level, or behavioral traits?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =====================================
    # RETRIEVAL
    # =====================================

    recommendations = retrieve_assessments(context)

    # =====================================
    # NO RESULTS
    # =====================================

    if len(recommendations) == 0:

        return {
            "reply": "No matching SHL assessments found.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # =====================================
    # FORMAT RESULTS
    # =====================================

    formatted_recommendations = []

    for rec in recommendations[:10]:

        formatted_recommendations.append(
            {
                "name": rec["name"],
                "url": rec["url"],
                "test_type": rec["test_type"]
            }
        )

    # =====================================
    # SUCCESS RESPONSE
    # =====================================

    return {
        "reply": (
            f"I found {len(formatted_recommendations)} "
            f"matching SHL assessments."
        ),
        "recommendations": formatted_recommendations,
        "end_of_conversation": True
    }


# =========================================
# SERVER ENTRYPOINT FOR RENDER / LOCAL
# =========================================

if __name__ == "__main__":
    # Dynamically bind to Render's PORT env variable (defaults to 10000)
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
