import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from typing import Dict
from streamlit_chat import message
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents import tool
from langchain.tools.base import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_core.runnables.history import RunnableWithMessageHistory
import json
from dateutil import parser
import datetime
import calendar
import random
import json
from faker import Faker

fake = Faker()
today = datetime.datetime.now()
hours = (9, 18)   # open hours


def load_environment_variables():
    dotenv_path = Path('C:/Users/abhis/.env')
    load_dotenv(dotenv_path=dotenv_path)

def initialize_chat_and_db():
    chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2)
    db = Chroma(persist_directory="../new_knowledge_db",embedding_function=OpenAIEmbeddings())
    return chat, db

def create_system_template():
    SYSTEM_TEMPLATE = """
    Imagine you are a human friend, talk to the user like a friend who understands their problem and keep the reply short.End with a follow up question. 
    If the user asks you about therapists then provide details such as the therapist's name, location, and description.
    When the user asks to book an appointment, ask about preferences such as location and preferred timings for the appointment.After user input, ask a question to keep the conversation going.
    If the user question is not relevant to mental health or therapists details, don't make something up and just say "I don't know":

    <context>
    
    </context>
    """
    return SYSTEM_TEMPLATE

def create_retriever(db):
    retriever = db.as_retriever(k=4)
    
    return retriever


def initialize_chat_history():
    demo_ephemeral_chat_history = ChatMessageHistory()
    return demo_ephemeral_chat_history

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! I'm Zenny.Ask me about therapy, mental health, or anything you want to talk about "]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey"]




def display_avatar_image():
    st.image("zen.jpg", width=300)

    # Upload an image on the sidebar
    avatar_image = "avatar.jpg"

    # Check if an image file is uploaded
    if avatar_image is not None:
        # Display the uploaded image on the sidebar
        st.sidebar.image(avatar_image, use_column_width=True)
        st.sidebar.markdown("""
        <div style="font-family: 'Arial', sans-serif; font-size: 20px; font-style: italic;">
            "I am Zenny! I'm here to be your virtual friend, to chat with you, and to help you find the support and resources you need. Whether you're feeling down and need someone to talk to, or you're looking for information on mental health and therapy, I'm here to listen and assist. So, let's chat and find the help you need!"
        </div>
    """, unsafe_allow_html=True)

def get_retriever_tool(retriever):
    tool = create_retriever_tool(
    retriever,
    "mental_health_and_therapist_knowledge_base",
    "This is a retreiver tool for therapist details and mental health journies,coping mechanisms,triggers, self care rountines and more",
    )
    return tool


"""
scheduler
"""
# create random schedule
def createSchedule(daysAhead=5, perDay=5):
    schedule = {}
    for d in range(0, daysAhead):
        date = (today + datetime.timedelta(days=d)).strftime('%m/%d/%y')
        schedule[date] = {}

        for h in range(0, perDay -d):
            hour = random.randint(hours[0], hours[1])
            if hour not in schedule[date]:
                schedule[date][hour] = fake.name()
                
    return schedule

# get available times for a date
def getAvailTimes(date, num=10):
    schedule = loadSchedule()

    if '/' not in date or 'mm' in date:
        return 'date parameter must be in format: mm/dd/yy'

    if date not in schedule:
        return 'that day is entirely open, all times are available'

    hoursAvail = 'hours available on %s are ' % date

    for h in range(hours[0], hours[1]):
        if str(h) not in schedule[date]:
            hoursAvail += str(h) +':00, '
            num -= 1
            if num == 0:
                break
    
    if num > 0:
        hoursAvail = hoursAvail[:-2] +' - all other times are reserved'
    else:
        hoursAvail = hoursAvail[:-2]
        
    return hoursAvail

# schedule available time
def scheduleTime(dateTime):
    schedule = loadSchedule()

    date, time = dateTime.split(',')
    
    if not date or not time:
        return "sorry parameters must be date and time comma separated, for example: `12/31/23, 10:00` would be the input if for Dec 31'st 2023 at 10am"

    # get hours
    if ':' in time:
        timeHour = int(time[:time.index(':')])
        print(timeHour)
        
        if timeHour not in schedule[date]:
            if timeHour >= hours[0] and timeHour <= hours[1]:
                schedule[date][timeHour] = fake.name()
                saveSchedule(schedule)
                print('Updated schedule json...')
                return 'thank you, appointment scheduled for %s under name %s' % (time, schedule[date][timeHour])
            else:
                return '%s is after hours, please select a time during business hours' % time
        else:
            return 'sorry that time (%s) on %s is not available' % (time, date)
    else:
        return '%s is not a valid time, time must be in format hh:mm'
    
# save schedule json
def saveSchedule(schedule):
    with open('schedule.json', 'w') as f:
        json.dump(schedule, f)
    
# load schedule json
def loadSchedule():
    global schedule
    
    with open('schedule.json') as json_file:
        return json.load(json_file)

# get today's date
def todayDate():
    return today.strftime('%m/%d/%y')

# get day of week for a date (or 'today')
def dayOfWeek(date):
    if date == 'today':
        return calendar.day_name[today.weekday()]
    else:
        try:
            theDate = parser.parse(date)
        except:
            return 'invalid date format, please use format: mm/dd/yy'
        
        return calendar.day_name[theDate.weekday()]
    
#########



"""
end scheduler
"""
def main():
    load_environment_variables()
    chat, db = initialize_chat_and_db()
    #question = "mental health and therapy"
    retriever= create_retriever(db)
    tools = [
    Tool(
        name = "today_date",
        func = lambda string: todayDate(),
        description="use to get today's date",
        ),
    Tool(
        name = "day_of_week",
        func = lambda string: dayOfWeek(string),
        description="use to get the day of the week, input is 'today' or date using format mm/dd/yy",
        ),
    Tool(
        name = 'available_appointments',
        func = lambda string: getAvailTimes(string),
        description="Use to check on available appointment times for a given date. The input to this tool should be a string in this format mm/dd/yy. This is the only way for you to answer questions about available appointments. This tool will reply with available times for the specified date in 24hour time, for example: 15:00 and 3pm are the same.",
        ),
    Tool(
        name = 'schedule_appointment',
        func = lambda string: scheduleTime(string),
        description="Use to schedule an appointment for a given date and time. The input to this tool should be a comma separated list of 2 strings: date and time in format: mm/dd/yy, hh:mm, convert date and time to these formats. For example, `12/31/23, 10:00` would be the input if for Dec 31'st 2023 at 10am",
        )]
    tools.append(get_retriever_tool(retriever))
    question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
             create_system_template(), 
            
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
    )
    agent = create_openai_tools_agent(chat, tools, question_answering_prompt)
    agent_executor = AgentExecutor(agent=agent,tools=tools, verbose=True)
    demo_ephemeral_chat_history = initialize_chat_history()
    conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: demo_ephemeral_chat_history,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history",
    )
    display_avatar_image()
    initialize_session_state()
    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Chat:", placeholder="Talk to ZEN.AI 👉", key='input')
            submit_button = st.form_submit_button(label='Send')
            if submit_button and user_input:
                demo_ephemeral_chat_history.add_user_message(user_input)
                
              
                response=conversational_agent_executor.invoke(
                       {"input": user_input},
                       {"configurable": {"session_id": "unused"}},
                        )
                output = response['output']
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
                continue

    end_chat_checkbox = st.checkbox("I entered all the details.")
    end_chat_button = st.button("End Chat")

    if end_chat_button and end_chat_checkbox:
        # Extract Process to snowflake
        st.success("An appointment will be scheduled for you.")
        # Clear session state
        st.session_state['past'] = []
        st.session_state['generated'] = []
        # Refresh the app
    elif end_chat_button:
        # Refresh the app without clearing session state
        st.session_state['past'] = []
        st.session_state['generated'] = []
        # Refresh the app
        st.experimental_rerun()



if __name__ == "__main__":
    main()
