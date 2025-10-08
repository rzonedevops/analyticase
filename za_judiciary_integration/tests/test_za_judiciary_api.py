#!/usr/bin/env python3
"""
Comprehensive tests for ZA Judiciary Integration API.
"""

import pytest
import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main_za_enhanced import app, db_manager
from api.za_judiciary_api import ZAJudiciaryIntegration

class TestZAJudiciaryAPI:
    """Test suite for ZA Judiciary Integration API."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def za_integration(self):
        """Create ZA integration instance for testing."""
        return ZAJudiciaryIntegration(db_manager)
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'za_judiciary_integration' in data
        assert data['za_judiciary_integration']['court_online'] is True
    
    def test_system_status(self, client):
        """Test system status endpoint."""
        response = client.get('/api/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'online'
        assert 'za_judiciary_integration' in data['components']
        assert 'court_online' in data['components']['za_judiciary_integration']
    
    def test_za_courts_endpoint(self, client):
        """Test ZA courts listing endpoint."""
        response = client.get('/api/za-judiciary/courts')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'courts' in data
        assert data['total_courts'] > 0
        assert data['court_online_enabled'] > 0
        
        # Check first court structure
        court = data['courts'][0]
        required_fields = ['court_code', 'court_name', 'division', 'court_online_enabled']
        for field in required_fields:
            assert field in court
    
    def test_case_types_endpoint(self, client):
        """Test case types endpoint."""
        response = client.get('/api/za-judiciary/case-types')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'case_types' in data
        assert data['total_types'] > 0
        
        # Check case type structure
        case_type = data['case_types'][0]
        required_fields = ['code', 'name', 'court_online_category']
        for field in required_fields:
            assert field in case_type
    
    def test_case_number_validation_valid(self, client):
        """Test case number validation with valid numbers."""
        valid_numbers = [
            "(GP) 12345/2025",
            "(WCC) 67890/2024", 
            "(GJ) 123456/2025",
            "(FS) 9999/2023"
        ]
        
        for case_number in valid_numbers:
            response = client.post('/api/za-judiciary/validate-case-number',
                                 json={'case_number': case_number})
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['is_valid'] is True
    
    def test_case_number_validation_invalid(self, client):
        """Test case number validation with invalid numbers."""
        invalid_numbers = [
            "GP 12345/2025",  # Missing parentheses
            "(GP) 12345",     # Missing year
            "12345/2025",     # Missing court code
            "(INVALID) 12345/2025",  # Invalid court code format
            "(GP) ABC/2025"   # Non-numeric case number
        ]
        
        for case_number in invalid_numbers:
            response = client.post('/api/za-judiciary/validate-case-number',
                                 json={'case_number': case_number})
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['is_valid'] is False
    
    def test_create_za_case_valid(self, client):
        """Test creating a valid ZA case."""
        case_data = {
            "case_number": "(GP) 12345/2025",
            "court_code": "GP",
            "case_type": "COM",
            "title": "Test Commercial Case", 
            "plaintiff": {"name": "Test Plaintiff", "type": "individual"},
            "defendant": {"name": "Test Defendant", "type": "corporate"}
        }
        
        response = client.post('/api/za-judiciary/cases', json=case_data)
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'case' in data
        
        case = data['case']
        assert case['case_number'] == case_data['case_number']
        assert case['court_code'] == case_data['court_code']
        assert 'court_online_integration' in case
        assert 'caselines_integration' in case
    
    def test_create_za_case_invalid(self, client):
        """Test creating an invalid ZA case."""
        # Missing required fields
        invalid_case_data = {
            "case_number": "(GP) 12345/2025",
            "court_code": "GP"
            # Missing other required fields
        }
        
        response = client.post('/api/za-judiciary/cases', json=invalid_case_data)
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['error'] is True
        assert 'Missing required field' in data['message']
    
    def test_create_caselines_bundle(self, client):
        """Test creating a CaseLines evidence bundle."""
        bundle_data = {
            "bundle_name": "Test Discovery Bundle",
            "bundle_type": "discovery",
            "documents": [
                {"name": "Document 1", "page_count": 10},
                {"name": "Document 2", "page_count": 15}
            ]
        }
        
        response = client.post('/api/za-judiciary/cases/test-case-123/bundles', 
                             json=bundle_data)
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'bundle' in data
        
        bundle = data['bundle']
        assert bundle['bundle_name'] == bundle_data['bundle_name']
        assert bundle['total_pages'] == 25  # Sum of page counts
        assert bundle['total_documents'] == 2
    
    def test_court_online_status(self, client):
        """Test Court Online status endpoint."""
        response = client.get('/api/za-judiciary/cases/test-case/court-online-status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'court_online_enabled' in data
        assert 'e_filing_enabled' in data
        assert 'sync_status' in data
    
    def test_caselines_status(self, client):
        """Test CaseLines status endpoint."""
        response = client.get('/api/za-judiciary/cases/test-case/caselines-status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'caselines_enabled' in data
        assert 'evidence_management_enabled' in data
        assert 'total_bundles' in data
    
    def test_electronic_filing(self, client):
        """Test electronic filing submission."""
        filing_data = {
            "case_id": "test-case-123",
            "filing_type": "Summons",
            "documents": ["summons.pdf", "particulars.pdf"],
            "filing_fee": 500.00,
            "payment_reference": "PAY123456"
        }
        
        response = client.post('/api/za-judiciary/electronic-filing', json=filing_data)
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'filing' in data
        
        filing = data['filing']
        assert filing['filing_type'] == filing_data['filing_type']
        assert filing['status'] == 'submitted'
        assert 'court_online_filing_id' in filing
    
    def test_integration_status(self, client):
        """Test overall integration status endpoint."""
        response = client.get('/api/za-judiciary/integration-status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'court_online' in data
        assert 'caselines' in data
        assert 'compliance' in data
        
        # Check Court Online status
        assert data['court_online']['status'] == 'operational'
        assert 'enabled_courts' in data['court_online']
        
        # Check CaseLines status
        assert data['caselines']['status'] == 'operational'
        assert 'total_bundles' in data['caselines']
        
        # Check compliance
        assert data['compliance']['electronic_filing_act_compliant'] is True
    
    def test_statistics_endpoint(self, client):
        """Test statistics endpoint."""
        response = client.get('/api/statistics')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        required_fields = ['active_cases', 'za_cases', 'entities_analyzed', 
                          'caselines_bundles', 'court_online_filings']
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], (int, float))
    
    def test_cases_list(self, client):
        """Test cases list endpoint."""
        response = client.get('/api/cases')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        
        if len(data) > 0:
            case = data[0]
            required_fields = ['id', 'case_number', 'title', 'status', 
                             'court_online_enabled', 'caselines_enabled']
            for field in required_fields:
                assert field in case
    
    def test_case_za_integration(self, client):
        """Test case ZA integration details endpoint."""
        response = client.get('/api/case/test-case-123/za-integration')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'court_online' in data
        assert 'caselines' in data
        assert 'compliance' in data
        
        # Check Court Online integration
        co_data = data['court_online']
        assert co_data['enabled'] is True
        assert 'filing_history' in co_data
        
        # Check CaseLines integration
        cl_data = data['caselines']
        assert cl_data['enabled'] is True
        assert 'bundles' in cl_data
    
    def test_court_online_filing(self, client):
        """Test Court Online filing submission."""
        filing_data = {
            "filing_type": "Motion",
            "documents": ["motion.pdf", "supporting_affidavit.pdf"],
            "filing_fee": 750.00
        }
        
        response = client.post('/api/case/test-case-123/court-online-filing', 
                             json=filing_data)
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'filing' in data
        
        filing = data['filing']
        assert filing['filing_type'] == filing_data['filing_type']
        assert 'court_online_reference' in filing
    
    def test_compliance_report(self, client):
        """Test ZA compliance report generation."""
        response = client.get('/api/za-compliance-report')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'compliance_areas' in data
        assert 'overall_score' in data
        assert 'certification_status' in data
        
        # Check compliance areas
        areas = data['compliance_areas']
        required_areas = ['electronic_filing_act', 'court_rules', 'data_protection']
        for area in required_areas:
            assert area in areas
            assert 'compliant' in areas[area]
            assert 'score' in areas[area]


class TestZAJudiciaryIntegration:
    """Test suite for ZAJudiciaryIntegration class."""
    
    @pytest.fixture
    def za_integration(self):
        """Create ZA integration instance for testing."""
        return ZAJudiciaryIntegration(db_manager)
    
    def test_validate_case_number(self, za_integration):
        """Test case number validation logic."""
        # Valid case numbers
        valid_cases = [
            "(GP) 12345/2025",
            "(WCC) 67890/2024",
            "(GJ) 123456/2025"
        ]
        
        for case_number in valid_cases:
            assert za_integration.validate_case_number(case_number) is True
        
        # Invalid case numbers
        invalid_cases = [
            "GP 12345/2025",      # No parentheses
            "(GP) 12345",         # No year
            "12345/2025",         # No court code
            "(TOOLONG) 12345/2025"  # Court code too long
        ]
        
        for case_number in invalid_cases:
            assert za_integration.validate_case_number(case_number) is False
    
    def test_get_court_divisions(self, za_integration):
        """Test getting court divisions."""
        courts = za_integration.get_court_divisions()
        
        assert isinstance(courts, list)
        assert len(courts) > 0
        
        # Check structure of first court
        court = courts[0]
        required_fields = ['court_code', 'court_name', 'division', 
                          'court_online_enabled', 'caselines_enabled']
        for field in required_fields:
            assert field in court
    
    def test_create_court_online_case(self, za_integration):
        """Test creating a Court Online case."""
        case_data = {
            "case_number": "(GP) 12345/2025",
            "court_code": "GP", 
            "case_type": "COM",
            "title": "Test Case",
            "plaintiff": {"name": "Test Plaintiff"},
            "defendant": {"name": "Test Defendant"}
        }
        
        case_record = za_integration.create_court_online_case(case_data)
        
        assert case_record['case_number'] == case_data['case_number']
        assert case_record['status'] == 'filed'
        assert 'court_online_integration' in case_record
        assert 'caselines_integration' in case_record
        assert case_record['court_online_integration']['enabled'] is True
    
    def test_create_caselines_bundle(self, za_integration):
        """Test creating a CaseLines bundle."""
        bundle_data = {
            "bundle_name": "Test Bundle",
            "bundle_type": "pleadings",
            "documents": [
                {"name": "Doc 1", "page_count": 5},
                {"name": "Doc 2", "page_count": 10}
            ]
        }
        
        bundle_record = za_integration.create_caselines_bundle("test-case", bundle_data)
        
        assert bundle_record['bundle_name'] == bundle_data['bundle_name']
        assert bundle_record['total_pages'] == 15
        assert bundle_record['total_documents'] == 2
        assert bundle_record['status'] == 'draft'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])