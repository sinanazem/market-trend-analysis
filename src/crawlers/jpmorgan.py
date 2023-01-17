from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import re
from pprint import pprint
from tqdm import tqdm
import pandas as pd
import requests
from bs4 import BeautifulSoup


class JPMorganInsight:
    def __init__(self):

        self.mainlink = 'https://www.jpmorgan.com/insights'
        self.news_link = 'https://www.jpmorgan.com/news'
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--headless")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=chrome_options)


    @staticmethod
    def jpmorgan_insight(link):

        response = requests.get(link)
        soup = BeautifulSoup(response.text)
        title = soup.find(class_='article__body__head').text.strip()
        tag = soup.find(class_='article__body__eyebrow').text.strip()
        date = soup.find(class_='article__body__abstract--date article__body__text--small').text.strip()
        raw_content = soup.find(class_='article__body__text').text
        content = re.sub('\s+', ' ', raw_content).strip()
        return {
                'index': '',
                'company': 'J.P.Morgan',
                'topic': 'Insight',
                'title': title,
                'date': date,
                'tag': tag,
                'link': link,
                'content': content,
                }

    @staticmethod
    def jpmorgan_news(link):

        if 'https://www.jpmorgan.com/news' in link:
            response = requests.get(link)
            soup = BeautifulSoup(response.text)
            title = soup.find(class_='article__body__head').text.strip()
            date = soup.find(class_='article__body__abstract--date article__body__text--small').text.strip()
            raw_content = soup.find(class_='article__body ss-print').text
            content = re.sub('\s+', ' ', raw_content).strip()
            return {         
                    'index': '',
                    'company': 'J.P.Morgan',
                    'topic': 'News',
                    'title': title,
                    'date': date,
                    'link': link,
                    'content': content,
                    }

    def get_all_jpmorgan_insight(self): 

        self.driver.get(self.mainlink)

        sleep(5)


        while True:

            try:
                show_more_button = driver.find_element(By.CSS_SELECTOR, '.fa-chevron-down')    
                self.driver.execute_script("arguments[0].click();", show_more_button)

            except: 
                pass



        link_list_insight = [i.get_attribute('href') for i in self.driver.find_elements(By.XPATH, '//*[@class="item"]/a')]

        jpmorgan_insight_list = []
        index = 1
        for link in link_list_insight:

            jpmorgan_dict = self.jpmorgan_insight(link)
            jpmorgan_dict.update({'index': index})
            jpmorgan_insight_list.append(jpmorgan_dict)
            index += 1


        return jpmorgan_insight_list


    def get_all_jpmorgan_news(self): 

        self.news_driver.get(self.news_link)
        sleep(5)


        link_list_news = [str(link.get_attribute('href')) for link in self.news_driver.find_elements(By.XPATH, '//*[@class="title"]//a')]

        jpmorgan_news_list = []
        index = 1
        for link in link_list_news:
            try:
                jpmorgan_dict = self.jpmorgan_news(link=link)
                jpmorgan_dict['index'] = index
                jpmorgan_news_list.append(jpmorgan_dict)
                index += 1
            except:
                print(link)


        return jpmorgan_news_list
