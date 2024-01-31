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
import time

chrome_options = Options()
chrome_options.add_argument("--headless")

dotenv_path = Path('c:/Users/abhis/.env')
load_dotenv(dotenv_path=dotenv_path)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

#define a prompt template for the summarization task


#pull article link from the list
def define_schema():
 schema = {
    "properties": {
        "mental_illness_title": {"type": "string"},
        "mental_illness_journey": {"type": "string"},
        "coping mechanism": {"type": "string"}
    },
    "required": ["mental_illness_title", "mental_illness_journey","mental_illness_summary","coping mechanism"],
 }
 return schema


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke("Group the content based on mental illness:"+content)


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
        chunk_size=1000, chunk_overlap=200
    )
    splits = splitter.split_documents(docs_transformed)

    try:
        extracted_content = extract(schema=schema, content=splits[0].page_content)
    except Exception as e:
        print(e)
        return None

    #extracted_content['text']['article'] = url
    pprint.pprint(extracted_content)
    
    return pd.DataFrame(extracted_content['text'])


def html_scrape(urls, schema):
    df_list = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []

        for url in urls:
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
                futures.clear()

                # Wait for a minute before processing the next batch
                time.sleep(60)

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
    return [url_list[i:i+5] for i in range(0,len(url_list),5)]
   
def main():
    base_url="https://www.blurtitout.org/blog/page/"
    url_list=list(set(threaded_url_list_pull(base_url)))
    #put in a check to not repeat the same url for future runs
    print('completed the url list')
    print(url_list,len(url_list))
    schema = define_schema()
    url_list=batch_url_list(url_list)
    df_list = html_scrape(url_list, schema=schema)
    result=pd.concat(df_list, ignore_index=True)
    result.to_csv('blurt_illness.csv')

if __name__=='__main__':
 main()