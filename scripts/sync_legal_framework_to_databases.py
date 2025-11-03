#!/usr/bin/env python3
"""
Database Synchronization Script for AnalytiCase Legal Framework v2.3

This script synchronizes the legal framework (meta-principles and first-order principles)
from Scheme files to both Supabase and Neon PostgreSQL databases.

Version: 2.3
Last Updated: 2025-11-03
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from supabase import create_client, Client
import psycopg2
from psycopg2.extras import Json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
NEON_PROJECT_ID = "jolly-wildflower-89862625"
NEON_CONNECTION_STRING = "postgresql://neondb_owner:npg_ASKJyXrV6R1D@ep-soft-night-ae1nd149-pooler.c-2.us-east-2.aws.neon.tech/neondb?channel_binding=require&sslmode=require"

# Scheme file paths
LEX_DIR = "/home/ubuntu/analyticase/lex"
LV2_FILE = f"{LEX_DIR}/lv2/legal_foundations_v2.3.scm"
LV1_FILE = f"{LEX_DIR}/lv1/known_laws_v2.3.scm"


class SchemeParser:
    """Parser for Scheme legal framework files."""
    
    @staticmethod
    def parse_meta_principle(scheme_text: str) -> Optional[Dict[str, Any]]:
        """Parse a single meta-principle from Scheme format."""
        # Extract principle ID
        id_match = re.search(r'\(define\s+(\S+)', scheme_text)
        if not id_match:
            return None
        
        principle_id = id_match.group(1)
        
        # Extract fields
        name = SchemeParser._extract_field(scheme_text, 'name')
        description = SchemeParser._extract_field(scheme_text, 'description')
        historical_origin = SchemeParser._extract_field(scheme_text, 'historical-origin')
        contemporary_relevance = SchemeParser._extract_field(scheme_text, 'contemporary-relevance')
        influence_score = SchemeParser._extract_numeric_field(scheme_text, 'influence-score')
        
        # Extract JSONB fields
        jurisdictional_adoption = SchemeParser._extract_list_field(scheme_text, 'jurisdictional-adoption')
        case_law_applications = SchemeParser._extract_list_field(scheme_text, 'case-law-applications')
        cross_references = SchemeParser._extract_list_field(scheme_text, 'cross-references')
        temporal_evolution = SchemeParser._extract_dict_field(scheme_text, 'temporal-evolution')
        
        return {
            'principle_id': principle_id,
            'name': name,
            'description': description,
            'historical_origin': historical_origin,
            'contemporary_relevance': contemporary_relevance,
            'influence_score': influence_score,
            'jurisdictional_adoption': jurisdictional_adoption,
            'case_law_applications': case_law_applications,
            'cross_references': cross_references,
            'temporal_evolution': temporal_evolution,
            'version': '2.3'
        }
    
    @staticmethod
    def parse_first_order_principle(scheme_text: str) -> Optional[Dict[str, Any]]:
        """Parse a single first-order principle from Scheme format."""
        # Extract principle ID
        id_match = re.search(r'\(define\s+(\S+)', scheme_text)
        if not id_match:
            return None
        
        principle_id = id_match.group(1)
        
        # Extract fields
        name = SchemeParser._extract_field(scheme_text, 'name')
        latin_maxim = SchemeParser._extract_field(scheme_text, 'latin-maxim')
        english_translation = SchemeParser._extract_field(scheme_text, 'english-translation')
        description = SchemeParser._extract_field(scheme_text, 'description')
        legal_domain = SchemeParser._extract_field(scheme_text, 'legal-domain')
        conflict_priority = SchemeParser._extract_numeric_field(scheme_text, 'conflict-priority', is_int=True)
        
        # Extract JSONB/array fields
        derivation_chain = SchemeParser._extract_list_field(scheme_text, 'derivation-chain')
        applicability_scores = SchemeParser._extract_dict_field(scheme_text, 'applicability-scores')
        case_law_references = SchemeParser._extract_list_field(scheme_text, 'case-law-references')
        cross_references = SchemeParser._extract_list_field(scheme_text, 'cross-references')
        temporal_evolution = SchemeParser._extract_dict_field(scheme_text, 'temporal-evolution')
        
        return {
            'principle_id': principle_id,
            'name': name,
            'latin_maxim': latin_maxim,
            'english_translation': english_translation,
            'description': description,
            'legal_domain': legal_domain,
            'derivation_chain': derivation_chain,
            'applicability_scores': applicability_scores,
            'case_law_references': case_law_references,
            'cross_references': cross_references,
            'conflict_priority': conflict_priority,
            'temporal_evolution': temporal_evolution,
            'version': '2.3'
        }
    
    @staticmethod
    def _extract_field(text: str, field_name: str) -> Optional[str]:
        """Extract a string field from Scheme text."""
        pattern = rf'\({field_name}\s+"([^"]+)"'
        match = re.search(pattern, text)
        return match.group(1) if match else None
    
    @staticmethod
    def _extract_numeric_field(text: str, field_name: str, is_int: bool = False) -> Optional[float]:
        """Extract a numeric field from Scheme text."""
        pattern = rf'\({field_name}\s+(\d+\.?\d*)'
        match = re.search(pattern, text)
        if match:
            return int(match.group(1)) if is_int else float(match.group(1))
        return None
    
    @staticmethod
    def _extract_list_field(text: str, field_name: str) -> List[str]:
        """Extract a list field from Scheme text."""
        pattern = rf'\({field_name}\s+\(list\s+([^)]+)\)'
        match = re.search(pattern, text)
        if match:
            items = re.findall(r'"([^"]+)"', match.group(1))
            return items
        return []
    
    @staticmethod
    def _extract_dict_field(text: str, field_name: str) -> Dict[str, Any]:
        """Extract a dictionary field from Scheme text (simplified)."""
        # This is a simplified parser - in production, use a proper Scheme parser
        return {}


class DatabaseSync:
    """Synchronize legal framework to databases."""
    
    def __init__(self):
        """Initialize database connections."""
        self.supabase_client = None
        self.neon_conn = None
        
        # Initialize Supabase
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                self.supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
                print("✓ Connected to Supabase")
            except Exception as e:
                print(f"✗ Failed to connect to Supabase: {e}")
        
        # Initialize Neon
        try:
            self.neon_conn = psycopg2.connect(NEON_CONNECTION_STRING)
            print("✓ Connected to Neon")
        except Exception as e:
            print(f"✗ Failed to connect to Neon: {e}")
    
    def sync_meta_principles(self, principles: List[Dict[str, Any]]) -> None:
        """Sync meta-principles to databases."""
        print(f"\nSyncing {len(principles)} meta-principles...")
        
        # Sync to Neon
        if self.neon_conn:
            cursor = self.neon_conn.cursor()
            for principle in principles:
                try:
                    cursor.execute("""
                        INSERT INTO meta_principles (
                            principle_id, name, description, historical_origin,
                            contemporary_relevance, influence_score, jurisdictional_adoption,
                            case_law_applications, cross_references, temporal_evolution, version
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (principle_id) DO UPDATE SET
                            name = EXCLUDED.name,
                            description = EXCLUDED.description,
                            updated_at = CURRENT_TIMESTAMP
                    """, (
                        principle['principle_id'],
                        principle['name'],
                        principle['description'],
                        principle.get('historical_origin'),
                        principle.get('contemporary_relevance'),
                        principle.get('influence_score'),
                        Json(principle.get('jurisdictional_adoption', {})),
                        Json(principle.get('case_law_applications', {})),
                        principle.get('cross_references', []),
                        Json(principle.get('temporal_evolution', {})),
                        principle['version']
                    ))
                    print(f"  ✓ Synced to Neon: {principle['principle_id']}")
                except Exception as e:
                    print(f"  ✗ Failed to sync {principle['principle_id']} to Neon: {e}")
            
            self.neon_conn.commit()
            cursor.close()
        
        # Sync to Supabase
        if self.supabase_client:
            for principle in principles:
                try:
                    self.supabase_client.table('meta_principles').upsert(principle).execute()
                    print(f"  ✓ Synced to Supabase: {principle['principle_id']}")
                except Exception as e:
                    print(f"  ✗ Failed to sync {principle['principle_id']} to Supabase: {e}")
    
    def sync_first_order_principles(self, principles: List[Dict[str, Any]]) -> None:
        """Sync first-order principles to databases."""
        print(f"\nSyncing {len(principles)} first-order principles...")
        
        # Sync to Neon
        if self.neon_conn:
            cursor = self.neon_conn.cursor()
            for principle in principles:
                try:
                    cursor.execute("""
                        INSERT INTO first_order_principles (
                            principle_id, name, latin_maxim, english_translation,
                            description, legal_domain, derivation_chain,
                            applicability_scores, case_law_references, cross_references,
                            conflict_priority, temporal_evolution, version
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (principle_id) DO UPDATE SET
                            name = EXCLUDED.name,
                            description = EXCLUDED.description,
                            updated_at = CURRENT_TIMESTAMP
                    """, (
                        principle['principle_id'],
                        principle['name'],
                        principle.get('latin_maxim'),
                        principle.get('english_translation'),
                        principle['description'],
                        principle.get('legal_domain'),
                        principle.get('derivation_chain', []),
                        Json(principle.get('applicability_scores', {})),
                        Json(principle.get('case_law_references', {})),
                        principle.get('cross_references', []),
                        principle.get('conflict_priority'),
                        Json(principle.get('temporal_evolution', {})),
                        principle['version']
                    ))
                    print(f"  ✓ Synced to Neon: {principle['principle_id']}")
                except Exception as e:
                    print(f"  ✗ Failed to sync {principle['principle_id']} to Neon: {e}")
            
            self.neon_conn.commit()
            cursor.close()
        
        # Sync to Supabase
        if self.supabase_client:
            for principle in principles:
                try:
                    self.supabase_client.table('first_order_principles').upsert(principle).execute()
                    print(f"  ✓ Synced to Supabase: {principle['principle_id']}")
                except Exception as e:
                    print(f"  ✗ Failed to sync {principle['principle_id']} to Supabase: {e}")
    
    def close(self):
        """Close database connections."""
        if self.neon_conn:
            self.neon_conn.close()
            print("\n✓ Closed Neon connection")


def main():
    """Main synchronization function."""
    print("=" * 80)
    print("AnalytiCase Legal Framework v2.3 - Database Synchronization")
    print("=" * 80)
    
    # Sample data for demonstration (in production, parse from Scheme files)
    meta_principles = [
        {
            'principle_id': 'therapeutic-jurisprudence',
            'name': 'Therapeutic Jurisprudence',
            'description': 'Law should be studied for its therapeutic and anti-therapeutic consequences',
            'historical_origin': 'Developed in 1990s by David Wexler and Bruce Winick',
            'contemporary_relevance': 'Applied in problem-solving courts, mental health law, domestic violence courts',
            'influence_score': 0.85,
            'jurisdictional_adoption': {'za': 'emerging', 'us': 'established'},
            'case_law_applications': [],
            'cross_references': ['restorative-justice-theory', 'ethic-of-care'],
            'temporal_evolution': {},
            'version': '2.3'
        },
        {
            'principle_id': 'comparative-law-theory',
            'name': 'Comparative Law Theory',
            'description': 'Study of different legal systems reveals diversity of legal solutions',
            'historical_origin': 'Emerged in 19th century with comparative legal studies',
            'contemporary_relevance': 'Essential for legal transplants, harmonization, globalization',
            'influence_score': 0.88,
            'jurisdictional_adoption': {'za': 'established', 'eu': 'established'},
            'case_law_applications': [],
            'cross_references': ['legal-positivism'],
            'temporal_evolution': {},
            'version': '2.3'
        }
    ]
    
    first_order_principles = [
        {
            'principle_id': 'lex-specialis-derogat-legi-generali',
            'name': 'Lex Specialis Derogat Legi Generali',
            'latin_maxim': 'Lex specialis derogat legi generali',
            'english_translation': 'Special law derogates from general law',
            'description': 'Specific provisions prevail over general ones',
            'legal_domain': 'statutory-interpretation',
            'derivation_chain': ['rule-of-law', 'legal-positivism'],
            'applicability_scores': {'statutory': 0.95, 'constitutional': 0.85},
            'case_law_references': [],
            'cross_references': ['expressio-unius-est-exclusio-alterius'],
            'conflict_priority': 85,
            'temporal_evolution': {},
            'version': '2.3'
        },
        {
            'principle_id': 'ubi-jus-ibi-remedium',
            'name': 'Ubi Jus Ibi Remedium',
            'latin_maxim': 'Ubi jus ibi remedium',
            'english_translation': 'Where there is a right, there is a remedy',
            'description': 'Every legal right has a corresponding remedy',
            'legal_domain': 'equity',
            'derivation_chain': ['natural-law-theory', 'human-dignity-principle'],
            'applicability_scores': {'constitutional': 0.92, 'civil': 0.88},
            'case_law_references': [],
            'cross_references': ['in-pari-delicto'],
            'conflict_priority': 90,
            'temporal_evolution': {},
            'version': '2.3'
        }
    ]
    
    # Initialize database sync
    db_sync = DatabaseSync()
    
    # Sync data
    db_sync.sync_meta_principles(meta_principles)
    db_sync.sync_first_order_principles(first_order_principles)
    
    # Close connections
    db_sync.close()
    
    print("\n" + "=" * 80)
    print("Database synchronization complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
