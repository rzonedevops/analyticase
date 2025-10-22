#!/usr/bin/env python3
"""
Lex Scheme Database Manager

This script provides utilities for managing the Lex Scheme database,
including schema deployment, data loading, and synchronization.
"""

import os
import logging
import psycopg2
from psycopg2.extras import Json, execute_values
from typing import Dict, Any, List, Optional
from pathlib import Path
from supabase import create_client, Client
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LexDatabaseManager:
    """Manager for Lex Scheme database operations."""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            connection_string: PostgreSQL connection string
        """
        self.connection_string = connection_string
        self.conn = None
        self.supabase_client: Optional[Client] = None
        
        # Initialize Supabase if credentials are available
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if supabase_url and supabase_key:
            self.supabase_client = create_client(supabase_url, supabase_key)
            logger.info("Supabase client initialized")
    
    def connect(self, connection_string: Optional[str] = None):
        """
        Connect to the database.
        
        Args:
            connection_string: PostgreSQL connection string
        """
        conn_str = connection_string or self.connection_string
        
        if not conn_str:
            raise ValueError("No connection string provided")
        
        try:
            self.conn = psycopg2.connect(conn_str)
            logger.info("Connected to database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.conn:
            self.conn.close()
            logger.info("Disconnected from database")
    
    def deploy_schema(self, schema_file: str):
        """
        Deploy the Lex Scheme schema to the database.
        
        Args:
            schema_file: Path to the SQL schema file
        """
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        schema_path = Path(schema_file)
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        try:
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            cursor = self.conn.cursor()
            cursor.execute(schema_sql)
            self.conn.commit()
            cursor.close()
            
            logger.info(f"Schema deployed successfully from {schema_file}")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to deploy schema: {e}")
            raise
    
    def insert_legal_node(
        self,
        node_id: str,
        node_type: str,
        name: str,
        content: str = "",
        jurisdiction: str = "za",
        metadata: Optional[Dict[str, Any]] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Insert a legal node into the database.
        
        Args:
            node_id: Unique node identifier
            node_type: Type of legal node
            name: Node name
            content: Node content
            jurisdiction: Jurisdiction code
            metadata: Additional metadata
            properties: Node properties
            
        Returns:
            True if successful, False otherwise
        """
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO lex_nodes (node_id, node_type, name, content, jurisdiction, metadata, properties)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (node_id) DO UPDATE
                SET name = EXCLUDED.name,
                    content = EXCLUDED.content,
                    metadata = EXCLUDED.metadata,
                    properties = EXCLUDED.properties,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                node_id, node_type, name, content, jurisdiction,
                Json(metadata or {}), Json(properties or {})
            ))
            self.conn.commit()
            cursor.close()
            
            logger.info(f"Inserted/updated legal node: {node_id}")
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert legal node: {e}")
            return False
    
    def insert_statute(
        self,
        statute_id: str,
        name: str,
        statute_number: str,
        short_title: str,
        enactment_date: Optional[str] = None,
        effective_date: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        Insert a statute into the database.
        
        Args:
            statute_id: Unique statute identifier
            name: Statute name
            statute_number: Official statute number
            short_title: Short title
            enactment_date: Date of enactment
            effective_date: Date when statute became effective
            **kwargs: Additional arguments for lex_nodes
            
        Returns:
            True if successful, False otherwise
        """
        # First insert into lex_nodes
        if not self.insert_legal_node(statute_id, 'statute', name, **kwargs):
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO lex_statutes (statute_id, statute_number, short_title, enactment_date, effective_date)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (statute_id) DO UPDATE
                SET statute_number = EXCLUDED.statute_number,
                    short_title = EXCLUDED.short_title,
                    enactment_date = EXCLUDED.enactment_date,
                    effective_date = EXCLUDED.effective_date,
                    updated_at = CURRENT_TIMESTAMP
            """, (statute_id, statute_number, short_title, enactment_date, effective_date))
            self.conn.commit()
            cursor.close()
            
            logger.info(f"Inserted/updated statute: {statute_id}")
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert statute: {e}")
            return False
    
    def insert_case(
        self,
        case_id: str,
        case_number: str,
        case_name: str,
        citation: Optional[str] = None,
        decision_date: Optional[str] = None,
        outcome: Optional[str] = None,
        is_precedent: bool = False,
        **kwargs
    ) -> bool:
        """
        Insert a legal case into the database.
        
        Args:
            case_id: Unique case identifier
            case_number: Official case number
            case_name: Case name
            citation: Case citation
            decision_date: Date of decision
            outcome: Case outcome
            is_precedent: Whether this is a precedent case
            **kwargs: Additional arguments for lex_nodes
            
        Returns:
            True if successful, False otherwise
        """
        # First insert into lex_nodes
        if not self.insert_legal_node(case_id, 'case', case_name, **kwargs):
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO lex_cases (case_id, case_number, case_name, citation, decision_date, outcome, is_precedent)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (case_id) DO UPDATE
                SET case_number = EXCLUDED.case_number,
                    case_name = EXCLUDED.case_name,
                    citation = EXCLUDED.citation,
                    decision_date = EXCLUDED.decision_date,
                    outcome = EXCLUDED.outcome,
                    is_precedent = EXCLUDED.is_precedent,
                    updated_at = CURRENT_TIMESTAMP
            """, (case_id, case_number, case_name, citation, decision_date, outcome, is_precedent))
            self.conn.commit()
            cursor.close()
            
            logger.info(f"Inserted/updated case: {case_id}")
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert case: {e}")
            return False
    
    def insert_hyperedge(
        self,
        edge_id: str,
        relation_type: str,
        node_ids: List[str],
        weight: float = 1.0,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Insert a hyperedge into the database.
        
        Args:
            edge_id: Unique edge identifier
            relation_type: Type of relationship
            node_ids: List of node IDs connected by this edge
            weight: Edge weight
            confidence: Confidence score
            metadata: Additional metadata
            
        Returns:
            True if successful, False otherwise
        """
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO lex_hyperedges (edge_id, relation_type, node_ids, weight, confidence, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (edge_id) DO UPDATE
                SET relation_type = EXCLUDED.relation_type,
                    node_ids = EXCLUDED.node_ids,
                    weight = EXCLUDED.weight,
                    confidence = EXCLUDED.confidence,
                    metadata = EXCLUDED.metadata,
                    updated_at = CURRENT_TIMESTAMP
            """, (edge_id, relation_type, node_ids, weight, confidence, Json(metadata or {})))
            self.conn.commit()
            cursor.close()
            
            logger.info(f"Inserted/updated hyperedge: {edge_id}")
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert hyperedge: {e}")
            return False
    
    def create_lex_ad_mapping(
        self,
        lex_node_id: str,
        ad_entity_type: str,
        ad_entity_id: str,
        mapping_type: str,
        confidence: float = 1.0
    ) -> bool:
        """
        Create a mapping between Lex node and AnalytiCase entity.
        
        Args:
            lex_node_id: Lex node identifier
            ad_entity_type: AnalytiCase entity type
            ad_entity_id: AnalytiCase entity identifier
            mapping_type: Type of mapping
            confidence: Confidence score
            
        Returns:
            True if successful, False otherwise
        """
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO lex_ad_mappings (lex_node_id, ad_entity_type, ad_entity_id, mapping_type, confidence)
                VALUES (%s, %s, %s, %s, %s)
            """, (lex_node_id, ad_entity_type, ad_entity_id, mapping_type, confidence))
            self.conn.commit()
            cursor.close()
            
            logger.info(f"Created Lex-AD mapping: {lex_node_id} -> {ad_entity_id}")
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to create Lex-AD mapping: {e}")
            return False
    
    def query_nodes_by_type(self, node_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Query nodes by type.
        
        Args:
            node_type: Node type to query
            limit: Maximum number of results
            
        Returns:
            List of nodes
        """
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT node_id, node_type, name, content, jurisdiction, metadata, properties
                FROM lex_nodes
                WHERE node_type = %s
                LIMIT %s
            """, (node_type, limit))
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            cursor.close()
            return results
        except Exception as e:
            logger.error(f"Failed to query nodes: {e}")
            return []
    
    def search_nodes(self, search_text: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Full-text search across legal nodes.
        
        Args:
            search_text: Text to search for
            limit: Maximum number of results
            
        Returns:
            List of matching nodes
        """
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT node_id, node_type, name, content, jurisdiction,
                       ts_rank(to_tsvector('english', name || ' ' || COALESCE(content, '')), 
                               plainto_tsquery('english', %s)) AS rank
                FROM lex_nodes
                WHERE to_tsvector('english', name || ' ' || COALESCE(content, '')) @@ plainto_tsquery('english', %s)
                ORDER BY rank DESC
                LIMIT %s
            """, (search_text, search_text, limit))
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            cursor.close()
            return results
        except Exception as e:
            logger.error(f"Failed to search nodes: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary of statistics
        """
        if not self.conn:
            raise RuntimeError("Not connected to database")
        
        try:
            cursor = self.conn.cursor()
            
            stats = {}
            
            # Count nodes by type
            cursor.execute("""
                SELECT node_type, COUNT(*) as count
                FROM lex_nodes
                GROUP BY node_type
            """)
            stats['nodes_by_type'] = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Count hyperedges by type
            cursor.execute("""
                SELECT relation_type, COUNT(*) as count
                FROM lex_hyperedges
                GROUP BY relation_type
            """)
            stats['edges_by_type'] = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Total counts
            cursor.execute("SELECT COUNT(*) FROM lex_nodes")
            stats['total_nodes'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM lex_hyperedges")
            stats['total_edges'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM lex_statutes")
            stats['total_statutes'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM lex_cases")
            stats['total_cases'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM lex_ad_mappings")
            stats['total_mappings'] = cursor.fetchone()[0]
            
            cursor.close()
            return stats
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}


def main():
    """Main function for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Lex Scheme Database Manager')
    parser.add_argument('--deploy-schema', action='store_true', help='Deploy schema')
    parser.add_argument('--schema-file', default='../schema/lex_scheme_enhanced.sql', help='Schema file path')
    parser.add_argument('--connection-string', help='PostgreSQL connection string')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    
    args = parser.parse_args()
    
    manager = LexDatabaseManager(args.connection_string)
    
    try:
        if args.deploy_schema:
            manager.connect()
            manager.deploy_schema(args.schema_file)
            logger.info("Schema deployment completed")
        
        if args.stats:
            manager.connect()
            stats = manager.get_statistics()
            logger.info(f"Database statistics: {json.dumps(stats, indent=2)}")
    
    finally:
        manager.disconnect()


if __name__ == "__main__":
    main()

