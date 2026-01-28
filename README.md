README.md

# LLM Email Extraction System – Task Harmony Assessment

## Overview

This project implements an LLM-powered pipeline to extract structured shipment details from freight forwarding pricing enquiry emails.

The system processes raw emails, extracts structured fields using a Groq-hosted LLM, applies business rules, validates outputs using Pydantic models, and evaluates accuracy against provided ground truth data.

Final achieved accuracy: **85.56%**

---

## Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt

2. Run extraction
python extract.py

3. Evaluate accuracy
python evaluate.py

Project Structure
├── extract.py                  # Main LLM extraction pipeline
├── evaluate.py                 # Accuracy evaluation script
├── schemas.py                  # Pydantic output models
├── prompts.py                  # Prompt versions (v1 → v2)
├── output.json                 # Generated extraction results
├── emails_input.json           # Input emails
├── ground_truth.json           # Expected outputs
├── port_codes_reference.json   # UN/LOCODE reference data
├── requirements.txt
└── README.md

Approach

Load raw emails from emails_input.json

Send email subject + body to Groq LLM using a structured extraction prompt

Enforce business rules directly in the prompt

Parse and clean LLM JSON responses

Validate output using Pydantic models

Apply fallback logic for failed extractions

Save structured results to output.json

Compare output with ground_truth.json to measure accuracy

Prompt Evolution
v1 – Basic extraction prompt

Accuracy: 78.22%

Issues:

LLM sometimes returned null values despite data being present

No examples were provided for guidance

Conservative extraction behavior

v2 – Explicit rules + example-based prompt

Accuracy: 85.56%

Improvements:

Forced extraction when information is present

Added a concrete example for better guidance

Added precedence rules (body overrides subject)

Added robust JSON parsing for code-block responses

Implemented retry logic for API errors

Accuracy Metrics
Metric	Result
Overall Accuracy	85.56%
Product Line	High
Port Extraction	High
Incoterm	High
Weight & CBM	Medium–High
Dangerous Goods	High
Error Handling & Reliability

Exponential backoff retry logic for Groq API failures

Graceful fallback with null values if extraction fails

Strict schema validation using Pydantic

No email is skipped during processing

Robust JSON cleaning for LLM code-block responses

System Design Answers
1. Scaling to 10,000 emails/day within 5 minutes

I would use an asynchronous worker-based architecture with a message queue (e.g., SQS or Redis Queue). Emails would be processed in parallel by multiple workers. Easy emails would use a cheaper model, while ambiguous ones would be routed to a stronger model. Caching repeated patterns and batching requests would reduce cost and latency. This design fits within a $500/month budget.

2. Monitoring accuracy degradation

I would continuously sample production outputs and compare them with human-verified labels. Field-level accuracy metrics would be tracked over time. Alerts would trigger if accuracy drops below a defined threshold, indicating prompt drift or data distribution changes. I would then review failed samples and iterate on the prompt or parsing logic.

3. Handling multilingual emails (Mandarin, Hindi)

I would add language detection as a preprocessing step and translate non-English emails into English before extraction. Accuracy would be measured per language to detect biases. For large volumes, I would consider a multilingual extraction model to avoid translation errors.

Notes

Temperature is set to 0 for reproducible results

The system is designed to be robust against malformed LLM responses

Output is included for review without re-running extraction

Author

Srikanth Banoth
Backend / AI Engineer


---
```
