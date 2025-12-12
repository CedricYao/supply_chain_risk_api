# Supply Chain Risk Monolith

A proactive supply chain risk assessment agent that uses Google's Gemini 1.5 Flash to analyze unstructured news snippets, identify potential disruptions (like strikes or weather events), and correlate them with active shipments to generate actionable mitigation advice.

## 🎯 Purpose

The primary goal of the **Supply Chain Risk Monolith** is to bridge the gap between unstructured external data (global news, weather reports) and structured internal logistics data.

In modern supply chains, critical disruptions often appear in news feeds hours or days before they are reflected in formal tracking systems. This application:
1.  **Monitors** unstructured text inputs for potential risks.
2.  **Structures** raw text into actionable data objects using Generative AI.
3.  **Identifies** specifically which active shipments are in the "blast radius" of a disruption.
4.  **Advises** logistics coordinators immediately, enabling proactive rerouting rather than reactive damage control.

## 🚀 Features

*   **Intelligent Extraction:** Uses GenAI to parse unstructured text into structured events (Port, Event Type, Severity).
*   **Risk Correlation:** Automatically matches detected events against a database of active shipments.
*   **Automated Mitigation:** Generates specific advice (e.g., "Reroute X shipments") based on the impact analysis.
*   **Modern Architecture:** Built with FastAPI, SQLAlchemy Async (2.0+), and Pydantic V2 for strict type safety and performance.

## 🛠️ Tech Stack

*   **Language:** Python 3.12+
*   **Framework:** FastAPI
*   **AI Engine:** Google Gemini 1.5 Flash (via `google-genai` SDK)
*   **Database:** PostgreSQL (production) / SQLite (testing) via SQLAlchemy Async
*   **Validation:** Pydantic V2
*   **Package Manager:** Poetry

## ⚡ Quick Start

### Prerequisites
*   Python 3.12 or higher
*   Poetry

### Installation

1.  Clone the repository and install dependencies:
    ```bash
    poetry install
    ```

2.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Edit .env and set your GOOGLE_API_KEY
    ```

### Running the Application

The application requires `seed_data.yaml` to be present in the root directory for initial data population.

Start the server using Uvicorn:

```bash
export PYTHONPATH=src
poetry run uvicorn app.main:app --reload
```

The server will automatically seed the database with sample shipments from `seed_data.yaml` on startup.

The API will be available at `http://127.0.0.1:8000`.
Health check: `http://127.0.0.1:8000/health`
Interactive Docs: `http://127.0.0.1:8000/docs`

### Testing

Run the full test suite (Unit, Integration, and E2E):

```bash
poetry run pytest
```

## 🐳 Docker

Build and run the container:

```bash
docker build -t cx-lifecycle .
docker run -p 8000:8000 --env-file .env cx-lifecycle
```

## 📦 Usage Example

**Endpoint:** `POST /api/v1/assessments/`

**Request:**
```json
{
  "news_text": "Labor unions have announced a 48-hour walkout at the Port of Rotterdam starting this Friday due to stalled wage negotiations."
}
```

**Response:**
```json
{
  "assessment_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2023-10-27T10:00:00Z",
  "detected_event": {
    "target_port": "Rotterdam",
    "event_type": "Strike",
    "is_disruption": true,
    "confidence_score": 0.98
  },
  "affected_shipments": [],
  "mitigation_strategy": {
    "recommendation_text": "Action Required: Reroute 0 shipments destined for Rotterdam due to Strike.",
    "action_required": true
  }
}
```
