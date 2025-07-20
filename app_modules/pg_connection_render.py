import psycopg2
import pandas as pd

# Replace these with your actual values
DB_HOST = 'dpg-d1qf31gdl3ps738s0hd0-a.frankfurt-postgres.render.com'
DB_PORT = '5432'
DB_NAME = 'ndb_n2p5'
DB_USER = 'numan'
DB_PASS = '08B9rgRF5eNMEbYOu6C2r481VZDNCCAh'

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    print("✅ Connected to PostgreSQL database successfully!")

    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    db_con_name = cur.connection.info.dsn_parameters
    dsn = pd.DataFrame.from_dict(db_con_name, orient='index', columns=['Value'])
    print(dsn)

    cur.close()
    conn.close()
except Exception as e:
    print("❌ Failed to connect:", e)
