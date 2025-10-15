#!/usr/bin/env python3
"""
Tests for Legal Framework Integration

This module tests the integration of all legal frameworks from the lex/ directory
with the HypergraphQL engine.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.ggmlex.hypergraphql import (
    HypergraphQLEngine, LegalNodeType
)


def test_all_frameworks_loaded():
    """Test that all legal frameworks are loaded."""
    print("Testing: All legal frameworks loaded...")
    
    engine = HypergraphQLEngine()
    
    # Should have loaded principles from all 8 frameworks
    result = engine.query_nodes(node_type=LegalNodeType.PRINCIPLE)
    
    assert len(result) > 700, f"Expected > 700 principles, got {len(result)}"
    print(f"✓ Loaded {len(result)} legal principles from all frameworks")
    

def test_civil_law_loaded():
    """Test that civil law framework is loaded."""
    print("\nTesting: Civil law framework loaded...")
    
    engine = HypergraphQLEngine()
    
    # Search for contract-related principles
    result = engine.query_by_content("contract")
    
    assert len(result) > 0, "No contract-related principles found"
    print(f"✓ Found {len(result)} contract-related principles")
    

def test_criminal_law_loaded():
    """Test that criminal law framework is loaded."""
    print("\nTesting: Criminal law framework loaded...")
    
    engine = HypergraphQLEngine()
    
    # Search for criminal law principles (using "actus" which is in cri framework)
    result = engine.query_by_content("actus")
    
    assert len(result) > 0, "No criminal law principles found"
    print(f"✓ Found {len(result)} criminal law principles")


def test_constitutional_law_loaded():
    """Test that constitutional law framework is loaded."""
    print("\nTesting: Constitutional law framework loaded...")
    
    engine = HypergraphQLEngine()
    
    # Search for constitutional principles
    result = engine.query_by_content("right")
    
    assert len(result) > 0, "No constitutional rights principles found"
    print(f"✓ Found {len(result)} constitutional principles")


def test_labour_law_loaded():
    """Test that labour law framework is loaded."""
    print("\nTesting: Labour law framework loaded...")
    
    engine = HypergraphQLEngine()
    
    # Search for labour law principles (using dismissal which is in lab framework)
    result = engine.query_by_content("dismissal")
    
    assert len(result) > 0, "No labour law principles found"
    print(f"✓ Found {len(result)} labour law principles")


def test_environmental_law_loaded():
    """Test that environmental law framework is loaded."""
    print("\nTesting: Environmental law framework loaded...")
    
    engine = HypergraphQLEngine()
    
    # Search for environmental principles
    result = engine.query_by_content("environment")
    
    assert len(result) > 0, "No environmental law principles found"
    print(f"✓ Found {len(result)} environmental law principles")


def test_administrative_law_loaded():
    """Test that administrative law framework is loaded."""
    print("\nTesting: Administrative law framework loaded...")
    
    engine = HypergraphQLEngine()
    
    # Search for administrative principles
    result = engine.query_by_content("administrative")
    
    assert len(result) > 0, "No administrative law principles found"
    print(f"✓ Found {len(result)} administrative law principles")


def test_construction_law_loaded():
    """Test that construction law framework is loaded."""
    print("\nTesting: Construction law framework loaded...")
    
    engine = HypergraphQLEngine()
    
    # Search for construction law principles
    result = engine.query_by_content("construction")
    
    assert len(result) > 0, "No construction law principles found"
    print(f"✓ Found {len(result)} construction law principles")


def test_international_law_loaded():
    """Test that international law framework is loaded."""
    print("\nTesting: International law framework loaded...")
    
    engine = HypergraphQLEngine()
    
    # Search for international law principles
    result = engine.query_by_content("international")
    
    assert len(result) > 0, "No international law principles found"
    print(f"✓ Found {len(result)} international law principles")


def test_framework_statistics():
    """Test getting statistics about loaded frameworks."""
    print("\nTesting: Framework statistics...")
    
    engine = HypergraphQLEngine()
    stats = engine.get_statistics()
    
    assert stats['num_nodes'] > 700, f"Expected > 700 nodes, got {stats['num_nodes']}"
    assert 'principle' in stats['node_types'], "Principle node type not found"
    
    print(f"✓ Total nodes: {stats['num_nodes']}")
    print(f"✓ Node types: {stats['node_types']}")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("Legal Framework Integration Tests")
    print("=" * 70)
    
    tests = [
        test_all_frameworks_loaded,
        test_civil_law_loaded,
        test_criminal_law_loaded,
        test_constitutional_law_loaded,
        test_labour_law_loaded,
        test_environmental_law_loaded,
        test_administrative_law_loaded,
        test_construction_law_loaded,
        test_international_law_loaded,
        test_framework_statistics
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
