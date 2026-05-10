# SHL AI Assessment Recommendation System

## Project Overview

The SHL AI Assessment Recommendation System is an intelligent FastAPI-based recommendation engine designed to suggest relevant SHL assessments based on hiring requirements, technical skills, behavioral traits, and communication needs.

The system uses:

* Context extraction
* Intent detection
* Semantic similarity search
* Transformer-based embeddings

to provide accurate and relevant assessment recommendations from the SHL assessment catalog.

The application supports:

* Multi-turn conversations
* Behavioral and stakeholder-based hiring analysis
* Technical role matching
* REST API interaction using FastAPI

---

# Live Deployment

## Production API

[Live API Endpoint](https://shl-ai-assessment-recommender-production.up.railway.app/chat?utm_source=chatgpt.com)

## Swagger Documentation

[Swagger Docs](https://shl-ai-assessment-recommender-production.up.railway.app/docs?utm_source=chatgpt.com)

## Health Check

[Health Endpoint](https://shl-ai-assessment-recommender-production.up.railway.app/health?utm_source=chatgpt.com)

---

# Features

* Intelligent SHL assessment recommendation system
* FastAPI REST backend
* Transformer-based semantic retrieval
* Multi-turn conversation support
* Technical skill understanding
* Stakeholder and communication intent detection
* Personality and behavioral recommendation support
* Refusal handling for irrelevant queries
* Swagger API documentation
* Railway cloud deployment

---

# Tech Stack

* Python
* FastAPI
* Sentence Transformers
* Scikit-learn
* Pandas
* Uvicorn
* Railway Deployment

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/vandu1312/shl-ai-assessment-recommender.git

cd shl-ai-assessment-recommender
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run the Application

```bash
uvicorn app:app --reload --port 8001
```

---

# Usage

## Open Swagger UI

After starting the server locally:

```text
http://127.0.0.1:8001/docs
```

---

# Example API Request

```bash
curl -X POST "http://127.0.0.1:8001/chat" \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {
      "role": "user",
      "content": "Need someone good at collaborating with stakeholders and communication"
    }
  ]
}'
```

---

# Example API Response

```json
{
  "reply": "I found 10 matching SHL assessments.",
  "recommendations": [
    {
      "name": "Interpersonal Communications",
      "url": "https://www.shl.com/solutions/products/product-catalog/view/interpersonal-communications/",
      "test_type": "K"
    }
  ],
  "end_of_conversation": true
}
```

---

# API Endpoints

## GET `/health`

Checks whether the system is running successfully.

### Example Response

```json
{
  "status": "ok"
}
```

---

## POST `/chat`

Returns SHL assessment recommendations based on user hiring requirements.

### Request Format

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring Python developer with teamwork and communication skills"
    }
  ]
}
```

---

# Project Structure

```text
shl-ai-assessment-recommender/
│
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
│
├── data/
│   └── shl_assessments.csv
│
├── src/
│   ├── retriever.py
│   └── utils.py
│
└── README.md
```

---

# System Workflow

1. User sends hiring requirement
2. Context extraction identifies:

   * roles
   * technical skills
   * behavioral needs
3. Intent detection classifies query
4. Semantic similarity retrieval matches SHL assessments
5. Top recommendations returned through API

---

# Deployment

This project is deployed using:

* [Railway](https://railway.app?utm_source=chatgpt.com)
* FastAPI
* Uvicorn

---

# Future Improvements

* Hybrid semantic + keyword retrieval
* Embedding caching for faster inference
* Docker container optimization
* Role-specific recommendation tuning
* Conversation memory improvements
* Advanced ranking strategies

---

# Author

## Vandana Harijana

* [GitHub Profile](https://github.com/vandu1312?utm_source=chatgpt.com)
* [LinkedIn Profile](https://www.linkedin.com/in/vandana-harijana/?utm_source=chatgpt.com)

---

# License

This project is intended for educational and assessment purposes.
