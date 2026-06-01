# DocRAG-Legal & Portfolio Strategy — Master Plan V2
# Written for Gemini CLI execution. Sam Karim. Clean slate.
# Generated: 2026-06-01

---

## PART 0 — READ THIS FIRST

This document is the single source of truth. There is no other plan.
No MASTER_PLAN.md, no MODAL_SETUP.md, no InstructionsV2. Those are gone.
Every Gemini CLI prompt references THIS file only.

### What changed from the failed build
| Old failure | Fix in this plan |
|---|---|
| run_build.sh pointed at wrong plan | One plan. This one. |
| Oracle remnants throughout | Oracle never mentioned again |
| Modal .remote() called synchronously in async FastAPI | All Modal calls wrapped with asyncio.run_in_executor |
| Modal auth missing in Cloud Run container | modal.config set at startup before any import |
| Gemini wrote rerank.py from incomplete spec | rerank.py is protected + fully specified here |
| storage.py function signatures missing from agent context | Full signatures in AGENT_CONTEXT section |
| services/rerank.py underspecified | Full implementation provided in protected files section |
| vertexai.preview import mismatch | One import style throughout: `from vertexai import rag` |
| No store_redline(), no /docs endpoint | Both added |

### Folder structure on VM
```
~/docrag-v2/                    ← NEW folder, nothing carried over
├── MASTER_PLAN_V2.md           ← this file
├── AGENT_CONTEXT.md            ← Gemini CLI reads first, always
├── protected/                  ← agent never touches these
│   ├── gemini.py
│   ├── rag.py
│   ├── rerank.py               ← NEW: added to protected
│   ├── eval_judge.py
│   ├── storage.py              ← NEW: added to protected (async fix)
│   └── query.py
├── backend/                    ← agent generates everything else here
└── frontend/                   ← agent generates
```

---

## PART 1 — PRODUCT DEFINITION

**DocRAG-Legal**: contract risk intelligence with adversarial self-auditing.

Not a ChatPDF. Not a legal chatbot. A system that challenges its own answers
at runtime and exposes the challenge to the user. That one sentence is the 
portfolio differentiator.

### Five endpoints
```
/query      → RAG retrieval → Gemini Pro synthesis → Flash adversarial judge inline
/risk       → clause heatmap (RED/YELLOW/GREEN) with statute citations
/redline    → clause diff with suggested rewrites, statute-backed
/ingest     → PDF upload → GCS → Vertex RAG async import
/eval       → GET eval history | POST /eval/batch (Cloud Scheduler hits this)
```

### Three additions that make this world-class

**1. Provenance chaining (session-level merkle chain)**
Every answer includes a `provenance_hash`. In V1 this was sha256(question+answer+context).
In V2 it chains: sha256(prev_hash + question + answer + context).
The genesis hash for a new session is the string "genesis".
This means a session's entire audit trail is tamper-evident.
Story: "not just citation-verified answers — cryptographically chained sessions."

**2. Challenge severity tier**
The Flash judge now returns `challenge_severity: LOW | MEDIUM | HIGH` alongside
the adversarial challenge. This makes the eval dashboard scannable — a HIGH
challenge gets a red warning icon, a LOW one gets a subtle indicator.
Frontend shows: ⚠ HIGH / ~ MEDIUM / · LOW next to each challenge.

**3. /docs/registry endpoint**
GET /docs — returns list of ingested documents from Modal registry.
Users can see exactly what's in the corpus. Makes the system feel real, not magic.
10 lines of code, huge UX impact.

---

## PART 2 — ENVIRONMENT BASELINE

Run these before anything else.

```bash
# Create clean folder
mkdir -p ~/docrag-v2/{protected,backend/{middleware,routers,services,models,utils},frontend,scripts,seed_docs/{statutes,contracts}}
cd ~/docrag-v2

# Verify tools
python3 --version          # need 3.10+
gcloud auth list           # need active account
gcloud config get-value project  # note your PROJECT_ID
modal token show           # need active token
gemini --version           # need gemini CLI

# Save project ID
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"
echo "PROJECT_ID=$PROJECT_ID REGION=$REGION"
echo "export PROJECT_ID=$PROJECT_ID" >> ~/.bashrc
echo "export REGION=$REGION" >> ~/.bashrc
```

---

## PART 3 — GCP SETUP

```bash
# Enable APIs (idempotent — safe to re-run)
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  storage.googleapis.com \
  secretmanager.googleapis.com \
  cloudscheduler.googleapis.com \
  discoveryengine.googleapis.com \
  firebase.googleapis.com

# GCS bucket for PDFs
gsutil mb -l $REGION gs://${PROJECT_ID}-docs 2>/dev/null || echo "bucket exists"

# Service account (may already exist from previous attempt — idempotent)
gcloud iam service-accounts create docrag-sa \
  --display-name="DocRAG Service Account" 2>/dev/null || echo "SA exists"

SA="docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant all required roles in one loop
for ROLE in \
  roles/aiplatform.user \
  roles/storage.objectAdmin \
  roles/secretmanager.secretAccessor \
  roles/discoveryengine.viewer \
  roles/firebaseauth.admin; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="$ROLE" --quiet
  echo "Granted $ROLE"
done

echo "GCP setup complete"
```

---

## PART 4 — FIREBASE (MANUAL — ~10 min)

These steps require a browser. Do them before running any agent phases.

1. Go to console.firebase.google.com
2. Add project → select $PROJECT_ID
3. Build → Authentication → Sign-in method → Email/Password → Enable
4. Users tab → Add user: test@docrag.dev / TestPass123!
5. Note the UID shown

Then run this on VM (uses ADC — no JSON key needed):
```bash
python3 - <<'CLAIMS_EOF'
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {'projectId': '$PROJECT_ID'})

# Replace with real UID from step 4 above
uid = "PASTE_UID_HERE"
auth.set_custom_user_claims(uid, {"role": "admin"})
print(f"Admin claims set for {uid}")
CLAIMS_EOF
```

Store firebase project config as secret (no JSON key — just the project ID):
```bash
echo -n "$PROJECT_ID" | gcloud secrets create firebase-project-id \
  --data-file=- --project=$PROJECT_ID 2>/dev/null || \
  echo -n "$PROJECT_ID" | gcloud secrets versions add firebase-project-id --data-file=-
```

---

## PART 5 — MODAL SETUP

```bash
# Verify logged in
modal token show

# Deploy the persistence app
# (store.py is in protected/ — copy it first)
cp ~/docrag-v2/protected/store.py ~/docrag-v2/modal/store.py 2>/dev/null || true
cd ~/docrag-v2/modal
modal deploy store.py

# Verify
modal app list | grep docrag-persistence
```

Store modal token in Secret Manager for Cloud Run:
```bash
TOKEN_ID=$(grep "token_id" ~/.modal.toml | head -1 | cut -d'"' -f2)
TOKEN_SECRET=$(grep "token_secret" ~/.modal.toml | head -1 | cut -d'"' -f2)

echo -n "$TOKEN_ID" | gcloud secrets create modal-token-id \
  --data-file=- --project=$PROJECT_ID 2>/dev/null || \
  echo -n "$TOKEN_ID" | gcloud secrets versions add modal-token-id --data-file=-

echo -n "$TOKEN_SECRET" | gcloud secrets create modal-token-secret \
  --data-file=- --project=$PROJECT_ID 2>/dev/null || \
  echo -n "$TOKEN_SECRET" | gcloud secrets versions add modal-token-secret --data-file=-

echo "Modal secrets stored"
```

---

## PART 6 — VERTEX RAG CORPUS CREATION

```bash
cat > ~/docrag-v2/scripts/create_corpus.py << 'CORPUS_EOF'
import vertexai
from vertexai import rag
import json, os, sys

PROJECT_ID = os.environ["PROJECT_ID"]
vertexai.init(project=PROJECT_ID, location="us-central1")

# Serverless mode — works for all projects, no Spanner allowlist needed
embedding_config = rag.RagEmbeddingModelConfig(
    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
        publisher_model="publishers/google/models/text-embedding-004"
    )
)
vector_db_config = rag.RagVectorDbConfig(
    vector_db=rag.RagManagedVertexVectorSearch(),
    rag_embedding_model_config=embedding_config
)

corpora = {
    "statutes": "Legal Statutes — Bangladesh",
    "contracts": "Contract Templates and Precedents"
}

corpus_ids = {}
for key, name in corpora.items():
    print(f"Creating {key} corpus...")
    try:
        corpus = rag.create_corpus(
            display_name=name,
            backend_config=vector_db_config
        )
        corpus_ids[key] = corpus.name
        print(f"  {key}: {corpus.name}")
    except Exception as e:
        print(f"  FAILED {key}: {e}")
        sys.exit(1)

out = os.path.expanduser("~/.docrag_corpus_ids.json")
with open(out, "w") as f:
    json.dump(corpus_ids, f, indent=2)

print(f"\nSaved to {out}")
for k, v in corpus_ids.items():
    print(f"CORPUS_{k.upper()}={v}")
CORPUS_EOF

python3 ~/docrag-v2/scripts/create_corpus.py
```

Store corpus IDs as secrets:
```bash
CORPUS_STATUTES=$(python3 -c "import json; d=json.load(open(os.path.expanduser('~/.docrag_corpus_ids.json'))); print(d['statutes'])")
CORPUS_CONTRACTS=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.docrag_corpus_ids.json'))); print(d['contracts'])")

echo -n "$CORPUS_STATUTES" | gcloud secrets create corpus-statutes --data-file=- --project=$PROJECT_ID
echo -n "$CORPUS_CONTRACTS" | gcloud secrets create corpus-contracts --data-file=- --project=$PROJECT_ID
echo "Corpus secrets stored"
```

---

## PART 7 — SEED DOCUMENTS

Minimum viable corpus for demo:
```bash
mkdir -p ~/docrag-v2/seed_docs/{statutes,contracts}

# ILO Labour Act 2006 (English, public domain)
curl -L "https://www.ilo.org/dyn/natlex/docs/ELECTRONIC/74481/119556/F-1222315587/BGD74481.pdf" \
  -o ~/docrag-v2/seed_docs/statutes/bangladesh_labour_act_2006.pdf --fail || \
  echo "Download failed — add PDF manually"

# Download 2-3 contract templates from lawinsider.com manually
# Place in ~/docrag-v2/seed_docs/contracts/

# Upload to GCS
gsutil -m cp ~/docrag-v2/seed_docs/statutes/*.pdf gs://${PROJECT_ID}-docs/statutes/ 2>/dev/null
gsutil -m cp ~/docrag-v2/seed_docs/contracts/*.pdf gs://${PROJECT_ID}-docs/contracts/ 2>/dev/null

# Ingest into corpus
cat > ~/docrag-v2/scripts/ingest_seed.py << 'INGEST_EOF'
import vertexai
from vertexai import rag
import json, os

PROJECT_ID = os.environ["PROJECT_ID"]
vertexai.init(project=PROJECT_ID, location="us-central1")

with open(os.path.expanduser("~/.docrag_corpus_ids.json")) as f:
    ids = json.load(f)

GCS = f"gs://{PROJECT_ID}-docs"

for key, chunk_size, overlap in [("statutes", 1024, 200), ("contracts", 512, 100)]:
    print(f"Ingesting {key}...")
    try:
        rag.import_files(
            corpus_name=ids[key],
            paths=[f"{GCS}/{key}/"],
            transformation_config={"chunking_config": {
                "chunk_size": chunk_size, "chunk_overlap": overlap
            }}
        )
        print(f"  {key}: submitted")
    except Exception as e:
        print(f"  {key}: {e}")

print("Done. Check Vertex AI console for status.")
INGEST_EOF

python3 ~/docrag-v2/scripts/ingest_seed.py
```

---

## PART 8 — PROTECTED FILES (DO NOT GIVE TO GEMINI CLI)

Write these yourself. They are the portfolio value.
Copy to ~/docrag-v2/protected/ before running the agent.

### protected/gemini.py
```python
import os

_initialized = False
_pro = None
_flash = None

def _init():
    global _initialized, _pro, _flash
    if _initialized:
        return
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig
    vertexai.init(
        project=os.environ["PROJECT_ID"],
        location=os.environ.get("REGION", "us-central1")
    )
    _pro = GenerativeModel(
        "gemini-1.5-pro-002",
        generation_config=GenerationConfig(temperature=0.1, max_output_tokens=2048)
    )
    _flash = GenerativeModel(
        "gemini-1.5-flash-002",
        generation_config=GenerationConfig(temperature=0.0, max_output_tokens=1024)
    )
    _initialized = True

def get_pro():
    _init()
    return _pro

def get_flash():
    _init()
    return _flash
```

### protected/rag.py
```python
import re
from typing import Optional
import vertexai
from vertexai import rag

ALPHA_DEFAULT  = 0.6
ALPHA_CITATION = 0.35

def _detect_alpha(query: str) -> float:
    if re.search(r"section\s+\d+|§\s*\d+|article\s+\d+|clause\s+\d+", query.lower()):
        return ALPHA_CITATION
    return ALPHA_DEFAULT

async def retrieve(
    query: str,
    corpus_name: str,
    top_k: int = 20,
    doc_type_filter: Optional[str] = None
) -> list:
    alpha = _detect_alpha(query)
    filter_obj = None
    if doc_type_filter:
        filter_obj = rag.Filter(
            vector_distance_threshold=0.4,
            metadata_filters=[{"key": "doc_type", "value": doc_type_filter}]
        )
    else:
        filter_obj = rag.Filter(vector_distance_threshold=0.4)

    config = rag.RagRetrievalConfig(top_k=top_k, filter=filter_obj)

    response = await rag.retrieval_query_async(
        rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
        text=query,
        rag_retrieval_config=config
    )
    return response.contexts.contexts
```

### protected/rerank.py
```python
import os
from google.cloud import discoveryengine_v1alpha as discoveryengine

async def rerank(query: str, chunks: list, top_n: int = 5) -> list:
    if not chunks:
        return []
    client = discoveryengine.RankServiceAsyncClient()
    records = [
        discoveryengine.RankingRecord(
            id=str(i),
            title=getattr(c, "source_display_name", "") or "",
            content=(c.text or "")[:512]
        )
        for i, c in enumerate(chunks)
    ]
    request = discoveryengine.RankRequest(
        ranking_config=(
            f"projects/{os.environ['PROJECT_ID']}/locations/global/"
            "rankingConfigs/default_ranking_config"
        ),
        model="semantic-ranker-512@latest",
        top_n=top_n,
        query=query,
        records=records
    )
    response = await client.rank(request)
    idx = [int(r.id) for r in response.records]
    return [chunks[i] for i in idx if i < len(chunks)]
```

### protected/eval_judge.py
```python
import json
import hashlib
from services.gemini import get_flash

PROMPT = """You are a legal RAG system evaluator. Legal errors cause real harm — be rigorous.

QUESTION: {question}
ANSWER: {answer}
RETRIEVED CONTEXT (numbered):
{context_block}
CITATIONS CLAIMED: {citations}
PREVIOUS SESSION HASH: {prev_hash}

Evaluate:
1. FAITHFULNESS (0.0-1.0): Is every claim in the answer supported by the context?
   Deduct 0.2 per unsupported claim.
2. CITATION_ACCURACY: Does each [N] reference exist in the context and support the claim?
   true/false per citation index.
3. ADVERSARIAL_CHALLENGE: One concrete counter-argument using the context.
   Reference the specific passage that creates ambiguity or contradiction.
4. CHALLENGE_SEVERITY: How seriously does this challenge undermine the answer?
   LOW = minor nuance | MEDIUM = partial contradiction | HIGH = fundamental error
5. VERDICT: PASS (faithfulness >= 0.85, all citations accurate) | REVIEW | FAIL

Return ONLY valid JSON:
{{
  "faithfulness_score": float,
  "citations_accurate": {{"{citation_id}": true/false}},
  "adversarial_challenge": "specific challenge with context reference",
  "challenge_severity": "LOW|MEDIUM|HIGH",
  "verdict": "PASS|REVIEW|FAIL",
  "reasoning": "brief explanation"
}}"""

async def judge(
    question: str,
    answer: str,
    chunks: list,
    citations: list,
    session_id: str = "unknown",
    prev_hash: str = "genesis"
) -> dict:
    context_block = "\n".join(
        f"[{i+1}] (Source: {getattr(c, 'source_display_name', 'unknown')}, "
        f"score: {getattr(c, 'score', 0):.3f})\n{(c.text or '')[:600]}"
        for i, c in enumerate(chunks)
    )

    # Chain the provenance hash — tamper-evident session audit trail
    raw = (prev_hash + question + answer + context_block).encode()
    provenance_hash = hashlib.sha256(raw).hexdigest()[:16]

    prompt = PROMPT.format(
        question=question,
        answer=answer,
        context_block=context_block,
        citations=citations,
        prev_hash=prev_hash
    )

    try:
        response = await get_flash().generate_content_async(
            prompt,
            generation_config={
                "temperature": 0.0,
                "response_mime_type": "application/json"
            }
        )
        result = json.loads(response.text)
    except Exception:
        result = {
            "faithfulness_score": 0.5,
            "citations_accurate": {},
            "adversarial_challenge": "Eval failed — manual review required",
            "challenge_severity": "MEDIUM",
            "verdict": "REVIEW",
            "reasoning": "Parse or generation error"
        }

    result["provenance_hash"] = provenance_hash
    return result
```

### protected/storage.py
```python
"""
Modal storage client — ALL persistence goes through here.
Critical: all Modal .remote() calls are wrapped with run_in_executor
to avoid blocking the FastAPI async event loop.
Modal auth is configured via env vars before this module is imported.
"""
import os
import asyncio
import modal
from typing import Optional

# Configure Modal auth from env (set in main.py before import)
# Functions looked up lazily to avoid import-time auth issues
_fn_cache: dict = {}

def _fn(name: str):
    if name not in _fn_cache:
        _fn_cache[name] = modal.Function.lookup("docrag-persistence", name)
    return _fn_cache[name]

def _dicts():
    return (
        modal.Dict.from_name("docrag-sessions", create_if_missing=True),
        modal.Dict.from_name("docrag-eval-cache", create_if_missing=True)
    )

async def _call(fn_name: str, *args):
    """Run Modal .remote() in executor to avoid blocking the event loop."""
    loop = asyncio.get_event_loop()
    fn = _fn(fn_name)
    return await loop.run_in_executor(None, fn.remote, *args)

# ── Public API ────────────────────────────────────────────────────────────────

async def store_interaction(
    session_id: str, user_id: str, question: str,
    answer: str, sources: list, eval_result: dict
) -> str:
    record = {
        "session_id": session_id,
        "user_id": user_id,
        "question": question[:1000],
        "answer": answer[:2000],
        "sources": sources,
        "faithfulness": eval_result.get("faithfulness_score", 0.0),
        "verdict": eval_result.get("verdict", "REVIEW"),
        "adversarial_challenge": eval_result.get("adversarial_challenge", ""),
        "challenge_severity": eval_result.get("challenge_severity", "LOW"),
        "provenance_hash": eval_result.get("provenance_hash", ""),
        "reasoning": eval_result.get("reasoning", "")
    }
    return await _call("append_eval", record)

async def store_risk_score(
    doc_id: str, clause_ref: str, clause_text: str,
    risk_level: str, conflicts: list, gaps: list,
    recommendation: str, statute_refs: list,
    confidence: float = 0.0, **kwargs
) -> str:
    record = {
        "doc_id": doc_id or "unknown",
        "clause_ref": clause_ref or "unref",
        "clause_text": clause_text[:1000],
        "risk_level": risk_level,
        "conflicts": conflicts,
        "gaps": gaps,
        "recommendation": recommendation,
        "statute_refs": statute_refs,
        "confidence": confidence
    }
    return await _call("append_risk", record)

async def store_redline(
    doc_id: str, clause_ref: str, clause_text: str,
    issues: list, rewritten_clause: str, risk_delta: str
) -> str:
    record = {
        "doc_id": doc_id or "unknown",
        "clause_ref": clause_ref or "unref",
        "clause_text": clause_text[:1000],
        "issues_count": len(issues),
        "highest_severity": max((i.get("severity","LOW") for i in issues), default="LOW"),
        "rewritten_clause": rewritten_clause[:1000],
        "risk_delta": risk_delta
    }
    return await _call("append_redline", record)

async def get_eval_history(limit: int = 50) -> list:
    _, eval_cache = _dicts()
    cached = eval_cache.get("recent_evals", [])
    if cached:
        return cached[:limit]
    return await _call("get_evals", limit)

async def get_risk_history(doc_id: Optional[str] = None, limit: int = 50) -> list:
    return await _call("get_risks", doc_id, limit)

async def get_redline_history(doc_id: Optional[str] = None, limit: int = 50) -> list:
    return await _call("get_redlines", doc_id, limit)

async def register_document(
    doc_id: str, doc_title: str, doc_type: str, gcs_path: str, user_id: str
) -> str:
    return await _call("register_doc", {
        "doc_id": doc_id, "doc_title": doc_title, "doc_type": doc_type,
        "gcs_path": gcs_path, "ingested_by": user_id
    })

async def get_documents(limit: int = 100) -> list:
    return await _call("get_docs", limit)

async def create_job(job_id: str, gcs_path: str, doc_type: str, user_id: str):
    return await _call("upsert_job", job_id, {
        "gcs_path": gcs_path, "doc_type": doc_type,
        "status": "pending", "created_by": user_id
    })

async def update_job(job_id: str, status: str, error: Optional[str] = None):
    update = {"status": status}
    if error:
        update["error_msg"] = error[:500]
    return await _call("upsert_job", job_id, update)

async def get_job_status(job_id: str) -> Optional[dict]:
    return await _call("get_job", job_id)

def save_session(session_id: str, data: dict):
    sessions, _ = _dicts()
    sessions[session_id] = data

def get_session(session_id: str) -> Optional[dict]:
    sessions, _ = _dicts()
    return sessions.get(session_id)
```

### protected/query.py
```python
from fastapi import APIRouter, Depends, HTTPException
from services.rag import retrieve
from services.rerank import rerank
from services.gemini import get_pro
from services.eval_judge import judge
from services.storage import store_interaction, get_session, save_session
from middleware.auth import require_role
from models.schemas import QueryRequest, QueryResponse
import os, re

router = APIRouter()

SYNTHESIS_PROMPT = """You are a legal research assistant. Use ONLY the provided context.
Cite sources as [1], [2], etc. If context is insufficient, say exactly:
"Insufficient context to answer."
Never speculate beyond the provided documents.

Question: {question}

Context:
{context_block}

Provide:
1. Direct answer with citations
2. Supporting evidence
3. Any important caveats or limitations"""

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    req: QueryRequest,
    user=Depends(require_role(["admin", "analyst", "viewer"]))
):
    corpus = (
        os.environ["CORPUS_STATUTES"] if req.corpus_type == "statutes"
        else os.environ["CORPUS_CONTRACTS"]
    )

    raw_chunks = await retrieve(
        query=req.question,
        corpus_name=corpus,
        top_k=20,
        doc_type_filter=req.doc_type_filter
    )
    if not raw_chunks:
        raise HTTPException(404, "No relevant documents found in corpus")

    ranked_chunks = await rerank(req.question, raw_chunks, top_n=5)

    context_block = "\n\n".join(
        f"[{i+1}] {getattr(c, 'source_display_name', 'unknown')}\n{c.text}"
        for i, c in enumerate(ranked_chunks)
    )

    synthesis = await get_pro().generate_content_async(
        SYNTHESIS_PROMPT.format(question=req.question, context_block=context_block),
        generation_config={"temperature": 0.1}
    )
    answer = synthesis.text
    citations = list(set(re.findall(r'\[(\d+)\]', answer)))

    # Retrieve previous hash for provenance chaining
    session_data = get_session(req.session_id) or {}
    prev_hash = session_data.get("last_hash", "genesis")

    eval_result = await judge(
        question=req.question,
        answer=answer,
        chunks=ranked_chunks,
        citations=citations,
        session_id=req.session_id,
        prev_hash=prev_hash
    )

    # Update session with new hash for chain
    save_session(req.session_id, {
        **session_data,
        "last_hash": eval_result["provenance_hash"]
    })

    await store_interaction(
        session_id=req.session_id,
        user_id=user["uid"],
        question=req.question,
        answer=answer,
        sources=[{
            "doc": getattr(c, "source_display_name", "unknown"),
            "score": getattr(c, "score", 0),
            "text_preview": (c.text or "")[:200]
        } for c in ranked_chunks],
        eval_result=eval_result
    )

    return QueryResponse(
        answer=answer,
        sources=[{
            "index": i+1,
            "doc_title": getattr(c, "source_display_name", "unknown"),
            "retrieval_score": round(getattr(c, "score", 0), 4),
            "text_preview": (c.text or "")[:300],
            "chunk_hash": hash(c.text or "")
        } for i, c in enumerate(ranked_chunks)],
        eval=eval_result,
        session_id=req.session_id
    )
```

### protected/store.py (Modal app)
```python
import modal
import json
import time
from typing import Optional

app = modal.App("docrag-persistence")

eval_volume     = modal.Volume.from_name("docrag-eval-logs",    create_if_missing=True)
risk_volume     = modal.Volume.from_name("docrag-risk-logs",    create_if_missing=True)
redline_volume  = modal.Volume.from_name("docrag-redline-logs", create_if_missing=True)
registry_volume = modal.Volume.from_name("docrag-doc-registry", create_if_missing=True)
jobs_volume     = modal.Volume.from_name("docrag-ingest-jobs",  create_if_missing=True)

session_dict = modal.Dict.from_name("docrag-sessions",    create_if_missing=True)
eval_cache   = modal.Dict.from_name("docrag-eval-cache",  create_if_missing=True)

def _append(path: str, record: dict):
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")

def _read(path: str, limit: int = 50, filter_key: str = None, filter_val=None) -> list:
    import os
    if not os.path.exists(path):
        return []
    with open(path) as f:
        records = [json.loads(l) for l in f if l.strip()]
    if filter_key and filter_val:
        records = [r for r in records if r.get(filter_key) == filter_val]
    return sorted(records, key=lambda x: x.get("timestamp", 0), reverse=True)[:limit]

@app.function(volumes={"/eval-logs": eval_volume})
def append_eval(record: dict) -> str:
    import uuid
    record.setdefault("eval_id", str(uuid.uuid4()))
    record["timestamp"] = time.time()
    _append("/eval-logs/evals.ndjson", record)
    eval_volume.commit()
    existing = eval_cache.get("recent_evals", [])
    existing.insert(0, record)
    eval_cache["recent_evals"] = existing[:100]
    return record["eval_id"]

@app.function(volumes={"/eval-logs": eval_volume})
def get_evals(limit: int = 50) -> list:
    return _read("/eval-logs/evals.ndjson", limit)

@app.function(volumes={"/risk-logs": risk_volume})
def append_risk(record: dict) -> str:
    import uuid
    record.setdefault("score_id", str(uuid.uuid4()))
    record["timestamp"] = time.time()
    _append("/risk-logs/risks.ndjson", record)
    risk_volume.commit()
    return record["score_id"]

@app.function(volumes={"/risk-logs": risk_volume})
def get_risks(doc_id: Optional[str] = None, limit: int = 50) -> list:
    return _read("/risk-logs/risks.ndjson", limit, "doc_id", doc_id)

@app.function(volumes={"/redline-logs": redline_volume})
def append_redline(record: dict) -> str:
    import uuid
    record.setdefault("redline_id", str(uuid.uuid4()))
    record["timestamp"] = time.time()
    _append("/redline-logs/redlines.ndjson", record)
    redline_volume.commit()
    return record["redline_id"]

@app.function(volumes={"/redline-logs": redline_volume})
def get_redlines(doc_id: Optional[str] = None, limit: int = 50) -> list:
    return _read("/redline-logs/redlines.ndjson", limit, "doc_id", doc_id)

@app.function(volumes={"/registry": registry_volume})
def register_doc(record: dict) -> str:
    import uuid
    record.setdefault("doc_id", str(uuid.uuid4()))
    record["timestamp"] = time.time()
    _append("/registry/docs.ndjson", record)
    registry_volume.commit()
    return record["doc_id"]

@app.function(volumes={"/registry": registry_volume})
def get_docs(limit: int = 100) -> list:
    return _read("/registry/docs.ndjson", limit)

@app.function(volumes={"/jobs": jobs_volume})
def upsert_job(job_id: str, update: dict) -> dict:
    import os
    path = f"/jobs/{job_id}.json"
    existing = {}
    if os.path.exists(path):
        with open(path) as f:
            existing = json.load(f)
    else:
        existing = {"job_id": job_id, "created_at": time.time()}
    existing.update(update)
    existing["updated_at"] = time.time()
    with open(path, "w") as f:
        json.dump(existing, f)
    jobs_volume.commit()
    return existing

@app.function(volumes={"/jobs": jobs_volume})
def get_job(job_id: str) -> Optional[dict]:
    import os
    path = f"/jobs/{job_id}.json"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)
```

---

## PART 9 — AGENT CONTEXT FILE

Write this exactly as AGENT_CONTEXT.md in ~/docrag-v2/:

```markdown
# DocRAG-Legal — Gemini CLI Agent Context

Read this file completely before doing anything.
Reference plan: MASTER_PLAN_V2.md in the same directory.

## Non-negotiable constraints
- Storage: Modal ONLY. No Oracle, no SQLite, no Firestore.
- All imports from services.storage use the exact signatures below.
- Auth: `from middleware.auth import require_role`
- Gemini clients: `from services.gemini import get_pro, get_flash`
- Never call vertexai.init() outside services/gemini.py
- All Pydantic models in models/schemas.py only
- All Vertex AI calls wrapped with @with_retry from utils/retry.py
- response_mime_type="application/json" on all Flash structured output
- Temperature: 0.1 for Pro synthesis, 0.0 for Flash structured output

## Files agent must NEVER write or overwrite
- services/gemini.py
- services/rag.py
- services/rerank.py
- services/eval_judge.py
- services/storage.py
- routers/query.py

## Storage function signatures (exact — deviating breaks the app)
store_interaction(session_id:str, user_id:str, question:str, answer:str, sources:list, eval_result:dict) -> str
store_risk_score(doc_id:str, clause_ref:str, clause_text:str, risk_level:str, conflicts:list, gaps:list, recommendation:str, statute_refs:list, confidence:float=0.0, **kwargs) -> str
store_redline(doc_id:str, clause_ref:str, clause_text:str, issues:list, rewritten_clause:str, risk_delta:str) -> str
get_eval_history(limit:int=50) -> list
get_risk_history(doc_id:str=None, limit:int=50) -> list
get_redline_history(doc_id:str=None, limit:int=50) -> list
register_document(doc_id:str, doc_title:str, doc_type:str, gcs_path:str, user_id:str) -> str
get_documents(limit:int=100) -> list
create_job(job_id:str, gcs_path:str, doc_type:str, user_id:str)
update_job(job_id:str, status:str, error:str=None)
get_job_status(job_id:str) -> Optional[dict]

## Schemas (source of truth)
[paste content of models/schemas.py here after agent generates it]

## Safety constraints
- Never run gcloud commands with --quiet on delete operations
- Never run gsutil rm -r
- If uncertain about a destructive operation, stop and report

## Directory layout
backend/
├── main.py
├── requirements.txt
├── Dockerfile
├── .env
├── middleware/auth.py
├── routers/ [query.py PROTECTED | risk.py | redline.py | ingest.py | eval.py]
├── services/ [gemini.py PROTECTED | rag.py PROTECTED | rerank.py PROTECTED | eval_judge.py PROTECTED | storage.py PROTECTED | rerank.py PROTECTED]
├── models/schemas.py
└── utils/retry.py
frontend/
scripts/
```

---

## PART 10 — GEMINI CLI EXECUTION SEQUENCE

### Pre-flight (you do this)
```bash
# 1. Copy protected files into place
cp ~/docrag-v2/protected/gemini.py ~/docrag-v2/backend/services/
cp ~/docrag-v2/protected/rag.py ~/docrag-v2/backend/services/
cp ~/docrag-v2/protected/rerank.py ~/docrag-v2/backend/services/
cp ~/docrag-v2/protected/eval_judge.py ~/docrag-v2/backend/services/
cp ~/docrag-v2/protected/storage.py ~/docrag-v2/backend/services/
cp ~/docrag-v2/protected/query.py ~/docrag-v2/backend/routers/

# 2. Start tmux
tmux new -s docrag-build
cd ~/docrag-v2
```

### Phase A — Backend boilerplate (agent)
```bash
gemini --yolo "
Read AGENT_CONTEXT.md and MASTER_PLAN_V2.md.

Write these files exactly. Do NOT write any file in the protected list.

1. backend/requirements.txt
   Include: fastapi==0.115.0 uvicorn[standard]==0.30.6 firebase-admin==6.5.0
   google-cloud-aiplatform==1.68.0 google-cloud-storage==2.18.2
   google-cloud-discoveryengine==0.13.4 vertexai==1.68.0 pydantic==2.8.2
   slowapi==0.1.9 python-dotenv==1.0.1 httpx==0.27.2 modal==0.64.145
   python-multipart==0.0.9

2. backend/models/schemas.py
   Include all schemas: QueryRequest, QueryResponse, SourceRef, EvalResult,
   RiskRequest, RedlineRequest, RedlineIssue, RedlineResponse, IngestRequest.
   EvalResult must include challenge_severity field (str, values: LOW|MEDIUM|HIGH).

3. backend/utils/retry.py
   Exponential backoff decorator with full jitter. Max 3 retries.
   Catches google.api_core.exceptions.ServiceUnavailable and ResourceExhausted.

4. backend/middleware/auth.py
   Firebase JWT verification using ADC (no JSON key file).
   Supports FIREBASE_CREDENTIALS_JSON env var as override.
   require_role() returns dependency for use in router Depends().
   In APP_ENV=development, bypass auth and return dev-user/admin.

5. backend/main.py
   FastAPI app. IMPORTANT: before any other imports, configure Modal auth:
     import os, modal
     _mid = os.environ.get('MODAL_TOKEN_ID')
     _msec = os.environ.get('MODAL_TOKEN_SECRET')
     if _mid and _msec:
         modal.config._profile.token_id = _mid
         modal.config._profile.token_secret = _msec
   Then import routers: query, risk, redline, ingest, eval_router.
   Mount all routers. Add CORS middleware (allow_origins=[*]).
   Add GET /health endpoint.
   Load dotenv at startup.

6. backend/Dockerfile
   Base: python:3.11-slim. Port 8080.
   CMD: uvicorn main:app --host 0.0.0.0 --port 8080
   No unnecessary layers.

7. backend/.env (placeholder values, never real secrets)
   PROJECT_ID=your-project-id
   REGION=us-central1
   GCS_BUCKET=your-project-id-docs
   CORPUS_STATUTES=placeholder
   CORPUS_CONTRACTS=placeholder
   FIREBASE_CREDENTIALS_JSON=
   MODAL_TOKEN_ID=placeholder
   MODAL_TOKEN_SECRET=placeholder
   APP_ENV=development

After writing all files, run:
   cd ~/docrag-v2/backend && pip install -r requirements.txt
Then run import check:
   python3 -c 'from main import app; print(\"Import OK\")'
Report any import errors. Stop if imports fail — do not continue.
"
```

### Phase B — Routers (agent)
```bash
gemini --yolo "
Read AGENT_CONTEXT.md and MASTER_PLAN_V2.md.
Do NOT write query.py — it is protected and already exists.

Write these routers:

1. backend/routers/risk.py
   POST /risk — takes RiskRequest, retrieves from CORPUS_STATUTES,
   reranks to top 4, asks Flash for RED/YELLOW/GREEN with statute refs.
   Calls store_risk_score() with exact signature from AGENT_CONTEXT.md.
   Returns raw dict (JSON-serializable).

2. backend/routers/redline.py
   POST /redline — takes RedlineRequest, retrieves from CORPUS_STATUTES,
   reranks to top 3, asks Flash for structured redline.
   Calls store_redline() with exact signature from AGENT_CONTEXT.md.
   Returns RedlineResponse.

3. backend/routers/ingest.py
   POST /ingest — multipart file upload, doc_type form field.
   Uploads PDF to GCS, calls create_job(), fires background task.
   Background task calls register_document() then update_job().
   GET /ingest/status/{job_id} — calls get_job_status().
   Admin and analyst roles only for POST. All roles for GET.

4. backend/routers/eval.py
   GET /eval — calls get_eval_history(50) and get_risk_history(limit=20).
   Returns summary stats (avg faithfulness, pass_rate, total_evaluated).
   Also returns redline_history from get_redline_history(20).
   POST /eval/batch — re-evaluates REVIEW verdict items.
   GET /docs — calls get_documents(100). Returns document registry.
   Admin/analyst roles for POST. All roles for GET.

After writing, run import check:
   python3 -c 'from routers.risk import router; from routers.redline import router; from routers.ingest import router; from routers.eval import router; print(\"Routers OK\")'
"
```

### Audit checkpoint (you do this before continuing)
```bash
cd ~/docrag-v2/backend
python3 -c "
from main import app
from routers.query import router
from services.storage import store_interaction, store_risk_score, store_redline
print('All imports OK')
"

# Check no oracle references survived
grep -r "oracle\|oracledb" ~/docrag-v2/backend/ && echo "ORACLE FOUND — FIX BEFORE CONTINUING" || echo "No oracle refs — clean"

# Check no hardcoded secrets
grep -r "your_oracle\|AKIA\|sk-proj" ~/docrag-v2/backend/ && echo "SECRETS FOUND" || echo "No hardcoded secrets — clean"

# Verify protected files weren't overwritten (check modification time)
ls -la ~/docrag-v2/backend/services/
```

### Phase C — Backend deploy (agent)
```bash
gemini --yolo "
Read AGENT_CONTEXT.md.
Run exactly:

cd ~/docrag-v2/backend

gcloud run deploy docrag-api \
  --source . \
  --region us-central1 \
  --service-account docrag-sa@\${PROJECT_ID}.iam.gserviceaccount.com \
  --set-env-vars PROJECT_ID=\${PROJECT_ID},REGION=us-central1,APP_ENV=production \
  --set-secrets \
    CORPUS_STATUTES=corpus-statutes:latest,\
    CORPUS_CONTRACTS=corpus-contracts:latest,\
    GCS_BUCKET=gcs-bucket:latest,\
    MODAL_TOKEN_ID=modal-token-id:latest,\
    MODAL_TOKEN_SECRET=modal-token-secret:latest \
  --allow-unauthenticated \
  --concurrency 80 \
  --memory 1Gi \
  --min-instances 0 \
  --max-instances 5

After deploy, save API_URL:
  export API_URL=\$(gcloud run services describe docrag-api --region us-central1 --format='value(status.url)')
  echo \"export API_URL=\$API_URL\" >> ~/.bashrc

Run health check: curl \$API_URL/health
Report the URL and health check result.
"
```

### Phase D — Frontend (agent)
```bash
gemini --yolo "
Read AGENT_CONTEXT.md and MASTER_PLAN_V2.md.

In ~/docrag-v2/frontend:

1. Run: npx create-next-app@14 . --typescript --tailwind --eslint --app --no-src-dir --import-alias '@/*'

2. Run: npm install react-markdown firebase chart.js react-chartjs-2

3. Create .env.local:
   NEXT_PUBLIC_API_URL=\$API_URL
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=\$PROJECT_ID
   (placeholder values for firebase keys)

4. Write lib/firebase.ts — init Firebase app from env vars, export auth

5. Write lib/api.ts — authFetch helper with Firebase JWT, export api object:
   api.query(body), api.risk(body), api.redline(body),
   api.ingest(formData), api.evalHistory(), api.batchEval(),
   api.jobStatus(id), api.docs()

6. Write components/ChatPanel.tsx
   Props: messages[], onSend(string), loading
   Render assistant messages as markdown (react-markdown)
   Show sources as collapsible list with retrieval_score
   Show eval badge: PASS=green, REVIEW=amber, FAIL=red
   Show challenge_severity icon: HIGH=⚠ red, MEDIUM=~ amber, LOW=· gray
   Toggle for adversarial_challenge text
   Tailwind only, no UI libraries

7. Write components/ProvenanceTree.tsx
   Props: sources[], provenance_hash
   Show source tree with chunk_hash, retrieval_score
   Show provenance_hash at bottom in monospace
   Click node expands text_preview

8. Write components/RiskHeatmap.tsx
   Props: clauses[]
   Grid of cards with left border: RED=red, YELLOW=amber, GREEN=green
   Click card expands conflicts, gaps, recommendation, statute_refs

9. Write components/RedlinePanel.tsx
   Props: original, result
   Left: original with problematic phrases highlighted red/amber
   Right: rewritten with same spans highlighted green
   Bottom: risk_delta summary

10. Write components/AdversarialPanel.tsx
    Props: evalHistory[]
    Stats: avg faithfulness, pass_rate
    Line chart (Chart.js): faithfulness over last 30 items
    Table: question preview, faithfulness bar, verdict badge,
           challenge_severity icon, adversarial_challenge (truncated/expandable)

11. Write app/page.tsx — Chat page with ChatPanel + ProvenanceTree
12. Write app/risk/page.tsx — RiskHeatmap
13. Write app/redline/page.tsx — RedlinePanel
14. Write app/eval/page.tsx — AdversarialPanel + document registry table
15. Write app/docs/page.tsx — document list from api.docs()

Run: npm run build
Report any TypeScript errors. Fix errors before reporting done.
"
```

### Phase E — Scheduler + smoke tests (agent)
```bash
gemini --yolo "
Read AGENT_CONTEXT.md.

1. Create Cloud Scheduler job:
gcloud scheduler jobs create http docrag-eval-batch \
  --schedule '0 */6 * * *' \
  --uri \"\${API_URL}/eval/batch\" \
  --http-method POST \
  --location us-central1 \
  --oidc-service-account-email docrag-sa@\${PROJECT_ID}.iam.gserviceaccount.com \
  --attempt-deadline 300s

2. Run smoke tests (use APP_ENV=development auth bypass):
curl \$API_URL/health
curl -X POST \$API_URL/query -H 'Content-Type: application/json' \
  -d '{\"question\":\"What are restrictions on share transfers?\",\"session_id\":\"smoke-001\",\"corpus_type\":\"statutes\"}'
curl -X POST \$API_URL/risk -H 'Content-Type: application/json' \
  -d '{\"clause_text\":\"Either party may terminate with 7 days notice.\",\"doc_id\":\"test\",\"clause_ref\":\"12.1\"}'
curl -X POST \$API_URL/redline -H 'Content-Type: application/json' \
  -d '{\"clause_text\":\"Contractor shall deliver work as requested by Client.\"}'
curl \$API_URL/eval
curl \$API_URL/docs

3. For any 500 error, read logs:
gcloud run services logs read docrag-api --region us-central1 --limit 30

Report: HTTP status and response shape for each endpoint.
"
```

---

## PART 11 — COST BUDGET

| Resource | Usage | Estimate |
|---|---|---|
| Corpus ingestion (50 docs) | Vertex RAG embeddings | ~$2 |
| Dev queries (200) | Pro synthesis | ~$8 |
| Dev eval (200) | Flash judging | ~$1 |
| Reranking (200 × 20 chunks) | Ranking API | ~$1 |
| Risk + redline (50 each) | Flash structured | ~$1 |
| Cloud Run | 5 instances, light usage | ~$3 |
| Modal | Volumes + Dict + function calls | ~$5 |
| Buffer | Debugging, iteration | ~$15 |
| **Total DocRAG** | | **~$36 of $67 GCP + $90 Modal** |

Remaining after DocRAG: ~$31 GCP + ~$85 Modal + $200 AWS + $1000 Gen AI App Builder credits.

---

## PART 12 — SECOND PROJECT: SEO Intelligence Platform

### Why this pairs with DocRAG
Same stack: FastAPI, Next.js, Modal, Gemini. 60-70% code reuse.
Different domain: content teams, agencies, solo operators — much larger market.
Toptal sees you can apply the same architectural thinking to a different problem.

### What it does
**ContentSight**: keyword intelligence + content gap analysis + 
AI-generated content briefs with self-auditing quality scores.

The differentiator: same adversarial eval pattern from DocRAG but applied to 
content quality. Every generated brief is challenged by a second model that 
checks for accuracy, specificity, and actionability. The "eval harness" becomes 
your portfolio's signature pattern.

### Endpoints
```
/analyze    → takes URL, scrapes + analyzes content vs top SERP competitors
/brief      → generates SEO content brief for a keyword, with quality eval
/gaps       → finds content gaps vs competitor corpus
/audit      → page-level SEO audit (title, meta, headings, internal links)
```

### Why it works in your budget
- AWS $200: run Playwright scraping workers on Lambda (pay-per-call, no idle cost)
- Modal: batch embedding of competitor content (reuse existing setup)
- GCP Gen AI App Builder $1000: build a Vertex Search index over competitor corpus
  (this is what the $1000 credits are FOR — Vertex Search is expensive at scale)
- Gemini Flash for brief generation (cheap, fast)
- Gemini Pro for quality judging (same pattern as DocRAG eval)

### Technical architecture
```
User submits keyword
  → Lambda scrapes top 10 SERP results (Playwright, AWS)
  → Content chunked + embedded → Modal batch job
  → Stored in Vertex Search index (Gen AI App Builder credits)
  → /brief: Flash generates content brief
  → /brief: Pro judges brief quality (same adversarial pattern)
  → Returns brief + quality_score + improvement_suggestions
```

### Build time
DocRAG takes ~7 hours with Gemini CLI. ContentSight takes ~4 hours after DocRAG
because the stack is identical. Total portfolio build: ~11 hours of actual work.

---

## PART 13 — THIRD PROJECT: AWS-NATIVE (uses your $200)

### CrisisRadar: real-time supply chain risk monitor

### Why AWS
You have $200 there, nothing built. Shows multi-cloud thinking on Toptal profile.
Different from GCP projects — demonstrates breadth.

### What it does
Monitors news + commodity prices + shipping data for supply chain disruptions.
Sends Slack/email alerts when risk threshold crossed.
Dashboard shows risk heatmap by region + commodity.

### Stack (AWS-native)
- Lambda: news ingestion from RSS + NewsAPI
- DynamoDB: event storage (free tier covers this)
- Bedrock (Claude Haiku): event classification + risk scoring
- EventBridge: scheduled ingestion every 15 min
- API Gateway: REST API for dashboard
- S3 + CloudFront: static Next.js frontend

### Why this works for Toptal
Event-driven architecture. Serverless. Real-time. Different domain (ops/supply chain vs legal).
Shows you know AWS primitives, not just GCP.
Claude Haiku on Bedrock is ~$0.25/million tokens — $200 covers enormous usage.

### Build time: ~5 hours
Lambda is simpler than Cloud Run. DynamoDB is simpler than Modal.
The frontend reuses the same Next.js + Tailwind pattern.

---

## PART 14 — EXECUTION PRIORITY

Week 1, Days 1-2: DocRAG clean rebuild (this plan)
Week 1, Day 3: ContentSight setup (Modal + AWS Lambda + Gen AI App Builder)
Week 1, Days 4-5: ContentSight backend + frontend
Week 2, Days 1-2: CrisisRadar (AWS-native, fresh skills signal)
Week 2, Day 3: Polish all three READMEs, record Loom demos
Week 2, Days 4-5: Toptal application + portfolio page

Three live demos. Three different cloud providers. One consistent architectural 
signature (eval harness, adversarial self-auditing, provenance hashing).
That is an unusual Toptal portfolio.

---

## PART 15 — README NORTH STAR SENTENCES

DocRAG-Legal:
"Contract risk intelligence with adversarial self-auditing — every answer 
challenges itself, every session is cryptographically chained, every risk 
assessment cites the exact statute it violates."

ContentSight:
"SEO content intelligence with adversarial quality scoring — every generated 
brief is challenged by a second model for accuracy, specificity, and 
actionability before reaching the user."

CrisisRadar:
"Real-time supply chain risk monitoring with event-driven classification — 
news, commodity data, and shipping signals unified into a regional risk heatmap 
with automated threshold alerts."

---

## CHECKLIST BEFORE FIRST GEMINI CLI PHASE

- [ ] Protected files written and in ~/docrag-v2/protected/
- [ ] store.py deployed to Modal (modal deploy store.py)
- [ ] Firebase manual setup done (auth enabled, test user created, claims set)
- [ ] Corpus creation run (create_corpus.py) and IDs stored as secrets
- [ ] Modal token stored as secrets in Secret Manager
- [ ] AGENT_CONTEXT.md written in ~/docrag-v2/
- [ ] tmux session started
- [ ] run_build.sh does NOT exist (we use direct gemini --yolo commands instead)
