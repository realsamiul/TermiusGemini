# DocRAG-Legal: Architectural Audit & Pre-Flight Review

This document compiles the comprehensive architectural audit, potential issue analysis, environment checks, and action plan for building **DocRAG-Legal** on this VM.

---

## 1. Project Overview & Architectural Mapping

You are building **DocRAG-Legal**, a contract risk intelligence system with an inline adversarial self-auditing evaluation harness. 

### High-Fidelity Blueprint:
* **Storage & DB Layer (Modal):** Replaces Oracle Autonomous DB entirely. Uses *Modal Dicts* for lightweight hot-caching (sessions, transient states) and *Modal Volumes* to persist structured audit trails as newline-delimited JSON (NDJSON) logs.
* **Retrieval Core (Vertex AI RAG Engine):** Separates documents into dynamic statutory (Bangladesh Companies Act, Contract Act, etc.) and contract-specific corpora, using adaptive hybrid search alphas (Citation-exact vs. Semantic) and reranked using the **Vertex AI Ranking API** down to the top 5 most relevant chunks.
* **Orchestration Layer (FastAPI on Cloud Run):** Hosts 5 critical endpoints:
  1. `/query` — RAG-driven synthesis using **Gemini 1.5 Pro**, coupled with inline adversarial judging by **Gemini 1.5 Flash**.
  2. `/risk` — Clause-by-clause compliance risk heatmap generator.
  3. `/redline` — Comparative clause diffing with statute-backed rewrite suggestions.
  4. `/ingest` — Multi-part document parser pushing uploaded files to GCS and importing them asynchronously into Vertex AI corpora.
  5. `/eval` — Read endpoint for metrics dashboards and scheduled `/eval/batch` cron triggers.
* **Presentation Layer (Next.js 14 / Tailwind):** A React-based interface showing interactive chat panels with visual provenance trees, editable heatmaps, visual redlines, and a metrics dashboard powered by Chart.js.

---

## 2. Environment Verification (Rule Zero Checks)

A real-time check of the VM environment was conducted on **Sunday, May 31, 2026** to determine system preparedness and rule out resource collisions:

| Parameter | State | Status | Impact / Action |
| :--- | :--- | :--- | :--- |
| **GCP Project ID** | `project-a1f62154-a7ad-4b37-93b` | **Active & Clean** | Safe to reuse. No existing Cloud Run services or colliding systems. |
| **Service Account** | `docrag-sa` (DocRAG Service Account) | **Exists** | Already configured in the project. No creation collision; just requires role-binding verification. |
| **Firestore DB** | None initialized (`[]`) | **Vacant** | Completely safe to run `gcloud firestore databases create` without name conflicts. |
| **Local Ports** | Port `8080` (FastAPI) and `3000` (Next.js) | **Free** | No port occupancy. Both local development environments can boot without conflicts. |
| **Modal Workspace** | `mortuzamanisha` | **Active** | Deployed apps listed (`bangladesh-...`, `cricsight-c...`). No app named `docrag-persistence` exists. No name clashes. |
| **Vertex AI SDK** | Initialized successfully via Python 3.14 | **Compatible** | Environment can run modern Generative SDK calls directly. |

---

## 3. Potential Bottlenecks & Critical Risks

### A. Showstopper: Missing Vertex AI Ranking API IAM Permissions
While `MODAL_SETUP.md` sets up permissions for `aiplatform.user`, `storage.objectAdmin`, `secretmanager.secretAccessor`, and `datastore.user`, the backend implementation uses the **Vertex AI Ranking API** (`google.cloud.discoveryengine`) for chunk reranking in `services/rerank.py`. 
* **The Risk:** Without explicit Discovery Engine permissions, `/query` and `/risk` will raise immediate `PermissionDenied` (403) errors at the reranking stage.
* **The Fix:** The `docrag-sa` service account must be granted `roles/discoveryengine.viewer` or `roles/discoveryengine.editor` before deployment.

### B. Oracle Code Remnants in Automation
`MASTER_PLAN.md` is heavily integrated with Oracle Autonomous DB ( TNS configurations, instant client drivers, wallet zip directory mounts, connection pools). 
* **The Risk:** The build automation runner `run_build.sh` originally pointed to the master plan for backend generation, which would compile Oracle code instead of Modal.
* **The Fix:** The build runner must be locked down to read `MODAL_SETUP.md` and ignore all database-related sections of `MASTER_PLAN.md`.

### C. Firebase Credentials & Claims Paths
The custom claims script uses a hardcoded path `/path/to/firebase-service-account.json` to execute claims on the admin test user.
* **The Risk:** The setup script will immediately crash if this key isn't locally present in the workspace.
* **The Fix:** Create a defined local folder `~/docrag-legal/secrets/` to hold these files and refer to them explicitly.

### D. Modal Cold Starts
Modal serverless functions run on demand, creating a ~2-second latency penalty on the initial query before scaling down to ~100ms.
* **The Risk:** Standard FastAPI/uvicorn connection pools or client-side Next.js fetch setups might raise timeout errors.
* **The Fix:** Ensure timeout parameters on the backend HTTP clients are relaxed to at least 15 seconds.

---

## 4. Autonomous Resolution Capabilities

As your automated engineering assistant, I can perform the majority of these pre-flight setups, configuration writing, and script assemblies directly.

### What I Can Fix Autonomously (Right Now):
1. **GCP IAM Policy Bindings:** I can execute the `gcloud projects add-iam-policy-binding` commands to grant `roles/discoveryengine.viewer` and all other necessary roles to your existing `docrag-sa` service account.
2. **Directory Structure Setup:** I can set up your entire `~/docrag-legal` workspace, creating all directories for the FastAPI backend, Next.js frontend, and corpus seed scripts.
3. **Boilerplate & Configuration Assembly:** I can write fully-compliant, non-placeholdered configuration files:
   * `backend/requirements.txt`
   * `backend/Dockerfile`
   * `backend/main.py`
   * `backend/services/storage.py` (The entire Modal client wrapper)
   * `backend/utils/retry.py` (The with_retry decorator)
   * `backend/models/schemas.py` (All schemas matched to AGENT_CONTEXT)
4. **Modal Deployment:** I can compile and trigger the deploy of `modal/store.py` to provision your serverless volumes and dict caches.
5. **Corpus Registry & Creation:** I can run the Python scripts to initialize and save your statutory and contract RAG corpora on Vertex AI.

### What You Must Do Manually:
1. **Firebase Authentication Setup:** You must go to the Firebase Console, link it to your GCP Project ID (`project-a1f62154-a7ad-4b37-93b`), enable Email/Password login, create the test user, and generate the Admin SDK Private Key JSON.
2. **Download / Supply Private JSON File:** You will need to copy or paste the downloaded Firebase private key file onto your VM (e.g., in `~/docrag-legal/secrets/firebase-key.json`). I cannot download this file from your personal Firebase console for you.
3. **Secret Manager Values:** I can set up the Secret Manager secret keys automatically, but you will need to provide the actual values for any third-party integrations (like the Firebase credentials content).

---

## 5. Concise Recommendation & Verdict

### Verdict: **SAFE TO BUILD WITH PRE-FLIGHT PREPARATION**

Your VM environment is extremely clean, conflicts are non-existent, and the active GCP project is completely empty of competing services. 

Rather than using Google Cloud Shell (which is prone to timing out and disconnects easily on phones/laptops), **we should build this directly on your current VM inside a persistent `tmux` session**.

### Recommended Action Order:
1. Bind the missing Discovery Engine role to the service account.
2. Structure the directory `~/docrag-legal` on the VM.
3. Generate the backend source code using the strict Modal-persistence specifications.
4. Set up the Firebase Console and retrieve your Private Key JSON.
5. Deploy the Modal persistence app.
6. Build and deploy the FastAPI container to Cloud Run.
7. Build and deploy the Next.js frontend.
