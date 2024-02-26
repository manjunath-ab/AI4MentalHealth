from dotenv import load_dotenv
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents import tool
from langchain.tools.base import Tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# Load environment variables from .env file
#dotenv_path = Path('/home/abhi/.env')
dotenv_path = Path('C:/Users/abhis/.env')
load_dotenv(dotenv_path=dotenv_path)

chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2)
db = Chroma(persist_directory="./knowledge_db",embedding_function=OpenAIEmbeddings())


retriever = db.as_retriever(k=4)
from langchain.tools.retriever import create_retriever_tool

tool = create_retriever_tool(
    retriever,
    "therapist_details",
    "this is a retreiver tool for therapist details",
)
tools = [tool]
"""
agent chat
"""



#get_word_length.invoke("abc")
tools = [tool]
#llm_with_tools = llm.bind_tools(tools)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


agent = create_openai_tools_agent(chat, tools, prompt)

agent_executor = AgentExecutor(agent=agent,tools=tools, verbose=True)



agent_executor.invoke({"messages": [HumanMessage(content="suggest some therapists in Boston?")]})

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history",
)

conversational_agent_executor.invoke(
    {
        "input": "suggest some therapists in Boston?",
    },
    {"configurable": {"session_id": "unused"}},
)