#!/usr/bin/env python3
"""
Automated Database Synchronization Script

This script synchronizes the local database schema with Supabase and Neon.
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection(db_url):
    """Establishes a connection to the database."""
    return psycopg2.connect(db_url)

def sync_schema(conn, schema_path):
    """Applies the schema to the database."""
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    with conn.cursor() as cur:
        cur.execute(schema)
    conn.commit()

def main():
    """Main function to synchronize databases."""
    supabase_url = os.getenv("SUPABASE_URL")
    neon_url = os.getenv("NEON_URL")
    schema_path = "/home/ubuntu/analyticase/schema/simulation_schema.sql"

    if supabase_url:
        print("Connecting to Supabase...")
        try:
            with get_db_connection(supabase_url) as conn:
                print("Synchronizing Supabase schema...")
                sync_schema(conn, schema_path)
                print("Supabase schema synchronized successfully.")
        except Exception as e:
            print(f"Error synchronizing with Supabase: {e}")

    if neon_url:
        print("Connecting to Neon...")
        try:
            with get_db_connection(neon_url) as conn:
                print("Synchronizing Neon schema...")
                sync_schema(conn, schema_path)
                print("Neon schema synchronized successfully.")
        except Exception as e:
            print(f"Error synchronizing with Neon: {e}")

if __name__ == "__main__":
    main()

