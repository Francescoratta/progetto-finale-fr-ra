from app import get_db_connection

try:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT 1;')
    print('Connected, SELECT 1 ->', cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    import traceback
    traceback.print_exc()
    print('Connection failed:', e)
