#!/usr/bin/env python3
"""
Simple test runner for ZA Judiciary Integration without complex imports.
"""

import sys
import os
import unittest
import json
import time
import subprocess
import threading

# Add the API directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'za_judiciary_integration', 'api'))

from za_judiciary_api import ZAJudiciaryIntegration

class MockDatabaseManager:
    """Mock database manager for testing."""
    def get_connection(self, db_type='supabase'):
        return None

class TestZAJudiciaryIntegration(unittest.TestCase):
    """Test the ZA Judiciary Integration functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.db_manager = MockDatabaseManager()
        self.za_integration = ZAJudiciaryIntegration(self.db_manager)
    
    def test_case_number_validation_valid(self):
        """Test valid case number formats."""
        valid_cases = [
            "(GP) 12345/2025",
            "(WCC) 67890/2024",
            "(GJ) 123456/2025",
            "(FS) 9999/2023"
        ]
        
        for case_number in valid_cases:
            with self.subTest(case_number=case_number):
                self.assertTrue(
                    self.za_integration.validate_case_number(case_number),
                    f"Case number {case_number} should be valid"
                )
    
    def test_case_number_validation_invalid(self):
        """Test invalid case number formats."""
        invalid_cases = [
            "GP 12345/2025",      # Missing parentheses
            "(GP) 12345",         # Missing year
            "12345/2025",         # Missing court code
            "(INVALID) 12345/2025", # Court code too long
            "(GP) ABC/2025"       # Non-numeric case number
        ]
        
        for case_number in invalid_cases:
            with self.subTest(case_number=case_number):
                self.assertFalse(
                    self.za_integration.validate_case_number(case_number),
                    f"Case number {case_number} should be invalid"
                )
    
    def test_get_court_divisions(self):
        """Test getting court divisions."""
        courts = self.za_integration.get_court_divisions()
        
        self.assertIsInstance(courts, list)
        self.assertGreater(len(courts), 0)
        
        # Check structure of first court
        court = courts[0]
        required_fields = ['court_code', 'court_name', 'division', 
                          'court_online_enabled', 'caselines_enabled']
        for field in required_fields:
            self.assertIn(field, court, f"Court should have {field} field")
    
    def test_create_court_online_case(self):
        """Test creating a Court Online case."""
        case_data = {
            "case_number": "(GP) 12345/2025",
            "court_code": "GP",
            "case_type": "COM",
            "title": "Test Case",
            "plaintiff": {"name": "Test Plaintiff"},
            "defendant": {"name": "Test Defendant"}
        }
        
        case_record = self.za_integration.create_court_online_case(case_data)
        
        self.assertEqual(case_record['case_number'], case_data['case_number'])
        self.assertEqual(case_record['status'], 'filed')
        self.assertIn('court_online_integration', case_record)
        self.assertIn('caselines_integration', case_record)
        self.assertTrue(case_record['court_online_integration']['enabled'])
    
    def test_create_court_online_case_invalid(self):
        """Test creating an invalid Court Online case."""
        invalid_case_data = {
            "case_number": "(GP) 12345/2025",
            "court_code": "GP"
            # Missing required fields
        }
        
        with self.assertRaises(ValueError):
            self.za_integration.create_court_online_case(invalid_case_data)
    
    def test_create_caselines_bundle(self):
        """Test creating a CaseLines bundle."""
        bundle_data = {
            "bundle_name": "Test Bundle",
            "bundle_type": "pleadings",
            "documents": [
                {"name": "Doc 1", "page_count": 5},
                {"name": "Doc 2", "page_count": 10}
            ]
        }
        
        bundle_record = self.za_integration.create_caselines_bundle("test-case", bundle_data)
        
        self.assertEqual(bundle_record['bundle_name'], bundle_data['bundle_name'])
        self.assertEqual(bundle_record['total_pages'], 15)
        self.assertEqual(bundle_record['total_documents'], 2)
        self.assertEqual(bundle_record['status'], 'draft')


def run_api_integration_tests():
    """Run integration tests against the API."""
    print("🧪 Running API Integration Tests")
    print("=" * 50)
    
    # Start the API server
    server_process = None
    try:
        os.chdir(os.path.join(os.path.dirname(__file__), 'za_judiciary_integration', 'api'))
        server_process = subprocess.Popen([
            sys.executable, 'main_za_enhanced.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Run the existing API test
        os.chdir(os.path.dirname(__file__))
        result = subprocess.run([sys.executable, 'test_api.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ API Integration Tests: PASSED")
            return True
        else:
            print("❌ API Integration Tests: FAILED")
            print(result.stdout)
            print(result.stderr)
            return False
            
    finally:
        if server_process:
            server_process.terminate()
            server_process.wait()


def main():
    """Main test function."""
    print("🚀 Running ZA Judiciary Integration Tests")
    print("📅 Test run: {}".format(time.strftime('%Y-%m-%d %H:%M:%S')))
    print("=" * 60)
    
    # Run unit tests
    print("🔬 Running Unit Tests")
    unittest_result = unittest.main(
        module=__name__, 
        argv=['test'], 
        exit=False, 
        verbosity=2
    )
    
    unit_tests_passed = unittest_result.result.wasSuccessful()
    
    print("\n" + "=" * 60)
    
    # Run API integration tests
    api_tests_passed = run_api_integration_tests()
    
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    print(f"Unit Tests: {'✅ PASSED' if unit_tests_passed else '❌ FAILED'}")
    print(f"API Tests:  {'✅ PASSED' if api_tests_passed else '❌ FAILED'}")
    
    overall_success = unit_tests_passed and api_tests_passed
    
    if overall_success:
        print("\n🎉 All tests passed! The ZA Judiciary Integration is working correctly.")
        print("🔧 Ready for production deployment.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)