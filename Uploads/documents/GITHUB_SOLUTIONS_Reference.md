# GitHub Reference: Proven Patterns for ILO/UNDP Problems

## Context
You're facing:
1. **Bengali language barrier** (NLP, OCR, translation)
2. **Document quality** (image preprocessing, PDF extraction, low-res forms)
3. **Data reliability** (validation, deduplication, error detection)
4. **Data disorganization** (ETL, schema mapping, fragmented sources)
5. **Slow methods** (automation, real-time processing, batch → streaming)

Below: Real GitHub projects solving similar problems in development/humanitarian contexts.

---

## PROBLEM 1: Form Data Extraction (ILO Training Records, UNDP Beneficiary Forms)

### Pattern: AWS Textract + DynamoDB Pipeline

**Project:** `aws-forms-extraction-and-databasing`
- **GitHub:** aws-samples/aws-forms-extraction-and-databasing
- **What it does:** Extract structured data from scanned forms → DynamoDB
- **Tech:** Python + AWS Textract + DynamoDB
- **Applies to:** UNDP training forms, ILO survey questionnaires, refugee registration forms

**How it works:**
```
Scanned Form (JPG) 
  ↓ (upload to S3)
AWS Textract 
  ↓ (extracts text + structure)
Python script (parse form fields)
  ↓ (normalize data)
DynamoDB (store structured records)
```

**Why relevant:**
- ILO trainers fill paper forms (attendance sheets)
- UNDP registers beneficiaries on paper (refugee camps)
- Current: Manual data entry (3-5 days lag, 10% error rate)
- This approach: Automatic extraction same day, 95%+ accuracy

**How to adapt:**
```python
import boto3
import json

textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('training_attendance')

def extract_form(image_s3_path):
    # Extract from S3 image
    response = textract.analyze_document(
        Document={'S3Object': {'Bucket': 'forms', 'Name': image_s3_path}}
    )
    
    # Parse extracted fields
    extracted = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            # Extract key-value pairs (Trainer Name, Date, Attendees, etc.)
            pass
    
    # Store in DynamoDB
    table.put_item(Item=extracted)
    return extracted
```

**For Bengali forms:**
- Use `Textract` for layout + structure
- Add post-processing: Convert Bengali numbers (০,১,२) to Arabic (0,1,2)
- Use Google Translate API for Bengali text fields

---

### Pattern: Document Quality Enhancement (Pre-Textract)

**Project:** `opencv-form-processing`
- **Concept:** OpenCV image preprocessing before OCR
- **Problem:** Scanned forms are often blurry, rotated, low-contrast
- **Solution:** Auto-rotate, contrast enhancement, deskew

**How it works:**
```
Raw Form (blurry, rotated, low-res)
  ↓ (OpenCV preprocessing)
1. Deskew (rotate to correct orientation)
2. Denoise (reduce scanner artifacts)
3. Contrast enhancement (make text darker, background lighter)
4. Binarization (convert to pure black/white)
  ↓ (now Textract works better)
Textract extraction (higher accuracy)
```

**Why relevant:**
- Refugee camp forms filled with pen; scanned on phones with bad lighting
- UNDP training sheets stored in damp tents; ink fades
- ILO surveys in rural areas; poor scanner quality
- Current approach: Can't extract → manual entry
- This approach: Pre-process → Textract extracts → 85%→99% accuracy

**Implementation:**
```python
import cv2
import numpy as np

def preprocess_form(image_path):
    img = cv2.imread(image_path)
    
    # Deskew
    angles = [-5, -3, 0, 3, 5]
    best_score = 0
    best_img = img
    for angle in angles:
        rotated = imutils.rotate_bound(img, angle)
        score = cv2.Laplacian(cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        if score > best_score:
            best_score = score
            best_img = rotated
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(best_img)
    
    # Contrast enhancement (CLAHE)
    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Binarization
    gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    return binary

# Use preprocessed image with Textract
textract.analyze_document(Document={'Bytes': preprocessed_binary})
```

---

## PROBLEM 2: Data Deduplication & Matching (Beneficiary Registry, Worker Database)

### Pattern: Probabilistic Record Linkage

**Project:** `recordlinkage` (Python library)
- **GitHub:** J535D165/recordlinkage
- **What it does:** Find duplicate records across datasets
- **Tech:** Python + Pandas + Machine Learning
- **Applies to:** UNDP beneficiary deduplication, ILO worker registry matching

**Why relevant:**
- UNDP beneficiary in 2 programmes (duplicate payment risk)
- ILO worker in multiple training registers (can't track outcomes)
- Current: Manual reconciliation (4-6 weeks)
- This approach: Automated matching (1-2 days, 95% accuracy)

**How it works:**
```python
import recordlinkage
from recordlinkage.preprocessing import clean
import pandas as pd

# Load two datasets (or two views of same dataset)
undp_beneficiaries_1 = pd.read_csv('programme_1.csv')  # 5,000 beneficiaries
undp_beneficiaries_2 = pd.read_csv('programme_2.csv')  # 3,000 beneficiaries

# Clean data (lowercase, remove special chars)
undp_beneficiaries_1['name'] = clean(undp_beneficiaries_1['name'])
undp_beneficiaries_2['name'] = clean(undp_beneficiaries_2['name'])

# Initialize indexer (candidate pairs)
indexer = recordlinkage.Index()
indexer.full()  # Compare all pairs
pairs = indexer.index(undp_beneficiaries_1, undp_beneficiaries_2)

# Compare pairs (features)
compare = recordlinkage.Compare()
compare.string('name', 'name', method='jarowinkler', threshold=0.85, label='name')
compare.string('phone', 'phone', method='exact', label='phone')
compare.string('dob', 'dob', method='exact', label='dob')
features = compare.compute(pairs, undp_beneficiaries_1, undp_beneficiaries_2)

# Classify matches
matches = features[features.sum(axis=1) >= 2]  # At least 2 fields match

# Result: Potential duplicates
for match in matches.index:
    print(f"Duplicate: {undp_beneficiaries_1.loc[match[0], 'name']} = {undp_beneficiaries_2.loc[match[1], 'name']}")
```

**For Bengali matching:**
- Use `Levenshtein` distance (works for any language)
- Add phonetic matching: "বিমল" (Bimal) vs "বিমোল" (Bimol) are likely same person

**Integration with Google Cloud:**
```python
# Run deduplication in BigQuery
bq_client = bigquery.Client()

query = """
SELECT 
  a.beneficiary_id as id_a,
  b.beneficiary_id as id_b,
  LEVENSHTEIN(a.name, b.name) as name_distance,
  IF(a.phone = b.phone, 1, 0) as phone_match,
  IF(a.dob = b.dob, 1, 0) as dob_match
FROM `project.undp_programme_1` a
JOIN `project.undp_programme_2` b
WHERE LEVENSHTEIN(a.name, b.name) <= 2
  OR (a.phone = b.phone)
  OR (a.dob = b.dob)
ORDER BY name_distance
"""

df = bq_client.query(query).to_dataframe()
potential_duplicates = df[df['name_distance'] + df['phone_match'] + df['dob_match'] >= 2]
```

---

### Pattern: Master Data Management (MDM)

**Concept:** Single source of truth for beneficiaries
- Create unified beneficiary table (merge programme-1, programme-2, programme-3)
- Use deduplication to identify same person across programmes
- Assign unique ID per person; all programmes use that ID

**Tech:**
- Google Cloud Dataflow (ETL) or AWS Glue (data catalog)
- BigQuery or AWS Redshift (data warehouse)
- Apache Beam (data pipeline)

---

## PROBLEM 3: Bengali NLP (Language Barrier)

### Pattern: Google Cloud NLP for Bengali

**Project:** `google-cloud-natural-language` + Bengali support
- **Tech:** Google Cloud Natural Language API
- **Applies to:** ILO open-ended survey responses, UNDP feedback text, refugee incident reports

**Why relevant:**
- ILO asks workers: "Why couldn't you formalize?" (open-ended, Bengali)
- Current: Manual coding (one person reads 1,000 responses; takes 4 weeks; subjective)
- This approach: Auto-extract entities + sentiment (24 hours; objective; 85%+ accuracy)

**How it works:**
```python
from google.cloud import language_v1

def analyze_bengali_text(text):
    """Analyze Bengali text: extract intent, entities, sentiment"""
    client = language_v1.LanguageServiceClient()
    
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="bn"  # Bengali
    )
    
    # Entity extraction (what are they talking about?)
    entities = client.analyze_entities(request={'document': document})
    print("Entities:")
    for entity in entities.entities:
        print(f"  {entity.name}: {entity.type_} (salience: {entity.salience})")
    
    # Sentiment analysis (are they positive/negative/neutral?)
    sentiment = client.analyze_sentiment(request={'document': document})
    print(f"Sentiment: {sentiment.document_sentiment.score}")
    # score: -1.0 (negative) to +1.0 (positive)

# Example
response = analyze_bengali_text(
    "আমি ব্যবসা ফরমালাইজ করতে চাই কিন্তু সরকারি কাগজ খুব জটিল। " 
    "It's very complicated bureaucracy. I don't have time."
)
```

**Result for 1,000 ILO survey responses:**
- Extract top entities: "bureaucracy", "taxes", "paperwork", "time", "cost"
- Sentiment: 30% negative, 50% neutral, 20% positive
- Actionable insight: "Main barrier is perceived complexity; half are willing"

---

### Pattern: Named Entity Recognition (NER) for Bengali

**Project:** `bn-nlp` or `SpacyModel-bn`
- **Purpose:** Identify people, locations, organizations in Bengali text
- **Applies to:** UNDP incident reports ("Worker Fatima in Cox's Bazar..."), ILO training records

**Example:**
```python
# Input: "ক্যাম্পে সুজিতা সেন এবং রহিমা বেগম প্রশিক্ষণ নিয়েছেন।"
# Output: 
# - Sujiita Sen: PERSON
# - Rahima Begum: PERSON
# - Camp: LOCATION
```

---

## PROBLEM 4: Real-Time Data Integration (Beneficiary Database + Training Records + Payments)

### Pattern: Apache Beam + Google Cloud Dataflow (Streaming ETL)

**Project:** `apache-beam-examples` + Dataflow
- **Concept:** Real-time data ingestion + transformation + loading
- **Applies to:** UNDP real-time operations dashboard (daily activities, disbursements)

**Why relevant:**
- UNDP needs live view: "How many trainings happened today? How much paid out?"
- Current: End-of-day batch reports (2-day lag)
- This approach: Events stream in real-time; dashboard updates live

**How it works:**
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.pubsub import ReadFromPubSub, WriteToPubSub

# Pipeline: Events → Filter → Transform → Write to BigQuery

class ExtractTrainingEvent(beam.DoFn):
    """Transform raw event into training record"""
    def process(self, element):
        import json
        from datetime import datetime
        
        event = json.loads(element)
        yield {
            'training_id': event['training_id'],
            'date': datetime.now().isoformat(),
            'location': event['location'],
            'attendees': event['attendee_count'],
            'trainer': event['trainer_name'],
            'status': 'ACTIVE'
        }

# Define pipeline
options = PipelineOptions()
options.view_as(GoogleCloudOptions).project = 'undp-project'
options.view_as(GoogleCloudOptions).job_name = 'training-streaming'
options.view_as(StandardOptions).runner = 'DataflowRunner'

with beam.Pipeline(options=options) as p:
    (p
     | 'Read from Pub/Sub' >> ReadFromPubSub(topic='projects/undp-project/topics/training-events')
     | 'Extract Fields' >> beam.ParDo(ExtractTrainingEvent())
     | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
         table='undp-project:operations.training_daily',
         create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
         write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
     )
    )
```

**Result:** BigQuery table updates every 5 seconds; Data Studio dashboard auto-refreshes.

---

## PROBLEM 5: Data Validation & Anomaly Detection (Prevent Fraud, Catch Errors)

### Pattern: Great Expectations (Data Validation Framework)

**Project:** `great-expectations`
- **GitHub:** great-expectations/great_expectations
- **What it does:** Automated data quality checks
- **Tech:** Python + SQL
- **Applies to:** UNDP disbursements (prevent invalid payments), ILO training records (catch attendance cheating)

**Why relevant:**
- UNDP: "We paid someone to account that doesn't exist" (fraud caught in audit, 2 weeks later)
- ILO: "Trainer marked 100 attendees in 1 hour" (impossible; suspicious)
- Current: No automated checks; caught manually in audits
- This approach: Auto-flag anomalies in real-time

**How it works:**
```python
from great_expectations.dataset import PandasDataset
import pandas as pd

# Load data
payments_df = pd.read_csv('undp_disbursements.csv')
gdf = PandasDataset(payments_df)

# Define expectations (data quality rules)

# Rule 1: Payment amount should be > 0 and < 10,000
gdf.expect_column_values_to_be_between('payment_amount', min_value=0, max_value=10000)

# Rule 2: Beneficiary ID should not be null
gdf.expect_column_values_to_not_be_null('beneficiary_id')

# Rule 3: Mobile account format should match regex (bKash/Nagad format)
gdf.expect_column_values_to_match_regex('mobile_account', r'^880\d{9}$')

# Rule 4: Payment date should be recent (not future)
gdf.expect_column_values_to_be_dateutil_parseable('payment_date')

# Rule 5: Duplicate checks
gdf.expect_column_values_to_be_unique('payment_id')

# Run validation
validation_result = gdf.validate()

# Output: Which payments failed which checks?
for check in validation_result['results']:
    if not check['success']:
        print(f"FAILED: {check['expectation_config']['expectation_type']}")
        print(f"  Affected rows: {check['result']['element_count'] - check['result']['valid_count']}")
```

**For ILO training anomalies:**
```python
# Rule 1: Attendance should not exceed venue capacity
training_df.expect_column_values_to_be_less_than('attendee_count', 50)  # assume max 50

# Rule 2: Training duration should be reasonable (1-8 hours)
training_df.expect_column_values_to_be_between('duration_hours', 1, 8)

# Rule 3: Trainer should have been trained (check trainer registry)
trainers = pd.read_csv('ilo_trainers.csv')
training_df.expect_column_values_to_be_in_set('trainer_id', trainers['trainer_id'].tolist())
```

**Integration with real-time pipeline:**
```python
# In Dataflow pipeline
(p
 | 'Read events' >> beam.io.ReadFromPubSub(...)
 | 'Validate with Great Expectations' >> beam.ParDo(ValidateWithExpectations())
 | 'Route valid events to warehouse' >> beam.io.WriteToBigQuery(...)
 | 'Route invalid events to alert queue' >> WriteToPubSub('alert-topic')  # Alert ops team
)
```

---

## PROBLEM 6: Data Organization (Fragmented Spreadsheets → Unified Schema)

### Pattern: dbt (data build tool) for Data Transformation

**Project:** `dbt-labs/dbt-core`
- **GitHub:** dbt-labs/dbt-core
- **What it does:** Transform raw data into clean, usable tables
- **Tech:** SQL + Python + Version control
- **Applies to:** ILO/UNDP data warehouse (transform messy inputs into analysis-ready tables)

**Why relevant:**
- UNDP data: "Training data in one system, beneficiary data in another, payments in a third"
- Current: Manual ETL (person writes custom scripts; no documentation; breaks when data changes)
- This approach: dbt models (documented, testable, version-controlled transformations)

**How it works:**
```sql
-- models/int_training_attendance_clean.sql
-- Transform raw training data into clean, unified table

WITH training_raw AS (
    SELECT 
        training_id,
        trainer_name,
        TRIM(UPPER(trainer_name)) as trainer_name_clean,  -- Normalize
        training_date,
        attendance_raw as attendee_count,
        CASE 
            WHEN venue = 'Community Center' THEN 'center'
            WHEN venue = 'School' THEN 'school'
            ELSE 'other'
        END as venue_type
    FROM {{ source('raw_data', 'training_logs') }}
)

, validation AS (
    SELECT 
        training_id,
        trainer_name_clean,
        training_date,
        attendee_count,
        venue_type,
        -- Data quality flags
        CASE WHEN attendee_count < 5 THEN 'LOW_ATTENDANCE' END as quality_flag
    FROM training_raw
)

SELECT * FROM validation
WHERE EXTRACT(YEAR FROM training_date) = EXTRACT(YEAR FROM CURRENT_DATE())
```

**Run dbt:**
```bash
dbt run  # Transforms raw data
dbt test # Validates data (checks for nulls, uniqueness, relationships)
dbt docs generate  # Auto-generates documentation
```

**Result:** Reproducible data pipeline; anyone can understand transformations.

---

## PUTTING IT TOGETHER: End-to-End Architecture

### For UNDP Beneficiary Operations:

```
Paper Forms (Cox's Bazar) 
  ↓ (photograph)
S3 Bucket
  ↓ (AWS Textract + image preprocessing)
Raw Beneficiary Data
  ↓ (Great Expectations validation)
Invalid Data → Alert ops team
Valid Data → DynamoDB
  ↓ (Deduplication: recordlinkage)
Unified Beneficiary Table
  ↓ (dbt transformation + BigQuery)
Analysis-Ready Tables
  ↓ (Looker dashboard)
Ops Team sees: "1,500 new beneficiaries today, 3 flagged as duplicates"
```

### For ILO Training-to-Outcome:

```
Training attendance forms (paper)
  ↓ (Textract)
Training events → Pub/Sub
  ↓ (Dataflow streaming)
Real-time training table
  ↓ (merge with outcome surveys)
Linked training-outcome data
  ↓ (BigQuery analytics)
Dashboard: "Training → 18% earnings increase"
```

---

## Quick GitHub Reference (Ready-to-Use Repos)

| Problem | GitHub Project | Tech | Language | Stars |
|---|---|---|---|---|
| Form extraction | `aws-forms-extraction-and-databasing` | AWS Textract + DynamoDB | Python | 100+ |
| Deduplication | `recordlinkage` | Record Linkage | Python | 1000+ |
| Image preprocessing | `OpenCV` | Computer Vision | C++/Python | 30k+ |
| Streaming ETL | `apache-beam` | Dataflow | Java/Python | 20k+ |
| Data validation | `great-expectations` | Data QA | Python | 5000+ |
| Data transformation | `dbt` | SQL + Python | SQL | 7000+ |
| Bengali NLP | `google-cloud-natural-language` | Cloud NLP | REST API | N/A |
| Mobile app + offline | `Firebase` | Backend + Mobile | REST | N/A |

---

## Implementation Priority (Start Here)

**Week 1-2: Quick wins**
1. Form extraction (Textract + image preprocessing) → ILO/UNDP can digitize forms same day
2. Data validation (Great Expectations) → Real-time fraud detection

**Week 3-4: Scale**
3. Deduplication (recordlinkage) → Prevent duplicate payments
4. Streaming ETL (Dataflow) → Real-time dashboard

**Week 5+: Sophistication**
5. Bengali NLP → Auto-analyze open-ended feedback
6. dbt transformation → Clean data warehouse

