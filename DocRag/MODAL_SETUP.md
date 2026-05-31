# Step by steps for DocRag  
  
Good switch. Modal is better here — no wallet complexity, no OracleDB driver issues, async-native, and your $60 credit covers the entire project with room to spare.  
**Modal replaces Oracle for all persistence. Architecture change:**  
**Modal replaces Oracle for all persistence. Architecture change:**  
```
Oracle Autonomous DB  →  Modal Dict (hot cache, sessions, eval history)
                     +  Modal Volume (structured JSON logs, persisted)

```
Modal Dict = in-memory KV with TTL, perfect for sessions and recent eval scores. Modal Volume = persistent filesystem mounted into functions, perfect for append-only eval/audit logs as newline-delimited JSON (NDJSON). No SQL, no schema migrations, no wallet.  
One tradeoff to know upfront: Modal Dict is not a database. For a portfolio demo running hundreds of queries, it's perfect. For production with millions, you'd graduate to Postgres. That's a feature, not a bug — it's an honest architectural decision you can articulate to Toptal reviewers.  
  
Now the complete step-by-step from modal auth to deployment.  
  
## Phase 0 — Environment baseline (do this now, ~15 min)  
```
# Confirm modal is authorized
modal token show
# Should print your token ID and workspace. If not: modal token new

# Confirm python version
python3 --version
# Need 3.10+ for match statements and type unions

# Install all backend deps in your VM
pip install fastapi "uvicorn[standard]" firebase-admin \
  google-cloud-aiplatform google-cloud-storage vertexai \
  pydantic slowapi python-dotenv httpx modal \
  google-cloud-discoveryengine

# Confirm gcloud is authenticated
gcloud auth list
gcloud config get-value project
# If project not set:
# gcloud config set project YOUR_PROJECT_ID

```
  
## Phase 1 — GCP project setup (~20 min)  
```
# If you already have a project skip creation, just set it
export PROJECT_ID="docrag-legal-$(date +%s | tail -c6)"
export REGION="us-central1"

# Create project (skip if reusing existing)
gcloud projects create $PROJECT_ID --name="DocRAG Legal"
gcloud config set project $PROJECT_ID

# Link billing — MUST do this before enabling APIs
gcloud billing accounts list
# Note the ACCOUNT_ID (format: XXXXXX-XXXXXX-XXXXXX)
export BILLING_ID="PASTE_YOUR_BILLING_ID_HERE"
gcloud billing projects link $PROJECT_ID --billing-account=$BILLING_ID

# Enable all needed APIs in one shot
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  storage.googleapis.com \
  firestore.googleapis.com \
  secretmanager.googleapis.com \
  cloudscheduler.googleapis.com \
  discoveryengine.googleapis.com

# Create GCS bucket for PDF storage
gsutil mb -l $REGION gs://${PROJECT_ID}-docs
echo "Bucket created: gs://${PROJECT_ID}-docs"

# Create service account for Cloud Run
gcloud iam service-accounts create docrag-sa \
  --display-name="DocRAG Service Account"

# Grant necessary roles
for ROLE in \
  roles/aiplatform.user \
  roles/storage.objectAdmin \
  roles/secretmanager.secretAccessor \
  roles/datastore.user; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="$ROLE"
done

# Init Firestore (needed for user sessions, job status)
gcloud firestore databases create --location=nam5

# Save PROJECT_ID for all future steps
echo "export PROJECT_ID=$PROJECT_ID" >> ~/.bashrc
echo "export REGION=$REGION" >> ~/.bashrc
source ~/.bashrc
echo "GCP setup complete. PROJECT_ID=$PROJECT_ID"

```
  
## Phase 2 — Firebase setup (~15 min)  
Do this in browser (Termius can open links):  
```
1. Go to console.firebase.google.com
2. Click "Add project" → select your GCP project ($PROJECT_ID)
3. Disable Google Analytics (not needed) → Create project
4. Go to Project Settings → Service Accounts
5. Click "Generate new private key" → download JSON file
6. Transfer to your VM (use scp or paste content directly)

```
Once you have the JSON file on your VM:  
```
# Store Firebase credentials as Secret Manager secret
# Method A: if file is on VM
cat /path/to/firebase-service-account.json | \
  gcloud secrets create firebase-creds \
  --data-file=- \
  --project=$PROJECT_ID

# Method B: paste inline (useful from Termius)
# First: cat the file, copy the JSON
# Then:
echo 'PASTE_JSON_HERE' | \
  gcloud secrets create firebase-creds \
  --data-file=- \
  --project=$PROJECT_ID

# Enable Email/Password auth in Firebase console:
# Authentication → Sign-in method → Email/Password → Enable
# Create one test user: Authentication → Users → Add user
# Email: test@docrag.dev  Password: TestPass123!
# Note the UID shown — you'll use it to set admin role

# Set admin custom claim for your test user
# Run this once from VM:
python3 - <<'EOF'
import firebase_admin
from firebase_admin import credentials, auth
import json, os

cred_json = open("/path/to/firebase-service-account.json").read()
cred = credentials.Certificate(json.loads(cred_json))
firebase_admin.initialize_app(cred)

# Replace with your test user UID from Firebase console
uid = "PASTE_UID_HERE"
auth.set_custom_user_claims(uid, {"role": "admin"})
print(f"Set admin role for {uid}")
EOF

```
  
## Phase 3 — Modal persistence layer setup (~20 min)  
Create the Modal app file first. This is your entire database layer.  
```
mkdir -p ~/docrag-legal/modal
cat > ~/docrag-legal/modal/store.py << 'MODAL_EOF'
import modal
import json
import time
from typing import Optional

app = modal.App("docrag-persistence")

# --- Volumes and Dicts ---

# Persistent volume: append-only NDJSON logs
# Survives restarts, acts as your audit trail
eval_volume = modal.Volume.from_name("docrag-eval-logs", create_if_missing=True)
risk_volume = modal.Volume.from_name("docrag-risk-logs", create_if_missing=True)
registry_volume = modal.Volume.from_name("docrag-doc-registry", create_if_missing=True)
jobs_volume = modal.Volume.from_name("docrag-ingest-jobs", create_if_missing=True)

# Dict: hot cache for sessions, recent eval scores (TTL-based)
session_dict = modal.Dict.from_name("docrag-sessions", create_if_missing=True)
eval_cache = modal.Dict.from_name("docrag-eval-cache", create_if_missing=True)

# --- Eval Functions ---

@app.function(volumes={"/eval-logs": eval_volume})
def append_eval(record: dict) -> str:
    """Append one eval result to persistent NDJSON log."""
    import uuid
    record["eval_id"] = record.get("eval_id", str(uuid.uuid4()))
    record["timestamp"] = time.time()
    
    with open("/eval-logs/evals.ndjson", "a") as f:
        f.write(json.dumps(record) + "\n")
    
    eval_volume.commit()
    
    # Also cache last 100 in Dict for fast reads
    cache_key = "recent_evals"
    existing = eval_cache.get(cache_key, [])
    existing.insert(0, record)
    eval_cache[cache_key] = existing[:100]
    
    return record["eval_id"]

@app.function(volumes={"/eval-logs": eval_volume})
def get_evals(limit: int = 50) -> list:
    """Read last N eval results."""
    import os
    path = "/eval-logs/evals.ndjson"
    if not os.path.exists(path):
        return []
    with open(path) as f:
        lines = f.readlines()
    records = [json.loads(l) for l in lines if l.strip()]
    return sorted(records, key=lambda x: x.get("timestamp", 0), reverse=True)[:limit]

# --- Risk Functions ---

@app.function(volumes={"/risk-logs": risk_volume})
def append_risk(record: dict) -> str:
    import uuid
    record["score_id"] = record.get("score_id", str(uuid.uuid4()))
    record["timestamp"] = time.time()
    with open("/risk-logs/risks.ndjson", "a") as f:
        f.write(json.dumps(record) + "\n")
    risk_volume.commit()
    return record["score_id"]

@app.function(volumes={"/risk-logs": risk_volume})
def get_risks(doc_id: Optional[str] = None, limit: int = 50) -> list:
    import os
    path = "/risk-logs/risks.ndjson"
    if not os.path.exists(path):
        return []
    with open(path) as f:
        records = [json.loads(l) for l in f if l.strip()]
    if doc_id:
        records = [r for r in records if r.get("doc_id") == doc_id]
    return sorted(records, key=lambda x: x.get("timestamp", 0), reverse=True)[:limit]

# --- Doc Registry ---

@app.function(volumes={"/registry": registry_volume})
def register_doc(record: dict) -> str:
    import uuid
    record["doc_id"] = record.get("doc_id", str(uuid.uuid4()))
    record["timestamp"] = time.time()
    with open("/registry/docs.ndjson", "a") as f:
        f.write(json.dumps(record) + "\n")
    registry_volume.commit()
    return record["doc_id"]

@app.function(volumes={"/registry": registry_volume})
def get_docs(limit: int = 100) -> list:
    import os
    path = "/registry/docs.ndjson"
    if not os.path.exists(path):
        return []
    with open(path) as f:
        records = [json.loads(l) for l in f if l.strip()]
    return sorted(records, key=lambda x: x.get("timestamp", 0), reverse=True)[:limit]

# --- Ingest Job Tracking ---

@app.function(volumes={"/jobs": jobs_volume})
def upsert_job(job_id: str, update: dict) -> dict:
    """Create or update an ingest job record."""
    import os
    path = f"/jobs/{job_id}.json"
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

MODAL_EOF

echo "Modal store.py created"

```
Deploy the Modal app (this provisions the volumes and dicts):  
```
cd ~/docrag-legal/modal
modal deploy store.py
# Expected output: Deployed app docrag-persistence
# Volumes and Dicts are created on first function call — no explicit init needed

```
Test Modal is working:  
```
python3 - <<'EOF'
import modal
# Test Dict access
d = modal.Dict.from_name("docrag-sessions", create_if_missing=True)
d["test"] = "hello"
print("Dict write:", d["test"])
print("Modal persistence: OK")
EOF

```
  
## Phase 4 — Modal client wrapper (FastAPI calls Modal functions) (~10 min)  
```
cat > ~/docrag-legal/backend/services/storage.py << 'EOF'
"""
Modal storage client.
All FastAPI persistence calls go through here.
Calls Modal functions via .remote() — runs in Modal's cloud, 
results returned synchronously to FastAPI.
"""
import modal
from typing import Optional

# Reference deployed Modal functions — no import of store.py needed
# These are remote function handles
_append_eval   = modal.Function.lookup("docrag-persistence", "append_eval")
_get_evals     = modal.Function.lookup("docrag-persistence", "get_evals")
_append_risk   = modal.Function.lookup("docrag-persistence", "append_risk")
_get_risks     = modal.Function.lookup("docrag-persistence", "get_risks")
_register_doc  = modal.Function.lookup("docrag-persistence", "register_doc")
_get_docs      = modal.Function.lookup("docrag-persistence", "get_docs")
_upsert_job    = modal.Function.lookup("docrag-persistence", "upsert_job")
_get_job       = modal.Function.lookup("docrag-persistence", "get_job")

# Session dict (direct access, no function call needed)
_sessions = modal.Dict.from_name("docrag-sessions", create_if_missing=True)
_eval_cache = modal.Dict.from_name("docrag-eval-cache", create_if_missing=True)

# --- Public API ---

async def store_interaction(
    session_id: str, user_id: str, question: str,
    answer: str, sources: list, eval_result: dict
) -> str:
    record = {
        "session_id": session_id,
        "user_id": user_id,
        "question": question,
        "answer": answer[:2000],  # truncate for storage
        "sources": sources,
        "faithfulness": eval_result.get("faithfulness_score", 0.0),
        "verdict": eval_result.get("verdict", "REVIEW"),
        "adversarial_challenge": eval_result.get("adversarial_challenge", ""),
        "provenance_hash": eval_result.get("provenance_hash", "")
    }
    return _append_eval.remote(record)

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
    return _append_risk.remote(record)

async def get_eval_history(limit: int = 50) -> list:
    cached = _eval_cache.get("recent_evals", [])
    if cached:
        return cached[:limit]
    return _get_evals.remote(limit)

async def get_risk_history(doc_id: str = None, limit: int = 50) -> list:
    return _get_risks.remote(doc_id, limit)

async def register_document(
    doc_id: str, doc_title: str, doc_type: str,
    gcs_path: str, user_id: str
) -> str:
    return _register_doc.remote({
        "doc_id": doc_id,
        "doc_title": doc_title,
        "doc_type": doc_type,
        "gcs_path": gcs_path,
        "ingested_by": user_id
    })

async def create_job(job_id: str, gcs_path: str, doc_type: str, user_id: str):
    return _upsert_job.remote(job_id, {
        "gcs_path": gcs_path,
        "doc_type": doc_type,
        "status": "pending",
        "created_by": user_id
    })

async def update_job(job_id: str, status: str, error: str = None):
    update = {"status": status}
    if error:
        update["error_msg"] = error[:500]
    return _upsert_job.remote(job_id, update)

async def get_job_status(job_id: str) -> Optional[dict]:
    return _get_job.remote(job_id)

# Session management (direct Dict access — fastest path)
def save_session(session_id: str, data: dict):
    _sessions[session_id] = data

def get_session(session_id: str) -> Optional[dict]:
    return _sessions.get(session_id)
EOF

```
Now update all imports in routers. Wherever the old plan said from services.oracle import ..., replace with:  
```
from services.storage import (
    store_interaction, store_risk_score, get_eval_history,
    get_risk_history, register_document, create_job,
    update_job, get_job_status
)

```
  
## Phase 5 — Corpus creation and seed ingestion (~30 min)  
```
mkdir -p ~/docrag-legal/scripts
cat > ~/docrag-legal/scripts/create_corpus.py << 'EOF'
import vertexai
from vertexai import rag
import json, os, sys

PROJECT_ID = os.environ.get("PROJECT_ID")
if not PROJECT_ID:
    sys.exit("ERROR: PROJECT_ID not set. Run: export PROJECT_ID=your-project-id")

vertexai.init(project=PROJECT_ID, location="us-central1")

corpora = {
    "statutes": "Legal Statutes — Bangladesh",
    "contracts": "Contract Templates and Precedents"
}

corpus_ids = {}
for key, display_name in corpora.items():
    print(f"Creating corpus: {display_name}...")
    corpus = rag.create_corpus(display_name=display_name)
    corpus_ids[key] = corpus.name
    print(f"  Created: {corpus.name}")

with open(os.path.expanduser("~/.docrag_corpus_ids.json"), "w") as f:
    json.dump(corpus_ids, f, indent=2)

print("\nCorpus IDs saved to ~/.docrag_corpus_ids.json")
print("\nAdd these to your .env and Secret Manager:")
for k, v in corpus_ids.items():
    print(f"  CORPUS_{k.upper()}={v}")
EOF

python3 ~/docrag-legal/scripts/create_corpus.py

```
Download seed PDFs:  
```
mkdir -p ~/docrag-legal/seed_docs/statutes
mkdir -p ~/docrag-legal/seed_docs/contracts

# Bangladesh Companies Act 1994 — bdlaws.minlaw.gov.bd
# Download manually in browser, then scp to VM
# OR use curl if direct PDF link is available:
curl -L "http://bdlaws.minlaw.gov.bd/act-details-723.html" \
  -o ~/docrag-legal/seed_docs/statutes/companies_act_1994.pdf \
  --fail --silent || echo "Manual download needed for Companies Act"

# Fallback: use these reliable public domain sources
# 1. ILO Bangladesh Labour Act (English PDF available):
curl -L "https://www.ilo.org/dyn/natlex/docs/ELECTRONIC/74481/119556/F-1222315587/BGD74481.pdf" \
  -o ~/docrag-legal/seed_docs/statutes/labour_act_2006.pdf

# 2. Contract templates from open sources
# LawInsider public templates — download 5-10 manually

# 3. MINIMAL viable corpus: even 3-4 PDFs is enough to demo
# The demo script only needs Companies Act + 2 contracts

# Upload to GCS
gsutil -m cp ~/docrag-legal/seed_docs/statutes/*.pdf \
  gs://${PROJECT_ID}-docs/statutes/

gsutil -m cp ~/docrag-legal/seed_docs/contracts/*.pdf \
  gs://${PROJECT_ID}-docs/contracts/

echo "PDFs uploaded to GCS"

```
Ingest into corpus:  
```
cat > ~/docrag-legal/scripts/ingest_seed.py << 'EOF'
import vertexai
from vertexai import rag
import json, os, sys, time

PROJECT_ID = os.environ["PROJECT_ID"]
vertexai.init(project=PROJECT_ID, location="us-central1")

with open(os.path.expanduser("~/.docrag_corpus_ids.json")) as f:
    corpus_ids = json.load(f)

GCS_BUCKET = f"gs://{PROJECT_ID}-docs"

ingest_configs = [
    {
        "corpus_name": corpus_ids["statutes"],
        "paths": [f"{GCS_BUCKET}/statutes/"],
        "chunk_size": 1024,
        "chunk_overlap": 200,
        "label": "statutes"
    },
    {
        "corpus_name": corpus_ids["contracts"],
        "paths": [f"{GCS_BUCKET}/contracts/"],
        "chunk_size": 512,
        "chunk_overlap": 100,
        "label": "contracts"
    }
]

for config in ingest_configs:
    print(f"Ingesting {config['label']}...")
    try:
        op = rag.import_files(
            corpus_name=config["corpus_name"],
            paths=config["paths"],
            transformation_config={
                "chunking_config": {
                    "chunk_size": config["chunk_size"],
                    "chunk_overlap": config["chunk_overlap"]
                }
            }
        )
        print(f"  Submitted. Operation: {op.operation.name if hasattr(op, 'operation') else 'running'}")
    except Exception as e:
        print(f"  Error: {e}")

print("\nIngestion jobs submitted.")
print("Check Vertex AI console → RAG Engine for status.")
print("Takes 2-5 min per corpus. Continue with backend setup in parallel.")
EOF

python3 ~/docrag-legal/scripts/ingest_seed.py

```
  
## Phase 6 — Secret Manager: store all secrets (~10 min)  
```
# Read corpus IDs from file created in Phase 5
CORPUS_STATUTES=$(python3 -c "import json; d=json.load(open(os.path.expanduser('~/.docrag_corpus_ids.json'))); print(d['statutes'])" 2>/dev/null || cat ~/.docrag_corpus_ids.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['statutes'])")

CORPUS_CONTRACTS=$(cat ~/.docrag_corpus_ids.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['contracts'])")

# Store in Secret Manager
echo -n "$CORPUS_STATUTES" | gcloud secrets create corpus-statutes --data-file=- --project=$PROJECT_ID
echo -n "$CORPUS_CONTRACTS" | gcloud secrets create corpus-contracts --data-file=- --project=$PROJECT_ID

# Firebase credentials (paste the JSON content)
cat /path/to/firebase-service-account.json | \
  gcloud secrets create firebase-creds --data-file=- --project=$PROJECT_ID

# Modal token (for Cloud Run to call Modal functions)
# Get your modal token:
modal token show
# Then store token ID and secret:
echo -n "PASTE_MODAL_TOKEN_ID" | gcloud secrets create modal-token-id --data-file=- --project=$PROJECT_ID
echo -n "PASTE_MODAL_TOKEN_SECRET" | gcloud secrets create modal-token-secret --data-file=- --project=$PROJECT_ID

# GCS bucket name
echo -n "${PROJECT_ID}-docs" | gcloud secrets create gcs-bucket --data-file=- --project=$PROJECT_ID

echo "All secrets stored"
gcloud secrets list --project=$PROJECT_ID

```
  
## Phase 7 — Build the backend (~6 hours of coding)  
Directory structure to create:  
```
mkdir -p ~/docrag-legal/backend/{middleware,routers,services,utils,models}
touch ~/docrag-legal/backend/{main.py,requirements.txt,Dockerfile,.env}
touch ~/docrag-legal/backend/middleware/auth.py
touch ~/docrag-legal/backend/routers/{query.py,risk.py,redline.py,ingest.py,eval.py}
touch ~/docrag-legal/backend/services/{rag.py,rerank.py,gemini.py,eval_judge.py,storage.py}
touch ~/docrag-legal/backend/utils/retry.py
touch ~/docrag-legal/backend/models/schemas.py

```
Write .env for local dev:  
```
cat > ~/docrag-legal/backend/.env << 'EOF'
PROJECT_ID=YOUR_PROJECT_ID
REGION=us-central1
GCS_BUCKET=YOUR_PROJECT_ID-docs
CORPUS_STATUTES=projects/xxx/locations/us-central1/ragCorpora/xxx
CORPUS_CONTRACTS=projects/xxx/locations/us-central1/ragCorpora/xxx
FIREBASE_CREDENTIALS_JSON=PASTE_FULL_JSON_HERE_AS_SINGLE_LINE
MODAL_TOKEN_ID=your_modal_token_id
MODAL_TOKEN_SECRET=your_modal_token_secret
APP_ENV=development
EOF

```
Write requirements.txt:  
```
cat > ~/docrag-legal/backend/requirements.txt << 'EOF'
fastapi==0.115.0
uvicorn[standard]==0.30.6
firebase-admin==6.5.0
google-cloud-aiplatform==1.67.1
google-cloud-storage==2.18.2
google-cloud-discoveryengine==0.13.4
vertexai==1.67.1
pydantic==2.8.2
slowapi==0.1.9
python-dotenv==1.0.1
httpx==0.27.2
modal==0.64.145
python-multipart==0.0.9
EOF

```
Write main.py:  
```
cat > ~/docrag-legal/backend/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from routers import query, risk, redline, ingest, eval as eval_router

app = FastAPI(
    title="DocRAG Legal",
    description="Contract risk intelligence with adversarial self-auditing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, tags=["Query"])
app.include_router(risk.router, tags=["Risk"])
app.include_router(redline.router, tags=["Redline"])
app.include_router(ingest.router, tags=["Ingest"])
app.include_router(eval_router.router, tags=["Eval"])

@app.get("/health")
async def health():
    return {"status": "ok", "project": os.environ.get("PROJECT_ID")}
EOF

```
Copy all service files from the master plan (previous response). The files to write directly — these contain the hard architecture:  
```
services/gemini.py    → lazy init version (from corrections above)
services/rag.py       → retrieve() with detect_alpha()
services/rerank.py    → rerank() with Ranking API
services/eval_judge.py → judge() with adversarial prompt
services/storage.py   → Modal client (from Phase 4 above)
middleware/auth.py    → Firebase JWT + role injection
utils/retry.py        → with_retry() decorator
models/schemas.py     → all Pydantic models

```
Files to generate with Gemini CLI (run these after writing core services):  
```
# Run each prompt from the master plan corrections
# Prompt 1: requirements.txt (already done above, skip)
# Prompt 2: Dockerfile
# Prompts 3-7: frontend components (do in Phase 9)

# For Dockerfile, run this Gemini CLI command:
gemini "Write a minimal Dockerfile for a FastAPI app. 
Base image: python:3.11-slim. 
Port 8080. 
Entry point: uvicorn main:app --host 0.0.0.0 --port 8080.
Copy requirements.txt, install deps, copy app code.
No unnecessary layers. Output only the Dockerfile content."

```
Test backend locally before deploying:  
```
cd ~/docrag-legal/backend
uvicorn main:app --reload --port 8080

# In another tmux pane:
curl http://localhost:8080/health
# Expected: {"status":"ok","project":"your-project-id"}

# Test query endpoint (will fail gracefully if corpus not ready)
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SKIP_FOR_LOCAL_TEST" \
  -d '{"question":"What does Section 14 say?","session_id":"test-001","corpus_type":"statutes"}'

```
Disable auth for local testing temporarily:  
```
# In middleware/auth.py, add at top of verify_token():
if os.environ.get("APP_ENV") == "development":
    return {"uid": "dev-user", "role": "admin"}

```
  
## Phase 8 — Cloud Run deployment (~20 min)  
Write Dockerfile (or use Gemini output):  
```
cat > ~/docrag-legal/backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

```
Deploy:  
```
cd ~/docrag-legal/backend

# Source-based deploy — Cloud Build builds the container for you
# No local Docker needed
gcloud run deploy docrag-api \
  --source . \
  --region $REGION \
  --service-account docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com \
  --set-env-vars \
    PROJECT_ID=${PROJECT_ID},\
    REGION=us-central1,\
    APP_ENV=production \
  --set-secrets \
    CORPUS_STATUTES=corpus-statutes:latest,\
    CORPUS_CONTRACTS=corpus-contracts:latest,\
    FIREBASE_CREDENTIALS_JSON=firebase-creds:latest,\
    GCS_BUCKET=gcs-bucket:latest,\
    MODAL_TOKEN_ID=modal-token-id:latest,\
    MODAL_TOKEN_SECRET=modal-token-secret:latest \
  --allow-unauthenticated \
  --concurrency 80 \
  --memory 1Gi \
  --min-instances 0 \
  --max-instances 10

# Save API URL
export API_URL=$(gcloud run services describe docrag-api \
  --region $REGION \
  --format='value(status.url)')
echo "API deployed: $API_URL"
echo "export API_URL=$API_URL" >> ~/.bashrc

# Smoke test
curl $API_URL/health

```
  
## Phase 9 — Frontend (~3 hours)  
```
mkdir -p ~/docrag-legal/frontend
cd ~/docrag-legal/frontend

# Init Next.js 14
npx create-next-app@14 . \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --no-src-dir \
  --import-alias "@/*"

# Install deps
npm install react-markdown firebase chart.js react-chartjs-2

# Create env file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=$API_URL
NEXT_PUBLIC_FIREBASE_API_KEY=from_firebase_console
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=$PROJECT_ID
EOF

```
Get Firebase web config:  
```
Firebase console → Project Settings → Your apps → Add app → Web
Copy the firebaseConfig object values into .env.local

```
Generate all 5 frontend components with Gemini CLI:  
```
# Run each of the 7 prompts from the master plan corrections
# Save output to the correct file paths:

gemini "PROMPT_3_CONTENT" > ~/docrag-legal/frontend/components/ChatPanel.tsx
gemini "PROMPT_4_CONTENT" > ~/docrag-legal/frontend/components/ProvenanceTree.tsx
gemini "PROMPT_5_CONTENT" > ~/docrag-legal/frontend/components/RiskHeatmap.tsx
gemini "PROMPT_6_CONTENT" > ~/docrag-legal/frontend/components/RedlinePanel.tsx
gemini "PROMPT_7_CONTENT" > ~/docrag-legal/frontend/components/AdversarialPanel.tsx

```
Create lib/firebase.ts:  
```
import { initializeApp, getApps } from 'firebase/app'
import { getAuth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
}

const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0]
export const auth = getAuth(app)

```
Create lib/api.ts:  
```
const API = process.env.NEXT_PUBLIC_API_URL

async function authFetch(path: string, opts: RequestInit = {}) {
  const { getAuth } = await import('firebase/auth')
  const user = getAuth().currentUser
  const token = user ? await user.getIdToken() : ''
  
  return fetch(`${API}${path}`, {
    ...opts,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...opts.headers,
    }
  })
}

export const api = {
  query:    (body: object) => authFetch('/query', { method: 'POST', body: JSON.stringify(body) }),
  risk:     (body: object) => authFetch('/risk', { method: 'POST', body: JSON.stringify(body) }),
  redline:  (body: object) => authFetch('/redline', { method: 'POST', body: JSON.stringify(body) }),
  ingest:   (form: FormData) => authFetch('/ingest', { method: 'POST', body: form, headers: {} }),
  evalHistory: () => authFetch('/eval'),
  batchEval: () => authFetch('/eval/batch', { method: 'POST' }),
  jobStatus: (id: string) => authFetch(`/ingest/status/${id}`),
}

```
Deploy frontend to Vercel:  
```
cd ~/docrag-legal/frontend

# Install Vercel CLI if not present
npm install -g vercel

# Deploy (will prompt for account on first run)
vercel --prod

# Set env vars in Vercel dashboard after first deploy:
# vercel.com → your project → Settings → Environment Variables
# Add all NEXT_PUBLIC_* vars from .env.local

```
  
## Phase 10 — Cloud Scheduler for batch eval (~5 min)  
```
# Create scheduler job — hits /eval/batch, not /eval
gcloud scheduler jobs create http docrag-eval-batch \
  --schedule "0 */6 * * *" \
  --uri "${API_URL}/eval/batch" \
  --http-method POST \
  --location $REGION \
  --oidc-service-account-email docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com \
  --attempt-deadline 300s

# Verify scheduler created
gcloud scheduler jobs list --location $REGION

# Manual trigger to test (runs immediately)
gcloud scheduler jobs run docrag-eval-batch --location $REGION

```
  
## Phase 11 — End-to-end smoke test  
```
# 1. Health check
curl $API_URL/health

# 2. Ingest test (requires auth token — get from Firebase console test)
# Or temporarily disable auth in APP_ENV=development

# 3. Query test
curl -X POST $API_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the restrictions on share transfers for private companies?",
    "session_id": "smoke-test-001",
    "corpus_type": "statutes"
  }'

# 4. Risk test
curl -X POST $API_URL/risk \
  -H "Content-Type: application/json" \
  -d '{
    "clause_text": "Either party may terminate this agreement with 7 days notice.",
    "doc_id": "test-doc-001",
    "clause_ref": "Section 12.1"
  }'

# 5. Redline test
curl -X POST $API_URL/redline \
  -H "Content-Type: application/json" \
  -d '{
    "clause_text": "Contractor shall deliver work product as requested by Client.",
    "compliance_target": "Bangladesh Contract Act"
  }'

# 6. Eval history
curl $API_URL/eval

# Expected: JSON responses for all. Any 500 = check Cloud Run logs:
gcloud run services logs read docrag-api --region $REGION --limit 50

```
  
## Phase 12 — Demo prep and README (~1 hour)  
```
# Record Loom following exactly this sequence (from Arena v4 demo script):
# 0:00-0:30  Upload Companies Act PDF → show ingestion status polling
# 0:30-1:00  Upload sample MSA contract
# 1:00-2:00  Query: "Does Section 14 restrict share transfers?"
#            → Show answer + citations + provenance tree
# 2:00-2:45  Show adversarial panel → "1 challenge raised"
# 2:45-3:30  Switch to Risk tab → paste termination clause → RED heatmap
# 3:30-4:00  Click RED clause → compliance card with statute refs
# 4:00-4:15  Switch to Redline tab → show suggested rewrite
# 4:15-4:30  Show Eval Dashboard → faithfulness chart from Oracle logs
# 4:30-5:00  Show README → architecture diagram, north-star sentence

# Write README
cat > ~/docrag-legal/README.md << 'EOF'
# DocRAG-Legal

> Contract risk intelligence with adversarial self-auditing — every answer is 
> challenged by a second model, every citation is hash-verified, every risk 
> assessment cites the specific statute it violates.

Built on Vertex AI RAG Engine with Gemini-as-judge evaluation harness.

## Architecture
[paste Mermaid diagram from Arena v4]

## Features
- /query   — RAG synthesis with inline adversarial challenge
- /risk    — Clause-level RED/YELLOW/GREEN heatmap against BD statutes  
- /redline — Suggested rewrites with statute-backed reasoning
- /ingest  — PDF upload with async processing and status polling
- /eval    — Faithfulness scoring + batch re-evaluation

## Stack
Vertex AI RAG Engine · Gemini 1.5 Pro (synthesis) · Gemini 1.5 Flash (judge) ·
FastAPI · Next.js 14 · Modal (persistence) · Firebase Auth · Cloud Run · Vercel

## Eval harness
Every /query response includes:
- faithfulness_score: 0.0–1.0 (Gemini-as-judge)
- adversarial_challenge: counter-argument from second model call
- provenance_hash: SHA-256 of question + answer + context
- verdict: PASS | REVIEW | FAIL

Automated batch re-evaluation runs every 6 hours via Cloud Scheduler.
EOF

```
  
## Summary: what Modal replaced and what it costs  

| Was | Now | Cost |
| --------------------------------------------------------- | ------------------------------------------- | ------------------------- |
| Oracle Autonomous DB (wallet setup, oracledb driver, DDL) | Modal Volumes (NDJSON) + Modal Dict (cache) | ~$2–5 of your $60 credits |
| create_pool_async bug | run_in_executor pattern → eliminated | — |
| Wallet file in container | Nothing — Modal is pure Python | — |
| Schema migrations | Append-only NDJSON — no migrations ever | — |
  
Modal cold start on first .remote() call: ~2 seconds. Subsequent calls: ~100ms. Acceptable for a portfolio demo. Not acceptable for sub-100ms SLAs — that's your honest architectural caveat when asked.  
Start at Phase 0. Everything above is terminal-executable from Termius.  
