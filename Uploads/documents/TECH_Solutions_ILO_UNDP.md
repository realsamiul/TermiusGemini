# Cloud Tech Solutions: ILO & UNDP Problem Stack
## AWS, GCP, Azure Pre-Packaged Solutions

---

## ILO SOLUTION STACK
### Problem: "Hidden Workers + Unmeasured Impact"

**Core Challenge:** ILO needs to:
1. Find & segment informal workers/businesses (hidden, scattered)
2. Track them through interventions (training, awareness campaigns, platform adoption)
3. Measure outcomes (formalization, wage improvement, rights awareness)
4. Consolidate fragmented data into unified dashboards

---

### **ILO SOLUTION 1: "Worker Intelligence Platform" (Enterprise Formalization)**

**Addresses:** Project 1 (Informal Business Formalization Campaign)

#### **Problem It Solves:**
- ILO can't target 500–5,000 informal businesses geographically
- No system to track which businesses actually formalized post-campaign
- Campaign ROI unmeasured (spent $100K, formalized how many businesses?)

#### **Tech Stack (GCP-first, Azure alternative):**

```
LAYER 1: POPULATION SEGMENTATION
├─ Input Data Sources:
│  ├─ Labour Force Surveys (ILO existing data)
│  ├─ Tax registry (BDT-linked informality proxy)
│  ├─ Mobile money transaction data (informal business spending patterns)
│  └─ Satellite imagery (commercial activity detection)
│
└─ GCP Tools:
   ├─ BigQuery (consolidate surveys + tax data + transaction data)
   ├─ Google Cloud Vision API (analyze satellite imagery; detect markets, factories)
   └─ Vertex AI AutoML (train model: "Predict informal business location")

LAYER 2: GEOGRAPHIC TARGETING
├─ Map informal business clusters
│  ├─ Input: Model predictions (where are informal businesses concentrated?)
│  ├─ Tool: Google Maps API + BigQuery GIS functions
│  └─ Output: Heat map (Dhaka District has 5,000+ informal businesses in textiles; Chittagong has 3,000+ in construction)
│
└─ Campaign allocation:
   ├─ Input: Campaign budget ($100K)
   ├─ Tool: Optimization algorithm (Vertex AI)
   └─ Output: "Allocate 40% budget to Dhaka textile cluster, 35% to Chittagong construction, 25% to Khulna retail"

LAYER 3: CAMPAIGN TRACKING & FEEDBACK
├─ Outreach data collection:
│  ├─ Tool: Google Forms (campaign events) + QR code check-in
│  ├─ Data: Who attended? Which sector? Contact info?
│  └─ Real-time: Google Sheets auto-updates with attendees
│
├─ Post-campaign follow-up:
│  ├─ Tool: Twilio SMS API (automated check-in: "Did you formalize your business?")
│  ├─ Frequency: SMS at 1 week, 1 month, 3 months post-event
│  └─ Response: Auto-logged in BigQuery
│
└─ Business registry cross-check (3 months post-campaign):
   ├─ Tool: Automated API call to Bangladesh Registrar of Joint Stock Companies database
   ├─ Query: "Is [business name] now registered?"
   └─ Result: Auto-matched with attendee list; track formalization rate

LAYER 4: DASHBOARDING & ROI MEASUREMENT
├─ Tool: Looker (GCP) or Power BI (Azure)
├─ Metrics displayed:
│  ├─ Campaign reach: 2,500 businesses attended (target: 3,000)
│  ├─ Formalization rate: 18% (450 businesses formally registered within 3 months)
│  ├─ Cost per formalization: $222 ($100K / 450)
│  ├─ By sector: IT: 22% formalization, Retail: 15%, Construction: 12%
│  └─ Geographic hotspots: Dhaka textile cluster highest (25% formalization)
│
└─ Feedback loop: 
   ├─ Which messaging works? (sentiment analysis of SMS responses)
   ├─ Which sectors most responsive? 
   └─ Recommendations for next campaign budget allocation
```

#### **Why This Matters for ILO:**
- **Previously:** "We held 20 awareness events; ~100 businesses showed up; didn't know if they formalized"
- **Now:** "We reached 2,500 businesses; 18% formalized within 3 months; we can measure ROI; IT sector most responsive"

#### **GCP Services Used (Pre-Packaged):**
1. **BigQuery** — Consolidates heterogeneous data sources
2. **Google Cloud Vision API** — Satellite imagery analysis (commercial activity detection)
3. **Vertex AI AutoML** — Zero-code ML model (where are informal businesses?)
4. **Google Maps API** — Geospatial visualization
5. **Looker** — Dashboard + drill-down analytics
6. **Google Forms + Sheets** — Event data capture
7. **Twilio API** — SMS follow-ups (3rd-party, integrates with GCP)

#### **Implementation Timeline:**
- Week 1–2: Data ingestion (surveys, tax data, transaction data into BigQuery)
- Week 3: Satellite imagery analysis + clustering model training
- Week 4: Campaign targeting recommendations
- Week 5–6: Forms + SMS automation setup
- Week 7–8: Dashboard deployment

#### **Cost Model (Bangladesh, GCP):**
- **Infrastructure:** ~$1–2K/month (BigQuery storage + API calls)
- **Your delivery:** 200 hours (project management, model training, dashboard build) = $10K
- **Client value:** Can optimize campaign budget; measure ROI; scale to 10K businesses
- **Typical project fee:** $20–30K

---

### **ILO SOLUTION 2: "Migration Intelligence Hub" (Overseas Employment Platform Adoption)**

**Addresses:** Project 2 (Overseas Employment Platform Launch & Tracking)

#### **Problem It Solves:**
- ILO has OEP platform; doesn't know who's using it or if it's reaching target workers
- Overseas workers scattered across 20+ countries; no way to measure adoption by location/demographics
- No feedback loop (which workers satisfied? which need support?)

#### **Tech Stack (AWS-first):**

```
LAYER 1: DIASPORA WORKER IDENTIFICATION
├─ Data sources:
│  ├─ Bangladesh Bank remittance data (who sends money from overseas?)
│  ├─ Mobile operator partnership data (which phone numbers are international roaming?)
│  ├─ BLMI agreement databases (workers in Gulf, Malaysia, etc. per bilateral agreement)
│  └─ Diaspora organization membership lists (NGOs, cultural groups tracking overseas workers)
│
└─ AWS Tools:
   ├─ AWS Glue (consolidate data from multiple sources)
   ├─ Amazon Athena (SQL queries across remittance data)
   └─ AWS Lake Formation (secure data catalog + privacy controls)

LAYER 2: TARGETED OUTREACH CAMPAIGN
├─ Segmentation:
│  ├─ Query: "Which workers are high-risk? (Low wages, new to country, no contract)"
│  ├─ Tool: Athena + custom SQL
│  └─ Result: 50K high-risk workers identified (priority for OEP platform)
│
├─ Channel strategy:
│  ├─ Tool: AWS Pinpoint (multi-channel marketing: SMS, email, social)
│  ├─ Channels: WhatsApp (diaspora groups), SMS (direct), email (those with email)
│  └─ Message: Localized to destination country (Arabic for Gulf, Malay for Malaysia)
│
└─ Tracking:
   ├─ SMS link: "bit.ly/oep-workers" → redirects to OEP platform
   ├─ Tool: Amazon Pinpoint tracks click-through rate
   ├─ Google Analytics tags on platform (source: SMS, email, WhatsApp)
   └─ Result: Can see "SMS campaign generated 15K new users; 8% conversion to registration"

LAYER 3: PLATFORM USAGE ANALYTICS
├─ Real-time event tracking:
│  ├─ Events: User login, job search, safe migration guide viewed, complaint filed, message sent to sponsor
│  ├─ Tool: AWS Kinesis (stream worker activity events)
│  └─ Processing: Lambda functions auto-flag anomalies (user logged in 50x in 1 hour; might be bot)
│
├─ User cohort tracking:
│  ├─ Cohort A: Users acquired via SMS campaign (15K)
│  ├─ Cohort B: Users from diaspora organizations (20K)
│  ├─ Cohort C: Organic discovery (10K)
│  └─ Query: Which cohort most engaged? Highest retention?
│
└─ Feature usage analysis:
   ├─ Which features most used? (Safe migration guide, job listings, complaint mechanism)
   ├─ Tool: Amazon Athena + QuickSight (visualize usage patterns)
   └─ Insight: 60% of users visit safe migration guide; 15% file complaints; 30% search jobs

LAYER 4: FEEDBACK LOOP & SUPPORT
├─ In-app feedback:
│  ├─ Tool: AWS Lex (chatbot) + connect to ILO support staff
│  ├─ Use case: "I was paid 2,000 BDT less than contract; what do I do?"
│  └─ Response: Lex suggests "File complaint; here's template" or routes to ILO counselor
│
├─ Sentiment analysis:
│  ├─ Tool: Amazon Comprehend (analyze user messages/feedback)
│  ├─ Sentiment: Positive ("platform helped me negotiate wage"), Negative ("confusing interface"), Neutral
│  └─ Result: Monthly sentiment score; alerts if plunge below threshold
│
└─ Recommendation system:
   ├─ For users searching jobs: ML model recommends safe employers + valid contracts
   ├─ Tool: Amazon SageMaker (train model on historical data; which employers safe?)
   └─ Outcome: Reduce user exposure to fraudulent/exploitative employers

LAYER 5: DASHBOARDING
├─ Tool: Amazon QuickSight
├─ Metrics:
│  ├─ Active users by country (Gulf: 35K, Malaysia: 25K, Singapore: 15K, Thailand: 10K)
│  ├─ Feature adoption (safe migration guide: 60%, job listings: 30%, complaint: 15%)
│  ├─ Cohort retention (Day 1 to Day 30: SMS cohort 35%, org cohort 55%)
│  ├─ Sentiment trend (↑↑ good, last month average 4.2/5)
│  └─ Support tickets by reason (wage dispute: 40%, contract issue: 30%, safety: 20%, other: 10%)
│
└─ Alerts:
   ├─ If user engagement drops >20% week-over-week: Alert ILO team
   ├─ If complaints spike: Alert safety team
   └─ If retention below cohort benchmark: Alert user engagement team
```

#### **Why This Matters for ILO:**
- **Previously:** "We launched OEP; we don't know how many overseas workers know about it or use it"
- **Now:** "We reached 50K high-risk workers; 25K registered on platform; 60% visiting safety guide; 8% complaint rate (acceptable); retention improving month-over-month"

#### **AWS Services Used (Pre-Packaged):**
1. **AWS Glue** — Multi-source data consolidation
2. **Amazon Athena** — SQL queries across data lake
3. **AWS Pinpoint** — Multi-channel marketing automation
4. **Amazon Kinesis** — Real-time event streaming
5. **AWS Lambda** — Serverless anomaly detection
6. **Amazon Lex** — Chatbot for support
7. **Amazon Comprehend** — Sentiment analysis
8. **Amazon SageMaker** — ML model for safe employer recommendation
9. **Amazon QuickSight** — Dashboard

#### **Implementation Timeline:**
- Week 1–2: Data integration (remittance data, mobile data, org lists)
- Week 3–4: Segmentation + SMS campaign setup
- Week 5–6: Platform event tracking + Kinesis pipeline
- Week 7–8: Chatbot + sentiment analysis deployment
- Week 9–10: Dashboard + alerts

#### **Cost Model (Bangladesh, AWS):**
- **Infrastructure:** ~$2–3K/month (Kinesis, Athena, Pinpoint)
- **Your delivery:** 250 hours = $12.5K
- **Client value:** Measurable platform adoption; user retention optimization; complaint tracking
- **Typical project fee:** $25–35K

---

### **ILO SOLUTION 3: "Impact Attribution Engine" (LAWC Midterm Evaluation)**

**Addresses:** Project 3 (Midterm Evaluation of LAWC Cluster)

#### **Problem It Solves:**
- ILO can't link "worker attended training in Month 3" → "same worker has better wages in Month 18"
- Data scattered: Training attendance, survey responses, wage data in separate systems
- Can't measure which interventions actually worked

#### **Tech Stack (Azure-first):**

```
LAYER 1: BENEFICIARY LINKAGE (THE CORE CHALLENGE)
├─ Problem: Baseline survey (2,000 people) done in Year 1; training data from Year 1-2; need Year 2-3 data
│           But beneficiary IDs different across systems (survey ID ≠ training ID ≠ wage registry ID)
│
├─ Solution: Master data management
│  ├─ Tools:
│  │  ├─ Azure Data Factory (ETL pipeline)
│  │  ├─ Azure Synapse (unified data warehouse)
│  │  └─ Microsoft's Fuzzy Matching (handle typos, name variations)
│  │
│  └─ Process:
│     ├─ Input: Baseline survey (2,000 people) + training records (50K people) + wage registry (subset)
│     ├─ Step 1: Standardize names, dates, phone numbers across systems
│     ├─ Step 2: Fuzzy match (does "Ravi Kumar" in survey ≈ "Ravi Kumarswamy" in training?) 
│     ├─ Step 3: Manual review of ambiguous matches
│     └─ Output: Single beneficiary ID linking all data
│
└─ Result: Can now query "Ravi Kumar: trained on Month 3, wage on Year 1 end, wage on Year 2 end"

LAYER 2: CONTROL GROUP CONSTRUCTION
├─ Problem: "LAWC trained 50K workers. Did wages increase? We don't know vs. what."
│
├─ Solution: Find comparison group using propensity score matching
│  ├─ Tools:
│  │  ├─ Azure Machine Learning (propensity score model)
│  │  ├─ Azure Notebooks (Python + scikit-learn)
│  │  └─ Azure Synapse (SQL queries for matching)
│  │
│  └─ Process:
│     ├─ Input: Baseline survey (demographics, baseline wage, sector, education)
│     ├─ Model: Train logistic regression (what predicts someone being in LAWC?)
│     ├─ Propensity: Score each person 0–100 (likelihood of being trained)
│     ├─ Match: For each LAWC trainee with score 65, find non-trainee with score 65–67
│     └─ Output: 50K LAWC trainees matched with 50K similar non-trainees (control group)
│
└─ Result: Now can say "LAWC trainees earned 15% more; control group earned 8%; LAWC impact = 7%"

LAYER 3: IMPACT MEASUREMENT (DIFFERENCE-IN-DIFFERENCES)
├─ Tools:
│  ├─ Azure Databricks (Apache Spark; handle large-scale computation)
│  ├─ R/Python notebooks (regression analysis)
│  └─ Synapse (store results)
│
├─ Analysis:
│  ├─ For each outcome (wage, rights awareness, formalization):
│  │  ├─ Calculate: (LAWC_trainee_Year2 - LAWC_trainee_Year1) - (Control_Year2 - Control_Year1)
│  │  ├─ Example: Wage impact = (trainee +15%) - (control +8%) = +7% attributable to LAWC
│  │  └─ Statistical test: Is this 7% significant or noise? (t-test)
│  │
│  └─ By segment:
│     ├─ IT sector: +12% impact (very high)
│     ├─ Construction: +5% impact (moderate)
│     ├─ RMG: +2% impact (minimal)
│     └─ Women: +10% impact; Men: +4% impact
│
└─ Output: "LAWC generated 7% average wage improvement; highest for IT & women; minimal for RMG"

LAYER 4: QUALITATIVE INTEGRATION (MIXED METHODS)
├─ Problem: Numbers don't tell full story ("Why did IT sector see 12% improvement but RMG only 2%?")
│
├─ Solution: Link quantitative results to qualitative feedback
│  ├─ Input: Baseline survey qualitative responses (open-ended Q: "What prevents you from getting a better job?")
│  ├─ Tool: Azure Cognitive Services (Text Analytics; extract themes)
│  ├─ Themes: Lack of skills (mentioned 800x), unfair wages (700x), harassment (300x), poor connections (500x)
│  └─ Map to outcomes:
│     ├─ IT sector: Most mentioned "lack of skills" (trainees learned, got better jobs) → explains high impact
│     ├─ RMG sector: Most mentioned "unfair wages + harassment" (training didn't help much) → explains low impact
│     └─ Insight: Training alone isn't enough for RMG; need parallel wage advocacy + safety intervention
│
└─ Output: Policy recommendation: "For RMG, combine training + wage negotiation support; for IT, training alone works"

LAYER 5: STORYTELLING ENGINE
├─ Problem: Numbers are hard to communicate to donors + policymakers
│
├─ Solution: Data-driven narrative + beneficiary stories
│  ├─ Quantitative spine: "LAWC generated 7% wage improvement for 50K workers = $X million economic impact"
│  ├─ Qualitative meat: 5 beneficiary stories with name + photo + wage data
│  │  ├─ Story 1: Ravi (IT, +35% wage, moved to senior role, married)
│  │  ├─ Story 2: Fatima (RMG, +5% wage, learned negotiation, stands up to supervisor)
│  │  └─ etc.
│  │
│  └─ Tools:
│     ├─ Azure Power BI (create interactive report)
│     ├─ Embed beneficiary stories + charts + data
│     └─ Share with donors: They can drill into data + read stories

LAYER 6: DASHBOARDING & ALERTS
├─ Tool: Power BI
├─ Metrics:
│  ├─ Overall impact: 7% wage improvement, 45% formalization, 60% rights awareness
│  ├─ By sector: IT +12%, Construction +5%, RMG +2%, Services +8%
│  ├─ By gender: Women +10%, Men +4%
│  ├─ Statistical significance: All p < 0.05 (real, not noise)
│  └─ Beneficiary stories: 5 highlighted stories with data
│
└─ Donor report: Power BI report shared with donors; they can explore data themselves
```

#### **Why This Matters for ILO:**
- **Previously:** "LAWC trained 50K workers; we think it helped but can't prove it; anecdotal success stories only"
- **Now:** "LAWC generated 7% wage improvement attributable to training; highest impact in IT (12%); minimal in RMG (2%); should adjust strategy; here are 5 beneficiary success stories backed by data"

#### **Azure Services Used (Pre-Packaged):**
1. **Azure Data Factory** — ETL pipeline
2. **Azure Synapse** — Unified data warehouse
3. **Azure Machine Learning** — Propensity score matching
4. **Azure Databricks** — Difference-in-differences analysis
5. **Azure Cognitive Services (Text Analytics)** — Qualitative theme extraction
6. **Microsoft Power BI** — Dashboard + reporting

#### **Implementation Timeline:**
- Week 1–2: Data integration (baseline survey + training records + wage data)
- Week 3–4: Beneficiary linkage + fuzzy matching
- Week 5–6: Control group construction (propensity score)
- Week 7–8: Impact analysis (difference-in-differences)
- Week 9: Qualitative integration + storytelling
- Week 10–11: Dashboard + Power BI report
- Week 12: Donor report + training

#### **Cost Model (Bangladesh, Azure):**
- **Infrastructure:** ~$1.5–2.5K/month (Synapse, Databricks)
- **Your delivery:** 300 hours (data integration, statistical analysis, dashboard) = $15K
- **Client value:** Evidence-based impact claim; donor confidence; policy direction
- **Typical project fee:** $35–50K

---

---

## UNDP SOLUTION STACK
### Problem: "Beneficiary Accountability + Data Fragmentation"

**Core Challenge:** UNDP needs to:
1. Verify beneficiary identity (is this really Fatima? Is she in 2 programmes?)
2. Track real-time activities (trainings, disbursements, outcomes)
3. Detect fraud/errors before they happen
4. Link activities to outcomes systematically

---

### **UNDP SOLUTION 1: "Beneficiary Verification Engine" (Training Allowances)**

**Addresses:** Project 1 (Facilitating Training Allowance Disbursement)

#### **Problem It Solves:**
- Duplicate payments: Same person gets allowance from 2 training centers
- Ghost attendees: Trainer signs off on attendance; person didn't actually attend
- Payment errors: Allowance goes to wrong phone number or bank account
- Audit failures: Can't prove who got what, when

#### **Tech Stack (GCP + third-party identity services):**

```
LAYER 1: BENEFICIARY IDENTITY VERIFICATION
├─ Problem: Paper attendance sheets; no way to verify "this is really Fatima"
│           Current system: Trainer calls office, office updates Excel; takes 2 weeks
│
├─ Solution: Biometric-enabled field collection
│  ├─ Devices: Android tablets at each training center
│  ├─ App: Custom app on Firebase (offline-first)
│  │
│  ├─ Enrollment process (Day 1 of training):
│  │  ├─ Trainer enters trainee name + age
│  │  ├─ Tablet captures: Fingerprint (or photo if no fingerprint reader)
│  │  ├─ Tablet compares to existing database (is this person already enrolled?)
│  │  └─ If yes: ALERT "Duplicate enrollment detected"; if no: Enroll
│  │
│  ├─ Attendance process (each training day):
│  │  ├─ Trainee touches fingerprint reader (or takes selfie)
│  │  ├─ Tablet queries: "Is this Fatima enrolled in this training?"
│  │  ├─ Tablet checks: "Did Fatima attend yesterday?" (no ghost attendees)
│  │  ├─ If all checks pass: Mark attendance; if flags raised: Manual review
│  │  └─ Data syncs offline; uploads when internet available
│  │
│  └─ Tools:
│     ├─ Firebase Realtime Database (offline-capable; beneficiary list syncs to tablets)
│     ├─ Firebase Cloud Functions (on attendance submit, auto-check for duplicates)
│     ├─ Cloud ML Kit (on-device fingerprint matching; no need to send biometrics to cloud)
│     └─ Google Cloud Storage (encrypted storage of biometric data)
│
└─ Result: Real-time duplicate detection; no ghost attendees; beneficiary identity verified

LAYER 2: PAYMENT ROUTING VERIFICATION
├─ Problem: Trainer says Fatima attended; but allowance goes to wrong mobile wallet
│           Current: Fatima gives number; accountant disburses; 10% of payments fail due to typos
│
├─ Solution: Verify payment recipient before disbursement
│  ├─ Process:
│  │  ├─ Fatima enrolls (during training): Provides mobile wallet # OR bank account
│  │  ├─ System: Sends SMS "Confirm your payment number: 01712345678. Reply YES/NO"
│  │  ├─ Fatima: Replies YES (or corrects if wrong)
│  │  ├─ System: Locks in number; any payment to different number blocked
│  │  └─ Accountant: Can only disburse to verified number
│  │
│  └─ Tools:
│     ├─ Firebase Functions (auto-send SMS confirmation)
│     ├─ Twilio (SMS provider)
│     └─ BigQuery (log confirmations; audit trail)
│
└─ Result: 99% payment accuracy; no bounced transfers; full audit trail

LAYER 3: REAL-TIME ALERTS
├─ Problem: Trainer marks Fatima as "attended" 10x in one day (impossible; fraud signal)
│
├─ Solution: Anomaly detection on attendance patterns
│  ├─ Tools:
│  │  ├─ Vertex AI (train model on historical attendance; flag outliers)
│  │  ├─ Cloud Pub/Sub (real-time event stream)
│  │  └─ Cloud Functions (auto-alert on anomaly)
│  │
│  ├─ Anomaly types detected:
│  │  ├─ Same person marked attended at 2 training centers simultaneously
│  │  ├─ Same person attended 0 days → suddenly gets full allowance
│  │  ├─ Trainer submitting attendance for 200 people in 30 minutes (unrealistic)
│  │  └─ Payment account changes mid-training (possible fraud)
│  │
│  └─ Alert output:
│     ├─ If low confidence: Flag for manual review (manager checks)
│     ├─ If high confidence fraud signal: Block payment; alert compliance officer
│     └─ Dashboard: UNDP monitor sees live alerts; can intervene
│
└─ Result: Fraud caught before payment; no bad payments

LAYER 4: DASHBOARDING & COMPLIANCE
├─ Tool: Looker (GCP)
├─ Metrics:
│  ├─ Beneficiaries: 4,500 trained across 4 districts
│  ├─ Duplicate enrollments detected: 12 (prevented duplicate payments)
│  ├─ Payment accuracy: 99.2% (vs. historical 85%)
│  ├─ Fraud alerts: 8 (stopped before payment)
│  ├─ Manual reviews: 3 (all resolved; 2 were legit, 1 was fraud)
│  └─ Compliance: 100% payment verified before disbursement
│
└─ Audit trail: Every attendance record linked to biometric proof; full audit trail for donor verification
```

#### **Why This Matters for UNDP:**
- **Previously:** "Paid 4,500 allowances; ~450 (10%) had errors or fraud; discovered during audits 3 months later"
- **Now:** "Paid 4,500 allowances; 99.2% accuracy; 0 fraud; caught anomalies in real time; full audit trail"

#### **GCP Services Used (Pre-Packaged):**
1. **Firebase Realtime Database** — Offline-capable app
2. **Cloud ML Kit** — On-device biometric matching
3. **Cloud Functions** — Serverless duplicate detection + SMS triggers
4. **Pub/Sub** — Real-time event streaming
5. **Vertex AI** — Anomaly detection model
6. **BigQuery** — Audit logging
7. **Looker** — Compliance dashboard
8. **Twilio** — SMS verification (3rd-party)

#### **Implementation Timeline:**
- Week 1–2: Tablet app development (Firebase + ML Kit)
- Week 3: Duplicate detection + SMS verification setup
- Week 4–5: Anomaly detection model training
- Week 6: Dashboard deployment
- Week 7–8: Pilot in 1 district; scale to all 4

#### **Cost Model (Bangladesh, GCP):**
- **Infrastructure:** ~$1.5–2K/month (Firebase, Vertex AI)
- **Your delivery:** 200 hours (app dev, model training, deployment) = $10K
- **Client value:** Fraud prevention, accuracy improvement, compliance assurance
- **Typical project fee:** $25–35K

---

### **UNDP SOLUTION 2: "Real-Time Programme Analytics" (Impact Assessment Platform)**

**Addresses:** Project 2 (SWAPNO II Impact Assessment)

#### **Problem It Solves:**
- UNDP has baseline data from 2 years ago; training records scattered; no endline data
- Can't answer: "Did training → job → wage increase?"
- Manual data consolidation takes 4–6 weeks

#### **Tech Stack (AWS-first):**

```
LAYER 1: UNIFIED BENEFICIARY DATASET
├─ Problem: Baseline survey data (2 years old) in Excel; training records in different system; endline data missing
│
├─ Solution: Centralized data lake + master data management
│  ├─ Tools:
│  │  ├─ AWS S3 (data lake; store all data sources)
│  │  ├─ AWS Glue (ETL; consolidate baseline + training + job placement data)
│  │  ├─ Amazon RDS (relational DB; single beneficiary record)
│  │  └─ AWS DMS (Database Migration Service; import legacy data)
│  │
│  ├─ Data sources:
│  │  ├─ Baseline survey (2,000 people; 80 questions; stored in old survey format)
│  │  ├─ Training attendance (50K records; trainer names, dates)
│  │  ├─ Job placement tracking (self-reported; stored in separate Excel)
│  │  └─ Wage data (partial; only 30% of trainees willing to share)
│  │
│  └─ Process:
│     ├─ AWS Glue: Auto-detect schema from each source
│     ├─ Fuzzy matching: Link "Ravi from survey" to "Ravi from training records"
│     ├─ Standardize: Dates, wages, sectors all use consistent format
│     └─ RDS: Single beneficiary table with all linked data
│
└─ Result: Can query "Ravi: baseline wage 8000, training completed 2023-Jun, current wage 10000, currently employed in IT"

LAYER 2: ENDLINE DATA COLLECTION
├─ Problem: Need to re-contact 2,000 baseline respondents 2 years later; get wages, job status, outcomes
│           But many have moved; old phone numbers no longer valid
│
├─ Solution: Multi-channel tracking + SMS/call campaign
│  ├─ Data available (from baseline):
│  │  ├─ Phone numbers (80% still valid after 2 years; 20% changed)
│  │  ├─ Locations (some may have migrated)
│  │  ├─ Alternative contacts (emergency contact from baseline)
│  │  └─ Social media info (if collected)
│  │
│  ├─ Tracking tools:
│  │  ├─ AWS SNS + Pinpoint (send SMS: "Hi Ravi! We'd like to follow up on your job. Reply with your current wage.")
│  │  ├─ AWS Pinpoint (auto-capture SMS responses; parse wage data)
│  │  ├─ Amazon Connect (if SMS fails, trigger phone call campaign)
│  │  └─ Fallback: In-person field visits for non-respondents (sample)
│  │
│  ├─ Response handling:
│  │  ├─ Tools: Amazon Lex (chatbot; parse SMS responses)
│  │  ├─ If Ravi replies "Current wage 10000": Auto-parse + log in RDS
│  │  ├─ If Ravi replies with ambiguous text: Route to human agent (Amazon Connect)
│  │  └─ If no response after 3 attempts: Mark as "lost to follow-up"
│  │
│  └─ Result: Endline data collected for ~1,500–1,700 baseline respondents (75–85% follow-up rate)

LAYER 3: CONTROL GROUP MATCHING (REPRISE)
├─ Same as ILO Solution 3, but for SWAPNO II scale (50K trainees vs. 100K comparison pool)
│  ├─ Tools: SageMaker (propensity score matching)
│  ├─ Output: Matched cohorts (50K trained, 50K control)
│  └─ Ready for impact analysis

LAYER 4: IMPACT ANALYSIS (DETAILED)
├─ Tools: Amazon Athena (SQL queries) + Python notebooks (ML-powered analysis)
│
├─ Outcomes measured:
│  ├─ Employment status: % with formal job
│  ├─ Wage level: Average wage in formal job
│  ├─ Job quality: Contract type, benefits, safety
│  ├─ Sector distribution: Where are trainees employed? (IT, RMG, services, etc.)
│  └─ Equity: Differences by gender, location, baseline education
│
├─ Analysis approach (Difference-in-Differences):
│  ├─ Outcome = (Trainee_endline - Trainee_baseline) - (Control_endline - Control_baseline)
│  │
│  ├─ Example results:
│  │  ├─ Employment rate: Trainees +25% (60% → 85%), Control +8% (60% → 68%) → Impact = +17%
│  │  ├─ Wage (formal jobs): Trainees +22%, Control +12% → Impact = +10%
│  │  ├─ Contract quality: Trainees 80% written contracts; Control 45% → Impact = +35 ppt
│  │  ├─ IT sector trainees: +35% employment impact
│  │  └─ Women: +28% impact; Men: +12% impact
│  │
│  └─ Statistical tests: All estimates p < 0.05 (real, not noise)
│
└─ Output: "SWAPNO II generated +17 ppt employment impact; +10% wage gains; particularly strong for IT & women"

LAYER 5: SECTORAL DRILL-DOWN
├─ SWAPNO II trained people across 5 sectors: IT, RMG, healthcare, construction, hospitality
├─ Question: Did all sectors benefit equally?
│
├─ Analysis:
│  ├─ Subset data: 10K IT trainees; analyze separately
│  ├─ IT sector impact: +35% employment (vs. +17% average)
│  ├─ RMG sector impact: +5% employment (vs. +17% average)
│  ├─ Why the difference?
│  │  ├─ IT sector: Growing demand + high wages; training directly skills businesses need
│  │  ├─ RMG sector: Wage suppression + overcrowding; training helps but limited by sector constraints
│  │  └─ Insight: SWAPNO II very effective for IT; less effective for RMG; should adjust strategy
│  │
│  └─ Recommendation: "Double down on IT/digital training; for RMG, combine training with advocacy/wage negotiation"

LAYER 6: EQUITY ANALYSIS
├─ Question: Did women, minorities, marginalized groups benefit equally?
│
├─ Analysis:
│  ├─ Gender: Women +28% employment impact; Men +12% impact (women benefited MORE)
│  ├─ Location: Urban trainees +20% impact; Rural trainees +8% impact (urban advantage)
│  ├─ Baseline education: College-educated +25% impact; High school +15% impact; Dropped out +5% impact
│  │
│  ├─ Equity finding: "SWAPNO II worked well for women; but rural/disadvantaged groups benefited less"
│  │
│  └─ Recommendation: "Future programming: Target rural areas + lower-education groups; pair with childcare support for women"

LAYER 7: DASHBOARDING & STORYTELLING
├─ Tool: Amazon QuickSight
├─ Narrative:
│  ├─ Headline: "SWAPNO II generated +17% employment impact for 50K trainees"
│  ├─ Subheadline: "Equivalent to 8,500 people who wouldn't have jobs otherwise"
│  ├─ Breakdowns:
│  │  ├─ "IT sector: +35% impact" → Interactive chart showing sector-by-sector
│  │  ├─ "Women particularly benefited: +28% impact" → Equity chart
│  │  └─ "Rural areas need more support: +8% impact vs. +20% urban" → Geographic map
│  │
│  ├─ Beneficiary stories: 5 success stories with names + photos + wage data
│  │  ├─ Story 1: Ravi (IT, baseline 8K → now 18K; first formal job; credits training)
│  │  ├─ Story 2: Fatima (RMG, baseline 7K → now 8.5K; negotiated wage; learned from training)
│  │  └─ etc.
│  │
│  └─ CTA: "Based on evidence, scale SWAPNO II and focus on IT + digital skills for highest impact"

LAYER 8: DONOR REPORTING
├─ Interactive Power BI/QuickSight dashboard shared with donors
├─ Donors can drill into: Geography → Sector → Gender → Individual stories
├─ Full audit trail: Every number linked to data source
└─ Confidence: "This is evidence-based impact, not anecdote"
```

#### **Why This Matters for UNDP:**
- **Previously:** "SWAPNO II trained 50K people; we think it worked; couldn't prove it"
- **Now:** "SWAPNO II generated +17% employment impact for 50K trainees; highest for IT & women; lowest for RMG & rural; here are 5 success stories backed by data"

#### **AWS Services Used (Pre-Packaged):**
1. **AWS Glue** — ETL pipeline
2. **Amazon RDS** — Unified database
3. **AWS DMS** — Legacy data migration
4. **Amazon S3** — Data lake
5. **AWS SNS + Pinpoint** — SMS endline survey campaign
6. **Amazon Lex** — Response parsing
7. **Amazon Athena** — SQL queries
8. **Amazon SageMaker** — Propensity score + analysis notebooks
9. **Amazon QuickSight** — Dashboard

#### **Implementation Timeline:**
- Week 1–2: Data consolidation (baseline + training + placement)
- Week 3–4: Endline data collection campaign (SMS + calls)
- Week 5–6: Control group matching
- Week 7–8: Impact analysis + equity breakdown
- Week 9–10: Dashboard + storytelling
- Week 11–12: Donor report

#### **Cost Model (Bangladesh, AWS):**
- **Infrastructure:** ~$2–3K/month (RDS, Athena, Pinpoint, SageMaker)
- **Your delivery:** 280 hours (data integration, analysis, dashboard, donor training) = $14K
- **Client value:** Evidence-based impact claim; donor confidence; programme optimization
- **Typical project fee:** $40–60K

---

### **UNDP SOLUTION 3: "Real-Time Programme Operations Dashboard" (Ecopia App Integration)**

**Addresses:** Project 3 (Ecopia App Maintenance + Integration)

#### **Problem It Solves:**
- Ecopia app generates data but isn't connected to UNDP systems
- Programme manager can't see: "How many trainings happened today? How many beneficiaries? Are we on track?"
- Data analysis takes days; needed real-time

#### **Tech Stack (GCP + Firebase + Looker):**

```
LAYER 1: REAL-TIME DATA SYNC FROM ECOPIA APP
├─ Problem: Ecopia app collects data offline; syncs to backend in batches (24-hour lag)
│           Programme manager needs: Live view of today's activities
│
├─ Solution: Firebase + real-time database
│  ├─ Current: Ecopia syncs to REST API once daily
│  ├─ New: Ecopia syncs to Firebase Realtime Database in real-time
│  │
│  ├─ Implementation:
│  │  ├─ Step 1: Add Firebase SDK to Ecopia app (minimal code change)
│  │  ├─ Step 2: When field staff submits activity (training, distribution, outcome), sync to Firebase in real-time
│  │  ├─ Step 3: Offline capability: If no internet, store locally; sync when available
│  │  └─ Step 4: Firebase webhooks notify UNDP backend (BigQuery) of new events
│  │
│  └─ Result: Data visible in dashboard within 5 minutes of field submission (vs. 24 hours)

LAYER 2: INTEGRATION WITH UNDP SYSTEMS
├─ Problem: Ecopia data siloed; not linked to UNDP's beneficiary DB, finance system, M&E platform
│
├─ Solution: API bridges + data pipeline
│  ├─ Tools:
│  │  ├─ Firebase Functions (serverless; trigger on new Ecopia event)
│  │  ├─ Google Cloud Tasks (reliable job queue; send data to UNDP systems)
│  │  ├─ BigQuery (receive + store Ecopia data)
│  │  └─ Pub/Sub (publish events; any UNDP system can subscribe)
│  │
│  ├─ Flow:
│  │  ├─ Event: Field staff marks "Training attended" in Ecopia for beneficiary #12345
│  │  ├─ Firebase: Event captured in real-time
│  │  ├─ Cloud Task: Send event to UNDP's beneficiary system (mark training as completed for #12345)
│  │  ├─ BigQuery: Log event (for analytics)
│  │  ├─ Pub/Sub: Publish event (M&E team can subscribe; see real-time training data)
│  │  └─ Finance: Auto-trigger training allowance calculation (beneficiary now eligible for allowance)
│  │
│  └─ Result: One activity in Ecopia triggers updates across all UNDP systems

LAYER 3: REAL-TIME DASHBOARDING
├─ Tool: Looker (Google)
├─ Metrics visible (live, updated every 5 minutes):
│  ├─ Today's activities:
│  │  ├─ Trainings delivered: 145 sessions (target: 150)
│  │  ├─ Beneficiaries trained: 2,890 (target: 3,000)
│  │  ├─ Distributions completed: 12 (blankets, food, hygiene kits)
│  │  ├─ Outcomes recorded: 340 (beneficiary progress reports)
│  │  └─ Geographic breakdown: Dhaka 35%, Chittagong 25%, Khulna 20%, Sylhet 20%
│  │
│  ├─ Versus targets:
│  │  ├─ Trainings: 145/150 = 97% (green; on track)
│  │  ├─ Beneficiaries: 2,890/3,000 = 96% (green)
│  │  ├─ Distributions: 12/12 = 100% (green)
│  │  └─ Sylhet distribution: Only 6/10 expected (red; alert)
│  │
│  ├─ Alerts:
│  │  ├─ Sylhet underperforming: Only 20% of expected distributions completed
│  │  ├─ Recommendation: "Check Sylhet field team; any logistical issues?"
│  │  └─ Auto-notify: Regional coordinator gets SMS alert
│  │
│  └─ Weekly/monthly views:
│     ├─ Trend: Are we catching up on backlogs or falling further behind?
│     ├─ Quality: Is data quality consistent across regions?
│     ├─ Beneficiary progress: Are trainees improving over time?
│     └─ Cost per outcome: $X per beneficiary trained (efficiency tracking)

LAYER 4: ENVIRONMENTAL DATA INTEGRATION
├─ Problem: Ecopia collects climate data (rainfall, soil moisture, temperature) but isn't used for decision-making
│
├─ Solution: Combine Ecopia climate data with beneficiary outcomes
│  ├─ Analysis questions:
│  │  ├─ Does rainfall influence livelihood outcomes? (e.g., farmers' income up when rainfall stable)
│  │  ├─ Which zones most climate-vulnerable? (low rainfall, high temperature variability)
│  │  └─ Should we prioritize climate-smart agricultural training in vulnerable zones?
│  │
│  ├─ Tools:
│  │  ├─ BigQuery (consolidate climate data + beneficiary data)
│  │  ├─ Data Studio (visualize: rainfall trend + farmer income trend side-by-side)
│  │  └─ Vertex AI (predict: "If rainfall drops 20%, expect 15% income drop; recommend early intervention")
│  │
│  └─ Output: Climate risk alerts ("Rainfall 30% below normal; trigger safety net payments for vulnerable households")

LAYER 5: PREDICTIVE ALERTS
├─ Problem: Programme manager reacts to problems (beneficiary not progressing) instead of preventing them
│
├─ Solution: ML model predicts who will struggle
│  ├─ Model inputs (from Ecopia + beneficiary data):
│  │  ├─ Attendance pattern (is beneficiary missing sessions?)
│  │  ├─ Engagement (is beneficiary actively participating?)
│  │  ├─ Climate stress (is their area experiencing rainfall/heat stress?)
│  │  └─ Baseline characteristics (age, education, prior experience)
│  │
│  ├─ Model output (Vertex AI):
│  │  ├─ Probability beneficiary will drop out (next 30 days)
│  │  ├─ Example: "Fatima (age 22, rural, attended 3/5 trainings, recent heat stress) = 65% dropout risk"
│  │  └─ Alert: Flag to field mentor "Check in with Fatima; at risk of dropout"
│  │
│  ├─ Intervention:
│  │  ├─ Field mentor receives alert; calls/visits Fatima
│  │  ├─ Discovers: Fatima's crop failed due to heat; she's considering quitting to migrate for work
│  │  ├─ Response: Programme manager approves emergency cash transfer; Fatima continues training
│  │  └─ Outcome: Fatima stays engaged; completes training; gets job; no dropout
│  │
│  └─ Impact: Proactive support prevents dropout; saves downstream costs

LAYER 6: ADVANCED ANALYTICS
├─ Tools: Vertex AI AutoML
├─ Analysis: What drives successful beneficiary outcomes?
│  ├─ Feature importance: Which factors most strongly predict success?
│  │  ├─ Top factor: Attendance (80% importance; makes sense)
│  │  ├─ 2nd: Climate stability (15% importance; reveals climate vulnerability)
│  │  ├─ 3rd: Baseline education (5% importance; less important than expected)
│  │  └─ Insight: "We should focus on attendance + climate support more than baseline education"
│  │
│  └─ Segmentation: Which beneficiary groups most likely to succeed?
│     ├─ Segment A: Urban, high school education, stable climate = 80% success rate
│     ├─ Segment B: Rural, lower education, climate stress = 40% success rate
│     └─ Insight: "Segment B needs more support; should pair with safety nets + climate adaptation"

LAYER 7: DONOR VISIBILITY & COMPLIANCE
├─ Tool: Looker + embedded reports
├─ Donors can see:
│  ├─ Real-time activities (today's trainings, distributions)
│  ├─ Progress vs. targets (on track? Behind?)
│  ├─ Beneficiary stories + photos (embedded in dashboard)
│  ├─ Climate risks & mitigation (Ecopia environmental data)
│  ├─ Outcomes (jobs secured, income improved)
│  └─ Full audit trail (every activity logged; linked to beneficiary record)
│
└─ Result: Transparent, real-time programme monitoring; donor confidence
```

#### **Why This Matters for UNDP:**
- **Previously:** "Ecopia collects data, but we see it 24 hours later; can't respond in real-time; climate data unused; no predictive alerts"
- **Now:** "Live ops dashboard; alerts when Sylhet underperforming; predict who will drop out; prevent dropout proactively; integrate climate data; donors see real-time progress"

#### **GCP Services Used (Pre-Packaged):**
1. **Firebase Realtime Database** — Real-time sync
2. **Cloud Functions** — Serverless event triggers
3. **Cloud Tasks** — Reliable job queue
4. **BigQuery** — Data consolidation + analytics
5. **Pub/Sub** — Event publishing
6. **Vertex AI** — Predictive model
7. **Data Studio** — Climate data visualization
8. **Looker** — Real-time ops dashboard

#### **Implementation Timeline:**
- Week 1–2: Firebase integration with Ecopia app
- Week 3–4: API bridges to UNDP systems
- Week 5–6: Real-time dashboard deployment
- Week 7–8: Climate data integration
- Week 9–10: Predictive model training
- Week 11: Donor reporting setup

#### **Cost Model (Bangladesh, GCP):**
- **Infrastructure:** ~$2–2.5K/month (Firebase, Vertex AI, Looker)
- **Your delivery:** 240 hours (integration, dashboard, model, testing) = $12K
- **Client value:** Real-time operations visibility, predictive alerts, proactive support, donor transparency
- **Typical project fee:** $30–45K

---

---

## SUMMARY: ILO & UNDP SOLUTION PACKAGES

| Solution | Organization | Problem | Pre-Built Stack | Timeline | Cost |
|---|---|---|---|---|---|
| **Worker Intelligence** | ILO | Hidden informal workers; unmeasured campaign ROI | GCP (BigQuery, Vision, Vertex AI, Looker) | 8 weeks | $20–30K |
| **Migration Hub** | ILO | Overseas workers scattered; OEP adoption unmeasured | AWS (Glue, Athena, Pinpoint, SageMaker, QuickSight) | 10 weeks | $25–35K |
| **Impact Attribution** | ILO | Training → outcome linkage unmeasured | Azure (Data Factory, Synapse, Databricks, Power BI) | 12 weeks | $35–50K |
| **Beneficiary Verification** | UNDP | Duplicate payments; fraud; identity verification | GCP (Firebase, ML Kit, Cloud Functions, Looker) | 8 weeks | $25–35K |
| **SWAPNO II Analytics** | UNDP | Baseline-to-endline matching; impact measurement | AWS (Glue, RDS, SNS, Pinpoint, Athena, SageMaker, QuickSight) | 12 weeks | $40–60K |
| **Ecopia Integration** | UNDP | Real-time programme operations; predictive alerts | GCP (Firebase, Functions, BigQuery, Vertex AI, Looker) | 11 weeks | $30–45K |

---

## POSITIONING FOR YOUR WEBSITE

### **Homepage Hero:**
> "From Field Data to Real-Time Intelligence"
> "UN organizations collect data across thousands of field staff and beneficiaries. The data is rich. But it's siloed, manual, and arrives too late to act on. We turn their data into live dashboards, predictive alerts, and evidence-based impact measurement."

### **Solution Pages (one per offering):**
1. **Worker Intelligence Platform** (ILO)
2. **Migration Hub** (ILO)
3. **Impact Attribution Engine** (ILO)
4. **Beneficiary Verification Engine** (UNDP)
5. **Real-Time Programme Analytics** (UNDP)
6. **Ecopia Integration & Operations Dashboard** (UNDP)

### **Case Study Template (anonymized but specific):**
- Problem: "Large UN org couldn't measure training ROI; 50K trainees; couldn't match baseline → endline outcomes"
- Our approach: "Azure data lake + propensity score matching + difference-in-differences analysis"
- Outcome: "Measured 17% employment impact; identified IT sector most responsive; directed future budget accordingly"
- Deliverables: "Interactive dashboard, 5 beneficiary stories, donor brief"
- Timeline: "12 weeks"
- Cost: "$45K"

