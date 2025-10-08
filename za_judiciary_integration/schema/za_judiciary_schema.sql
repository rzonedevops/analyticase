-- HyperGNN Analysis Framework - South African Judiciary Integration Schema
-- Aligned with Court Online and CaseLines systems
-- Compatible with ZA High Courts electronic filing and evidence management

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Court Online Integration Tables

-- ZA Court Registry aligned with Court Online system
CREATE TABLE IF NOT EXISTS za_court_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    court_code VARCHAR(10) UNIQUE NOT NULL, -- e.g., 'GP', 'WCC', 'KZP'
    court_name VARCHAR(255) NOT NULL,
    division VARCHAR(100) NOT NULL, -- Gauteng Division, Western Cape Division, etc.
    jurisdiction VARCHAR(100) NOT NULL,
    court_type VARCHAR(50) CHECK (court_type IN ('High Court', 'Supreme Court of Appeal', 'Constitutional Court')),
    physical_address TEXT,
    postal_address TEXT,
    contact_number VARCHAR(20),
    email VARCHAR(255),
    registrar_name VARCHAR(255),
    is_court_online_enabled BOOLEAN DEFAULT FALSE,
    is_caselines_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Legal practitioners registration (aligned with Court Online user management)
CREATE TABLE IF NOT EXISTS za_legal_practitioners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    practitioner_number VARCHAR(20) UNIQUE NOT NULL, -- Law Society registration number
    firm_name VARCHAR(255),
    practitioner_name VARCHAR(255) NOT NULL,
    practitioner_type VARCHAR(50) CHECK (practitioner_type IN ('Attorney', 'Advocate', 'Legal Advisor', 'In-house Counsel')),
    law_society VARCHAR(100), -- Provincial Law Society
    admission_date DATE,
    practice_areas TEXT[],
    contact_details JSONB DEFAULT '{}',
    court_online_user_id VARCHAR(100), -- Court Online system user ID
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ZA Case types aligned with Court Online proceedings
CREATE TABLE IF NOT EXISTS za_case_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_type_code VARCHAR(20) UNIQUE NOT NULL,
    case_type_name VARCHAR(255) NOT NULL,
    description TEXT,
    court_online_category VARCHAR(100), -- Maps to Court Online categories
    is_civil BOOLEAN DEFAULT TRUE,
    is_criminal BOOLEAN DEFAULT FALSE,
    requires_case_management BOOLEAN DEFAULT FALSE,
    typical_duration_days INTEGER,
    filing_fee_amount DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enhanced cases table with ZA judiciary compliance
CREATE TABLE IF NOT EXISTS za_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_number VARCHAR(50) UNIQUE NOT NULL, -- ZA format: (GP) 12345/2025
    court_file_number VARCHAR(50), -- Internal court file number
    case_type_id UUID REFERENCES za_case_types(id),
    court_id UUID REFERENCES za_court_registry(id),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(30) DEFAULT 'filed' CHECK (status IN ('filed', 'served', 'defended', 'trial_ready', 'trial', 'judgment', 'appeal', 'closed', 'archived')),
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('urgent', 'high', 'normal', 'low')),
    
    -- Parties information
    plaintiff_details JSONB DEFAULT '{}',
    defendant_details JSONB DEFAULT '{}',
    other_parties JSONB DEFAULT '[]',
    
    -- Legal representation
    plaintiff_attorney_id UUID REFERENCES za_legal_practitioners(id),
    defendant_attorney_id UUID REFERENCES za_legal_practitioners(id),
    
    -- Court Online integration
    court_online_case_id VARCHAR(100), -- Court Online system case ID
    e_filing_enabled BOOLEAN DEFAULT FALSE,
    caselines_bundle_id VARCHAR(100), -- CaseLines bundle identifier
    
    -- Dates and scheduling
    filing_date DATE NOT NULL,
    service_date DATE,
    plea_date DATE,
    trial_date DATE,
    judgment_date DATE,
    
    -- Financial information
    amount_claimed DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'ZAR',
    costs_awarded DECIMAL(15,2),
    
    -- Case management
    case_manager VARCHAR(255),
    allocated_judge VARCHAR(255),
    court_room VARCHAR(50),
    
    -- Metadata and tracking
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    closed_at TIMESTAMP WITH TIME ZONE
);

-- CaseLines Evidence Management Integration

-- Evidence bundles aligned with CaseLines structure
CREATE TABLE IF NOT EXISTS za_evidence_bundles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES za_cases(id) ON DELETE CASCADE,
    bundle_name VARCHAR(255) NOT NULL,
    bundle_type VARCHAR(50) CHECK (bundle_type IN ('pleadings', 'discovery', 'expert_reports', 'correspondence', 'multimedia', 'trial_bundle')),
    caselines_bundle_id VARCHAR(100), -- CaseLines system bundle ID
    bundle_description TEXT,
    total_pages INTEGER DEFAULT 0,
    total_documents INTEGER DEFAULT 0,
    bundle_status VARCHAR(30) DEFAULT 'draft' CHECK (bundle_status IN ('draft', 'submitted', 'served', 'filed', 'archived')),
    created_by UUID REFERENCES za_legal_practitioners(id),
    pagination_complete BOOLEAN DEFAULT FALSE,
    redaction_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Individual evidence documents within bundles
CREATE TABLE IF NOT EXISTS za_evidence_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bundle_id UUID REFERENCES za_evidence_bundles(id) ON DELETE CASCADE,
    case_id UUID REFERENCES za_cases(id) ON DELETE CASCADE,
    document_name VARCHAR(500) NOT NULL,
    document_type VARCHAR(100) CHECK (document_type IN ('summons', 'plea', 'affidavit', 'expert_report', 'correspondence', 'contract', 'invoice', 'photograph', 'video', 'audio', 'other')),
    
    -- CaseLines integration
    caselines_document_id VARCHAR(100),
    page_range VARCHAR(50), -- e.g., "1-15" for CaseLines pagination
    bundle_position INTEGER, -- Position within bundle
    
    -- Document properties
    file_path VARCHAR(1000),
    file_name VARCHAR(500),
    file_size BIGINT,
    file_hash VARCHAR(128),
    mime_type VARCHAR(100),
    page_count INTEGER,
    
    -- Document metadata
    author VARCHAR(255),
    creation_date DATE,
    document_date DATE, -- Date of the document content
    confidentiality_level VARCHAR(30) DEFAULT 'standard' CHECK (confidentiality_level IN ('public', 'standard', 'confidential', 'privileged')),
    
    -- Processing status
    is_redacted BOOLEAN DEFAULT FALSE,
    is_paginated BOOLEAN DEFAULT FALSE,
    is_searchable BOOLEAN DEFAULT FALSE,
    ocr_completed BOOLEAN DEFAULT FALSE,
    
    -- Legal significance
    relevance_score DECIMAL(3,2) CHECK (relevance_score >= 0 AND relevance_score <= 1),
    privilege_claimed BOOLEAN DEFAULT FALSE,
    privilege_type VARCHAR(100),
    
    uploaded_by UUID REFERENCES za_legal_practitioners(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Court proceedings and hearings
CREATE TABLE IF NOT EXISTS za_court_proceedings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES za_cases(id) ON DELETE CASCADE,
    proceeding_type VARCHAR(100) CHECK (proceeding_type IN ('case_management', 'motion', 'trial', 'appeal', 'judgment', 'settlement_conference')),
    proceeding_date DATE NOT NULL,
    proceeding_time TIME,
    court_room VARCHAR(50),
    presiding_judge VARCHAR(255),
    
    -- Court Online integration
    court_online_hearing_id VARCHAR(100),
    virtual_hearing BOOLEAN DEFAULT FALSE,
    teams_link VARCHAR(500),
    
    -- CaseLines integration
    caselines_hearing_bundle VARCHAR(100),
    electronic_presentation BOOLEAN DEFAULT FALSE,
    
    -- Participants
    attending_parties JSONB DEFAULT '[]',
    attending_attorneys JSONB DEFAULT '[]',
    
    -- Outcomes
    orders_made TEXT,
    next_hearing_date DATE,
    costs_order TEXT,
    
    -- Documentation
    transcript_available BOOLEAN DEFAULT FALSE,
    transcript_path VARCHAR(1000),
    audio_recording_path VARCHAR(1000),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Court orders and judgments
CREATE TABLE IF NOT EXISTS za_court_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES za_cases(id) ON DELETE CASCADE,
    proceeding_id UUID REFERENCES za_court_proceedings(id),
    order_type VARCHAR(100) CHECK (order_type IN ('interlocutory', 'final', 'default', 'summary', 'consent', 'costs')),
    order_date DATE NOT NULL,
    presiding_judge VARCHAR(255) NOT NULL,
    
    -- Order content
    order_title VARCHAR(500),
    order_text TEXT NOT NULL,
    order_summary TEXT,
    
    -- Legal implications
    is_appealable BOOLEAN DEFAULT TRUE,
    appeal_deadline DATE,
    execution_date DATE,
    
    -- Financial orders
    monetary_award DECIMAL(15,2),
    costs_awarded DECIMAL(15,2),
    interest_rate DECIMAL(5,2),
    
    -- Document management
    order_document_path VARCHAR(1000),
    caselines_order_id VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Electronic filing tracking (Court Online integration)
CREATE TABLE IF NOT EXISTS za_electronic_filings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES za_cases(id) ON DELETE CASCADE,
    filing_type VARCHAR(100) NOT NULL,
    filing_description TEXT,
    
    -- Court Online integration
    court_online_filing_id VARCHAR(100) UNIQUE,
    submission_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    filing_status VARCHAR(50) DEFAULT 'submitted' CHECK (filing_status IN ('draft', 'submitted', 'accepted', 'rejected', 'served')),
    
    -- Filing details
    filed_by UUID REFERENCES za_legal_practitioners(id),
    filing_fee DECIMAL(10,2),
    payment_reference VARCHAR(100),
    
    -- Document references
    documents_filed JSONB DEFAULT '[]', -- Array of document IDs
    total_pages INTEGER DEFAULT 0,
    
    -- Processing
    registrar_notes TEXT,
    rejection_reason TEXT,
    acceptance_timestamp TIMESTAMP WITH TIME ZONE,
    service_timestamp TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- SMS and Email notifications (Court Online gateway integration)
CREATE TABLE IF NOT EXISTS za_court_notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES za_cases(id) ON DELETE CASCADE,
    recipient_type VARCHAR(50) CHECK (recipient_type IN ('attorney', 'litigant', 'court_staff', 'judge')),
    recipient_id UUID, -- Can reference different tables based on type
    
    -- Notification details
    notification_type VARCHAR(100) CHECK (notification_type IN ('hearing_date', 'filing_accepted', 'filing_rejected', 'judgment', 'order', 'deadline_reminder')),
    subject VARCHAR(500),
    message_content TEXT NOT NULL,
    
    -- Delivery channels
    sms_number VARCHAR(20),
    email_address VARCHAR(255),
    
    -- Delivery status
    sms_sent BOOLEAN DEFAULT FALSE,
    email_sent BOOLEAN DEFAULT FALSE,
    sms_delivered BOOLEAN DEFAULT FALSE,
    email_delivered BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    scheduled_for TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sent_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit trail for compliance and tracking
CREATE TABLE IF NOT EXISTS za_audit_trail (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES za_cases(id),
    user_id UUID, -- Can reference different user types
    user_type VARCHAR(50) CHECK (user_type IN ('attorney', 'court_staff', 'judge', 'registrar', 'system')),
    
    -- Action details
    action_type VARCHAR(100) NOT NULL,
    action_description TEXT,
    affected_entity VARCHAR(100), -- Table or entity affected
    affected_entity_id UUID,
    
    -- System integration
    court_online_action_id VARCHAR(100),
    caselines_action_id VARCHAR(100),
    
    -- Change tracking
    old_values JSONB,
    new_values JSONB,
    
    -- Context
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert ZA-specific reference data

-- Insert South African court divisions
INSERT INTO za_court_registry (court_code, court_name, division, jurisdiction, court_type, is_court_online_enabled, is_caselines_enabled) VALUES
('GP', 'Gauteng Division, Pretoria', 'Gauteng Division', 'Gauteng Province', 'High Court', TRUE, TRUE),
('GJ', 'Gauteng Division, Johannesburg', 'Gauteng Division', 'Gauteng Province', 'High Court', TRUE, TRUE),
('WCC', 'Western Cape Division, Cape Town', 'Western Cape Division', 'Western Cape Province', 'High Court', TRUE, TRUE),
('KZP', 'KwaZulu-Natal Division, Pietermaritzburg', 'KwaZulu-Natal Division', 'KwaZulu-Natal Province', 'High Court', FALSE, FALSE),
('KZD', 'KwaZulu-Natal Division, Durban', 'KwaZulu-Natal Division', 'KwaZulu-Natal Province', 'High Court', FALSE, FALSE),
('FS', 'Free State Division, Bloemfontein', 'Free State Division', 'Free State Province', 'High Court', TRUE, FALSE),
('ECG', 'Eastern Cape Division, Grahamstown', 'Eastern Cape Division', 'Eastern Cape Province', 'High Court', FALSE, FALSE),
('ECP', 'Eastern Cape Division, Port Elizabeth', 'Eastern Cape Division', 'Eastern Cape Province', 'High Court', FALSE, FALSE),
('NWM', 'North West Division, Mahikeng', 'North West Division', 'North West Province', 'High Court', FALSE, FALSE),
('LP', 'Limpopo Division, Thohoyandou', 'Limpopo Division', 'Limpopo Province', 'High Court', FALSE, FALSE),
('MP', 'Mpumalanga Division, Nelspruit', 'Mpumalanga Division', 'Mpumalanga Province', 'High Court', FALSE, FALSE),
('NC', 'Northern Cape Division, Kimberley', 'Northern Cape Division', 'Northern Cape Province', 'High Court', FALSE, FALSE)
ON CONFLICT (court_code) DO NOTHING;

-- Insert ZA case types aligned with Court Online
INSERT INTO za_case_types (case_type_code, case_type_name, court_online_category, is_civil, is_criminal) VALUES
('JCM', 'Judicial Case Management', 'Judicial Case Management', TRUE, FALSE),
('CCA', 'Civil and Criminal Appeals', 'Civil and Criminal Appeals', TRUE, TRUE),
('COM', 'Commercial Court', 'Commercial Court', TRUE, FALSE),
('DEF', 'Default Judgements', 'Default Judgements', TRUE, FALSE),
('DIV', 'Divorce Actions', 'Divorce Actions', TRUE, FALSE),
('LTA', 'Leave to Appeal', 'Leave to Appeal', TRUE, TRUE),
('OPM', 'Opposed Motions', 'Opposed Motions', TRUE, FALSE),
('OCT', 'Ordinary Civil Trials', 'Ordinary Civil Trials', TRUE, FALSE),
('R43', 'Rule 43 Applications', 'Rule 43 Applications', TRUE, FALSE),
('SCT', 'Special Civil Trials', 'Special Civil Trials', TRUE, FALSE),
('SPM', 'Special Motions/3rd Court', 'Special Motions/ 3rd Court', TRUE, FALSE),
('SJA', 'Summary Judgement Applications', 'Summary Judgement Applications', TRUE, FALSE),
('TIA', 'Trial Interlocutory Applications', 'Trial Interlocutory Applications', TRUE, FALSE),
('UNM', 'Unopposed Motions', 'Unopposed Motion', TRUE, FALSE)
ON CONFLICT (case_type_code) DO NOTHING;

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_za_cases_case_number ON za_cases(case_number);
CREATE INDEX IF NOT EXISTS idx_za_cases_court_id ON za_cases(court_id);
CREATE INDEX IF NOT EXISTS idx_za_cases_status ON za_cases(status);
CREATE INDEX IF NOT EXISTS idx_za_cases_filing_date ON za_cases(filing_date);
CREATE INDEX IF NOT EXISTS idx_za_cases_court_online_id ON za_cases(court_online_case_id);

CREATE INDEX IF NOT EXISTS idx_za_evidence_bundles_case_id ON za_evidence_bundles(case_id);
CREATE INDEX IF NOT EXISTS idx_za_evidence_bundles_caselines_id ON za_evidence_bundles(caselines_bundle_id);

CREATE INDEX IF NOT EXISTS idx_za_evidence_documents_bundle_id ON za_evidence_documents(bundle_id);
CREATE INDEX IF NOT EXISTS idx_za_evidence_documents_case_id ON za_evidence_documents(case_id);
CREATE INDEX IF NOT EXISTS idx_za_evidence_documents_type ON za_evidence_documents(document_type);

CREATE INDEX IF NOT EXISTS idx_za_court_proceedings_case_id ON za_court_proceedings(case_id);
CREATE INDEX IF NOT EXISTS idx_za_court_proceedings_date ON za_court_proceedings(proceeding_date);

CREATE INDEX IF NOT EXISTS idx_za_electronic_filings_case_id ON za_electronic_filings(case_id);
CREATE INDEX IF NOT EXISTS idx_za_electronic_filings_court_online_id ON za_electronic_filings(court_online_filing_id);
CREATE INDEX IF NOT EXISTS idx_za_electronic_filings_status ON za_electronic_filings(filing_status);

CREATE INDEX IF NOT EXISTS idx_za_audit_trail_case_id ON za_audit_trail(case_id);
CREATE INDEX IF NOT EXISTS idx_za_audit_trail_created_at ON za_audit_trail(created_at);
CREATE INDEX IF NOT EXISTS idx_za_audit_trail_action_type ON za_audit_trail(action_type);
