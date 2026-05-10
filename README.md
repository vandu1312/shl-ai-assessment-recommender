
# SHL Assessment Recommendation System

## Project Description

This project is a FastAPI-based intelligent recommendation system that suggests relevant SHL assessments based on user job requirements, skills, and behavioral needs. It uses context extraction, rule-based intent detection, and semantic keyword matching to deliver accurate assessment recommendations from the SHL catalog.

The system supports multi-turn conversations, understands role requirements, and can differentiate between technical, personality, and stakeholder-related hiring needs.

---

## Table of Contents
- Installation
- Usage
- Project Structure
- Features
- API Endpoints
- Author Links

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-repo/shl-ai-assessment.git
cd shl-ai-assessment
````

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
uvicorn app:app --reload --port 8001
```

---

## Usage

### Swagger UI

After running the server, open:

```
http://127.0.0.1:8001/docs
```

### Example API Request

```bash
curl -X POST "http://127.0.0.1:8001/chat" \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {
      "role": "user",
      "content": "Need someone good at collaborating with stakeholders"
    }
  ]
}'
```

### Example Response

```json
{
  "reply": "I found 10 SHL assessments matching your needs.",
  "recommendations": [
    {
      "name": "Occupational Personality Questionnaire OPQ32r",
      "url": "https://www.shl.com/solutions/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
      "test_type": "P"
    }
  ],
  "end_of_conversation": false
}
```

---

## Project Structure

* **app.py** → Main FastAPI application containing API endpoints and search logic
* **src/utils.py** → Handles context building, intent detection, and conversation understanding
* **data/shl_assessments.csv** → SHL assessment catalog used for recommendations
* **src/retriever.py** →  Handles retrieval logic for matching assessments
* **venv/** → Python virtual environment (not included in deployment)

---

## Features

* Multi-turn conversation support
* Role and skill-based context extraction
* Behavioral intent detection (personality, stakeholder, communication)
* Semantic keyword-based recommendation system
* SHL catalog-based filtering
* Safety and refusal handling for irrelevant queries
* FastAPI REST backend with Swagger UI

---

## API Endpoints

### GET /health

Checks if system is running

### POST /chat

Returns SHL assessment recommendations based on user input

---

## Author Links

LinkedIn: [https://www.linkedin.com/in/vandana-harijana/](https://www.linkedin.com/in/vandana-harijana/)
GitHub: [https://github.com/vandu1312](https://github.com/vandu1312)


