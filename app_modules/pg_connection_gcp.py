import psycopg2
import pandas as pd
from IPython.display import display


# Replace these with your actual values
DB_HOST = '34.155.124.126'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'B&s$rtLy[1<sn&c1'

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
    params_dsn = pd.DataFrame.from_dict(db_con_name, orient='index', columns=['Value'])
    # query = "SELECT * FROM testTbl WHERE schemaname = 'public';"  
    query = "SELECT * FROM testTbl"  
    # print(params_dsn)    
    cur.execute(query)
    results = cur.fetchall()
    df = pd.DataFrame(results, columns=[desc[0] for desc in cur.description])
    display(df)
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Failed to connect:", e)
