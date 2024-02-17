from langchain_community.document_loaders.snowflake_loader import SnowflakeLoader
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
# Load environment variables from .env file
dotenv_path = Path('c:/Users/abhis/.env')
load_dotenv(dotenv_path=dotenv_path)


snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
snowflake_user = os.getenv('SNOWFLAKE_USER')
snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
snowflake_role = os.getenv('SNOWFLAKE_ROLE')
QUERY = "select * from CHATBOT_KNOWLEDGE"
snowflake_loader = SnowflakeLoader(
    query=QUERY,
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema,
    role=snowflake_role
)
snowflake_documents = snowflake_loader.load()
embeddings = HuggingFaceEmbeddings()


text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
docs = text_splitter.split_documents(snowflake_documents)
db = Chroma.from_documents(docs, OpenAIEmbeddings())


query = "Tell me about depression. Talk about the symptoms and coping mechanisms like a friend"
docs = db.similarity_search(query)
print(docs[0].page_content)