
import os
import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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


# =========================================
# FASTAPI APP
# =========================================

app = FastAPI(
    title="SHL AI Assessment Recommender",
    description="AI-powered assessment recommendation system using semantic search.",
    version="1.0"
)


# =========================================
# HOMEPAGE
# =========================================

@app.get("/", response_class=HTMLResponse)
def homepage():

    return """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>SHL AI Assessment Recommender</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: white;
                min-height: 100vh;
            }

            nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 22px 8%;
                background: #111c32;
            }

            nav h2 {
                color: #38bdf8;
                font-size: 22px;
            }

            nav a {
                color: white;
                text-decoration: none;
                margin-left: 22px;
                font-size: 14px;
            }

            .hero {
                min-height: 75vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 40px 20px;
            }

            .tag {
                background: #1e3a5f;
                color: #7dd3fc;
                padding: 9px 18px;
                border-radius: 25px;
                font-size: 13px;
                margin-bottom: 25px;
            }

            h1 {
                font-size: clamp(34px, 6vw, 58px);
                max-width: 850px;
                line-height: 1.2;
                margin-bottom: 22px;
            }

            h1 span {
                color: #38bdf8;
            }

            .description {
                max-width: 650px;
                color: #cbd5e1;
                font-size: 18px;
                line-height: 1.8;
            }

            .buttons {
                margin-top: 35px;
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                justify-content: center;
            }

            .btn {
                padding: 15px 25px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                transition: 0.2s;
            }

            .primary {
                background: #38bdf8;
                color: #082f49;
            }

            .secondary {
                border: 1px solid #64748b;
                color: white;
            }

            .btn:hover {
                transform: translateY(-3px);
            }

            .features {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 20px;
                padding: 35px 20px;
            }

            .feature {
                background: #1e293b;
                border: 1px solid #334155;
                padding: 25px;
                border-radius: 12px;
                width: 260px;
                text-align: center;
            }

            .feature h3 {
                color: #38bdf8;
                margin-bottom: 12px;
            }

            .feature p {
                color: #cbd5e1;
                font-size: 14px;
                line-height: 1.6;
            }

            footer {
                text-align: center;
                padding: 25px;
                color: #94a3b8;
                font-size: 13px;
            }

            @media(max-width: 600px) {
                nav {
                    flex-direction: column;
                    gap: 15px;
                }

                nav a {
                    margin: 0 8px;
                }
            }
        </style>
    </head>

    <body>

        <nav>
            <h2>SHL AI Recommender</h2>

            <div>
                <a href="/">Home</a>
                <a href="/docs">API Docs</a>
                <a href="/health">Health</a>
            </div>
        </nav>

        <section class="hero">

            <div class="tag">
                AI-Powered Assessment Recommendation
            </div>

            <h1>
                Find the Right <span>SHL Assessments</span>
                for Your Hiring Needs
            </h1>

            <p class="description">
                An intelligent assessment recommendation system
                that uses natural language understanding and
                semantic search to identify relevant SHL assessments
                based on job roles, skills, and hiring requirements.
            </p>

            <div class="buttons">
                <a class="btn primary" href="/docs">
                    Explore API
                </a>

                <a class="btn secondary" href="/health">
                    Check System Status
                </a>
            </div>

        </section>

        <section class="features">

            <div class="feature">
                <h3>Semantic Search</h3>
                <p>
                    Understands hiring requirements using
                    sentence embeddings and semantic similarity.
                </p>
            </div>

            <div class="feature">
                <h3>AI Recommendations</h3>
                <p>
                    Retrieves relevant SHL assessments based
                    on skills, roles, and behavioral requirements.
                </p>
            </div>

            <div class="feature">
                <h3>FastAPI Backend</h3>
                <p>
                    Provides structured REST API endpoints
                    for assessment recommendation requests.
                </p>
            </div>

        </section>

        <footer>
            SHL AI Assessment Recommender | Built with FastAPI
        </footer>

    </body>
    </html>
    """


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

    # BUILD CONTEXT

    context = build_context(messages)

    # DETECT INTENT

    intent = detect_intent(context)

    # REFUSAL

    if intent == "refusal":

        return {
            "reply": refusal_response(),
            "recommendations": [],
            "end_of_conversation": True
        }

    # COMPARISON

    elif intent == "comparison":

        return {
            "reply": build_comparison_response(),
            "recommendations": [],
            "end_of_conversation": False
        }

    # CLARIFICATION

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

    # RETRIEVAL

    recommendations = retrieve_assessments(context)

    # NO RESULTS

    if len(recommendations) == 0:

        return {
            "reply": "No matching SHL assessments found.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # FORMAT RESULTS

    formatted_recommendations = []

    for rec in recommendations[:10]:

        formatted_recommendations.append(
            {
                "name": rec["name"],
                "url": rec["url"],
                "test_type": rec["test_type"]
            }
        )

    # SUCCESS RESPONSE

    return {
        "reply": (
            f"I found {len(formatted_recommendations)} "
            f"matching SHL assessments."
        ),
        "recommendations": formatted_recommendations,
        "end_of_conversation": True
    }


# =========================================
# SERVER ENTRYPOINT
# =========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port
    )
