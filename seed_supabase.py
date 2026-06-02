from app import get_db_connection
from init_db import champions_data


def seed_database():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM champions')
    count = cur.fetchone()[0]
    if count > 0:
        print(f'La tabella champions contiene già {count} record. Nessun inserimento eseguito.')
        cur.close()
        conn.close()
        return

    insert_query = '''
        INSERT INTO champions (name, role, lore, difficulty, image_vertical, image_horizontal)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''

    cur.executemany(insert_query, champions_data)
    conn.commit()
    print(f'Inseriti {len(champions_data)} campioni nella tabella champions.')
    cur.close()
    conn.close()


if __name__ == '__main__':
    seed_database()
