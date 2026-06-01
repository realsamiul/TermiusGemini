#!/bin/bash
# DocRAG-V2 Pre-flight Setup
# Run this yourself before handing anything to Gemini CLI.
# Every section is idempotent — safe to re-run.
set -e

echo "=== DocRAG-V2 Pre-flight Setup ==="
echo ""

# ── 0. Environment check ──────────────────────────────────────────────────────
echo "[0] Checking environment..."
python3 --version || { echo "ERROR: python3 not found"; exit 1; }
gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 || { echo "ERROR: not authenticated to gcloud"; exit 1; }
modal token show > /dev/null 2>&1 || { echo "ERROR: modal not authenticated. Run: modal token new"; exit 1; }

export PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
export REGION="us-central1"
[ -z "$PROJECT_ID" ] && { echo "ERROR: no GCP project set. Run: gcloud config set project YOUR_ID"; exit 1; }
echo "  PROJECT_ID: $PROJECT_ID"
echo "  REGION: $REGION"
echo "" >> ~/.bashrc
echo "export PROJECT_ID=$PROJECT_ID" >> ~/.bashrc
echo "export REGION=$REGION" >> ~/.bashrc

# ── 1. Folder structure ───────────────────────────────────────────────────────
echo "[1] Creating folder structure..."
mkdir -p ~/docrag-v2/{protected,modal,backend/{middleware,routers,services,models,utils},frontend,scripts,seed_docs/{statutes,contracts}}
echo "  Done"

# ── 2. GCP APIs + IAM ─────────────────────────────────────────────────────────
echo "[2] Enabling GCP APIs..."
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  storage.googleapis.com \
  secretmanager.googleapis.com \
  cloudscheduler.googleapis.com \
  discoveryengine.googleapis.com \
  --quiet
echo "  APIs enabled"

echo "[2] Creating GCS bucket..."
gsutil mb -l $REGION gs://${PROJECT_ID}-docs 2>/dev/null || echo "  Bucket already exists"

echo "[2] Setting up service account..."
gcloud iam service-accounts create docrag-sa \
  --display-name="DocRAG Service Account" 2>/dev/null || echo "  SA already exists"

SA="docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com"
for ROLE in \
  roles/aiplatform.user \
  roles/storage.objectAdmin \
  roles/secretmanager.secretAccessor \
  roles/discoveryengine.viewer \
  roles/firebaseauth.admin; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="$ROLE" --quiet 2>/dev/null
done
echo "  IAM roles granted"

# ── 3. Modal setup ────────────────────────────────────────────────────────────
echo "[3] Storing Modal token in Secret Manager..."
TOKEN_ID=$(grep "token_id" ~/.modal.toml 2>/dev/null | head -1 | cut -d'"' -f2 || echo "")
TOKEN_SECRET=$(grep "token_secret" ~/.modal.toml 2>/dev/null | head -1 | cut -d'"' -f2 || echo "")

if [ -z "$TOKEN_ID" ]; then
  echo "  WARNING: Could not read Modal token from ~/.modal.toml"
  echo "  Run 'modal token show' and store values manually"
else
  echo -n "$TOKEN_ID" | gcloud secrets create modal-token-id \
    --data-file=- --project=$PROJECT_ID 2>/dev/null || \
    echo -n "$TOKEN_ID" | gcloud secrets versions add modal-token-id \
    --data-file=- --project=$PROJECT_ID
  echo -n "$TOKEN_SECRET" | gcloud secrets create modal-token-secret \
    --data-file=- --project=$PROJECT_ID 2>/dev/null || \
    echo -n "$TOKEN_SECRET" | gcloud secrets versions add modal-token-secret \
    --data-file=- --project=$PROJECT_ID
  echo "  Modal token stored"
fi

# ── 4. GCS bucket secret ──────────────────────────────────────────────────────
echo "[4] Storing GCS bucket name as secret..."
echo -n "${PROJECT_ID}-docs" | gcloud secrets create gcs-bucket \
  --data-file=- --project=$PROJECT_ID 2>/dev/null || \
  echo -n "${PROJECT_ID}-docs" | gcloud secrets versions add gcs-bucket \
  --data-file=- --project=$PROJECT_ID
echo "  GCS bucket secret stored"

# ── 5. Vertex RAG corpus creation ─────────────────────────────────────────────
echo "[5] Creating Vertex RAG corpora (serverless mode)..."
pip install google-cloud-aiplatform vertexai --quiet 2>/dev/null

python3 ~/docrag-v2/scripts/create_corpus.py 2>&1 | tail -10

if [ -f ~/.docrag_corpus_ids.json ]; then
  CORPUS_STATUTES=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.docrag_corpus_ids.json'))); print(d['statutes'])")
  CORPUS_CONTRACTS=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.docrag_corpus_ids.json'))); print(d['contracts'])")

  echo -n "$CORPUS_STATUTES" | gcloud secrets create corpus-statutes \
    --data-file=- --project=$PROJECT_ID 2>/dev/null || \
    echo -n "$CORPUS_STATUTES" | gcloud secrets versions add corpus-statutes \
    --data-file=- --project=$PROJECT_ID

  echo -n "$CORPUS_CONTRACTS" | gcloud secrets create corpus-contracts \
    --data-file=- --project=$PROJECT_ID 2>/dev/null || \
    echo -n "$CORPUS_CONTRACTS" | gcloud secrets versions add corpus-contracts \
    --data-file=- --project=$PROJECT_ID
  echo "  Corpus secrets stored"
else
  echo "  WARNING: corpus creation may have failed — check above output"
fi

# ── 6. Deploy Modal persistence app ───────────────────────────────────────────
echo "[6] Deploying Modal persistence app..."
if [ -f ~/docrag-v2/protected/store.py ]; then
  mkdir -p ~/docrag-v2/modal
  cp ~/docrag-v2/protected/store.py ~/docrag-v2/modal/
  cd ~/docrag-v2/modal
  modal deploy store.py
  echo "  Modal app deployed"
else
  echo "  WARNING: ~/docrag-v2/protected/store.py not found"
  echo "  Write the store.py protected file first, then re-run this script"
fi

# ── 7. Copy protected files into backend ──────────────────────────────────────
echo "[7] Copying protected files to backend..."
for f in gemini.py rag.py rerank.py eval_judge.py storage.py; do
  if [ -f ~/docrag-v2/protected/$f ]; then
    cp ~/docrag-v2/protected/$f ~/docrag-v2/backend/services/
    echo "  Copied services/$f"
  else
    echo "  MISSING: protected/$f — write this file before continuing"
  fi
done

if [ -f ~/docrag-v2/protected/query.py ]; then
  cp ~/docrag-v2/protected/query.py ~/docrag-v2/backend/routers/
  echo "  Copied routers/query.py"
else
  echo "  MISSING: protected/query.py"
fi

# ── 8. Summary ────────────────────────────────────────────────────────────────
echo ""
echo "=== Pre-flight complete ==="
echo ""
echo "MANUAL STEPS STILL REQUIRED:"
echo "  1. Firebase console: enable Email/Password auth"
echo "     URL: https://console.firebase.google.com"
echo "     Project: $PROJECT_ID"
echo "     Build → Authentication → Sign-in method → Email/Password → Enable"
echo "  2. Create test user: test@docrag.dev / TestPass123!"
echo "  3. Note the UID and run the custom claims script from MASTER_PLAN_V2.md"
echo ""
echo "THEN run the Gemini CLI phases from MASTER_PLAN_V2.md Part 10:"
echo "  tmux new -s docrag-build"
echo "  cd ~/docrag-v2"
echo "  [copy Phase A command from MASTER_PLAN_V2.md]"
echo ""
echo "Secrets stored:"
gcloud secrets list --project=$PROJECT_ID --format="value(name)" 2>/dev/null | sort
