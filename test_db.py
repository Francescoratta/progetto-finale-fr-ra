# test_db.py
import os
import psycopg2
from psycopg2.extras import DictCursor

db_url = os.environ.get("DATABASE_URL")
print("Using:", db_url and db_url[:80] + ("..." if len(db_url)>80 else ""))

try:
    conn = psycopg2.connect(db_url, cursor_factory=DictCursor, connect_timeout=10)
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("DB connected, SELECT 1 ->", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("Connection error:", repr(e))