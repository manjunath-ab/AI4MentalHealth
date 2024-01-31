import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
dotenv_path = Path('c:/Users/abhis/.env')
load_dotenv(dotenv_path=dotenv_path)

# Snowflake connection parameters
snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
snowflake_user = os.getenv('SNOWFLAKE_USER')
snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')

# Snowflake connection
conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema
)


cursor = conn.cursor()
cursor.execute("SELECT * FROM AI4MENTALHEALTH.STAGING.TEST")
rows = cursor.fetchall()
for row in rows:
    print(row)
