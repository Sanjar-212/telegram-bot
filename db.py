import psycopg
from psycopg import connect
def get_connection():
    return connect(
        dbname="foton_db",
        user="postgres",
        password="1234",      
        host="127.0.0.1",
        port="5432"
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kontaktlar (
    id SERIAL PRIMARY KEY,
    ism TEXT,
    tel TEXT,
    tg_id BIGINT,
    username TEXT,
    sana TIMESTAMP DEFAULT NOW()
);
    """)
    conn.commit()
    cur.close()
    conn.close()