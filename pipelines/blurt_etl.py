"""
author:manjunath-ab
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain.chains import create_extraction_chain
from langchain.prompts import PromptTemplate
import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time
import random
import os

chrome_options = Options()
chrome_options.add_argument("--headless")

# dotenv_path = Path('c:/Users/abhis/.env')
# load_dotenv(dotenv_path=dotenv_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=1, model="gpt-3.5-turbo-0613")


# Create an instance of the ChatOpenAI class
llm = ChatOpenAI(temperature=1, model='gpt-3.5-turbo-0125')


def define_schema():
 schema = {
    "properties": {
        "mental_illness_title": {"type": "string"},
        "mental_illness_story": {"type": "string"},
        "coping_mechanism": {"type": "string"},
        "support_system": {"type": "string"},
        "triggers": {"type": "string"},      
        "self_care_practices:": {"type": "string"},
        "reflections": {"type": "string"},
    },
    "required": ["mental_illness_title","mental_illness_story","coping_mechanism","support_system","triggers","self_care_practices","reflections"],
 }
 return schema


# # Define the prompt templates
# prompt_template_mental_illness_title = "Imagine you're a compassionate mental health therapist. Explore the unique aspects of the mental health condition titled '{mental_illness_title}'. Provide insights into its symptoms, prevalence, and any distinctive features. Share details as if you're helping someone understand this condition for the first time."

# prompt_template_mental_illness_story = "Put yourself in the shoes of a supportive friend. Listen to the personal story of someone dealing with '{mental_illness_title}'. Capture the emotions, challenges faced, and moments of resilience. Provide a narrative that reflects empathy and understanding towards their mental health journey."

# prompt_template_coping_mechanism = "As a caring mental health advocate, delve into the coping mechanism '{coping_mechanism}' adopted by individuals facing '{mental_illness_title}'. Explore its origins, effectiveness, and any rituals associated with it. Consider discussing how this coping mechanism provides a sense of comfort and stability in their lives."

# prompt_template_support_system = "Imagine acting as a supportive figure in someone's life. Explore the robust support system surrounding individuals dealing with '{mental_illness_title}'. Identify key individuals, organizations, or resources contributing to their well-being. Highlight the roles these support networks play in fostering mental health resilience."

# prompt_template_triggers = "Envision yourself as a perceptive mental health researcher. Investigate the triggers associated with '{mental_illness_title}'. Uncover environmental, emotional, or situational factors that exacerbate the condition. Consider discussing strategies employed to manage or mitigate these triggers in their day-to-day experiences."

# prompt_template_self_care_practices = "Take on the role of a caring wellness advisor. Explore the self-care practices employed by individuals dealing with '{mental_illness_title}'. Dive into the routines, rituals, and habits that contribute to their mental well-being. Discuss the evolution of these practices and their impact on overall mental health."

# prompt_template_reflections = "Imagine yourself as a reflective companion. Explore the personal reflections of individuals dealing with '{mental_illness_title}'. Delve into their thoughts on the journey, progress, and lessons learned. Capture the nuanced aspects of their mental health narrative, considering both challenges and moments of growth."

# prompt_templates_combined = PromptTemplate(
#     input_variables=['mental_illness_title', 'coping_mechanism', 'support_system', 'triggers', 'self_care_practices', 'reflections'],
#     template="Imagine you are both a compassionate mental health therapist and a supportive friend. Explore the unique aspects of the mental health condition titled '{mental_illness_title}'. Delve into the coping mechanism '{coping_mechanism}' adopted by individuals facing this condition. Identify the robust support system surrounding them, considering key individuals, organizations, or resources. Investigate the triggers associated with '{mental_illness_title}', uncovering environmental, emotional, or situational factors. Delve into the self-care practices employed, exploring the routines, rituals, and habits contributing to mental well-being. Finally, reflect on the personal journey, progress, and lessons learned, capturing nuanced aspects of their mental health narrative."
# )


def extract(content: str, schema: dict):
    prompt = (
        f"Explore and provide detailed insights into all of the following aspects related to mental health. As you provide this information, imagine you are both a compassionate mental health therapist and a empathetic, supportive friend.\n"
        f"1. **Mental Illness Title:** Describe the specific mental health condition or challenge.\n"
        f"2. **Mental Illness Story:** Narrate a detailed and emotive story of someone navigating this mental health condition. Include their emotions, challenges, and moments of resilience.\n"
        f"3. **Coping Mechanism:** Explain the strategies and methods adopted by the individual to cope with their mental health challenges.\n"
        f"4. **Support System:** Identify and elaborate on the crucial individuals, organizations, or resources that contribute to the individual's well-being.\n"
        f"5. **Triggers:** Delve into a nuanced exploration of environmental, emotional, or situational triggers that significantly impact or exacerbate the mental health condition.\n"
        f"6. **Self-Care Practices:** Provide a detailed examination of the daily routines, rituals, and habits that actively contribute to the individual's mental well-being.\n"
        f"7. **Reflections:** acknowledging progress made and lessons learned, offering a holistic perspective on the individual's mental health experiences.\n"
        f"If specific data is not available for any of the fields, please add content more closely associated with the mental illness, creating a comprehensive and insightful narrative.\n"
        f"As you navigate this exploration, envision yourself peeling back layers to reveal a profound understanding of the diverse triggers impacting the individual's mental health."
    )
    return create_extraction_chain(schema=schema, llm=llm).invoke(prompt+content)

def batching_dataframes():
   pass

#url is a list of urls batched for the sake of OPENAI API rate limits
def process_url(url, schema):
    loader = AsyncHtmlLoader(url)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["p"]
    )

    print("Extracting content with LLM for the URL: ", url)

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=350
    )
    splits = splitter.split_documents(docs_transformed)

    try:
        extracted_content = extract(schema=schema, content=splits[0].page_content)
    except Exception as e:
        print(e)
        return None

    #extracted_content['text']['article'] = url
    pprint.pprint(extracted_content)

    # Define the expected schema with column names and their corresponding data types
    schema_dict = {
    "mental_illness_title": str,
    "mental_illness_story": str,
    "coping_mechanism": str,
    "support_system": str,
    "triggers": str,
    "self_care_practices": str,
    "reflections": str
    }

    
    if extracted_content['text'] is list:
        df=pd.DataFrame(extracted_content['text'][0])
    else:
        df=pd.DataFrame(extracted_content['text'])
    # Check if all expected columns are present in the DataFrame
    missing_columns = set(schema_dict.keys()) - set(df.columns)
    # Add missing columns with NaN values
    for column in missing_columns:
      df[column] = None
    
    return df


def html_scrape(urls, schema):
    df_list = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []

        for i,url in enumerate(urls):
            print(f"Processing URL set {i+1} of {len(urls)}")
            # Submit each URL for processing in the thread pool
            future = executor.submit(process_url, url, schema)
            futures.append(future)

            # If we've processed a batch of 3 URL sets, wait for a minute
            if len(futures) == 3:
                for completed_future in futures:
                    result_df = completed_future.result()
                    if result_df is not None:
                        df_list.append(result_df)

                # Clear the futures list for the next batch
                print("Clearing the futures list")
                futures.clear()

                # Wait for a minute 20 before processing the next batch
                print("Waiting for 70 seconds before processing the next batch of URLs...")
                time.sleep(70)
            time.sleep(5)

        # Wait for any remaining threads to finish
        for future in futures:
            result_df = future.result()
            if result_df is not None:
                df_list.append(result_df)

    return df_list

def scrape_with_playwright(urls, schema):
  df_list=[]
  #batch the urls into groups of 10
  for i in range(0,20,10): #len(urls)
    loader = AsyncChromiumLoader(urls[i:i+10])
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["p"]
    )
    #print(docs_transformed)
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)
    #print(f'content being used is {splits[0]}')
    # Process the first split
    """
    Need to wrap the extract function in a try except block to handle the case where the content is empty
    """
    try:
        extracted_content = extract(schema=schema, content=splits[0].page_content)
        #pprint.pprint(extracted_content)
    except:
        print('content is empty')
        continue

    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint.pprint(extracted_content)

    #convert into a dataframe
    df = pd.DataFrame(extracted_content)
    df_list.append(df)
  return df_list

def initial_fetch(url_thread):
   driver = webdriver.Chrome(options=chrome_options)
   driver.get(url_thread)
   # Find all elements with the class "read-link"
   link_elements = driver.find_elements(By.CLASS_NAME, 'read-link')
   # Extract href attribute from each element and store in a list
   href_list = [link.get_attribute("href") for link in link_elements]
   driver.quit()
   return href_list



def threaded_url_list_pull(base_url, num_threads=5):
    print('starting the threaded url list pull')
    url_list = []
    i = 1

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Create a list to hold the futures
        futures = []

        while True:
            url_thread = base_url + str(i)
            # Submit the task to the thread pool and store the future
            future = executor.submit(initial_fetch, url_thread)
            futures.append(future)

            if i > 16:
                break

            i += 1
            print(i)

        # Wait for all threads to complete before moving on
        for completed_future in as_completed(futures):
            url_list.extend(completed_future.result())

    return url_list


def button_sequence_flow(base_url):
   url_list=[]
   driver = webdriver.Chrome() #options=chrome_options
   driver.get(base_url)
   while True:
 
    link_elements = driver.find_elements(By.CLASS_NAME, 'read-link')
    # Extract href attribute from each element and store in a list
    url_list.extend([link.get_attribute("href") for link in link_elements])
    print(url_list)

    try:
        # Look for the next button and click it
        next_button = driver.find_elements(By.CLASS_NAME,'next page-numbers')
        next_button.click()
    except Exception:
        # If the next button is not found, break out of the loop
        break

# Close the webdriver
   driver.quit()

def batch_url_list(url_list):
    batch_size = random.randint(3, 20)
    return [url_list[i:i+batch_size] for i in range(0, len(url_list), batch_size)]

def main():
    base_url="https://www.blurtitout.org/blog/page/"
    url_list=list(set(threaded_url_list_pull(base_url)))
    #put in a check to not repeat the same url for future runs
    print('completed the url list')
    print(url_list,len(url_list))
    schema = define_schema()
    url_list=batch_url_list(url_list)
    start_time = time.time()
    df_list = html_scrape(url_list, schema=schema)
    end_time = time.time()
    print("Time taken to process all URLs: ", end_time - start_time)
    result=pd.concat(df_list, ignore_index=True)
    result.dropna(how='all',inplace=True)
    result.to_csv('blurt_illness2.csv',index=False)

if __name__=='__main__':
 main()