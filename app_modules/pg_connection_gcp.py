import psycopg2
import pandas as pd
from IPython.display import display
import json
from datetime import datetime

# Replace these with your actual values
DB_HOST = '34.155.124.126'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'B&s$rtLy[1<sn&c1'

train_info = {
    "id": "11",
    "station_name": "Central Station",
    "line_name": "Blue Line",
    "destination": "Airport",
    "departure_time": datetime(2025, 7, 20, 14, 30).isoformat(),
    "platform": "3A",
    "status": "On Time"
}

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


    # Insert the train information into the database
    sql = "INSERT INTO testTbl (id, station_name, line_name, destination, departure_time, platform, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data_list = [
        (
            int(train_info['id']), 
            train_info['station_name'], 
            train_info['line_name'], 
            train_info['destination'], 
            train_info['departure_time'], 
            train_info['platform'], 
            train_info['status']
        )
    ]
    # cur.executemany(sql, data_list)
    # conn.commit()

    # get the updated data from the database
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
