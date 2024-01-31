"""
author:manjunath-ab
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.chains import create_extraction_chain
from langchain.prompts import (
    PromptTemplate,
)
import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")

dotenv_path = Path('c:/Users/abhis/.env')
load_dotenv(dotenv_path=dotenv_path)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

#define a prompt template for the summarization task



def define_schema():
 schema = {
    "properties": {
        "mental_illness_title": {"type": "string"},
        "mental_illness_journey": {"type": "string"},
        "mental_illness_summary": {"type": "string"},
        "article_link": {"type": "string"},
    },
    "required": ["mental_illness_title", "mental_illness_journey","mental_illness_summary","article_link"],
 }
 return schema


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke("Give me the summarization of the story:"+content)


def batching_dataframes():
   pass

def scrape_with_playwright(urls, schema):
  df_list=[]
  #batch the urls into groups of 10
  for i in range(0, len(urls), 10):
    loader = AsyncChromiumLoader(urls[0:i+10])
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

        
   
def main():
    base_url="https://www.blurtitout.org/blog/page/"
    url_list=set(threaded_url_list_pull(base_url))
    #put in a check to not repeat the same url for future runs
    print('completed the url list')
    print(url_list,len(url_list))
    schema = define_schema()
    df_list = scrape_with_playwright(url_list, schema=schema)
    result=pd.concat(df_list,reset_index=True)
    print(result)

if __name__=='__main__':
 main()