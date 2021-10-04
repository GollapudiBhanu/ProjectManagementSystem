import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd


class Scrapping:

    def __init__(self, website_url):
        self.url = website_url
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(options=options)

    def readWebsite(self, link):
        page = urlopen(link)
        html = page.read().decode("utf-8")
        project_soup = BeautifulSoup(html, 'html.parser')
        section = project_soup.findAll('section', attrs={'class': 'ProductListComponent products'})
        product_list = []
        for div in section[0].findAll('div', attrs={'class': 'ProductCardComponent'}):
            div_sec = div.findAll('section', attrs={'class': 'column products-tile__details'})
            title = list(div_sec[0].children)[0].getText()
            product_link = list(div_sec[0].children)[1].find('a').get('href')
            reviews = self.getReviews(product_link, title)
            df = pd.DataFrame(reviews)
            # data = {'Title': title,
            #        'Review': reviews}
            product_list.append(df)
            # description = self.getProductText(product_link)
            # data = {'title': title,
            #        'Product_Description': description}
            # product_list.append(data)
        vertical_stack = pd.concat(product_list, axis=0)
        vertical_stack.to_csv(
            '/Users/bhanugollapudi/Documents/Ding_Proj/Project_Management_Software/ProjectManagementSoftware_Reviews_1.csv')

    def readDriverElement(self, url, link_text):
        wait = WebDriverWait(self.driver, 5)
        try:
            self.driver.get(url)
        except:
            pass
        try:
            view_all_products_link = wait.until(
                EC.presence_of_element_located((By.LINK_TEXT, link_text))).get_attribute('href')
            self.readWebsite(view_all_products_link)
        except:
            print('error')

    def getProductText(self, url):
        wait = WebDriverWait(self.driver, 5)
        self.driver.get(url)
        try:
            self.driver.find_element_by_link_text('Read more').click()
        except:
            print('No readmore')
        try:
            data = wait.until(EC.presence_of_element_located((By.ID, 'overview-text')))
            return data.text
        except:
            print('No Text')
            return None

    def getReviewLink(self, url):
        page = urlopen(url)
        html = page.read().decode("utf-8")
        project_soup = BeautifulSoup(html, 'html.parser')
        section = project_soup.findAll('div', attrs={'class': 'MenuItemComponent column menu__item'})
        link = section[0].find('a').get('href')
        if link is None:
            self.getSinglePageReviews(project_soup)
        else:
            return link

    def getSinglePageReviews(self, url, title):
        page = urlopen(url)
        html = page.read().decode("utf-8")
        project_soup = BeautifulSoup(html, 'html.parser')
        section = project_soup.findAll('div', attrs={'class': 'review-copy-container'})
        data = self.getReviewsData(section)
        data['Title'] = title
        try:
            profile_name = project_soup.findAll('div', attrs={'class': 'review-profile-user'})[0].text
            data['User_Name'] = profile_name
        except:
            data['User_Name'] = None
        return [data]

    def getReviews(self, url, title):
        review_pages_list = []
        for i in range(1, 100):
            request_url = url + 'reviews/?review.page=' + str(i)
            response = requests.get(request_url)
            if response.status_code == 404:
                return self.getSinglePageReviews(url, title)
            self.driver.get(request_url)
            html = self.driver.page_source
            project_soup = BeautifulSoup(html, 'html.parser')
            try:
                right_button = project_soup.find('div', class_="pagination-arrows-right")
                reviews_list = project_soup.findAll('div', attrs={'class': 'reviews'})
                review_pages_list.append(reviews_list[0])
                if right_button is None:
                    break
            except:
                continue
        data_list = self.getPaginationReviews(review_pages_list, title)
        return data_list

    def getPaginationReviews(self, review_pages_list, title):
        data_list = []
        review_dict = {}
        for review_page in review_pages_list:
            for div in review_page.findAll('div', attrs={'class': 'review'}):
                try:
                    review_summary = div.findAll('div', attrs={'class': 'review-copy-container'})
                    review_dict = self.getReviewsData(review_summary)
                except:
                    print('error')
                review_dict['Title'] = title
                try:
                    profile_name = div.findAll('p', attrs={'class': 'review-profile-user'})[0].text
                    review_dict['User_Name'] = profile_name
                except:
                    review_dict['User_Name'] = None
                data_list.append(review_dict)
        return data_list

    def getReviewsData(self, review_summary):
        data = {}
        for child in review_summary[0].children:
            try:
                if child.attrs['class'][0] == 'review-copy-header':
                    data['Review_title'] = child.text
                elif child.attrs['class'][0] == 'review-copy-summary':
                    data['Review_Summary'] = child.text
                elif child.text == 'Pros':
                    data['hasPros'] = True
                elif child.text == 'Cons':
                    data['hasCons'] = True
                elif child.attrs['class'][0] == 'ui' and data['hasPros'] == True:
                    data['hasPros'] = False
                    data['Pros'] = child.text
                elif child.attrs['class'][0] == 'ui' and data['hasCons'] == True:
                    data['Cons'] = child.text
            except:
                continue
        for child in review_summary[0].children:
            try:
                extract_data = child.find_all('p')
                data[extract_data[0].text] = extract_data[1].text
            except:
                continue
        return data


if __name__ == '__main__':
    obj = Scrapping('https://www.softwareadvice.com/project-management/')
    obj.readDriverElement('https://www.softwareadvice.com/project-management/', "View all products")
    # obj.getSinglePageReviews('https://www.softwareadvice.com/project-management/rodeo-profile/')
