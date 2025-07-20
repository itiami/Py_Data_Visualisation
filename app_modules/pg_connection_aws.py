import psycopg2
import pandas as pd

# Replace these with your actual values
DB_HOST = 'n-psql-instance-1.cz0cemu2oz3y.eu-north-1.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'ndb'
DB_USER = 'numan'
DB_PASS = '5WJ8J0eyDMBxvj46AC8ZkfRvhzeu6Zl2VVNemuHhWtvMFNATMqDiRo8eiH2AurviE87GkIaZ9BQq6oUR35X1K5aLefgNlmU65uybH0y7gTTfOKooLHphW3VCMMpOXeHW'

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
