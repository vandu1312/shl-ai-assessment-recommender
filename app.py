from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from src.utils import (
    build_context,
    detect_intent,
    has_enough_context,
    build_comparison_response,
    refusal_response,
)

from src.retriever import retrieve_assessments

app = FastAPI()

# =====================================
# REQUEST SCHEMA
# =====================================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# =====================================
# HEALTH ENDPOINT
# =====================================

@app.get("/health")
def health():

    return {"status": "ok"}


# =====================================
# CHAT ENDPOINT
# =====================================

@app.post("/chat")
def chat(request: ChatRequest):

    messages = [
        msg.dict()
        for msg in request.messages
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
            "end_of_conversation": False
        }

    # =====================================
    # COMPARISON
    # =====================================

    if intent == "comparison":

        return {
            "reply": build_comparison_response(),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =====================================
    # CLARIFICATION
    # =====================================

    if not has_enough_context(context):

        return {
            "reply": (
                "Could you share more details about the role, "
                "skills, or seniority level?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =====================================
    # SEMANTIC RETRIEVAL
    # =====================================

    recommendations = retrieve_assessments(context)

    # =====================================
    # NO RESULTS
    # =====================================

    if len(recommendations) == 0:

        return {
            "reply": (
                "I could not find matching SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =====================================
    # SUCCESS
    # =====================================

    return {
        "reply": (
            f"I found {len(recommendations)} "
            f"SHL assessments matching your needs."
        ),
        "recommendations": recommendations,
        "end_of_conversation": True
    }