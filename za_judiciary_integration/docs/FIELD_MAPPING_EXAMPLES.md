# Field Mapping Examples: HyperGNN ↔ Court Online/CaseLines

## Sample Data Transformations

### 1. Case Creation Example

#### HyperGNN Input Data
```json
{
  "id": "hypergnn-case-001",
  "title": "Financial Fraud Investigation - ABC Corporation",
  "description": "Investigation into suspicious financial transactions involving multiple shell companies and offshore accounts",
  "status": "active",
  "priority": "high",
  "created_at": "2025-10-08T10:30:00Z",
  "entities": [
    {
      "id": "entity-001",
      "name": "ABC Corporation",
      "type": "organization",
      "properties": {
        "registration_number": "2019/123456/07",
        "address": "123 Business Street, Sandton, 2196",
        "contact": "+27 11 123 4567"
      }
    },
    {
      "id": "entity-002", 
      "name": "John Smith",
      "type": "person",
      "properties": {
        "id_number": "8001015009088",
        "address": "456 Residential Ave, Johannesburg, 2001",
        "contact": "+27 82 987 6543"
      }
    }
  ]
}
```

#### ZA Integration Layer Transformation
```sql
-- Insert into za_cases table
INSERT INTO za_cases (
    id,
    case_number,
    title,
    description,
    status,
    priority,
    court_id,
    case_type_id,
    plaintiff_details,
    defendant_details,
    filing_date,
    court_online_case_id,
    e_filing_enabled,
    caselines_bundle_id
) VALUES (
    'hypergnn-case-001',
    '(GP) 12345/2025',  -- Generated ZA case number
    'Financial Fraud Investigation - ABC Corporation',
    'Investigation into suspicious financial transactions involving multiple shell companies and offshore accounts',
    'filed',  -- Mapped from 'active'
    'high',
    (SELECT id FROM za_court_registry WHERE court_code = 'GP'),
    (SELECT id FROM za_case_types WHERE case_type_code = 'COM'),  -- Commercial Court
    '{"name": "State vs", "type": "prosecution", "attorney": "Director of Public Prosecutions"}',
    '{"name": "ABC Corporation", "type": "corporate", "registration": "2019/123456/07", "address": "123 Business Street, Sandton, 2196"}',
    '2025-10-08',
    'co-gp-12345-2025',  -- Court Online case ID
    true,
    'cl-gp-12345-2025'   -- CaseLines bundle ID
);
```

#### Court Online Output Format
```json
{
  "case_id": "co-gp-12345-2025",
  "case_number": "(GP) 12345/2025",
  "case_title": "Financial Fraud Investigation - ABC Corporation",
  "case_description": "Investigation into suspicious financial transactions involving multiple shell companies and offshore accounts",
  "case_type": "Commercial Court",
  "court_division": "Gauteng Division, Pretoria",
  "filing_date": "2025-10-08",
  "case_status": "filed",
  "urgency_level": "high",
  "plaintiff": {
    "party_id": "plaintiff-001",
    "party_name": "State vs",
    "party_type": "prosecution",
    "legal_representative": "Director of Public Prosecutions"
  },
  "defendant": {
    "party_id": "defendant-001", 
    "party_name": "ABC Corporation",
    "party_type": "corporate",
    "registration_number": "2019/123456/07",
    "party_address": "123 Business Street, Sandton, 2196"
  },
  "e_filing_enabled": true,
  "case_management_enabled": true
}
```

### 2. Evidence Bundle Example

#### HyperGNN Evidence Input
```json
{
  "evidence_items": [
    {
      "id": "evidence-001",
      "title": "Bank Statement - ABC Corp Account",
      "evidence_type": "financial",
      "file_path": "/evidence/bank_statements/abc_corp_2025.pdf",
      "file_size": 2048576,
      "file_hash": "sha256:a1b2c3d4e5f6...",
      "metadata": {
        "pages": 15,
        "date_range": "2025-01-01 to 2025-09-30",
        "account_number": "****1234"
      },
      "created_at": "2025-10-08T11:00:00Z"
    },
    {
      "id": "evidence-002",
      "title": "Email Correspondence - Suspicious Transactions",
      "evidence_type": "communication", 
      "file_path": "/evidence/emails/suspicious_emails.pdf",
      "file_size": 1024768,
      "file_hash": "sha256:b2c3d4e5f6a1...",
      "metadata": {
        "pages": 8,
        "email_count": 23,
        "date_range": "2025-03-15 to 2025-08-20"
      },
      "created_at": "2025-10-08T11:15:00Z"
    }
  ]
}
```

#### ZA Integration Layer Transformation
```sql
-- Create evidence bundle
INSERT INTO za_evidence_bundles (
    id,
    case_id,
    bundle_name,
    bundle_type,
    caselines_bundle_id,
    total_pages,
    total_documents,
    bundle_status,
    created_by
) VALUES (
    'bundle-discovery-001',
    'hypergnn-case-001',
    'Discovery Bundle - Financial Evidence',
    'discovery',
    'cl-bundle-discovery-001',
    23,  -- Total pages (15 + 8)
    2,   -- Total documents
    'draft',
    (SELECT id FROM za_legal_practitioners WHERE practitioner_number = 'ATT001')
);

-- Insert individual documents
INSERT INTO za_evidence_documents (
    id,
    bundle_id,
    case_id,
    document_name,
    document_type,
    caselines_document_id,
    page_range,
    bundle_position,
    file_path,
    file_size,
    file_hash,
    page_count,
    document_date,
    confidentiality_level,
    relevance_score
) VALUES 
(
    'evidence-001',
    'bundle-discovery-001',
    'hypergnn-case-001',
    'Bank Statement - ABC Corp Account',
    'financial_document',
    'cl-doc-001',
    '1-15',
    1,
    '/evidence/bank_statements/abc_corp_2025.pdf',
    2048576,
    'sha256:a1b2c3d4e5f6...',
    15,
    '2025-09-30',
    'confidential',
    0.95
),
(
    'evidence-002',
    'bundle-discovery-001', 
    'hypergnn-case-001',
    'Email Correspondence - Suspicious Transactions',
    'correspondence',
    'cl-doc-002',
    '16-23',
    2,
    '/evidence/emails/suspicious_emails.pdf',
    1024768,
    'sha256:b2c3d4e5f6a1...',
    8,
    '2025-08-20',
    'confidential',
    0.88
);
```

#### CaseLines Output Format
```json
{
  "bundle_id": "cl-bundle-discovery-001",
  "bundle_name": "Discovery Bundle - Financial Evidence",
  "bundle_type": "discovery",
  "case_reference": "(GP) 12345/2025",
  "total_documents": 2,
  "total_pages": 23,
  "bundle_status": "draft",
  "pagination_complete": false,
  "redaction_complete": false,
  "documents": [
    {
      "document_id": "cl-doc-001",
      "document_name": "Bank Statement - ABC Corp Account",
      "document_type": "financial_document",
      "page_range": "1-15",
      "bundle_position": 1,
      "file_location": "/caselines/bundles/cl-bundle-discovery-001/doc-001.pdf",
      "file_size": 2048576,
      "document_hash": "sha256:a1b2c3d4e5f6...",
      "page_count": 15,
      "confidentiality_level": "confidential",
      "redaction_required": true,
      "upload_date": "2025-10-08T11:00:00Z"
    },
    {
      "document_id": "cl-doc-002",
      "document_name": "Email Correspondence - Suspicious Transactions", 
      "document_type": "correspondence",
      "page_range": "16-23",
      "bundle_position": 2,
      "file_location": "/caselines/bundles/cl-bundle-discovery-001/doc-002.pdf",
      "file_size": 1024768,
      "document_hash": "sha256:b2c3d4e5f6a1...",
      "page_count": 8,
      "confidentiality_level": "confidential",
      "redaction_required": true,
      "upload_date": "2025-10-08T11:15:00Z"
    }
  ]
}
```

### 3. Court Proceeding Example

#### HyperGNN Timeline Event Input
```json
{
  "timeline_event": {
    "id": "event-001",
    "case_id": "hypergnn-case-001",
    "event_date": "2025-11-15T10:00:00Z",
    "title": "Case Management Conference",
    "description": "Initial case management conference to set trial dates and discovery deadlines",
    "event_type": "case_management",
    "location": "Court Room 5A, Gauteng High Court, Pretoria",
    "participants": [
      "Judge Sarah Johnson",
      "Adv. Michael Brown (State)",
      "Adv. Lisa Wilson (Defendant)"
    ]
  }
}
```

#### ZA Integration Layer Transformation
```sql
INSERT INTO za_court_proceedings (
    id,
    case_id,
    proceeding_type,
    proceeding_date,
    proceeding_time,
    court_room,
    presiding_judge,
    court_online_hearing_id,
    virtual_hearing,
    attending_parties,
    attending_attorneys
) VALUES (
    'event-001',
    'hypergnn-case-001',
    'case_management',
    '2025-11-15',
    '10:00:00',
    'Court Room 5A',
    'Judge Sarah Johnson',
    'co-hearing-001',
    false,
    '["State vs", "ABC Corporation"]',
    '["Adv. Michael Brown", "Adv. Lisa Wilson"]'
);
```

#### Court Online Output Format
```json
{
  "hearing_id": "co-hearing-001",
  "case_reference": "(GP) 12345/2025",
  "hearing_type": "case_management",
  "hearing_date": "2025-11-15",
  "hearing_time": "10:00",
  "court_room": "Court Room 5A",
  "court_location": "Gauteng High Court, Pretoria",
  "presiding_judge": "Judge Sarah Johnson",
  "virtual_hearing": false,
  "teams_link": null,
  "parties_required": [
    {
      "party_name": "State vs",
      "party_type": "prosecution",
      "legal_representative": "Adv. Michael Brown",
      "attendance_required": true
    },
    {
      "party_name": "ABC Corporation",
      "party_type": "corporate",
      "legal_representative": "Adv. Lisa Wilson", 
      "attendance_required": true
    }
  ],
  "hearing_purpose": "Initial case management conference to set trial dates and discovery deadlines",
  "notification_sent": true,
  "sms_notifications": [
    {
      "recipient": "+27 82 987 6543",
      "message": "Court hearing scheduled for (GP) 12345/2025 on 15 Nov 2025 at 10:00 in Court Room 5A"
    }
  ],
  "email_notifications": [
    {
      "recipient": "legal@abccorp.co.za",
      "subject": "Court Hearing Notice - Case (GP) 12345/2025",
      "message": "You are required to attend a case management conference..."
    }
  ]
}
```

### 4. Electronic Filing Example

#### HyperGNN Filing Request
```json
{
  "filing_request": {
    "case_id": "hypergnn-case-001",
    "filing_type": "Plea",
    "documents": [
      {
        "document_name": "Plea to Summons",
        "file_path": "/filings/plea_abc_corp.pdf",
        "file_size": 512000,
        "page_count": 5
      },
      {
        "document_name": "Notice of Intention to Defend",
        "file_path": "/filings/notice_defend.pdf", 
        "file_size": 256000,
        "page_count": 2
      }
    ],
    "filing_fee": 200.00,
    "payment_reference": "PAY-2025-001234",
    "filed_by": "Adv. Lisa Wilson"
  }
}
```

#### ZA Integration Layer Transformation
```sql
INSERT INTO za_electronic_filings (
    id,
    case_id,
    filing_type,
    filing_description,
    court_online_filing_id,
    submission_timestamp,
    filing_status,
    filed_by,
    filing_fee,
    payment_reference,
    documents_filed,
    total_pages
) VALUES (
    'filing-001',
    'hypergnn-case-001',
    'Plea',
    'Plea to Summons and Notice of Intention to Defend',
    'co-filing-20251008-001',
    '2025-10-08T14:30:00Z',
    'submitted',
    (SELECT id FROM za_legal_practitioners WHERE practitioner_name = 'Adv. Lisa Wilson'),
    200.00,
    'PAY-2025-001234',
    '[{"name": "Plea to Summons", "pages": 5}, {"name": "Notice of Intention to Defend", "pages": 2}]',
    7
);
```

#### Court Online Filing Output
```json
{
  "filing_id": "co-filing-20251008-001",
  "case_reference": "(GP) 12345/2025",
  "filing_type": "Plea",
  "filing_description": "Plea to Summons and Notice of Intention to Defend",
  "submission_timestamp": "2025-10-08T14:30:00Z",
  "filing_status": "submitted",
  "filed_by": {
    "practitioner_name": "Adv. Lisa Wilson",
    "practitioner_number": "ADV001",
    "law_firm": "Wilson & Associates",
    "contact_email": "l.wilson@wilsonlaw.co.za"
  },
  "documents_submitted": [
    {
      "document_name": "Plea to Summons",
      "file_reference": "co-doc-plea-001",
      "file_size": 512000,
      "page_count": 5,
      "document_hash": "sha256:c3d4e5f6a1b2..."
    },
    {
      "document_name": "Notice of Intention to Defend",
      "file_reference": "co-doc-notice-001", 
      "file_size": 256000,
      "page_count": 2,
      "document_hash": "sha256:d4e5f6a1b2c3..."
    }
  ],
  "filing_fee": 200.00,
  "payment_reference": "PAY-2025-001234",
  "payment_status": "confirmed",
  "processing_status": "pending_registrar_review",
  "estimated_processing_time": "2-5 business days",
  "service_required": true,
  "service_parties": [
    {
      "party_name": "Director of Public Prosecutions",
      "service_method": "electronic",
      "service_address": "dpp@npa.gov.za"
    }
  ]
}
```

## Data Validation Examples

### 1. Case Number Validation
```python
def validate_za_case_number(case_number):
    """
    Validate South African case number format
    Expected format: (COURT_CODE) NUMBER/YEAR
    Examples: (GP) 12345/2025, (WCC) 67890/2025
    """
    import re
    
    pattern = r'^\([A-Z]{2,3}\)\s*\d{4,6}\/\d{4}$'
    
    test_cases = [
        "(GP) 12345/2025",     # ✅ Valid
        "(WCC) 67890/2025",    # ✅ Valid  
        "(GJ) 123/2025",       # ✅ Valid (short number)
        "(INVALID) 123/2025",  # ❌ Invalid court code
        "GP 12345/2025",       # ❌ Missing parentheses
        "(GP) 12345-2025",     # ❌ Wrong separator
        "(GP) ABC/2025"        # ❌ Non-numeric case number
    ]
    
    for case_num in test_cases:
        is_valid = bool(re.match(pattern, case_num))
        print(f"{case_num}: {'✅ Valid' if is_valid else '❌ Invalid'}")
```

### 2. Document Type Mapping Validation
```python
def map_evidence_type_to_caselines(hypergnn_type):
    """
    Map HyperGNN evidence types to CaseLines document types
    """
    mapping = {
        'document': 'pleading',
        'image': 'photograph', 
        'video': 'video_evidence',
        'audio': 'audio_recording',
        'financial': 'financial_document',
        'communication': 'correspondence',
        'physical': 'physical_evidence'
    }
    
    caselines_type = mapping.get(hypergnn_type, 'other')
    
    # Validate CaseLines type
    valid_caselines_types = [
        'pleading', 'photograph', 'video_evidence', 'audio_recording',
        'financial_document', 'correspondence', 'physical_evidence', 'other'
    ]
    
    if caselines_type not in valid_caselines_types:
        raise ValueError(f"Invalid CaseLines document type: {caselines_type}")
    
    return caselines_type
```

### 3. Bundle Organization Validation
```python
def validate_bundle_organization(documents):
    """
    Validate that documents are properly organized for CaseLines bundles
    """
    bundle_rules = {
        'pleadings': ['summons', 'plea', 'affidavit'],
        'discovery': ['bank_statement', 'invoice', 'contract'],
        'correspondence': ['email', 'letter', 'notice'],
        'multimedia': ['photograph', 'video_evidence', 'audio_recording']
    }
    
    for bundle_type, doc_types in bundle_rules.items():
        bundle_docs = [doc for doc in documents if doc['type'] in doc_types]
        
        if bundle_docs:
            print(f"{bundle_type.title()} Bundle: {len(bundle_docs)} documents")
            for doc in bundle_docs:
                print(f"  - {doc['name']} ({doc['type']})")
```

This comprehensive field mapping demonstrates how HyperGNN data seamlessly transforms into Court Online and CaseLines formats while maintaining data integrity and legal compliance.
