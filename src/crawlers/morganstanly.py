import requests
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
from pprint import pprint
from tqdm import tqdm
import pandas as pd


class MorganStanleyInsights:

    def __init__(self,main_url):

        self.main_url = main_url

        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)


    @staticmethod
    def text_cleaning(raw_text):
        text = re.sub('\s+',' ', raw_text).strip().lower()
        return text

    @staticmethod
    def extract_content(link):
        # Send request and create BeautifulSoup object
        response = requests.get(link)
        soup = BeautifulSoup(response.text)

        # Content
        content = soup.find('div',class_='insightsContent')
        if bool(content) is True:
            content = text_cleaning(content.text)
        else:
            content = 'N/A'


        return content


    def get_morganstanley_insights(self):

        self.driver.get(self.main_url)
        self.driver.implicitly_wait(5)

        title_list = [i.text for i in self.driver.find_elements(By.CSS_SELECTOR,'.insightsIndexList')]
        link_list = [i.get_attribute('href') for i in self.driver.find_elements(By.CSS_SELECTOR,'.insightsIndexList')]
        date_list = [i.text for i in self.driver.find_elements(By.CSS_SELECTOR,'#latestInsights .pfdincoldBold span')]
        description_list = [i.text for i in self.driver.find_elements(By.CSS_SELECTOR,'.pressCenterText')]
        tag_list = [i.text for i in self.driver.find_elements(By.CSS_SELECTOR,'#latestInsights .pressCenterType')]


        morganstanley_insights_list = []
        index = 1
        for title, link, date, description, tag, in tqdm(zip(title_list, link_list, date_list, description_list, tag_list)):

            morganstanley_insights_dict = {
                'index': index,
                'company': 'Morgan Stanley',
                'topic': 'Insight',
                'tag': tag,
                'section': '',
                'title': title,
                'date': date,
                'link': link,
                'abstract': description,
                'content': self.extract_content(link),
            }
            morganstanley_insights_list.append(morganstanley_insights_dict)
            index += 1

        return morganstanley_insights_list