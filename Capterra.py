from threading import Thread

from bs4 import BeautifulSoup
import urllib
import sys
import random
from urllib.request import urlopen
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
from pathlib import Path




sys.setrecursionlimit(200000)

desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

links = [
 'https://www.capterra.com/professional-services-automation-software/',
 'https://www.capterra.com/idea-management-software/',
 'https://www.capterra.com/collaboration-software/',
 'https://www.capterra.com/workflow-management-software/',
 'https://www.capterra.com/time-tracking-software/',
 'https://www.capterra.com/time-and-expense-software/',
 'https://www.capterra.com/task-management-software/',
 'https://www.capterra.com/resource-management-software/',
 'https://www.capterra.com/requirements-management-software/',
 'https://www.capterra.com/project-portfolio-management-software/',
 'https://www.capterra.com/diagram-software/',
 'https://www.capterra.com/it-management-software/',
 'https://www.capterra.com/application-development-software/',
 'https://www.capterra.com/wireframe-software/',
 'https://www.capterra.com/digital-workplace-software/',
 'https://www.capterra.com/meeting-software/',
 'https://www.capterra.com/video-interviewing-software/',
 'https://www.capterra.com/team-communication-software/',
 'https://www.capterra.com/remote-support-software/',
 'https://www.capterra.com/employee-monitoring-software/',
 'https://www.capterra.com/web-conferencing-software/',
 'https://www.capterra.com/softphone-software/',
 'https://www.capterra.com/remote-monitoring-and-management-software/',
 'https://www.capterra.com/live-chat-software/',
 'https://www.capterra.com/webinar-software/',
 'https://www.capterra.com/workforce-management-software/',
 'https://www.capterra.com/accounting-practice-management-software/',
 'https://www.capterra.com/contract-management-software/',
 'https://www.capterra.com/proposal-management-software/',
 'https://www.capterra.com/social-networking-software/',
 'https://www.capterra.com/screen-sharing-software/',
 'https://www.capterra.com/community-software/',
 'https://www.capterra.com/business-process-management-software/',
 'https://www.capterra.com/billing-and-invoicing-software/',
 'https://www.capterra.com/time-clock-software/',
 'https://www.capterra.com/legal-billing-software/',
 'https://www.capterra.com/expense-report-software/',
 'https://www.capterra.com/demand-planning-software/',
 'https://www.capterra.com/marketing-planning-software/',
 'https://www.capterra.com/employee-scheduling-software/',
 'https://www.capterra.com/enterprise-resource-planning-software/',
 'https://www.capterra.com/project-planning-software/',
 'https://www.capterra.com/product-lifecycle-management-software/',
 'https://www.capterra.com/data-visualization-software/',
 'https://www.capterra.com/artificial-intelligence-software/',
 'https://www.capterra.com/presentation-software/',
 'https://www.capterra.com/network-security-software/',
 'https://www.capterra.com/saas-management-software/',
 'https://www.capterra.com/network-monitoring-software/',
 'https://www.capterra.com/it-asset-management-software/',
 'https://www.capterra.com/business-continuity-software/',
 'https://www.capterra.com/website-monitoring-software/']

class Scrapping:

    def __init__(self, website_url = ''):
        self.url = website_url
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def random_headers(self):
        return {'User-Agent': random.choice(desktop_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    def get_json_request(self, url):
        req = urllib.request.Request(url, headers=self.random_headers())
        r = urllib.request.urlopen(req)
        beautifulsoup = BeautifulSoup(r, "lxml")
        return beautifulsoup

    def getAbstract(self):
        reviews_count = 0
        while(reviews_count <= 200):
            self.driver.get(self.url)
            html = self.driver.page_source
            project_soup = BeautifulSoup(html, 'html.parser')
            button_class = project_soup.find_all('div', {'class': 'more-reviews-btn-container nb-flex nb-mt-md nb-justify-center'})
            button = button_class[0].find('button')
            try:
                time.sleep(5)
                button.click()
                reviews = project_soup.find_all('div', {'class': 'nb-w-full nb-px-2xs'})
                reviews_count = reviews_count + len(reviews)
            except:
                reviews = project_soup.find_all('div', {'class': 'nb-w-full nb-px-2xs'})
                reviews_count = reviews_count + len(reviews)
                continue

    def getAbstract1(self, url, title):
        self.driver.get(url)
        html = self.driver.page_source
        project_soup = BeautifulSoup(html, 'html.parser')
        product_cards = project_soup.find_all('div', {'class': 'nb-block nb-w-100'})
        review_links = []
        for product in product_cards:
            link = product.find_all('div', {'class': 'nb-mb-xs sm:nb-mb-0'})
            review_link = link[0].find('a').get('href')
            review_links.append(review_link)
        self.saveData(review_links, title)

    def saveData(self, links_list, title):
        path = '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/'
        dict = {title: links_list}
        df = pd.DataFrame(dict)
        df.to_csv(path + title + '.csv')

    def removeDuplicateLinks(self, dir_path):
        csv_files = os.listdir(dir_path)
        final_df = []
        for csv_file in csv_files:
            print(csv_file)
            df = pd.read_csv(dir_path + '/' + csv_file)
            reviews_list = df[df.columns[1]].values.tolist()
            reviews_set = list(set(reviews_list))
            df = pd.DataFrame({'Reviews': reviews_set})
            final_df.append(df)
        df = pd.concat(final_df)
        df.drop_duplicates(inplace=True)
        print(dir_path + '/final_links_Bhanu.csv')
        df.to_csv(dir_path + '/final_links_Bhanu.csv')


    def removeDuplicateLinks_1(self, dir_path):
        df = pd.read_csv(dir_path)
        reviews_list = df[df.columns[1]].values.tolist()
        reviews_set = list(set(reviews_list))
        print(len(reviews_set))
        print(len(reviews_list))


if __name__ == '__main__':
    obj = Scrapping('')
    obj.removeDuplicateLinks_1('/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/final_links_Bhanu.csv')
    #temp_links = links
    #for i, link in enumerate(temp_links):
    #   p = Path(link)
    #    links.remove(link)
    #    obj.getAbstract1(link, p.name)
    #    break
