# Implementation Plan: Supply Chain Risk Monolith

## 🛠️ Phase 1: Project Scaffolding
*Goal: Initialize the repository, virtual environment, and dependency structure to support the Modular Monolith architecture.*

### Step 1.1: Initialize Project Structure
- **Command:** `poetry new cx-lifecycle --src`
- **Command:** `mv cx-lifecycle/src/cx_lifecycle cx-lifecycle/src/app` (Rename default package to `app` to match Architecture)
- **Command:** `cd cx-lifecycle`
- **Command:** `git init`
- **Action:** Create `.gitignore` ignoring `__pycache__`, `*.pyc`, `.env`, `.venv/`, `.pytest_cache/`, `dist/`.

### Step 1.2: Install Dependencies
- **Command:** `poetry add fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg pydantic-settings alembic google-genai google-cloud-aiplatform`
- **Command:** `poetry add --group dev pytest pytest-asyncio httpx greenlet dirty-equals mypy pytest-mock`

### Step 1.3: Project Hygiene & Configuration
- **Action:** Delete `tests/test_cx_lifecycle.py` (default created by poetry).
- **Action:** Create `src/app/__init__.py`.
- **Action:** Create `pytest.ini`:
  ```ini
  [pytest]
  pythonpath = src
  testpaths = tests
  asyncio_mode = auto
  ```
- **Action:** Create `.env.example` with placeholders for `DATABASE_URL`, `GOOGLE_API_KEY`, `PROJECT_ID`.

---

## 🧪 Phase 2: Domain Schemas (Pydantic V2)
*Goal: Implement strict Data Contracts and Validation Logic.*

### Step 2.1: Shipment Schema
- **Test:** Create `tests/unit/schemas/test_shipment_schema.py`.
  - Case: Valid shipment data -> Pass.
  - Case: Missing destination -> Fail (ValidationError).
- **Implement:** Create `src/app/schemas/shipment.py`.
  - Define `ShipmentSchema` with `id`, `destination_port`, `goods_description`.
  - Use `ConfigDict(from_attributes=True)`.
- **Verify:** `pytest tests/unit/schemas/test_shipment_schema.py`

### Step 2.2: Risk Assessment Schemas
- **Test:** Create `tests/unit/schemas/test_assessment_schema.py`.
  - Case: `DisruptionEvent` with `confidence_score` < 0 -> Fail.
  - Case: `RiskAssessmentRequest` with empty/short text -> Fail (Validation for `min_length=10`).
  - Case: `DisruptionEvent` valid creation.
- **Implement:** Create `src/app/schemas/assessment.py`.
  - Define `DisruptionEvent`, `MitigationAdvice`, `RiskAssessmentRequest`, `RiskAssessmentResponse`.
  - **Constraint:** Use `field_validator` or strict types. No `pass`.
- **Verify:** `pytest tests/unit/schemas/test_assessment_schema.py`

---

## 💾 Phase 3: Persistence & Infrastructure
*Goal: Implement SQLAlchemy Async Models and Database Connectivity.*

### Step 3.1: Database Configuration
- **Action:** Create `src/app/core/config.py` using `BaseSettings` to load `DATABASE_URL`.
- **Action:** Create `src/app/db/base.py` defining `Base = declarative_base()`.
- **Action:** Create `src/app/db/session.py` with `AsyncEngine` and `get_db` dependency.

### Step 3.2: Shipment Model
- **Test:** Create `tests/integration/db/test_shipment_model.py`.
  - Case: Create `ShipmentModel` instance, persist to in-memory SQLite (or Dockerized PG), retrieve.
- **Implement:** Create `src/app/models/shipment.py`.
  - Define `ShipmentModel` with `Mapped` types.
- **Action:** Initialize Alembic: `poetry run alembic init src/alembic`.
- **Action:** Update `src/alembic/env.py` to import `Base` and set `target_metadata`.

### Step 3.3: Risk Assessment Model
- **Test:** Create `tests/integration/db/test_assessment_model.py`.
  - Case: Persist `RiskAssessmentModel` with JSONB data for `detected_event`.
  - Verify JSONB data integrity upon retrieval.
- **Implement:** Create `src/app/models/assessment.py`.
  - Define `RiskAssessmentModel` using `JSONB` for `detected_event` and `mitigation_strategy`.
- **Verify:** Run integration tests.

### Step 3.4: Shipment Repository
- **Test:** Create `tests/integration/repositories/test_shipment_repo.py`.
  - Case: `get_by_destination("Rotterdam")` returns correct shipments.
  - Case: `get_by_destination("Unknown")` returns empty list.
- **Implement:** Create `src/app/repositories/shipment_repo.py`.
  - Class `ShipmentRepository`.
  - Method `get_by_destination(port_name: str) -> Sequence[ShipmentModel]`.
  - **Constraint:** Implementation must use `select(ShipmentModel).where(...)`.

---

## ⚙️ Phase 4: Service Layer (Business Logic & AI)
*Goal: Implement pure logic, orchestrating AI and DB interactions.*

### Step 4.1: Intelligent Extraction Service (GenAI Wrapper)
- **Test:** Create `tests/unit/services/test_extraction_service.py`.
  - Use `pytest-mock` to mock `google_genai.Client` or the underlying HTTP call.
  - Case: `parse_snippet` returns valid `DisruptionEvent` when LLM responds correctly.
  - Case: Handle LLM failure/timeout (raise custom `ExtractionError`).
- **Implement:** Create `src/app/services/extraction_service.py`.
  - Class `IntelligentExtractionService`.
  - Method `parse_snippet(text: str) -> DisruptionEvent`.
  - **Constraint:** Use actual `google-genai` types and Pydantic validation on response.

### Step 4.2: Risk Assessment Service (Core Logic)
- **Test:** Create `tests/unit/services/test_risk_service.py`.
  - Mock `IntelligentExtractionService`, `ShipmentRepository`, `AsyncSession`.
  - Case: **BR-001** Empty text -> Value Error.
  - Case: **BR-005/006** Valid "Strike" event -> calls `repo.get_by_destination` -> generates "Action Required" advice -> saves to DB.
  - Case: **BR-007** Non-disruptive event -> skips repo lookup -> generates "No action" advice -> saves to DB.
- **Implement:** Create `src/app/services/risk_service.py`.
  - Class `RiskAssessmentService`.
  - Method `create_assessment(news_text: str)`.
  - Implement `_generate_strategy` internal logic.
  - **Constraint:** Fully implement the orchestration logic. No `...` or `pass`.

---

## 🚀 Phase 5: API & Wiring
*Goal: Expose endpoints via FastAPI.*

### Step 5.1: Dependency Injection
- **Implement:** Create `src/app/deps.py`.
  - `get_shipment_repo(db=Depends(get_db))`
  - `get_extraction_service()` (Configure API Key here).
  - `get_risk_service(db=..., repo=..., extractor=...)`.

### Step 5.2: Assessment Endpoint
- **Test:** Create `tests/e2e/test_assessment_api.py`.
  - Use `httpx.AsyncClient` and override `get_risk_service` dependency with a mock.
  - Case: POST `/api/v1/assessments/` with valid JSON -> 201 Created + Response Body.
  - Case: POST with invalid payload -> 422 Unprocessable Entity.
- **Implement:** Create `src/app/api/v1/endpoints/assessment.py`.
  - Router definition.
  - POST handler utilizing `RiskAssessmentService`.

### Step 5.3: Main Application
- **Implement:** Create `src/app/main.py`.
  - Initialize `FastAPI` app.
  - Include routers.
  - Add `lifespan` for DB connection management if needed.

---

## 🐳 Phase 6: Finalization
*Goal: Dockerize and ensure Quality.*

### Step 6.1: Dockerfile
- **Action:** Create `Dockerfile`.
  - Base: `python:3.12-slim`.
  - Install system deps (if needed for `asyncpg`).
  - Copy `pyproject.toml` and install via `poetry`.
  - CMD: `uvicorn src.app.main:app --host 0.0.0.0`.

### Step 6.2: Quality Check
- **Command:** `pytest` (Must pass all).
- **Command:** `mypy src` (Must have zero errors).
- **Manual Verification:** Grep for `TODO`, `pass`, `...` in `src/`.

---

## ✅ Success Criteria
1. **Zero Placeholders:** logic branches in `RiskAssessmentService` are fully coded.
2. **Type Safety:** `mypy` strict checks pass.
3. **Test Coverage:** Core business logic (Service Layer) has 100% branch coverage.
