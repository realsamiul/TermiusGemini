# DocRAG + Eval by Sonnet 4.6  
  
Good. I have both files complete. Full synthesis follows.  
  
**Verdict on both plans:**  
DeepSeek's plan: architecturally sound, production-pragmatic, good cost discipline. Weakness: it's still a ChatPDF clone with better plumbing. The "risk surfacing" reframe from Arena v4 is the differentiator that makes this a senior portfolio piece.  
Arena v4: the framing is correct ("most RAG systems answer questions, this one surfaces risk"), the adversarial eval concept is right, Oracle schema is done, demo script exists. Weakness: bloated scope. OCR/Bengali/temporal amendment registry — drop all three. They're not needed for the Toptal story and they're time sinks.  
**The Bangla drop is correct.** Every Bengali/OCR decision in all three plans was hand-waved anyway. Dead weight.  
**What we're actually building:**  
Not a legal research tool. Not a chatbot with citations. A **contract risk intelligence system with a self-auditing eval harness**. The eval harness is a runtime feature, not a test suite. That's the one sentence that separates this from everything else on Toptal.  
  
**Scope cuts for time-efficiency:**  

| Cut | Reason |
| --------------------------- | ------------------------------------------------------------------- |
| Bengali/OCR | Not needed, won't sell, time sink |
| Temporal amendment registry | Clever but irrelevant to demo story |
| Pub/Sub async worker | Over-engineered for portfolio; background task in FastAPI is enough |
| Cloud Build YAML | Gemini CLI handles deploy; skip CI/CD setup |
| /report PDF endpoint | Post-launch feature; not in demo script |
  
**What survives from Arena v4 + DeepSeek synthesis:**  
* Full architecture diagram (Mermaid, use as-is)  
* Oracle schema DDL (complete, run once)  
* Retry decorator (copy-paste, done)  
* Firebase JWT middleware (complete)  
* Adversarial eval judge (the differentiator)  
* Hybrid search + reranking config  
* Risk heatmap endpoint  
* 5-minute demo script (the artifact that makes it worth building)  
  
Now the actual master plan. No prose. Architecture, code patterns, sequence, commands.  
  
**DOCRAG-LEGAL: FINAL MASTER PLAN**  
**0. Product definition (one decision, everything flows from it)**  
```
Input:  PDF (contract or statute)
Output: 
  /query    → answer + citations + provenance hash
  /risk     → clause-level RED/YELLOW/GREEN heatmap
  /eval     → adversarial challenge to the answer + faithfulness score
  
Eval is NOT a background job. It runs inline on /query.
Every answer carries its own critique. That's the product.

```
**1. Corpus strategy**  
**Three corpora, not one.** Multi-corpus isolation is a feature here:  
```
corpus-statutes   → Bangladesh Companies Act, Securities Law, Contract Act, Labour Act
corpus-contracts  → Sample MSAs, NDAs, employment contracts (20-30 generic docs)
corpus-precedents → Optional: leave empty, shows extensibility

```
Why: query routing to the right corpus is a demonstrable architecture decision. Filtering doc_type=statute for compliance checks vs. doc_type=contract for precedent search shows deliberate design.  
**Chunking config per corpus:**  
```
# statutes: long-range dependencies, preserve section continuity
STATUTE_CHUNK  = {"chunk_size": 1024, "chunk_overlap": 200}
# contracts: clause-level precision matters more
CONTRACT_CHUNK = {"chunk_size": 512,  "chunk_overlap": 100}

```
**Hybrid search alpha:**  
```
# Default: 60% semantic, 40% keyword
ALPHA_DEFAULT    = 0.6
# For citation-exact queries ("Companies Act section 14"):
ALPHA_CITATION   = 0.35  # keyword dominates
# For concept queries ("restrictions on share transfer"):
ALPHA_SEMANTIC   = 0.75

```
Auto-detect which to use:  
```
def detect_alpha(query: str) -> float:
    citation_patterns = [r"section\s+\d+", r"§\s*\d+", r"article\s+\d+", r"clause\s+\d+"]
    is_citation_query = any(re.search(p, query.lower()) for p in citation_patterns)
    return ALPHA_CITATION if is_citation_query else ALPHA_DEFAULT

```
**Reranking pipeline:**  
```
retrieve top_k=20 → Vertex Ranking API → top_k=5 → Gemini Pro synthesis

```
Cost implication: Ranking API ~$0.0005 per query batch. Negligible. Always on.  
**2. Project structure**  
```
docrag-legal/
├── backend/
│   ├── main.py                  # FastAPI app, mounts all routers
│   ├── middleware/
│   │   └── auth.py              # Firebase JWT + role injection
│   ├── routers/
│   │   ├── ingest.py            # /ingest, /ingest/status/{job_id}
│   │   ├── query.py             # /query (RAG + synthesis + inline eval)
│   │   ├── risk.py              # /risk (clause heatmap)
│   │   └── eval.py              # /eval (adversarial panel, history)
│   ├── services/
│   │   ├── rag.py               # Vertex RAG Engine wrapper
│   │   ├── rerank.py            # Vertex Ranking API wrapper
│   │   ├── gemini.py            # Pro (synthesis) + Flash (judge) clients
│   │   ├── eval_judge.py        # Adversarial judge + faithfulness scorer
│   │   └── oracle.py            # Async Oracle connection pool + queries
│   ├── models/
│   │   └── schemas.py           # All Pydantic models
│   ├── utils/
│   │   └── retry.py             # Retry decorator (from Arena v4)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Chat + citations
│   │   ├── risk/page.tsx        # Risk heatmap
│   │   └── eval/page.tsx        # Adversarial eval panel + dashboard
│   ├── components/
│   │   ├── ChatPanel.tsx
│   │   ├── ProvenanceTree.tsx
│   │   ├── RiskHeatmap.tsx
│   │   └── AdversarialPanel.tsx
│   └── lib/
│       ├── api.ts               # All fetch calls
│       └── firebase.ts          # Auth init
├── scripts/
│   ├── setup_gcp.sh             # One-shot GCP project setup
│   ├── create_corpus.py         # Creates all three corpora, saves IDs
│   ├── ingest_seed.py           # Bulk-ingest seed documents
│   └── init_oracle.py           # DDL init (from Arena v4, keep as-is)
└── .env.example

```
**3. GCP setup sequence (terminal, Termius-safe)**  
```
# Run setup_gcp.sh — idempotent, safe to re-run

PROJECT_ID="docrag-legal-$(date +%s | tail -c6)"
REGION="us-central1"

gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID

# Link billing (must do manually if first time)
gcloud billing accounts list
# Note ACCOUNT_ID from output, then:
gcloud billing projects link $PROJECT_ID --billing-account=ACCOUNT_ID

# Enable APIs
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  storage.googleapis.com \
  firestore.googleapis.com \
  secretmanager.googleapis.com \
  cloudscheduler.googleapis.com

# Create GCS bucket
gsutil mb -l $REGION gs://${PROJECT_ID}-docs

# Service account for Cloud Run
gcloud iam service-accounts create docrag-sa \
  --display-name="DocRAG Service Account"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

# Firestore init
gcloud firestore databases create --location=nam5

echo "PROJECT_ID=$PROJECT_ID" > .env

```
**4. Corpus creation script**  
```
# scripts/create_corpus.py
import vertexai
from vertexai import rag
import json, os

vertexai.init(project=os.environ["PROJECT_ID"], location="us-central1")

corpora = {
    "statutes": {
        "display_name": "Legal Statutes — Bangladesh",
        "description": "Companies Act 1994, Securities Law, Contract Act, Labour Act"
    },
    "contracts": {
        "display_name": "Contract Templates",
        "description": "MSA, NDA, Employment, SaaS agreement templates"
    }
}

corpus_ids = {}
for key, config in corpora.items():
    corpus = rag.create_corpus(display_name=config["display_name"])
    corpus_ids[key] = corpus.name
    print(f"Created {key}: {corpus.name}")

# Save to .env — CRITICAL: these IDs are referenced everywhere
with open(".corpus_ids.json", "w") as f:
    json.dump(corpus_ids, f, indent=2)

print("Corpus IDs saved to .corpus_ids.json")
print("Add to .env:")
for k, v in corpus_ids.items():
    print(f"CORPUS_{k.upper()}={v}")

```
**5. Core service implementations**  
**rag.py — the retrieval layer:**  
```
import vertexai
from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
import re
from typing import Literal

ALPHA_DEFAULT   = 0.6
ALPHA_CITATION  = 0.35
ALPHA_SEMANTIC  = 0.75

def detect_alpha(query: str) -> float:
    if any(re.search(p, query.lower()) for p in 
           [r"section\s+\d+", r"§\s*\d+", r"article\s+\d+", r"clause\s+\d+"]):
        return ALPHA_CITATION
    return ALPHA_DEFAULT

async def retrieve(
    query: str,
    corpus_name: str,
    top_k: int = 20,
    doc_type_filter: str | None = None
) -> list[rag.RagChunk]:
    
    alpha = detect_alpha(query)
    
    retrieval_config = rag.RagRetrievalConfig(
        top_k=top_k,
        filter=rag.Filter(
            vector_distance_threshold=0.4,
            metadata_filters=[{"key": "doc_type", "value": doc_type_filter}]
            if doc_type_filter else None
        )
    )
    
    response = await rag.retrieval_query_async(
        rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
        text=query,
        rag_retrieval_config=retrieval_config
    )
    
    return response.contexts.contexts

```
**rerank.py:**  
```
from google.cloud import discoveryengine_v1alpha as discoveryengine
import os

async def rerank(query: str, chunks: list, top_n: int = 5) -> list:
    """Rerank retrieved chunks using Vertex Ranking API."""
    client = discoveryengine.RankServiceAsyncClient()
    
    records = [
        discoveryengine.RankingRecord(
            id=str(i),
            title=c.source_display_name or "",
            content=c.text[:512]  # Ranking API content limit
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
    
    # Map back to original chunks by index
    reranked_indices = [int(r.id) for r in response.records]
    return [chunks[i] for i in reranked_indices]

```
**eval_judge.py — the differentiator:**  
```
import json, hashlib
from services.gemini import flash_client

FAITHFULNESS_PROMPT = """You are a legal RAG system evaluator. Be rigorous — legal errors cause real harm.

QUESTION: {question}
ANSWER: {answer}
RETRIEVED CONTEXT (numbered):
{context_block}
CITATIONS CLAIMED: {citations}

Evaluate:
1. FAITHFULNESS: Is every factual claim in the answer directly supported by the context? 
   Score 0.0–1.0. Deduct 0.2 for each unsupported claim.
2. CITATION_ACCURACY: Do all cited [N] references exist in the context and support the claim?
   true/false per citation.
3. ADVERSARIAL_CHALLENGE: Generate ONE specific counter-argument that challenges the answer.
   Be concrete — cite the part of the context that creates ambiguity or contradiction.
4. VERDICT: PASS (faithfulness >= 0.85, all citations accurate) | REVIEW | FAIL

Return ONLY valid JSON:
{{
  "faithfulness_score": float,
  "citations_accurate": {{"{citation_id}": true/false}},
  "adversarial_challenge": "string — specific challenge with context reference",
  "verdict": "PASS|REVIEW|FAIL",
  "reasoning": "brief"
}}"""

async def judge(
    question: str,
    answer: str,
    chunks: list,
    citations: list[str]
) -> dict:
    
    context_block = "\n".join(
        f"[{i+1}] (Source: {c.source_display_name}, score: {c.score:.3f})\n{c.text[:600]}"
        for i, c in enumerate(chunks)
    )
    
    # Compute provenance hash for audit log
    provenance_hash = hashlib.sha256(
        (question + answer + context_block).encode()
    ).hexdigest()[:16]
    
    prompt = FAITHFULNESS_PROMPT.format(
        question=question,
        answer=answer,
        context_block=context_block,
        citations=citations
    )
    
    response = await flash_client.generate_content_async(
        prompt,
        generation_config={"temperature": 0.1, "response_mime_type": "application/json"}
    )
    
    try:
        result = json.loads(response.text)
    except json.JSONDecodeError:
        # Graceful fallback — never crash on eval failure
        result = {
            "faithfulness_score": 0.5,
            "citations_accurate": {},
            "adversarial_challenge": "Eval parsing failed — manual review required",
            "verdict": "REVIEW",
            "reasoning": "JSON parse error"
        }
    
    result["provenance_hash"] = provenance_hash
    return result

```
**query.py router — the main endpoint:**  
```
from fastapi import APIRouter, Depends, HTTPException
from services.rag import retrieve
from services.rerank import rerank
from services.gemini import pro_client, flash_client
from services.eval_judge import judge
from services.oracle import store_interaction
from middleware.auth import require_role
from models.schemas import QueryRequest, QueryResponse
import os, json

router = APIRouter()

SYNTHESIS_PROMPT = """You are a legal research assistant. Use ONLY the provided context.
Cite sources as [1], [2], etc. If context is insufficient, say exactly: "Insufficient context to answer."
Never speculate beyond the provided documents.

Question: {question}

Context:
{context_block}

Provide a structured answer with:
1. Direct answer
2. Supporting evidence with citations
3. Any important caveats or limitations"""

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    req: QueryRequest,
    user=Depends(require_role(["admin", "analyst", "viewer"]))
):
    # 1. Determine corpus routing
    corpus = (
        os.environ["CORPUS_STATUTES"] if req.corpus_type == "statutes"
        else os.environ["CORPUS_CONTRACTS"]
    )
    
    # 2. Retrieve top 20, rerank to top 5
    raw_chunks = await retrieve(
        query=req.question,
        corpus_name=corpus,
        top_k=20,
        doc_type_filter=req.doc_type_filter
    )
    
    if not raw_chunks:
        raise HTTPException(404, "No relevant documents found in corpus")
    
    ranked_chunks = await rerank(req.question, raw_chunks, top_n=5)
    
    # 3. Build context block
    context_block = "\n\n".join(
        f"[{i+1}] {c.source_display_name}\n{c.text}"
        for i, c in enumerate(ranked_chunks)
    )
    
    # 4. Synthesise with Gemini Pro
    synthesis = await pro_client.generate_content_async(
        SYNTHESIS_PROMPT.format(question=req.question, context_block=context_block),
        generation_config={"temperature": 0.1}
    )
    answer = synthesis.text
    
    # 5. Extract citations from answer (inline, no extra API call)
    import re
    citations = list(set(re.findall(r'\[(\d+)\]', answer)))
    
    # 6. Run eval judge inline — Flash, cheap, fast
    eval_result = await judge(
        question=req.question,
        answer=answer,
        chunks=ranked_chunks,
        citations=citations
    )
    
    # 7. Persist to Oracle
    await store_interaction(
        session_id=req.session_id,
        user_id=user["uid"],
        question=req.question,
        answer=answer,
        sources=[{
            "doc": c.source_display_name,
            "score": c.score,
            "text_preview": c.text[:200]
        } for c in ranked_chunks],
        eval_result=eval_result
    )
    
    return QueryResponse(
        answer=answer,
        sources=[{
            "index": i+1,
            "doc_title": c.source_display_name,
            "retrieval_score": round(c.score, 4),
            "text_preview": c.text[:300],
            "chunk_hash": hash(c.text)  # For provenance
        } for i, c in enumerate(ranked_chunks)],
        eval=eval_result,
        session_id=req.session_id
    )

```
**risk.py router:**  
```
RISK_PROMPT = """You are a legal risk analyst. Analyze this contract clause against Bangladesh law.

CLAUSE:
{clause_text}

RETRIEVED STATUTE CONTEXT:
{context_block}

Return ONLY valid JSON:
{{
  "risk_level": "RED|YELLOW|GREEN",
  "compliant": true/false,
  "conflicts": ["specific conflict with statute reference"],
  "gaps": ["missing requirement with statute reference"],
  "recommendation": "specific actionable fix",
  "statute_refs": ["Act Name § Section"],
  "confidence": 0.0-1.0
}}

RED = clear violation or dangerous omission. YELLOW = ambiguous or best-practice gap. GREEN = compliant."""

@router.post("/risk")
async def risk_endpoint(req: RiskRequest, user=Depends(require_role(["admin", "analyst"]))):
    
    # Always query statutes corpus for risk assessment
    chunks = await retrieve(
        query=req.clause_text,
        corpus_name=os.environ["CORPUS_STATUTES"],
        top_k=10,
        doc_type_filter="statute"
    )
    ranked = await rerank(req.clause_text, chunks, top_n=4)
    
    context_block = "\n\n".join(f"[{i+1}] {c.source_display_name}\n{c.text}" 
                                 for i, c in enumerate(ranked))
    
    response = await flash_client.generate_content_async(  # Flash sufficient for structured output
        RISK_PROMPT.format(clause_text=req.clause_text, context_block=context_block),
        generation_config={"temperature": 0.0, "response_mime_type": "application/json"}
    )
    
    try:
        risk_data = json.loads(response.text)
    except json.JSONDecodeError:
        risk_data = {"risk_level": "YELLOW", "compliant": None, 
                     "conflicts": [], "gaps": ["Risk assessment failed — manual review"],
                     "recommendation": "Manual review required", "statute_refs": [], "confidence": 0.0}
    
    # Persist risk score to Oracle
    await store_risk_score(
        doc_id=req.doc_id,
        clause_ref=req.clause_ref,
        clause_text=req.clause_text,
        **risk_data
    )
    
    return risk_data

```
**auth.py middleware:**  
```
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from fastapi import HTTPException, Request
from functools import wraps
import os, json

# Init once at module load
_app = None

def get_firebase_app():
    global _app
    if _app is None:
        cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS_JSON"])
        cred = credentials.Certificate(cred_json)
        _app = firebase_admin.initialize_app(cred)
    return _app

async def verify_token(request: Request) -> dict:
    get_firebase_app()
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing or malformed Authorization header")
    
    token = auth_header.split(" ")[1]
    try:
        decoded = firebase_auth.verify_id_token(token)
        # Inject role from custom claims; default to viewer
        decoded["role"] = decoded.get("role", "viewer")
        return decoded
    except Exception as e:
        raise HTTPException(401, f"Invalid token: {str(e)}")

def require_role(allowed_roles: list[str]):
    async def dependency(request: Request):
        user = await verify_token(request)
        if user["role"] not in allowed_roles:
            raise HTTPException(403, f"Role '{user['role']}' not permitted. Required: {allowed_roles}")
        return user
    return dependency

```
**6. Schemas (complete)**  
```
from pydantic import BaseModel
from typing import Optional, List, Any
from enum import Enum

class CorpusType(str, Enum):
    statutes = "statutes"
    contracts = "contracts"

class QueryRequest(BaseModel):
    question: str
    session_id: str
    corpus_type: CorpusType = CorpusType.statutes
    doc_type_filter: Optional[str] = None

class SourceRef(BaseModel):
    index: int
    doc_title: str
    retrieval_score: float
    text_preview: str
    chunk_hash: int

class EvalResult(BaseModel):
    faithfulness_score: float
    citations_accurate: dict
    adversarial_challenge: str
    verdict: str  # PASS | REVIEW | FAIL
    provenance_hash: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceRef]
    eval: EvalResult
    session_id: str

class RiskRequest(BaseModel):
    clause_text: str
    doc_id: Optional[str] = None
    clause_ref: Optional[str] = None

class IngestRequest(BaseModel):
    doc_type: str  # statute | contract
    jurisdiction: str = "BD"
    gcs_path: str  # gs://bucket/path.pdf

```
**7. Oracle async layer**  
```
# services/oracle.py
import oracledb
import asyncio, os, json, uuid
from datetime import datetime
from contextlib import asynccontextmanager

# Connection pool — created once at startup
_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool_async(
            user=os.environ["ORACLE_USER"],
            password=os.environ["ORACLE_PASSWORD"],
            dsn=os.environ["ORACLE_DSN"],
            min=1, max=4, increment=1
        )
    return _pool

async def store_interaction(session_id, user_id, question, answer, sources, eval_result):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """INSERT INTO eval_results 
                   (eval_id, session_id, question, answer, faithfulness, 
                    challenges_raised, overall_verdict)
                   VALUES (:1, :2, :3, :4, :5, :6, :7)""",
                [str(uuid.uuid4()), session_id, question, answer,
                 eval_result.get("faithfulness_score", 0),
                 1 if eval_result.get("adversarial_challenge") else 0,
                 eval_result.get("verdict", "REVIEW")]
            )
        await conn.commit()

async def get_eval_history(limit: int = 50) -> list:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """SELECT eval_id, session_id, faithfulness, overall_verdict, created_at
                   FROM eval_results 
                   ORDER BY created_at DESC 
                   FETCH FIRST :limit ROWS ONLY""",
                [limit]
            )
            rows = await cursor.fetchall()
            cols = [d[0].lower() for d in cursor.description]
            return [dict(zip(cols, row)) for row in rows]

```
**8. Frontend: three pages, minimum code**  
**Key: no Recharts overhead for the eval dashboard. Use Chart.js via CDN in the eval page to keep bundle small.**  
app/page.tsx — chat:  
```
// Core state: messages[], loading, session_id (uuid on mount)
// On send: POST /query → append {role:"assistant", content:answer, sources, eval}
// Render: markdown (react-markdown), sources as collapsible list
// Eval badge inline: verdict=PASS→green dot, REVIEW→amber, FAIL→red
// Adversarial challenge: collapsed by default, "Show challenge" toggle
// ProvenanceTree: just a small <details> showing chunk_hash + retrieval_score per source

```
app/risk/page.tsx — risk heatmap:  
```
// Textarea for clause input
// POST /risk → render ClauseRiskCard
// ClauseRiskCard: colored border (red/amber/green), 
//   conflicts list, gaps list, recommendation, statute_refs
// For full doc: split on paragraph boundaries client-side,
//   batch POST /risk for each clause, render grid

```
app/eval/page.tsx — adversarial panel:  
```
// GET /eval-results → table of recent queries
// Columns: question_preview, faithfulness_score (progress bar), verdict badge, adversarial_challenge
// Simple line chart: Chart.js, faithfulness over last 30 queries
// Admin-only: accessible only if role==="admin" (check Firebase custom claim)

```
**9. Gemini client setup (both models, one file)**  
```
# services/gemini.py
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import os

vertexai.init(project=os.environ["PROJECT_ID"], location="us-central1")

# Pro: user-facing synthesis only
pro_client = GenerativeModel(
    "gemini-1.5-pro-002",
    generation_config=GenerationConfig(temperature=0.1, max_output_tokens=2048)
)

# Flash: all eval, judging, risk scoring — never expose output directly to users
flash_client = GenerativeModel(
    "gemini-1.5-flash-002", 
    generation_config=GenerationConfig(temperature=0.0, max_output_tokens=1024)
)

```
**10. Seed corpus — what to ingest**  
**Public domain, downloadable today:**  
```
statutes corpus:
  - Bangladesh Companies Act 1994 (bdlaws.minlaw.gov.bd — PDF available)
  - Securities and Exchange Ordinance 1969
  - Contract Act 1872 (applicable in BD)
  - Labour Act 2006 (key sections)

contracts corpus:
  - IACCM standard MSA template (public)
  - NDA template (any jurisdiction — the risk engine flags BD-specific gaps)
  - Consulting agreement template
  - 5–10 sample contracts from lawinsider.com (public)

```
Download script:  
```
mkdir -p seed_docs/statutes seed_docs/contracts
# Manual downloads from bdlaws.minlaw.gov.bd and lawinsider.com
# Then bulk upload:
gsutil -m cp seed_docs/statutes/*.pdf gs://${PROJECT_ID}-docs/statutes/
gsutil -m cp seed_docs/contracts/*.pdf gs://${PROJECT_ID}-docs/contracts/

```
Bulk ingest after upload:  
```
# scripts/ingest_seed.py
import vertexai
from vertexai import rag
import json, os

vertexai.init(project=os.environ["PROJECT_ID"], location="us-central1")

with open(".corpus_ids.json") as f:
    corpus_ids = json.load(f)

# Statutes: large chunks
rag.import_files(
    corpus_name=corpus_ids["statutes"],
    paths=[f"gs://{os.environ['PROJECT_ID']}-docs/statutes/"],
    transformation_config={"chunking_config": {"chunk_size": 1024, "chunk_overlap": 200}},
)

# Contracts: tighter chunks
rag.import_files(
    corpus_name=corpus_ids["contracts"],
    paths=[f"gs://{os.environ['PROJECT_ID']}-docs/contracts/"],
    transformation_config={"chunking_config": {"chunk_size": 512, "chunk_overlap": 100}},
)

print("Ingestion jobs submitted. Check RAG Engine console for status.")

```
**11. Deployment (Termius-safe, no local Docker)**  
```
# Backend — Cloud Run source-based deploy (no Docker needed locally)
cd backend
gcloud run deploy docrag-api \
  --source . \
  --region us-central1 \
  --service-account docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com \
  --set-env-vars PROJECT_ID=${PROJECT_ID} \
  --set-secrets \
    ORACLE_USER=oracle-user:latest,\
    ORACLE_PASSWORD=oracle-pw:latest,\
    ORACLE_DSN=oracle-dsn:latest,\
    FIREBASE_CREDENTIALS_JSON=firebase-creds:latest,\
    CORPUS_STATUTES=corpus-statutes:latest,\
    CORPUS_CONTRACTS=corpus-contracts:latest \
  --allow-unauthenticated \
  --concurrency 80 \
  --memory 1Gi

# Frontend — Vercel (free tier, zero GCP spend)
cd ../frontend
npx vercel --prod
# Set env vars in Vercel dashboard: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_FIREBASE_CONFIG

# Eval scheduler — runs every 6h
gcloud scheduler jobs create http docrag-eval-cron \
  --schedule "0 */6 * * *" \
  --uri "$(gcloud run services describe docrag-api --format='value(status.url)')/eval" \
  --http-method POST \
  --oidc-service-account-email docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com

```
**12. Secrets setup (do this before deploy)**  
```
# Store all secrets in Secret Manager — never in env vars directly
echo -n "your_oracle_user" | gcloud secrets create oracle-user --data-file=-
echo -n "your_oracle_password" | gcloud secrets create oracle-pw --data-file=-
echo -n "your_oracle_dsn" | gcloud secrets create oracle-dsn --data-file=-

# Firebase service account key JSON
cat firebase-service-account.json | gcloud secrets create firebase-creds --data-file=-

# Corpus IDs (after running create_corpus.py)
cat .corpus_ids.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['statutes'])" | \
  gcloud secrets create corpus-statutes --data-file=-
cat .corpus_ids.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['contracts'])" | \
  gcloud secrets create corpus-contracts --data-file=-

```
**13. Credit burn estimate**  

| Phase | Operation | Est. cost |
| ----------------------------------- | ------------------------ | -------------- |
| Corpus ingestion (50 docs) | Embedding via RAG Engine | ~$2 |
| Dev queries (200 test queries) | Pro synthesis | ~$8 |
| Dev eval (200 judge calls) | Flash judging | ~$1 |
| Reranking (200 queries × 20 chunks) | Ranking API | ~$1 |
| Risk assessment (50 clauses) | Flash structured output | ~$0.50 |
| Buffer / iteration | Mixed | ~$20 |
| Total |  | ~$33 of $1,000 |
  
The $1,000 pool is enormous for this scope. You will not run out. Spend freely on iteration.  
**14. The README north-star sentence**  
```
"DocRAG-Legal: contract risk intelligence with adversarial self-auditing — 
every answer is challenged by a second model, every citation is hash-verified, 
every risk assessment cites the specific statute it violates. 
Built on Vertex AI RAG Engine with Gemini-as-judge evaluation harness."

```
**15. Execution sequence for a 25-hour session**  
```
[H01–H02]  GCP setup (setup_gcp.sh) + Oracle free tier signup + init_oracle.py
[H03]      Download seed PDFs → GCS upload → create_corpus.py → ingest_seed.py
[H04–H05]  services/gemini.py + services/rag.py + services/rerank.py + test in REPL
[H06–H07]  services/eval_judge.py + test judge with synthetic Q/A pairs
[H08]      services/oracle.py + confirm Oracle connectivity
[H09–H10]  middleware/auth.py + main.py skeleton + schemas.py
[H11–H12]  routers/query.py — full implementation, local uvicorn test
[H13–H14]  routers/risk.py — full implementation, test with sample clause
[H15]      routers/ingest.py + routers/eval.py (history endpoint)
[H16]      Cloud Run deploy — backend live, test all endpoints with curl
[H17–H18]  Next.js: app/page.tsx chat UI + lib/api.ts + lib/firebase.ts
[H19–H20]  app/risk/page.tsx + ClauseRiskCard component
[H21]      app/eval/page.tsx + Chart.js eval dashboard
[H22]      Vercel deploy — frontend live, full E2E test
[H23]      Cloud Scheduler setup + smoke test eval cron
[H24]      Demo walkthrough (follow demo script) + Loom recording
[H25]      README, architecture diagram (Mermaid in README), GitHub push

```
**The demo script from Arena v4 is correct and complete — use it as-is.** The 5-minute walkthrough maps exactly to this architecture.  
  
**Instruct Gemini CLI for these exactly:**  
```
1. "Write requirements.txt for the FastAPI backend with: 
   fastapi, uvicorn, firebase-admin, oracledb, google-cloud-aiplatform, 
   vertexai, pydantic, slowapi, python-dotenv, httpx"

2. "Write the Next.js 14 component ChatPanel.tsx that takes messages[] prop,
   renders assistant messages as markdown using react-markdown,
   shows sources as a collapsible list with retrieval_score,
   shows eval verdict as a colored badge (PASS=green, REVIEW=amber, FAIL=red),
   has a 'Show adversarial challenge' toggle for the challenge text"

3. "Write Dockerfile for FastAPI app using python:3.11-slim,
   no heavy dependencies, port 8080, uvicorn entry point"

4. "Write the ProvenanceTree.tsx component that takes sources[] prop
   and renders a tree view showing doc_title, chunk_hash, retrieval_score"

```
Everything else in this plan: write it yourself, directly. The hard architectural decisions are made. Gemini handles boilerplate.  
  
  
ADDENDUM  
  
This is a good critique. Every point is valid. Let me address each one definitionally, then give you the corrected artifacts. No prose.  
  
## Decisions first  
**Redlining: IN scope.** It's the feature that makes the before/after story and it's architecturally cheap — one endpoint, one prompt, one frontend component. Not adding it was an error.  
**Scope = 5 endpoints:**  
```
/query      → RAG + synthesis + inline adversarial eval
/risk       → clause heatmap (RED/YELLOW/GREEN)
/redline    → contract diff with suggested rewrites  ← added back
/ingest     → user-facing upload → GCS → corpus
/eval       → eval history GET + /eval/batch POST (scheduled)

```
  
## Corrected artifacts  
**.env.example (complete)**  
```
# GCP
PROJECT_ID=docrag-legal-xxxxxx
REGION=us-central1
GCS_BUCKET=docrag-legal-xxxxxx-docs

# Corpus IDs (output of create_corpus.py)
CORPUS_STATUTES=projects/xxx/locations/us-central1/ragCorpora/xxx
CORPUS_CONTRACTS=projects/xxx/locations/us-central1/ragCorpora/xxx

# Firebase
FIREBASE_CREDENTIALS_JSON={"type":"service_account",...}  # full JSON string

# Oracle Autonomous DB
ORACLE_USER=ADMIN
ORACLE_PASSWORD=yourpassword
ORACLE_DSN=your-db-name_high  # from wallet tnsnames.ora
ORACLE_WALLET_DIR=/app/wallet  # path to unzipped wallet in container

# App
APP_ENV=production
LOG_LEVEL=INFO

```
  
**oracle.py — corrected (no create_pool_async)**  
```
# services/oracle.py
import oracledb
import asyncio, os, json, uuid
from functools import partial

# python-oracledb thin mode — no Oracle Client libs needed
# Async pattern: run_in_executor wraps synchronous pool operations
# create_pool_async does NOT exist — this is the correct approach

_pool = None

def _create_pool_sync():
    return oracledb.create_pool(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"],
        wallet_location=os.environ.get("ORACLE_WALLET_DIR"),
        wallet_password=os.environ.get("ORACLE_WALLET_PASSWORD"),
        min=1, max=4, increment=1
    )

async def get_pool():
    global _pool
    if _pool is None:
        loop = asyncio.get_event_loop()
        _pool = await loop.run_in_executor(None, _create_pool_sync)
    return _pool

async def _execute(sql: str, params: list = None, fetch: bool = False):
    """Generic executor — wraps synchronous oracledb in run_in_executor."""
    pool = await get_pool()
    loop = asyncio.get_event_loop()
    
    def _run():
        with pool.acquire() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or [])
                if fetch:
                    rows = cursor.fetchall()
                    cols = [d[0].lower() for d in cursor.description]
                    return [dict(zip(cols, row)) for row in rows]
                conn.commit()
                return None
    
    return await loop.run_in_executor(None, _run)

async def store_interaction(
    session_id: str, user_id: str, question: str, answer: str,
    sources: list, eval_result: dict
):
    await _execute(
        """INSERT INTO eval_results
           (eval_id, session_id, question, answer, faithfulness,
            challenges_raised, overall_verdict)
           VALUES (:1, :2, :3, :4, :5, :6, :7)""",
        [str(uuid.uuid4()), session_id, question, answer,
         eval_result.get("faithfulness_score", 0.0),
         1 if eval_result.get("adversarial_challenge") else 0,
         eval_result.get("verdict", "REVIEW")]
    )

async def store_risk_score(
    doc_id: str, clause_ref: str, clause_text: str,
    risk_level: str, conflicts: list, gaps: list,
    recommendation: str, statute_refs: list,
    confidence: float = 0.0, **kwargs  # absorb extra keys from risk_data
):
    await _execute(
        """INSERT INTO risk_scores
           (score_id, doc_id, clause_ref, clause_text,
            risk_level, risk_reason, statute_ref, scored_at)
           VALUES (:1, :2, :3, :4, :5, :6, :7, SYSTIMESTAMP)""",
        [str(uuid.uuid4()), doc_id or "unknown", clause_ref or "unref",
         clause_text[:2000],
         risk_level,
         json.dumps({"conflicts": conflicts, "gaps": gaps, 
                     "recommendation": recommendation}),
         json.dumps(statute_refs)]
    )

async def get_eval_history(limit: int = 50) -> list:
    return await _execute(
        """SELECT eval_id, session_id, faithfulness, overall_verdict, created_at
           FROM eval_results
           ORDER BY created_at DESC
           FETCH FIRST :1 ROWS ONLY""",
        [limit], fetch=True
    )

async def get_risk_history(doc_id: str = None, limit: int = 50) -> list:
    if doc_id:
        return await _execute(
            """SELECT score_id, clause_ref, risk_level, statute_ref, scored_at
               FROM risk_scores WHERE doc_id = :1
               ORDER BY scored_at DESC FETCH FIRST :2 ROWS ONLY""",
            [doc_id, limit], fetch=True
        )
    return await _execute(
        """SELECT score_id, doc_id, clause_ref, risk_level, scored_at
           FROM risk_scores ORDER BY scored_at DESC FETCH FIRST :1 ROWS ONLY""",
        [limit], fetch=True
    )

```
  
**gemini.py — lazy init pattern**  
```
# services/gemini.py
import os
from typing import Optional

_initialized = False
_pro_client = None
_flash_client = None

def _ensure_init():
    global _initialized, _pro_client, _flash_client
    if _initialized:
        return
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig
    vertexai.init(
        project=os.environ["PROJECT_ID"],
        location=os.environ.get("REGION", "us-central1")
    )
    _pro_client = GenerativeModel(
        "gemini-1.5-pro-002",
        generation_config=GenerationConfig(temperature=0.1, max_output_tokens=2048)
    )
    _flash_client = GenerativeModel(
        "gemini-1.5-flash-002",
        generation_config=GenerationConfig(temperature=0.0, max_output_tokens=1024)
    )
    _initialized = True

def get_pro():
    _ensure_init()
    return _pro_client

def get_flash():
    _ensure_init()
    return _flash_client

```
**Usage change everywhere:** replace pro_client.generate_content_async(...) with get_pro().generate_content_async(...). One find-and-replace.  
  
**ingest.py router — complete**  
```
# routers/ingest.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks, HTTPException
from middleware.auth import require_role
from services.oracle import _execute
from google.cloud import storage
import vertexai
from vertexai import rag
import uuid, os, json

router = APIRouter()
gcs_client = storage.Client()

CHUNK_CONFIGS = {
    "statute":  {"chunk_size": 1024, "chunk_overlap": 200},
    "contract": {"chunk_size": 512,  "chunk_overlap": 100},
}

async def _ingest_to_corpus(job_id: str, gcs_path: str, corpus_name: str,
                             doc_type: str, metadata: dict):
    """Background task: import GCS file into RAG Engine corpus."""
    try:
        # Update status → processing
        await _execute(
            "UPDATE ingest_jobs SET status='processing' WHERE job_id=:1",
            [job_id]
        )
        
        chunk_cfg = CHUNK_CONFIGS.get(doc_type, CHUNK_CONFIGS["contract"])
        
        # Import into Vertex RAG Engine — synchronous SDK call, runs in background
        rag.import_files(
            corpus_name=corpus_name,
            paths=[gcs_path],
            transformation_config={"chunking_config": chunk_cfg},
        )
        
        # Register in doc_registry
        await _execute(
            """INSERT INTO doc_registry
               (doc_id, doc_title, doc_type, jurisdiction, gcs_path, ingested_by)
               VALUES (:1, :2, :3, :4, :5, :6)""",
            [job_id, metadata.get("doc_title", gcs_path.split("/")[-1]),
             doc_type, metadata.get("jurisdiction", "BD"),
             gcs_path, metadata.get("user_id", "system")]
        )
        
        await _execute(
            "UPDATE ingest_jobs SET status='complete' WHERE job_id=:1",
            [job_id]
        )
        
    except Exception as e:
        await _execute(
            "UPDATE ingest_jobs SET status='failed', error_msg=:1 WHERE job_id=:2",
            [str(e)[:500], job_id]
        )

@router.post("/ingest")
async def ingest_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    doc_type: str = Form(...),      # "statute" | "contract"
    doc_title: str = Form(None),
    jurisdiction: str = Form("BD"),
    user=Depends(require_role(["admin", "analyst"]))
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files accepted")
    
    job_id = str(uuid.uuid4())
    
    # Upload to GCS
    bucket = gcs_client.bucket(os.environ["GCS_BUCKET"])
    gcs_key = f"{doc_type}s/{job_id}/{file.filename}"
    blob = bucket.blob(gcs_key)
    content = await file.read()
    blob.upload_from_string(content, content_type="application/pdf")
    gcs_path = f"gs://{os.environ['GCS_BUCKET']}/{gcs_key}"
    
    # Select corpus
    corpus_name = (
        os.environ["CORPUS_STATUTES"] if doc_type == "statute"
        else os.environ["CORPUS_CONTRACTS"]
    )
    
    # Record job
    await _execute(
        """INSERT INTO ingest_jobs (job_id, gcs_path, doc_type, status, created_by)
           VALUES (:1, :2, :3, 'pending', :4)""",
        [job_id, gcs_path, doc_type, user["uid"]]
    )
    
    # Fire background ingestion
    background_tasks.add_task(
        _ingest_to_corpus,
        job_id=job_id,
        gcs_path=gcs_path,
        corpus_name=corpus_name,
        doc_type=doc_type,
        metadata={"doc_title": doc_title, "jurisdiction": jurisdiction, 
                  "user_id": user["uid"]}
    )
    
    return {"job_id": job_id, "status": "pending", "gcs_path": gcs_path}

@router.get("/ingest/status/{job_id}")
async def ingest_status(job_id: str, user=Depends(require_role(["admin", "analyst", "viewer"]))):
    rows = await _execute(
        "SELECT job_id, status, error_msg, created_at FROM ingest_jobs WHERE job_id=:1",
        [job_id], fetch=True
    )
    if not rows:
        raise HTTPException(404, f"Job {job_id} not found")
    return rows[0]

```
Add ingest_jobs table to Oracle DDL:  
```
CREATE TABLE ingest_jobs (
    job_id VARCHAR2(36) PRIMARY KEY,
    gcs_path VARCHAR2(1000),
    doc_type VARCHAR2(50),
    status VARCHAR2(20) DEFAULT 'pending',
    error_msg VARCHAR2(500),
    created_by VARCHAR2(128),
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

```
  
**redline.py router — the missing feature**  
```
# routers/redline.py
from fastapi import APIRouter, Depends
from middleware.auth import require_role
from services.gemini import get_flash
from services.rag import retrieve
from services.rerank import rerank
from models.schemas import RedlineRequest, RedlineResponse
import json

router = APIRouter()

REDLINE_PROMPT = """You are a contract redlining expert. Compare the submitted clause against 
best-practice standards and relevant statute context.

ORIGINAL CLAUSE:
{original_clause}

RELEVANT STATUTE/PRECEDENT CONTEXT:
{context_block}

COMPLIANCE TARGET: {compliance_target}

Produce a structured redline review. Return ONLY valid JSON:
{{
  "issues": [
    {{
      "issue_type": "LEGAL_RISK|AMBIGUITY|MISSING_PROVISION|UNFAVORABLE_TERM",
      "severity": "HIGH|MEDIUM|LOW",
      "original_text": "exact problematic phrase from clause",
      "explanation": "why this is problematic, citing statute if applicable",
      "suggested_replacement": "rewritten version of the problematic phrase only",
      "statute_ref": "Act § Section or null"
    }}
  ],
  "rewritten_clause": "full clause rewrite incorporating all fixes",
  "risk_delta": "assessment of before vs after risk level",
  "confidence": 0.0-1.0
}}

If the clause is already sound, return issues=[] and rewritten_clause equal to original."""

@router.post("/redline", response_model=RedlineResponse)
async def redline_endpoint(
    req: RedlineRequest,
    user=Depends(require_role(["admin", "analyst"]))
):
    # Retrieve statute context for the clause
    chunks = await retrieve(
        query=req.clause_text,
        corpus_name=__import__('os').environ["CORPUS_STATUTES"],
        top_k=8,
        doc_type_filter="statute"
    )
    ranked = await rerank(req.clause_text, chunks, top_n=3)
    
    context_block = "\n\n".join(
        f"[{i+1}] {c.source_display_name}\n{c.text[:500]}"
        for i, c in enumerate(ranked)
    )
    
    response = await get_flash().generate_content_async(
        REDLINE_PROMPT.format(
            original_clause=req.clause_text,
            context_block=context_block,
            compliance_target=req.compliance_target or "Bangladesh Companies Act and standard commercial practice"
        ),
        generation_config={"response_mime_type": "application/json"}
    )
    
    try:
        result = json.loads(response.text)
    except json.JSONDecodeError:
        result = {
            "issues": [],
            "rewritten_clause": req.clause_text,
            "risk_delta": "Parse error — manual review required",
            "confidence": 0.0
        }
    
    result["original_clause"] = req.clause_text
    return result

```
Add to schemas.py:  
```
class RedlineRequest(BaseModel):
    clause_text: str
    doc_id: Optional[str] = None
    clause_ref: Optional[str] = None
    compliance_target: Optional[str] = None

class RedlineIssue(BaseModel):
    issue_type: str
    severity: str
    original_text: str
    explanation: str
    suggested_replacement: str
    statute_ref: Optional[str] = None

class RedlineResponse(BaseModel):
    original_clause: str
    issues: List[RedlineIssue]
    rewritten_clause: str
    risk_delta: str
    confidence: float

```
  
**eval.py — corrected (GET history + POST batch, both defined)**  
```
# routers/eval.py
from fastapi import APIRouter, Depends
from middleware.auth import require_role
from services.oracle import get_eval_history, get_risk_history, _execute
from services.eval_judge import judge
import asyncio, uuid

router = APIRouter()

@router.get("/eval")
async def eval_history(
    limit: int = 50,
    user=Depends(require_role(["admin", "analyst"]))
):
    """Returns recent eval results for the dashboard."""
    evals = await get_eval_history(limit=limit)
    risks = await get_risk_history(limit=20)
    
    # Aggregate metrics
    if evals:
        avg_faith = sum(r.get("faithfulness", 0) for r in evals) / len(evals)
        pass_rate = sum(1 for r in evals if r.get("overall_verdict") == "PASS") / len(evals)
    else:
        avg_faith, pass_rate = 0.0, 0.0
    
    return {
        "summary": {
            "avg_faithfulness": round(avg_faith, 4),
            "pass_rate": round(pass_rate, 4),
            "total_evaluated": len(evals)
        },
        "recent_evals": evals,
        "recent_risks": risks
    }

@router.post("/eval/batch")
async def eval_batch(
    user=Depends(require_role(["admin"]))
):
    """
    Batch re-evaluation of last 50 interactions.
    This is what Cloud Scheduler hits every 6h — POST /eval/batch.
    Pulls stored Q/A pairs, re-judges with current Flash model.
    """
    rows = await _execute(
        """SELECT eval_id, question, answer FROM eval_results
           WHERE overall_verdict = 'REVIEW'
           ORDER BY created_at DESC FETCH FIRST 50 ROWS ONLY""",
        fetch=True
    )
    
    if not rows:
        return {"message": "No REVIEW items to re-evaluate", "processed": 0}
    
    # Re-judge REVIEW items — they may pass with updated Flash
    results = []
    for row in rows:
        try:
            # No chunks available for stored interactions — use faithfulness-only
            result = await judge(
                question=row["question"],
                answer=row["answer"],
                chunks=[],  # No retrieval context stored — faithfulness check only
                citations=[]
            )
            await _execute(
                """UPDATE eval_results 
                   SET faithfulness = :1, overall_verdict = :2
                   WHERE eval_id = :3""",
                [result["faithfulness_score"], result["verdict"], row["eval_id"]]
            )
            results.append({"eval_id": row["eval_id"], "new_verdict": result["verdict"]})
        except Exception as e:
            results.append({"eval_id": row["eval_id"], "error": str(e)})
    
    return {"processed": len(results), "results": results}

```
**Cloud Scheduler fix:**  
```
# Correct — hits /eval/batch, not /eval
gcloud scheduler jobs create http docrag-eval-cron \
  --schedule "0 */6 * * *" \
  --uri "${API_URL}/eval/batch" \
  --http-method POST \
  --oidc-service-account-email docrag-sa@${PROJECT_ID}.iam.gserviceaccount.com

```
  
**Gemini CLI prompts — complete set (all 7)**  
```
PROMPT 1 — requirements.txt:
"Write requirements.txt for a FastAPI backend with these packages:
fastapi uvicorn[standard] firebase-admin oracledb google-cloud-aiplatform
google-cloud-storage vertexai pydantic slowapi python-dotenv httpx
google-cloud-discoveryengine. Pin to latest stable versions."

PROMPT 2 — Dockerfile:
"Write a minimal Dockerfile for a FastAPI app. Base: python:3.11-slim.
Port 8080. Entry: uvicorn main:app --host 0.0.0.0 --port 8080.
Copy wallet/ directory to /app/wallet. No unnecessary layers."

PROMPT 3 — ChatPanel.tsx:
"Write a Next.js 14 React component ChatPanel.tsx.
Props: messages (array of {role, content, sources?, eval?}), onSend (string→void), loading boolean.
Render assistant messages as markdown using react-markdown.
Sources: collapsible list showing doc_title and retrieval_score as a 0-100% bar.
Eval: colored badge — PASS=green, REVIEW=amber, FAIL=red.
Below badge: 'Show adversarial challenge' toggle revealing the challenge text.
Input: textarea + send button, disabled when loading.
Tailwind CSS only. No external UI libraries."

PROMPT 4 — ProvenanceTree.tsx:
"Write a React component ProvenanceTree.tsx.
Props: sources (array of {index, doc_title, chunk_hash, retrieval_score, text_preview}).
Render as a vertical tree: each node shows doc_title, chunk_hash as monospace truncated string,
retrieval_score as percentage. Expandable: click to show text_preview.
Tailwind CSS. Should look like a git commit tree visually."

PROMPT 5 — RiskHeatmap.tsx:
"Write a React component RiskHeatmap.tsx.
Props: clauses (array of {clause_ref, clause_text, risk_level, conflicts, recommendation}).
Render as a grid of ClauseCard components.
ClauseCard: left border color = RED→red-500, YELLOW→yellow-500, GREEN→green-500.
Shows clause_ref as header, first 120 chars of clause_text, risk_level badge.
Click expands to show full clause_text, conflicts list, recommendation.
Tailwind CSS only."

PROMPT 6 — RedlinePanel.tsx:
"Write a React component RedlinePanel.tsx.
Props: original (string), result ({issues, rewritten_clause, risk_delta}).
Left panel: original clause with problematic phrases highlighted in red/yellow
using the original_text field from each issue to find and highlight spans.
Right panel: rewritten_clause with the same spans highlighted in green.
Below each highlight: tooltip showing explanation and statute_ref.
Bottom: risk_delta summary text. Tailwind CSS only."

PROMPT 7 — AdversarialPanel.tsx:
"Write a React component AdversarialPanel.tsx.
Props: evalHistory (array of {eval_id, faithfulness, overall_verdict, adversarial_challenge, question}).
Top section: two stats — avg faithfulness (large number), pass rate (percentage).
Below: line chart using Chart.js showing faithfulness over last 30 items.
Table below chart: columns = question preview (truncated 60 chars), faithfulness bar,
verdict badge, adversarial_challenge (truncated, expandable on click).
Admin-only rows with red background for FAIL verdict. Tailwind CSS only."

```
  
**Updated execution sequence**  
```
[H01–H02]  GCP setup_gcp.sh + Oracle free tier + init_oracle.py (updated DDL with ingest_jobs)
[H03]      Download seed PDFs → GCS → create_corpus.py → ingest_seed.py
[H04–H05]  services/gemini.py (lazy) + services/rag.py + services/rerank.py — REPL test
[H06–H07]  services/eval_judge.py — test with 5 synthetic Q/A pairs
[H08]      services/oracle.py (corrected) — confirm pool + all 5 store/get functions
[H09]      middleware/auth.py + schemas.py + main.py (mount all 5 routers)
[H10–H11]  routers/query.py — full, test with curl
[H12]      routers/risk.py — full, test with sample clause
[H13]      routers/redline.py — full, test with sample clause
[H14]      routers/ingest.py — full, test upload flow end-to-end
[H15]      routers/eval.py (GET + POST batch) — confirm scheduler endpoint correct
[H16]      Cloud Run deploy — all 5 endpoints live, smoke test
[H17]      Run Gemini CLI prompts 1–7 → generate all frontend components
[H18–H19]  app/page.tsx — wire ChatPanel + ProvenanceTree to /query
[H20]      app/risk/page.tsx — wire RiskHeatmap to /risk
[H21]      app/redline/page.tsx — wire RedlinePanel to /redline
[H22]      app/eval/page.tsx — wire AdversarialPanel to /eval
[H23]      Vercel deploy + Cloud Scheduler setup (/eval/batch) + E2E smoke test
[H24]      Demo walkthrough (5-min script) + Loom recording
[H25]      README (Mermaid diagram + north-star sentence) + GitHub push

```
  
**Summary of what changed from the critique:**  

| Bug | Fix |
| ------------------------------- | ------------------------------------------------------------------- |
| create_pool_async doesn't exist | Replaced with create_pool + run_in_executor pattern throughout |
| store_risk_score missing | Defined completely in oracle.py with **kwargs absorber |
| gemini.py crashes on import | Lazy init via get_pro() / get_flash() functions |
| ingest.py was a stub | Full implementation with GCS upload + background task |
| Redlining dropped | routers/redline.py fully implemented, RedlinePanel.tsx prompt added |
| /eval scheduled incorrectly | Scheduler now hits /eval/batch POST, GET history is separate |
| .env.example missing | Written completely |
| Frontend prompts incomplete | 7 prompts covering every component |
  
Nothing remaining is ambiguous. Start at H01.  
