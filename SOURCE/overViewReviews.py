import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import os

class GetOverViewReviews:

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        # self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def getReviews(self, url, title):
        review_pages_list = []
        request_url = url + 'reviews'
        response = requests.get(request_url)
        self.driver.get(request_url)
        html = self.driver.page_source
        project_soup = BeautifulSoup(html, 'html.parser')
        overview_dict = self.getOverViewReviews(project_soup)
        print(overview_dict)

    def getOverViewReviews(self, project_soup):
        header_dict = self.getHeaderDetails(project_soup)
        reviews_dict = self.overViewReviews(project_soup)
        return {**header_dict, **reviews_dict}

    def getHeaderDetails(self, project_soup):
        section = project_soup.find_all('footer', attrs={'class': 'Grid-row Grid-row-nowrap u-pb-16'})
        data = {}
        for subsection in section[0].children:
            for subchildren in subsection.children:
                if len(subchildren.contents) > 1:
                    try:
                        overallrating = subchildren.contents[1].findAll('span', attrs={'class': 'rank-average strong'})[0].text
                        data['Product_Overall_rating'] = overallrating
                    except:
                        data['Product_Overall_rating'] = None
                    try:
                        frontRunners = subchildren.contents[1].findAll('span', attrs={'class': 'product-frontrunners-badge tooltip'})[0].text
                        data['AdviceFrom'] = frontRunners
                    except:
                        data['AdviceFrom'] = None
                    try:
                        recommendation = subchildren.contents[4].text
                        data['recommendation']=recommendation
                    except:
                        data['recommendation']=None
        return data

    def overViewReviews(self, project_soup):
        section = project_soup.find_all('section', attrs={'class': 'summary-container'})
        featuers = self.getOverallfeatureratings(section)
        ratings = self.getRatingsBreakDown(section)
        proscons = self.getProsandCons(section)
        final_dict = {**featuers, **ratings, **proscons}
        return final_dict

    def getOverallfeatureratings(self, section):
        ratingdiv = section[0].find_all('div', attrs={'class': 'Grid-row summary Grid-cell--6of12_md Grid-cell--12of12_sm'})
        children = ratingdiv[0].contents[0]
        children = children.contents[0]
        data = {}
        for subchild in children:
            if len(subchild.contents) == 2:
                try:
                    data[subchild.contents[0].text] = subchild.contents[1].text
                except:
                    continue

        return data

    def getRatingsBreakDown(self, section):
        div = section[0].find_all('div', attrs={'class': "histogram"})
        data = {}
        for children in div[0].children:
            try:
                data[children.contents[0].contents[0].text] = children.contents[0].contents[2].text
            except:
                continue
        return data

    def getProsandCons(self, section):
        div = section[0].find_all('ul', attrs={'class': "pros Grid-cell--6of12 Grid-cell--12of12_sm"})
        pros_list = []
        cons_list = []
        for children in div[0].children:
            try:
                if children.text == 'Pros':
                    continue
                pros_list.append(children.text)
            except:
                continue

        div = section[0].find_all('ul', attrs={'class': "cons Grid-cell--6of12 Grid-cell--12of12_sm"})
        for children in div[0].children:
            try:
                if children.text == 'Cons':
                    continue
                cons_list.append(children.text)
            except:
                continue

        data= {'Pros': pros_list,
               'Cons': cons_list}
        return data

obj = GetOverViewReviews()
obj.getReviews('https://www.softwareadvice.com/project-management/workzone-profile/', 'Bhanu')






