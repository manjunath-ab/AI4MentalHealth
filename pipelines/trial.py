from python_to_snowflake import create_snowflake_conn

conn = create_snowflake_conn() 

import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
import snowflake.connector

# Specify the columns you want to select
columns_to_select = [
    'SUPPORT_SYSTEM',
    'SELF_CARE_PRACTICES',
    'MENTAL_ILLNESS_STORY',
    'COPING_MECHANISM',
    'MENTAL_ILLNESS_TITLE',
    'TRIGGERS',
    'REFLECTIONS'
]

# Construct the SQL query
columns_string = ', '.join(columns_to_select)
query = f"SELECT {columns_string} FROM CHATBOT_KNOWLEDGE LIMIT 10"

# Extract data from Snowflake
snowflake_data = pd.read_sql_query(query, conn)

# Concatenate text data from all selected columns
text_data = snowflake_data.apply(lambda x: ' '.join(x.dropna()), axis=1).tolist()

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Tokenize and embed text data using BERT
embeddings = []
for text in text_data:
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    pooled_output = outputs.pooler_output  # You can use other outputs such as last hidden states if needed
    embeddings.append(pooled_output.numpy())

# Now 'embeddings' contains the BERT embeddings for each text in your data


import pinecone 
import numpy as np

# Initialize Pinecone with your API key
pinecone.init(api_key='your_api_key')

# Create an index in Pinecone
index_name = 'your_index_name'
dimension = len(embeddings[0])  # Assuming all embeddings have the same dimension
pinecone.create_index(index_name, dimension=dimension)

# Upsert embeddings into the Pinecone index
items = [{'id': str(i), 'vector': embedding.tolist()} for i, embedding in enumerate(embeddings)]
pinecone.upsert_items(index_name, items)

print("Embeddings stored in Pinecone successfully.")
