# Concrete Products & Processes: ILO & UNDP Solutions

---

# ILO SOLUTIONS

## PRODUCT 1: Worker Registry + Segmentation Engine
### Problem It Solves
ILO doesn't know where informal workers/businesses are. They can't answer: "How many workers in construction sector in Dhaka? How many women? How many doing hazardous work?"

### The Product (What It Is)
**Name:** "Worker Intelligence Hub"
- **Core:** Unified database of Bangladeshi workers + businesses, updated quarterly via surveys + administrative data
- **Features:**
  1. Worker identification (name, ID, demographics, current sector/status)
  2. Segmentation (formal/informal, sector, region, gender, age, hazard exposure)
  3. Geographic heat mapping (concentration of informal workers by district/upazila)
  4. Trend tracking (how many formalized? moved sectors? entered/exited workforce?)

### Known Techniques to Build This

#### Technique 1: Multi-Source Data Integration (Proven in Bangladesh)
**What it is:**
- Combine 4 data sources: Labour Force Survey (LFS) + ILO field surveys + National ID registry + Bank account data

**How it works:**
1. **LFS baseline:** Bangladesh Bureau of Statistics runs LFS quarterly (~20,000 households); contains occupation, sector, employer, wages
2. **ILO surveys:** ILO runs project-specific surveys (formalization study, safety study, migration study); ~5,000 respondents each
3. **National ID linkage:** Bangladesh has NID (National ID) system; can match workers to government records
4. **Formal sector data:** Banks have account data for wage workers; Ministry of Labour has factory registrations

**Why it works:** You're not building from scratch; you're LINKING existing data sources

**Process:**
```
Step 1: Data Acquisition (Months 1-2)
├─ LFS data (request from BBS; 20K household records)
├─ ILO survey data (compile across 10+ ILO projects; ~50K respondent records)
├─ NID registry (request sample; ~100K NID + occupation data)
└─ Factory registry (Ministry of Labour; formal sector establishments)

Step 2: Standardization (Month 2-3)
├─ Create common identifier (Name + DOB + Phone + NID)
├─ Standardize occupation codes (Map ILO to BBS to National codes)
├─ Standardize location codes (Map all to district/upazila/union level)
└─ Handle duplicates (Same person appears in 2 surveys? Deduplicate)

Step 3: Linkage (Month 3-4)
├─ Probabilistic matching (Name + DOB + Phone likely same person)
├─ Manual review (Ambiguous matches reviewed by human)
├─ Create unified identifier (UUID for each unique worker)
└─ Build relationship matrix (Worker A appears in LFS, ILO survey, bank data)

Step 4: Analysis (Month 4-6)
├─ Segmentation queries (SQL: SELECT * WHERE sector=construction AND gender=female)
├─ Geographic heat maps (Worker density by location)
├─ Trend analysis (Year-over-year: formal vs. informal, sector shifts)
└─ Risk scoring (Workers in hazardous sectors, unstable employment, low wage)
```

**Tech Stack (GCP):**
- **Ingestion:** Google Cloud Storage (raw CSV files from BBS, ILO, Ministry)
- **ETL:** Google Cloud Dataprep (standardize + deduplicate) OR Dataflow (Apache Beam pipelines)
- **Matching:** BigQuery ML (probabilistic matching via ML model) + manual review tool (Sheets + conditional formatting)
- **Storage:** BigQuery (unified worker table; queryable by segment)
- **Visualization:** Looker (geographic heat maps, segment breakdowns)

**Implementation Process:**
```
Phase 1: Proof of Concept (Weeks 1-4)
├─ Ingest 10K LFS records
├─ Ingest 5K ILO survey records
├─ Manual matching (test approach)
├─ Build simple Looker dashboard (worker count by sector + region)
└─ Demo to ILO leadership

Phase 2: Production (Weeks 5-12)
├─ Ingest full datasets (200K+ records)
├─ Automated deduplication (99%+ accuracy target)
├─ Risk scoring model (which workers are vulnerable?)
├─ Live dashboard (ILO team can query on demand)
└─ Training for ILO data team

Phase 3: Operationalization (Weeks 13-16)
├─ Quarterly update process (refresh LFS + new ILO survey data)
├─ Automated anomaly detection (spike in informal sector growth?)
├─ API for downstream systems (UNDP, NGOs can query)
└─ Documentation + handoff to ILO team
```

#### Technique 2: Occupational Network Analysis (Emerging but Proven)
**What it is:**
- Map career pathways: Which workers move FROM sector A TO sector B? (e.g., construction → manufacturing, informal → formal)

**Why it works:** 
- Instead of static snapshots, you track MOVEMENT
- Shows which interventions work (if ILO trains construction workers → do they move to safer sectors?)

**How to implement:**
1. **Panel data:** Re-survey same workers quarterly for 1–2 years (track their movement)
2. **Transition matrix:** Build Markov chain (probability: construction worker → manufacturing in Q1?)
3. **Intervention impact:** Do workers who get ILO training move sectors faster than control group?

**Tech Stack (GCP):**
- BigQuery: Transition matrix queries (SQL window functions)
- Vertex AI: Predictive modeling (which workers likely to move sectors in next 12 months?)
- Data Studio: Sankey diagrams showing worker flow between sectors

---

## PRODUCT 2: Training-to-Outcome Linkage System
### Problem It Solves
ILO trains workers but can't answer: "Did they actually use what they learned? Did earnings increase? Did they formalize?"

### The Product (What It Is)
**Name:** "Impact Tracking Platform"
- **Core:** Link individual worker across ENTIRE ILO journey (pre-training → training attended → post-training outcomes)
- **Features:**
  1. Unified worker identifier (same person tracked across all ILO projects)
  2. Training registry (which trainings, which dates, which topics, which outcomes)
  3. Outcome measurement (follow-up surveys at 3, 6, 12 months post-training)
  4. Attribution analysis (compare trained vs. untrained workers; measure true impact)

### Known Techniques to Build This

#### Technique 1: Longitudinal Cohort Design (Gold Standard in Development)
**What it is:**
- Divide workers into 2 groups: Treatment (gets training) + Control (doesn't); track both over time

**Why it works:**
- ONLY way to prove causation (training → outcome change)
- Current ILO approach: "We trained 1,000 workers; 200 now earn more" (could be random economic growth, not training)
- Better approach: "We trained 500 workers; control group of 500 similar workers didn't get training. Trained group earned 18% more after 1 year; control group earned 2%"

**Process:**
```
Month 1-2: Baseline
├─ Recruit 2,000 workers interested in training
├─ Randomly assign 1,000 to treatment (get training NOW), 1,000 to control (get training later)
├─ Survey both groups on: current income, education, skills, aspirations
└─ Verify groups are balanced (same demographics, baseline earnings, etc.)

Month 3-9: Intervention
├─ Treatment group: Attend training (5 days + 3-month follow-on coaching)
├─ Control group: Business as usual (waiting list)
└─ Track attendance (who actually completed?)

Month 10, 15, 21: Follow-up Surveys
├─ Re-survey BOTH groups on: current income, job type, skills used, confidence, business formalization
├─ Compare outcomes (Did training group improve more than control?)
└─ Analyze heterogeneity (Did it work better for women? For young workers? For specific sectors?)
```

**Why this is hard in practice:**
- Requires **long-term tracking** of same workers (phone numbers change, people move)
- Requires **honest income data** (workers often underreport or exaggerate)
- Requires **control group patience** (they have to wait to get training; creates ethical tension)

**Tech solution to make it work:**
```
Challenge 1: Tracking workers over 2 years
→ Solution: SMS surveys (send questions via WhatsApp; worker replies with income)
→ Tech: Twilio (SMS), Zapier (auto-parse replies), Google Sheets (aggregate)

Challenge 2: Reducing response attrition (lose 30% of respondents by year 2)
→ Solution: Incentivize (small cash rewards for survey completion); multiple contact methods
→ Tech: Firebase (mobile app), SMS, phone calls; payment via bKash/Nagad

Challenge 3: Income validation (can't trust what workers self-report)
→ Solution: Triangulation (ask about job type + hours + wage rate; cross-check)
→ Tech: Logic checks in survey (if says "garment factory worker" but reports 50K income, flag as possible error)

Challenge 4: Control group feels left out
→ Solution: Ethical design (offer control group training AFTER study ends)
→ Tech: Logistics app to manage training waitlist; automatic scheduling
```

**Tech Stack (GCP + SMS):**
- **Baseline survey:** Google Forms (standardized questions)
- **Longitudinal tracking:** Firebase + Twilio (SMS surveys at 3, 6, 12 months)
- **Data validation:** BigQuery ML (anomaly detection on income data)
- **Analysis:** BigQuery (comparison: treatment vs. control earnings; impact = difference)
- **Visualization:** Looker (impact dashboard: earnings by training type, sector, gender)

**Implementation Process:**
```
Phase 1: Study Design (Month 1)
├─ Partner with 3 ILO training programs
├─ Recruit 2,000 workers (1,000 treatment, 1,000 control)
├─ Baseline survey (online + phone)
└─ Verify randomization (groups balanced)

Phase 2: Training Delivery + Tracking (Months 2-12)
├─ Treatment group starts training
├─ Automated SMS follow-ups (attendance reminders, post-training surveys)
├─ Control group stays on waitlist
└─ Monthly data quality checks (any obvious errors?)

Phase 3: Follow-up Surveys (Months 10, 15, 21)
├─ Re-survey both groups via SMS (lower cost than phone interviews)
├─ Validate income data (triangulation checks)
├─ Clean data (handle non-responses, inconsistencies)
└─ Initial analysis (treatment group earnings ↑ vs. control?)

Phase 4: Final Analysis + Publication (Month 24)
├─ Statistical analysis (regression: impact = treatment effect on earnings)
├─ Subgroup analysis (did it work for women? Young workers? Specific sectors?)
├─ Cost-benefit (cost per person = $X; earnings gain per person = $Y; ROI = Y/X)
└─ Briefing to ILO leadership + partners
```

#### Technique 2: Rapid Cycle Testing (Agile Impact Measurement)
**What it is:**
- Instead of waiting 2 years for results, test small pilots every 3 months; iterate quickly

**Why it works:**
- ILO's current approach: "We'll train 1,000 people; measure impact in 2 years" (slow + risky)
- Better approach: "We'll train 50 people; measure at 3 months; learn what worked; train 200 more with tweaks; measure again"

**Process:**
```
Cycle 1 (Months 1-3): Pilot
├─ Train 50 workers on Module A (e.g., "entrepreneurship for informal workers")
├─ Collect rapid feedback (weekly check-ins; SMS surveys)
├─ Measure: Did they start a business? Are they earning more?
└─ Decision: Keep as-is, tweak, or redesign?

Cycle 2 (Months 4-6): Scale + Iterate
├─ Train 200 workers on Module A (with tweaks from Cycle 1)
├─ Add Module B to same cohort (e.g., "financial management")
├─ Measure again
└─ Decision: Which modules work? Which don't? Which combinations?

Cycle 3 (Months 7-9): Optimize
├─ Train 500 workers on best-performing module combination
├─ Measure at 3, 6, 9 months
└─ Build business case: "This approach generates X% ROI"
```

**Tech Stack:**
- **Weekly pulse surveys:** Google Forms (1–3 quick questions)
- **Rapid analysis:** BigQuery (automated dashboards; results ready by Friday)
- **Decision support:** Data Studio (compare Cycle 1 vs. Cycle 2 outcomes side-by-side)

---

## PRODUCT 3: Campaign Effectiveness Dashboard
### Problem It Solves
ILO runs awareness campaigns (formal business registration, worker rights, safe migration) but can't measure: Did it reach people? Did they change behavior?

### The Product (What It Is)
**Name:** "Campaign Analytics Platform"
- **Core:** Track campaign exposure → awareness → behavior change across different sectors/geographies
- **Features:**
  1. Reach tracking (how many people saw the campaign?)
  2. Engagement metrics (did they click? Share? Comment?)
  3. Behavior change indicators (did they formalize? Report unsafe conditions?)
  4. ROI analysis (cost per person reached, cost per behavior change)

### Known Techniques to Build This

#### Technique 1: Digital Tracking Pixels + Custom Surveys
**What it is:**
- Use Google Ads / Facebook Ads to show campaign materials; track clicks
- Pair with surveys to verify awareness + behavior change

**Why it works:**
- Digital campaigns are trackable (you see exactly who clicked)
- Surveys verify actual behavior (not just clicks; did they really formalize?)

**Process:**
```
Step 1: Campaign Design (Week 1-2)
├─ Create ads in Bengali (text, images, video)
├─ Multiple versions (different messaging for different sectors)
├─ Configure tracking pixels (Google Ads, Facebook Ads)
└─ Set up landing pages (Formalization quiz, Worker rights checklist)

Step 2: Campaign Launch (Week 3-6)
├─ Run digital ads for 4 weeks (target: construction workers, garment workers, informal businesses)
├─ Track metrics (impressions, clicks, video views, landing page visits)
└─ Adjust targeting in real-time (if construction ads underperforming, increase budget to business owner ads)

Step 3: Survey-Based Verification (Week 7-8)
├─ SMS survey to 5,000 random workers in target areas
├─ Ask: "Have you heard about worker rights? Formal registration? Safe migration?"
├─ Ask: "Have you acted on any of this?"
└─ Compare: Who clicked ads? Who saw ads but didn't click? Who didn't see ads?

Step 4: Analysis (Week 9)
├─ Reach: X% of target audience saw campaign
├─ Engagement: Y% clicked through
├─ Behavior change: Z% of engaged people took action (registered, reported issue, etc.)
├─ ROI: Cost per person reached = $A; Cost per behavior change = $B
└─ Segmental breakdown: Which sector responded best? Which messaging?
```

**Tech Stack (Google Ads + Surveys):**
- **Campaign deployment:** Google Ads (text, image, video ads)
- **Tracking:** Google Analytics + UTM parameters (trace every click)
- **Landing pages:** Google Sites or Carrd (simple, trackable, forms)
- **Surveys:** Google Forms + SMS (Twilio; send survey links via text)
- **Data integration:** Zapier (Google Ads data → BigQuery; Form responses → BigQuery)
- **Analysis:** BigQuery (SQL queries: "Of people who clicked on ad X, what % formalized?")
- **Visualization:** Looker (dashboard: reach, engagement, behavior change, ROI by sector)

**Implementation Process:**
```
Phase 1: Pilot Campaign (2 weeks)
├─ Design 3 ad variants (different messaging)
├─ Target: 100K impressions
├─ Budget: ~$500 (cheap; testing phase)
├─ Measure: engagement rate, click-through rate
└─ Decision: Which messaging resonates?

Phase 2: Full Campaign (4 weeks)
├─ Launch winning variant from Phase 1
├─ Scale budget based on engagement metrics
├─ Run surveys (2 weeks post-campaign end)
├─ Measure: reach, engagement, behavior change
└─ Initial ROI: cost per formalization, cost per awareness

Phase 3: Optimization + Reporting (2 weeks)
├─ Analyze subgroup performance (which sectors most receptive?)
├─ Compile findings (key messages, effective channels, ROI by segment)
├─ Brief ILO leadership
└─ Recommend next campaign
```

#### Technique 2: Behavioral Economics Nudges
**What it is:**
- Use behavioral science (social proof, loss aversion, defaults) to increase campaign effectiveness

**Examples:**
- **Social proof:** "500+ businesses in your area have formalized. You could be next."
- **Loss aversion:** "Workers without formal registration lose 30% in pension benefits. Formalize today."
- **Defaults:** Send registration link directly; make it the easy action

**Why it works:**
- Traditional campaigns: "Formalization is good for you." → 5% uptake
- Behavioral nudges: "Your neighbor formalized. You could too." + "Easy 5-minute online registration" → 15% uptake

**Process:**
```
Test 1: Social Proof Message
├─ Ad A: "Formalization is good."
├─ Ad B: "500+ businesses in your area have formalized. You could be next."
├─ Run both; compare behavior change rates

Test 2: Defaults
├─ Ad A: "Consider filling out the registration form."
├─ Ad B: "We've pre-filled your info. Click here to confirm."
├─ Compare completion rates

Test 3: Frequency
├─ Cohort A: 1 ad exposure
├─ Cohort B: 3 ad exposures (spaced 1 week apart)
├─ Compare awareness + behavior change
```

**Tech to implement:**
- **Dynamic messaging:** Google Ads dynamic creative optimization (system tests different messages automatically)
- **A/B testing:** Google Optimize (serve different messages to different users; track outcomes)
- **Personalization:** Firebase (if user is from construction sector, show construction-specific messages)

---

---

# UNDP SOLUTIONS

## PRODUCT 1: Beneficiary Identity Verification System
### Problem It Solves
UNDP sends money to beneficiaries but can't verify: Is this really the person? Are they in 2 programmes simultaneously (duplicate payment)? Are they eligible?

### The Product (What It Is)
**Name:** "Beneficiary Verification Platform"
- **Core:** Biometric + identity matching system; prevents duplicate registrations + fraud
- **Features:**
  1. Fingerprint capture (unique identifier for each beneficiary)
  2. Photo + NID matching (verify identity)
  3. Duplicate detection (is this person already in another UNDP programme?)
  4. Eligibility verification (does this person meet criteria? Update status in real-time)

### Known Techniques to Build This

#### Technique 1: Biometric Deduplication (Proven at Scale)
**What it is:**
- Capture fingerprints or iris scans at beneficiary registration
- Compare against existing database to detect duplicates

**Why it works:**
- Bangladesh has 50M+ NID holders; many share same name/DOB
- Biometric is unique (even identical twins have different fingerprints)
- Eliminates duplicate registrations + fraud

**Real-world example:**
- India's UIDAI (Unique Identification Authority) uses fingerprints; has 1B+ citizens with no duplicates
- Cost: ~$1 per registration (fingerprint capture + database lookup)

**Process:**
```
Step 1: Hardware Setup (Week 1)
├─ Deploy fingerprint readers to 20 registration sites (UNDP field offices, training centers)
├─ Test connectivity (readers sync to cloud)
└─ Train staff on fingerprint capture technique

Step 2: Database Baseline (Weeks 2-4)
├─ Enroll all existing UNDP beneficiaries (100K+ people)
├─ Capture fingerprints (10-finger scan per person)
├─ Upload to central database (Google Cloud Biometric API OR AWS Rekognition)
└─ Build searchable index

Step 3: New Registrations (Ongoing)
├─ New beneficiary arrives
├─ Capture 4 fingerprints (thumbs + index fingers; faster than 10-finger)
├─ System searches database (1-2 second match)
├─ Result: "New person" OR "Duplicate found: Already registered as [Name]"
└─ If duplicate: Merge records; flag for investigation

Step 4: Ongoing Monitoring (Weekly)
├─ Check for cross-programme duplicates (same person in IOM + UNDP + UNHCR)
├─ Alert finance team (prevent duplicate payments)
└─ Investigation log (which duplicates? Why? Any fraud patterns?)
```

**Tech Stack:**
- **Biometric capture:** Mobile app (Android) with fingerprint SDK (IDEMIA, NEC, or open-source NIST IDENT)
- **Cloud matching:** Google Cloud Biometric API (compares fingerprint against database; <1% false positive rate)
- **Storage:** BigQuery (fingerprint hashes; never store raw fingerprints)
- **Alerts:** Cloud Tasks + Gmail (if duplicate found, alert programme manager)

**Implementation Process:**
```
Phase 1: Pilot (4 weeks)
├─ Deploy fingerprint readers to 5 sites
├─ Register 5,000 beneficiaries
├─ Test duplicate detection accuracy
├─ Manual verification of flagged duplicates
└─ Refine process

Phase 2: Scale (8 weeks)
├─ Deploy to 20 sites nationwide
├─ Register 100K beneficiaries
├─ Cross-check with other organizations (IOM, UNHCR) for inter-org duplicates
└─ Training for registration staff

Phase 3: Integration (4 weeks)
├─ Link to payment system (verify beneficiary before disbursement)
├─ Daily reconciliation reports
├─ Dashboard for compliance team
└─ Handoff to UNDP team
```

#### Technique 2: NID + Photo Matching (Faster Alternative)
**What it is:**
- Use Bangladesh's National ID + photo database
- Match beneficiary photo against NID database

**Why it works:**
- Bangladesh has digitized NID database (~140M people)
- Photo matching is faster than fingerprint (2–3 seconds vs. 1–2 seconds, but easier to scale)
- Less privacy concerns (photos already public on NID)

**Process:**
```
Step 1: Beneficiary Registration
├─ Collect: NID number, photo (selfie)
└─ System calls Bangladesh National ID API

Step 2: NID Verification
├─ Look up NID in government database
├─ Retrieve official NID photo
├─ Compare beneficiary selfie to NID photo (Microsoft Face API OR Google Vision AI)
├─ Result: "Match" (>95% confidence) OR "No match" (requires manual review)

Step 3: Duplicate Detection
├─ Check UNDP database: Is this NID already registered?
├─ If yes: "Duplicate found"
└─ If no: "New person"
```

**Tech Stack:**
- **Photo capture:** Mobile app (built with React Native or Flutter)
- **NID API:** Bangladesh government NID lookup service (requires government partnership)
- **Face matching:** Google Cloud Vision API OR Microsoft Azure Face API
- **Duplicate checking:** BigQuery (NID table; fast lookup)

**Advantage over fingerprints:**
- Faster to implement (no hardware deployment)
- Lower cost (~$0.20 per registration vs. $1 for biometric)
- Can use existing mobile devices (no fingerprint readers)

---

## PRODUCT 2: Real-Time Activity Tracking Dashboard
### Problem It Solves
UNDP runs training + disbursement programmes but has no real-time visibility: How many trainings today? How much disbursed? Any anomalies?

### The Product (What It Is)
**Name:** "Operations Intelligence Dashboard"
- **Core:** Live, unified view of all UNDP activities (trainings, disbursements, attendance, incidents)
- **Features:**
  1. Daily activity log (today's trainings, attendees, instructors)
  2. Real-time disbursement tracking (who got paid, how much, to which account)
  3. Anomaly alerts (attendance spike? Missing trainer? Payment to invalid account?)
  4. Geographic heat map (activity concentration by district)

### Known Techniques to Build This

#### Technique 1: Event-Driven Architecture (Streaming Data)
**What it is:**
- Every activity (training started, person marked present, payment sent) is an EVENT
- Events stream to dashboard in real-time (not batch/daily updates)

**Why it works:**
- Current approach: Activity reports submitted end-of-day or end-of-week → lag
- Better approach: Activity logged in real-time → dashboard updates instantly
- Enables fast response (if attendance low at noon, can launch rescue intervention by afternoon)

**Process:**
```
Step 1: Data Collection (Forms in the Field)
├─ Training starts: Form filled out (trainer name, location, expected attendees)
├─ Attendance: Trainer marks present/absent as people arrive (app, not paper)
├─ Disbursement: Payment officer marks "Fatima received 5,000 BDT to bKash account X"
└─ Incident: Any problem logged (trainer sick, power outage, etc.)

Step 2: Event Streaming
├─ Each action (attendance mark, payment, incident) = 1 event
├─ Event sent to message queue (Google Pub/Sub OR AWS Kinesis)
├─ Real-time subscribers listen for events
└─ Events trigger: Dashboard update, alert checks, logging

Step 3: Aggregation
├─ Events aggregated into facts (Total attendees today = 4,500; Total paid = 22.5M BDT)
├─ Facts stored in real-time database (Firebase OR DynamoDB)
└─ Dashboard reads facts (queries lightning-fast because pre-aggregated)

Step 4: Anomaly Detection
├─ Attendance anomaly: "Expected 50 attendees; only 15 showed up" → alert
├─ Payment anomaly: "Payment to account not in beneficiary database" → alert
├─ Trainer anomaly: "Trainer marked 100 attendees in 1 hour; usually 20-30" → suspicious
└─ Geographic anomaly: "All trainees from one district today; usually mixed" → investigate
```

**Tech Stack (GCP):**
- **Field forms:** Google Forms (with offline mode) OR Firebase + mobile app
- **Event streaming:** Google Cloud Pub/Sub (publish-subscribe; real-time)
- **Event processing:** Google Cloud Dataflow (Apache Beam; transform raw events into facts)
- **Real-time storage:** Firebase Realtime Database OR BigQuery streaming inserts
- **Dashboard:** Google Data Studio (pulls from Firebase/BigQuery; auto-refreshes every 30 seconds)
- **Alerts:** Cloud Functions (lambda-like; trigger on anomaly events; send email/SMS)

**Implementation Process:**
```
Phase 1: MVP (2 weeks)
├─ Build forms for training start + attendance + disbursement
├─ Set up Pub/Sub + Dataflow (simple processing pipeline)
├─ Build Data Studio dashboard (daily total: trainings, attendees, payments)
├─ Test with 1 training centre (real data)
└─ Demo to UNDP

Phase 2: Anomaly Detection (1 week)
├─ Add rules (if attendance < 70% of expected, alert)
├─ Test with real data (identify false positives)
└─ Tune thresholds

Phase 3: Scale (2 weeks)
├─ Deploy forms + app to 20 training centers
├─ Test streaming (peak load: 500+ events/minute during training hours)
├─ Add geographic heat map
└─ Integration with finance system (verify payments)

Phase 4: Dashboard Refinement (1 week)
├─ Add drill-down (click on district → see center-by-center data)
├─ Add trend lines (trainings/day over 30 days)
├─ Custom KPI tiles (training completion rate, payment accuracy, etc.)
└─ Hand off to UNDP operations team
```

#### Technique 2: Mobile-First Data Collection (Low-Bandwidth)
**What it is:**
- Instead of forms, use mobile apps that work offline; sync when connectivity available

**Why it works:**
- Bangladesh has spotty internet (especially in refugee camps, rural areas)
- Offline-first app: Works even with no internet; syncs automatically when connected
- Faster data entry (native app, not browser form)

**Process:**
```
Development:
├─ Build Android app (React Native or Flutter for iOS + Android)
├─ Features: attendance marking, incident logging, offline data storage
├─ Data syncs to cloud when internet available
└─ App works fine with no internet (queues data locally)

Deployment:
├─ Install app on tablets/phones at 20 training centers
├─ Train staff (2 minutes to learn)
└─ Data starts flowing automatically

Data Flow:
├─ Training center (no internet): Staff marks 50 people present on app
├─ App stores locally on phone
├─ Evening (internet available): Auto-sync; data uploads to cloud
└─ Dashboard updates with day-old data (acceptable lag)
```

**Tech Stack:**
- **Mobile app:** React Native (iOS + Android from one codebase)
- **Offline storage:** SQLite (local database on phone)
- **Cloud sync:** Firebase Realtime Database (auto-sync; built-in conflict resolution)
- **Dashboard:** Data Studio (reads from Firebase)

---

## PRODUCT 3: Outcome Measurement System
### Problem It Solves
UNDP runs programmes (job training, social protection, climate adaptation) but can't answer: Did lives improve? For whom? Which interventions worked?

### The Product (What It Is)
**Name:** "Impact Intelligence Platform"
- **Core:** Track beneficiaries pre- to post-programme; measure changes in income, employment, wellbeing
- **Features:**
  1. Longitudinal tracking (same person surveyed before, after, 6-month follow-up)
  2. Outcome metrics (income, employment, skills, wellbeing, climate resilience)
  3. Comparison (programme beneficiaries vs. similar non-beneficiaries; measured impact)
  4. Subgroup analysis (did it work for women? Youth? Different regions?)

### Known Techniques to Build This

#### Technique 1: Quasi-Experimental Design (Practical Gold Standard)
**What it is:**
- Compare programme beneficiaries to similar non-beneficiaries
- Not perfect (can't randomly assign people to not-get-training), but close

**Why it works:**
- True experiments impossible (ethical: can't deny services to people)
- Quasi-experimental: Find similar people; compare outcomes
- Example: "Trainees vs. non-trainees with similar baseline characteristics"

**Process:**
```
Step 1: Baseline Survey (Month 1-2)
├─ Survey 3,000 programme participants (income, skills, employment, wellbeing)
├─ Identify 3,000 comparison group (similar people NOT in programme; matched on demographics + baseline income)
└─ Verify groups are balanced (same average income, education, age, gender)

Step 2: Programme Delivery (Months 3-12)
├─ Programme group: Receives training + support
├─ Comparison group: Business as usual
└─ Track programme dosage (who attended how many sessions?)

Step 3: Endline Survey (Month 18)
├─ Re-survey BOTH groups (income, employment, skills, wellbeing)
├─ Ask about activities post-baseline (did they get jobs? Start businesses? Get promoted?)
└─ Compare: Programme group outcome minus Comparison group outcome = impact

Step 4: Analysis (Month 19-20)
├─ Average impact (across all participants)
├─ Heterogeneous impact (did it work for women? Young people? Poor people?)
├─ Cost-effectiveness (cost per person = $X; income gain per person = $Y; ROI = Y/X)
└─ Briefing to UNDP leadership
```

**Why quasi-experimental works:**
- True RCT: "We randomly chose who gets training" (best, but ethically hard)
- Quasi-experimental: "We matched trainees with similar non-trainees" (nearly as good, easier)
- Before-after: "Trainees earned more after training" (could be random growth; no control)

**Tech Stack:**
- **Survey design:** Google Forms (or Qualtrics for complex branching)
- **Survey distribution:** Twilio (SMS to beneficiaries with survey link) + local enumerators (for people without phones)
- **Data collection:** Firebase (responses stored in real-time)
- **Matching:** BigQuery ML (statistical matching; find comparison groups similar to trainees)
- **Analysis:** BigQuery SQL (regression: impact = outcome difference) + R (complex stats)
- **Visualization:** Looker (outcomes by subgroup; impact dashboard)

**Implementation Process:**
```
Phase 1: Study Design + Baseline (2 months)
├─ Partner with 3 UNDP programmes
├─ Design baseline survey (income, employment, skills, wellbeing)
├─ Survey 3,000 programme participants + 3,000 comparison group
├─ Matching process (find similar comparison individuals)
└─ Baseline report (groups are balanced)

Phase 2: Programme Delivery (12 months)
├─ Programmes deliver training/services
├─ Monthly data collection (track attendance, activities)
└─ Mid-year check (any issues? Any early wins?)

Phase 3: Endline Survey + Analysis (3 months)
├─ Re-survey both groups (endline)
├─ Validate data (income patterns, employment status)
├─ Statistical analysis (calculate impact; generate findings)
└─ Subgroup analysis (impact for women, young people, different regions)

Phase 4: Synthesis + Reporting (1 month)
├─ Generate dashboards (impact by programme, region, subgroup)
├─ Cost-benefit analysis (ROI per person)
├─ Recommendations (which programmes most effective? Scaling opportunities?)
└─ Briefing to UNDP leadership
```

#### Technique 2: Rapid Feedback Surveys (Quick Wins)
**What it is:**
- Instead of waiting 18 months, collect rapid feedback every 3 months
- Short surveys (5 questions, 2 minutes)
- Show quick wins + allow mid-course corrections

**Why it works:**
- Traditional: "Deliver 18-month programme; measure impact at end" (slow; inflexible)
- Better: "Measure every 3 months; adjust approach based on results"

**Process:**
```
Month 3: Quick Feedback
├─ SMS survey to 1,000 trainees: "Have you used any skills from training? Yes/No. Any income change? Higher/Same/Lower."
├─ 50% response rate (500 responses)
├─ Results: "70% used skills; 45% report income increase"
└─ Decision: Continue or adjust?

Month 6: Deeper Follow-up
├─ Phone interviews with 200 trainees
├─ Ask: What skills used? What job did you get? How much are you earning?
├─ Identify common success patterns (e.g., "Trainees who got formal jobs earned 25% more")
└─ Decision: Adjust training to emphasize job-search skills

Month 9: Scaling Decision
├─ Based on Month 3 + Month 6 results, decide: Scale to 10,000 trainees or pivot?
├─ Compare: Cost = $X per person; Impact (income gain) = $Y; ROI = Y/X
└─ If ROI positive, scale; if not, redesign training

Month 12-18: Endline Study
├─ Full study of scaled programme
├─ Compare to baseline + control group
└─ Final impact numbers
```

**Tech Stack:**
- **Rapid surveys:** Google Forms + SMS (Twilio)
- **Data analysis:** BigQuery (quick SQL queries; results by end of day)
- **Visualization:** Looker (dashboard updated weekly)

---

---

## SUMMARY TABLE: 6 Products, Techniques, Tech Stacks

| Product | Org | Problem | Technique | Primary Tech | Timeline | Cost |
|---|---|---|---|---|---|---|
| **Worker Registry** | ILO | Can't segment hidden workers | Multi-source data integration + Occupational networks | GCP BigQuery + Looker | 4-6 months | $50-80K |
| **Training-to-Outcome** | ILO | Can't measure training impact | Longitudinal cohort design + Rapid cycle testing | GCP BigQuery + Firebase + SMS | 2 years (ongoing testing) | $100-150K |
| **Campaign Analytics** | ILO | Can't measure awareness campaigns | Digital tracking + Behavioral nudges | Google Ads + Google Analytics | 2-3 months | $30-50K |
| **Beneficiary Verification** | UNDP | Can't prevent duplicate payments | Biometric deduplication + NID matching | Google Cloud Biometric API + Mobile App | 2-3 months | $40-60K |
| **Real-Time Operations** | UNDP | No visibility into daily activities | Event-driven streaming + Mobile-first collection | GCP Pub/Sub + Firebase + Data Studio | 1-2 months | $30-50K |
| **Outcome Measurement** | UNDP | Can't measure programme impact | Quasi-experimental design + Rapid feedback | BigQuery + SMS surveys + Looker | 18-24 months | $150-200K |

---

## QUICK-WINS (What to Pitch First)

**Best immediate opportunities:**

1. **Beneficiary Verification (UNDP):** 2-3 months to deliver; prevents fraud; immediate ROI (every duplicate prevented = $5K saved)

2. **Real-Time Operations (UNDP):** 1-2 months; solves operational visibility; no complex analysis needed

3. **Campaign Analytics (ILO):** 2-3 months; uses Google Ads (already available); quick proof of concept

4. **Worker Registry (ILO):** 4-6 months; requires data integration; but massive impact once live

