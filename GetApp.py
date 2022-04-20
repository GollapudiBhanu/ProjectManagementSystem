import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import os

class Scrapping:

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(options=options)

    def getProductReviewURLS(self):
        review_pages_list = []
        for i in range(1, 30):
            request_url = 'https://www.getapp.com/customer-management-software/crm/page-' + str(i) + '/'
            response = requests.get(request_url)
            if response.status_code == 404:
                continue
            self.driver.get(request_url)
            html = self.driver.page_source
            project_soup = BeautifulSoup(html, 'html.parser')
            products = project_soup.findAll('div', attrs={'class': 'MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-12 MuiGrid-grid-md-8 MuiGrid-grid-lg-9'})
            for product in products:
                reviews = product.findAll('div', attrs={'class': 'jss328'})
                for review in reviews.children:
                    print(review)
                    print("#########")
                break

    def getNoReviewProducts(self, dirpath):
        csv_files = os.listdir(dirpath)
        names = []
        for csvfile in csv_files:
            try:
                df = pd.read_csv(dirpath + csvfile)
                if df.size == 0:
                    name=csvfile.split('PricingFeaturesReviewsAlternatives.csv')[0]
                    names.append(name)
            except:
                continue
        df = pd.DataFrame({"NoReviews": names})
        df.to_csv('/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/ScoreRanking/NoReviewProducts.csv')



if __name__ == '__main__':
    obj = Scrapping()
    #obj.getProductReviewURLS()
    obj.getNoReviewProducts('/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Get_APP_docs/')
