import snowflake.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from dagster import Definitions,asset,op,define_asset_job
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

@asset
def create_snowflake_conn(context,publish_to_snowflake):
    # Snowflake connection
    identifier=publish_to_snowflake
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )
    cursor=conn.cursor()
    return conn,cursor,identifier
@asset
def upload_to_stage(context,create_snowflake_conn):
    # Create a stage
    conn,cursor,identifier=create_snowflake_conn
    file_path=Path(os.getenv('FILE_PATH'))
    file_name=f'knowledge-{identifier}.csv'
    cursor.execute("CREATE STAGE IF NOT EXISTS KNOWLEDGEBASE_STAGE ")
    cursor.execute(f"PUT file:///{file_path}/{file_name} @KNOWLEDGEBASE_STAGE")
    return conn,cursor

@asset
def stage_to_table(context,upload_to_stage):
    # Copy data from stage to table
    conn,cursor=upload_to_stage
    cursor.execute("COPY INTO CHATBOT_KNOWLEDGE FROM @KNOWLEDGEBASE_STAGE FILE_FORMAT='PYTHON' ON_ERROR=CONTINUE ")
    cursor.close()
    conn.close()
    return


