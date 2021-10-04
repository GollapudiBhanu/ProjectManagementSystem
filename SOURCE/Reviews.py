from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import pandas as pd
import time

class Scrapping:

    def __init__(self, url):
        self.url = url
        options = Options()
        #options.add_argument('--headless')
        #options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome()

    def readWebsite(self, link):
        page = urlopen(link)
        html = page.read().decode("utf-8")
        project_soup = BeautifulSoup(html, 'html.parser')
        section = project_soup.findAll('section', attrs={'class': 'ProductListComponent products'})

        for div in section[0].findAll('div', attrs={'class': 'ProductCardComponent'}):
            div_sec = div.findAll('section', attrs={'class': 'column products-tile__details'})
            product_link = list(div_sec[0].children)[1].find('a').get('href')
            #self.getProductText(product_link)


    def get_Reviews(self, link_text):
        wait = WebDriverWait(self.driver, 5)
        try:
            self.driver.get(self.url)
        except:
            pass
        try:
            view_all_products_link = wait.until(
                EC.presence_of_element_located((By.LINK_TEXT, link_text))).get_attribute('href')
            self.readWebsite(view_all_products_link)
        except:
            print('error')

    def getReviewLink(self, url):
        page = urlopen(url)
        html = page.read().decode("utf-8")
        project_soup = BeautifulSoup(html, 'html.parser')
        section = project_soup.findAll('div', attrs={'class': 'MenuItemComponent column menu__item'})
        link = section[0].find('a').get('href')
        if link is None:
            #self.reviews(project_soup)
            self.getPagination(project_soup)
            return None
        else:
            return link

    def getReviews(self, url):
        review_link = self.getReviewLink(url)
        if review_link is not None:
            page = urlopen(review_link)
            html = page.read().decode("utf-8")
            project_soup = BeautifulSoup(html, 'html.parser')
            reviews_list = project_soup.findAll('div', attrs={'class': 'reviews'})
            for div in reviews_list[0].findAll('div', attrs={'class': 'review'}):
                try:
                    review_summary = div.findAll('div', attrs={'class': 'review-copy-container'})
                    s = review_summary[0].find_all("p", {"class": "ui"})
                    print(s[0].text)
                    print(s[1].text)
                    print(s[2].text)
                    print(s[3].text)
                    print(s[4].text)
                except:
                    print('No profile_name')

    def reviews(self, project_soup):
        section = project_soup.findAll('div', attrs={'class': 'review-copy-container'})

        s = section[0].find_all("p", {"class": "ui"})
        print(s[0].text)
        print(s[1].text)

        s = section[0].find_all("p", {"class": "review-copy-header strong"})
        print(s)
        print(s[0].text)

        s = section[0].find_all("p", {"class": "review-copy-sub-header strong"})
        print(s[0].text)

        s = section[0].find_all("p", {"class": "review-copy-sub-header strong"})
        print(s[0].text)

        print('######')
        section = project_soup.findAll('p', attrs={'class': 'small review-profile-defined'})

        print(section)
        print(section[0].text)


    def getPagination(self, review_link):
        product_all_pages = []
        for i in range(1, 12):
            request = "https://www.softwareadvice.com/project-management/workzone-profile/reviews/?review.page=" + str(i)
            response = requests.get(request)
            self.driver.get(request)
            html = self.driver.page_source
            project_soup = BeautifulSoup(html, 'html.parser')
            try:
                right_button = project_soup.find('div', class_="pagination-arrows-right")
                reviews_list = project_soup.findAll('div', attrs={'class': 'reviews'})
                product_all_pages.append(reviews_list[0])
                if right_button is None:
                    break
            except:
                continue
        print(len(product_all_pages))
        review_list = []

        for review_page in product_all_pages:
            for div in review_page.findAll('div', attrs={'class': 'review'}):
                data = {'Title': 'Bhanu'}
                try:
                    profile_name = div.findAll('p', attrs={'class': 'review-profile-name'})[0].text
                    data['User_Name'] = profile_name
                except:
                    data['User_Name'] = None
                try:
                    review_summary = div.findAll('div', attrs={'class': 'review-copy-container'})
                    for child in review_summary[0].children:
                        try:
                            te = child.find_all('p')
                            print(te)
                            print(te[0].text)
                            print(te[1].text)
                        except:
                            continue
                except:
                    print('Error')





if __name__ == '__main__':
    obj = Scrapping('https://www.softwareadvice.com/project-management/openair-srp-profile/')
    #obj.getProductText('https://www.softwareadvice.com/project-management/openair-srp-profile/')
    #obj.getReviews('https://www.softwareadvice.com/project-management/rodeo-profile/')
    obj.getPagination('https://www.softwareadvice.com/project-management/workzone-profile/reviews/')
    #obj.getReviews('https://www.softwareadvice.com/project-management/workzone-profile/reviews/')



'''
1.review-profile-name
2.review-profile-company
3.review-copy-header strong
4.review-copy-summary ui
5.review-copy-pros ui
6.review-copy-cons ui
7.review-profile-size
8.class="review-profile-time-used"

'''