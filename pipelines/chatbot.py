# import streamlit as st
# from langchain_community.document_loaders.snowflake_loader import SnowflakeLoader
# from dotenv import load_dotenv
# from pathlib import Path
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# import os
# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
# from langchain_openai import ChatOpenAI
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.memory import ChatMessageHistory
# from langchain_core.runnables import RunnablePassthrough
# from typing import Dict

# # Load environment variables from .env file
# dotenv_path = Path('/Users/sivaranjanis/Desktop/genai/AI4MentalHealth/.env')
# load_dotenv(dotenv_path=dotenv_path)

# # Initialize Streamlit app
# st.title("Mental Health Chatbot")

# # Load embeddings
# db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())

# # Define Streamlit UI elements
# query = st.text_input("Enter your query:", "Tell me about bipolar disorder and how to cope with it")
# if st.button("Submit"):
#     # Perform similarity search
#     result = db.similarity_search(query)
#     retriever = db.as_retriever(k=4)
#     docs = retriever.invoke("how can i battle depression?")
    
#     # Initialize ChatOpenAI model
#     chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2)

#     # Define ChatPromptTemplate
#     question_answering_prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 "Imagine you are a therapist, talk to the user like a friend who understands their problem and keep the answer short..end with a question:\n\n{context}",
#             ),
#             MessagesPlaceholder(variable_name="messages"),
#         ]
#     )

#     # Create document chain
#     document_chain = create_stuff_documents_chain(chat, question_answering_prompt)

#     # Define parse_retriever_input function
#     def parse_retriever_input(params: Dict):
#         return params["messages"][-1].content

#     # Define retrieval_chain
#     retrieval_chain = RunnablePassthrough.assign(
#         context=parse_retriever_input | retriever,
#     ).assign(
#         answer=document_chain,
#     )

#     # Invoke retrieval_chain
#     demo_ephemeral_chat_history = ChatMessageHistory()
#     demo_ephemeral_chat_history.add_user_message(query)
#     response = retrieval_chain.invoke(
#         {
#             "messages": demo_ephemeral_chat_history.messages,
#         }
#     )

#     # Display response
#     st.text_area("Response:", value=response['answer'])
import streamlit as st
from langchain_community.document_loaders.snowflake_loader import SnowflakeLoader
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from typing import Dict

# Load environment variables from .env file
dotenv_path = Path('/Users/sivaranjanis/Desktop/genai/AI4MentalHealth/.env')
load_dotenv(dotenv_path=dotenv_path)

# Initialize Streamlit app
st.title("Mental Health Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load embeddings
db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())

# Initialize ChatOpenAI model
chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2)

# Define ChatPromptTemplate
question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Imagine you are a therapist, talk to the user like a friend who understands their problem and keep the answer short..end with a question:\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Create document chain
document_chain = create_stuff_documents_chain(chat, question_answering_prompt)

# Define parse_retriever_input function
def parse_retriever_input(params: Dict):
    messages = params["messages"]
    if messages:
        return messages[-1]  # Return the last message
    else:
        return ""  # Return empty string if there are no messages

# Define retrieval_chain
retriever = db.as_retriever(k=4)
retrieval_chain = RunnablePassthrough.assign(
    context=parse_retriever_input | retriever,
).assign(
    answer=document_chain,
)

# Display conversation history
st.write("Conversation History:")
for message in st.session_state.chat_history:
    if message.startswith("You:"):
        st.write(f"💬 **You:** {message[5:]}")
    elif message.startswith("System:"):
        st.write(f"🤖 **System:** {message[8:]}")

# User input
st.write("Your Message:")
user_query = st.text_input("")

# Send button
if st.button("Send"):
    # Add user message to chat history
    user_message = f"You: {user_query}"
    st.session_state.chat_history.append(user_message)
    
    # Invoke retrieval_chain
    response = retrieval_chain.invoke(
        {
            "messages": [message.split(": ")[1] for message in st.session_state.chat_history if message.startswith("You:")],
        }
    )
    
    # Add system response to chat history
    system_message = f"System: {response['answer']}"
    st.session_state.chat_history.append(system_message)
