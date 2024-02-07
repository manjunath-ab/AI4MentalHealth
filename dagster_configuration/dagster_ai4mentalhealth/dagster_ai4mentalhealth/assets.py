
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
from dagster import Output,asset

chrome_options = Options()
chrome_options.add_argument("--headless")
dotenv_path = Path('c:/Users/abhis/.env')
load_dotenv(dotenv_path=dotenv_path)


def initial_fetch(url_thread):
   driver = webdriver.Chrome(options=chrome_options)
   driver.get(url_thread)
   # Find all elements with the class "read-link"
   link_elements = driver.find_elements(By.CLASS_NAME, 'read-link')
   # Extract href attribute from each element and store in a list
   href_list = [link.get_attribute("href") for link in link_elements]
   driver.quit()
   return href_list


@asset
def threaded_url_list_pull():
    num_threads=5
    base_url="https://www.blurtitout.org/blog/page/"
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

@asset
def tester(context, threaded_url_list_pull):
    result=threaded_url_list_pull
    print(Output(value=result))
    context.log.info(result)
    return Output(value=result)