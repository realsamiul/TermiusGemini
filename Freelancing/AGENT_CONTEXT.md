# DocRAG-Legal — Gemini CLI Agent Context
# Read this file completely before doing anything.
# Reference plan: MASTER_PLAN_V2.md in the same directory.

## Non-negotiable constraints
- Storage: Modal ONLY. No Oracle, no SQLite, no Firestore, no oracledb.
- Imports from services.storage use EXACT signatures listed below — no deviations.
- Auth: `from middleware.auth import require_role`
- Gemini clients: `from services.gemini import get_pro, get_flash`
- Never call vertexai.init() outside services/gemini.py.
- All Pydantic models in models/schemas.py only. Never define models in routers.
- All Vertex AI calls wrapped with @with_retry from utils/retry.py.
- Use response_mime_type="application/json" on ALL Flash structured output calls.
- Temperature: 0.1 for Pro synthesis, 0.0 for Flash structured output.
- Python 3.10+ type hints. Use `list[str]` not `List[str]`, `str | None` not `Optional[str]`.

## Files agent must NEVER write or overwrite
These already exist. Do not regenerate, do not modify, do not check their contents.
- backend/services/gemini.py
- backend/services/rag.py
- backend/services/rerank.py
- backend/services/eval_judge.py
- backend/services/storage.py
- backend/routers/query.py

## Storage function signatures (EXACT — wrong signatures cause silent runtime failures)
```
store_interaction(session_id:str, user_id:str, question:str, answer:str, sources:list, eval_result:dict) -> str
store_risk_score(doc_id:str, clause_ref:str, clause_text:str, risk_level:str, conflicts:list, gaps:list, recommendation:str, statute_refs:list, confidence:float=0.0, **kwargs) -> str
store_redline(doc_id:str, clause_ref:str, clause_text:str, issues:list, rewritten_clause:str, risk_delta:str) -> str
get_eval_history(limit:int=50) -> list
get_risk_history(doc_id:str=None, limit:int=50) -> list
get_redline_history(doc_id:str=None, limit:int=50) -> list
register_document(doc_id:str, doc_title:str, doc_type:str, gcs_path:str, user_id:str) -> str
get_documents(limit:int=100) -> list
create_job(job_id:str, gcs_path:str, doc_type:str, user_id:str) -> None
update_job(job_id:str, status:str, error:str=None) -> None
get_job_status(job_id:str) -> dict | None
```

## Import patterns (use exactly as written)
```python
from services.storage import (
    store_interaction, store_risk_score, store_redline,
    get_eval_history, get_risk_history, get_redline_history,
    register_document, get_documents,
    create_job, update_job, get_job_status
)
from services.gemini import get_pro, get_flash
from services.rag import retrieve
from services.rerank import rerank
from middleware.auth import require_role
from models.schemas import (
    QueryRequest, QueryResponse, SourceRef, EvalResult,
    RiskRequest, RedlineRequest, RedlineIssue, RedlineResponse
)
from utils.retry import with_retry
```

## EvalResult schema (includes challenge_severity — do not omit)
```python
class EvalResult(BaseModel):
    faithfulness_score: float
    citations_accurate: dict
    adversarial_challenge: str
    challenge_severity: str  # LOW | MEDIUM | HIGH
    verdict: str             # PASS | REVIEW | FAIL
    provenance_hash: str
    reasoning: str
```

## Directory layout
```
backend/
├── main.py                          ← configure Modal auth FIRST, then imports
├── requirements.txt
├── Dockerfile
├── .env
├── middleware/
│   └── auth.py
├── routers/
│   ├── query.py    ← PROTECTED
│   ├── risk.py
│   ├── redline.py
│   ├── ingest.py
│   └── eval.py    ← includes GET /eval, POST /eval/batch, GET /docs
├── services/
│   ├── gemini.py       ← PROTECTED
│   ├── rag.py          ← PROTECTED
│   ├── rerank.py       ← PROTECTED
│   ├── eval_judge.py   ← PROTECTED
│   └── storage.py      ← PROTECTED
├── models/
│   └── schemas.py
└── utils/
    └── retry.py
frontend/
scripts/
```

## main.py Modal auth pattern (CRITICAL — must appear before all other imports)
```python
import os
import modal

_modal_token_id = os.environ.get("MODAL_TOKEN_ID")
_modal_token_secret = os.environ.get("MODAL_TOKEN_SECRET")
if _modal_token_id and _modal_token_secret:
    modal.config._profile.token_id = _modal_token_id
    modal.config._profile.token_secret = _modal_token_secret

from fastapi import FastAPI
# ... rest of imports
```

## auth.py pattern (ADC-first, JSON env var as override)
```python
def get_firebase_app():
    global _app
    if _app is None:
        cred_string = os.environ.get("FIREBASE_CREDENTIALS_JSON", "").strip()
        if cred_string and cred_string != "":
            try:
                cred = credentials.Certificate(json.loads(cred_string))
                _app = firebase_admin.initialize_app(cred)
            except Exception:
                _app = firebase_admin.initialize_app()  # ADC fallback
        else:
            _app = firebase_admin.initialize_app()  # ADC
    return _app
```

## Development auth bypass (APP_ENV=development)
In middleware/auth.py, verify_token() should start with:
```python
if os.environ.get("APP_ENV") == "development":
    return {"uid": "dev-user", "role": "admin", "email": "dev@docrag.dev"}
```

## Safety constraints
- Never run gcloud commands with --quiet on delete operations
- Never run gsutil rm -r
- Never modify IAM policies beyond what MASTER_PLAN_V2.md specifies
- Stop and report if any destructive operation is uncertain
