#!/usr/bin/env python3
"""
Simple test script to verify the ZA Judiciary Integration API works correctly.
"""

import requests
import json
import time
import sys
import os
import threading
import subprocess
from datetime import datetime

def start_server():
    """Start the Flask server in a separate process."""
    os.chdir('/home/runner/work/analyticase/analyticase/za_judiciary_integration/api')
    return subprocess.Popen([
        sys.executable, 'main_za_enhanced.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def test_endpoints():
    """Test all API endpoints."""
    base_url = "http://localhost:5000"
    
    print(f"🧪 Testing API endpoints at {base_url}")
    print("=" * 60)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    test_results = []
    
    # Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            test_results.append(("Health Check", True))
        else:
            print(f"❌ Health check failed: {response.status_code}")
            test_results.append(("Health Check", False))
    except Exception as e:
        print(f"❌ Health check error: {e}")
        test_results.append(("Health Check", False))
    
    # Status endpoint
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ Status endpoint passed")
            test_results.append(("Status", True))
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            test_results.append(("Status", False))
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
        test_results.append(("Status", False))
    
    # ZA Judiciary Courts
    try:
        response = requests.get(f"{base_url}/api/za-judiciary/courts", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ZA Courts endpoint passed - {data.get('total_courts', 0)} courts found")
            test_results.append(("ZA Courts", True))
        else:
            print(f"❌ ZA Courts endpoint failed: {response.status_code}")
            test_results.append(("ZA Courts", False))
    except Exception as e:
        print(f"❌ ZA Courts endpoint error: {e}")
        test_results.append(("ZA Courts", False))
    
    # Case Types
    try:
        response = requests.get(f"{base_url}/api/za-judiciary/case-types", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Case Types endpoint passed - {data.get('total_types', 0)} types found")
            test_results.append(("Case Types", True))
        else:
            print(f"❌ Case Types endpoint failed: {response.status_code}")
            test_results.append(("Case Types", False))
    except Exception as e:
        print(f"❌ Case Types endpoint error: {e}")
        test_results.append(("Case Types", False))
    
    # Create ZA Case
    case_data = {
        "case_number": "(GP) 12345/2025",
        "court_code": "GP",
        "case_type": "COM",
        "title": "Test Financial Fraud Case",
        "plaintiff": {"name": "State vs", "type": "prosecution"},
        "defendant": {"name": "Test Corporation", "type": "corporate"}
    }
    
    try:
        response = requests.post(f"{base_url}/api/za-judiciary/cases", json=case_data, timeout=5)
        if response.status_code == 201:
            print("✅ Create ZA Case endpoint passed")
            test_results.append(("Create Case", True))
        else:
            print(f"❌ Create ZA Case endpoint failed: {response.status_code}")
            test_results.append(("Create Case", False))
    except Exception as e:
        print(f"❌ Create ZA Case endpoint error: {e}")
        test_results.append(("Create Case", False))
    
    # Case number validation
    try:
        response = requests.post(f"{base_url}/api/za-judiciary/validate-case-number", 
                                json={"case_number": "(GP) 12345/2025"}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('is_valid'):
                print("✅ Case number validation passed")
                test_results.append(("Case Validation", True))
            else:
                print("❌ Case number validation failed - invalid number")
                test_results.append(("Case Validation", False))
        else:
            print(f"❌ Case number validation endpoint failed: {response.status_code}")
            test_results.append(("Case Validation", False))
    except Exception as e:
        print(f"❌ Case number validation error: {e}")
        test_results.append(("Case Validation", False))
    
    # Integration status
    try:
        response = requests.get(f"{base_url}/api/za-judiciary/integration-status", timeout=5)
        if response.status_code == 200:
            print("✅ Integration status endpoint passed")
            test_results.append(("Integration Status", True))
        else:
            print(f"❌ Integration status endpoint failed: {response.status_code}")
            test_results.append(("Integration Status", False))
    except Exception as e:
        print(f"❌ Integration status endpoint error: {e}")
        test_results.append(("Integration Status", False))
    
    # Statistics
    try:
        response = requests.get(f"{base_url}/api/statistics", timeout=5)
        if response.status_code == 200:
            print("✅ Statistics endpoint passed")
            test_results.append(("Statistics", True))
        else:
            print(f"❌ Statistics endpoint failed: {response.status_code}")
            test_results.append(("Statistics", False))
    except Exception as e:
        print(f"❌ Statistics endpoint error: {e}")
        test_results.append(("Statistics", False))
    
    # Cases list
    try:
        response = requests.get(f"{base_url}/api/cases", timeout=5)
        if response.status_code == 200:
            print("✅ Cases list endpoint passed")
            test_results.append(("Cases List", True))
        else:
            print(f"❌ Cases list endpoint failed: {response.status_code}")
            test_results.append(("Cases List", False))
    except Exception as e:
        print(f"❌ Cases list endpoint error: {e}")
        test_results.append(("Cases List", False))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the server logs.")
        return False

def main():
    """Main test function."""
    print("🚀 Starting ZA Judiciary Integration API Test")
    print(f"📅 Test run: {datetime.now().isoformat()}")
    
    # Start the server
    server_process = start_server()
    
    try:
        # Run tests
        success = test_endpoints()
        
        if success:
            print("\n✅ All API endpoints are working correctly!")
            print("🔧 Ready for deployment and production use.")
        else:
            print("\n❌ Some API endpoints have issues.")
            print("🔍 Check server logs for more details.")
            
        return success
        
    finally:
        # Stop the server
        print("\n🛑 Stopping test server...")
        server_process.terminate()
        server_process.wait()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)