'''
Change file paths
'''

import os
import codecs
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import re

class Scrapping:

    #Intialisation

    def __init__(self, website_url):
        self.url = website_url
        options = Options()
        '''
        while running this code, if you are not able to collect the data, just comment this below line and try
        '''
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.delete_all_cookies()

    def readWebsite(self, link):
        page = urlopen(link)
        html = page.read().decode("utf-8")
        project_soup = BeautifulSoup(html, 'html.parser')
        section = project_soup.findAll('section',
                                       attrs={'class': 'ProductListComponent products'})
        product_list = []
        for div in section[0].findAll('div', attrs={'class': 'ProductCardComponent alternatives-card'}):
            product_card = div.find('a', attrs = {'class': 'product-title'})
            product_dict = {}
            title = product_card.text
            profile_link = product_card.attrs['href']
            product_dict['Title'] = title
            product_dict['Profile_link'] = profile_link
            product_list.append(product_dict)
        df = pd.DataFrame(product_list)
        df.to_csv('/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/CallCenter/AccountingProductLinks.csv')

    def getProduct_Details(self, filepath):
        df = pd.read_csv(filepath)
        tilte_list = df['Title'].values.tolist()
        links_list = df['Profile_link'].values.tolist()
        product_details_list = []
        for title, link in zip(tilte_list, links_list):
            product_dict = {}
            product_dict['Title'] = title
            overrviewDict = self.getProductOverView(link)
            product_dict.update(overrviewDict)
            product_details_list.append(product_dict)
        df = pd.DataFrame(product_details_list)
        df.to_csv('/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/HR/ProductDetailsOverView.csv')

    def getProductOverView(self, url):
        wait = WebDriverWait(self.driver, 5)
        self.driver.get(url)
        about_Dict = {}
        try:
            self.driver.find_element_by_link_text('Read more').click()
        except:
            print('No readmore')
        try:
            data = wait.until(EC.presence_of_element_located((By.ID, 'overview-text')))
            about_Dict['Product_Description'] = data.text
            pricingDict = self.getProduct_priceDetails(url)
            about_Dict.update(pricingDict)
        except:
            print('No Text')

        return about_Dict

    def getProduct_priceDetails(self, url):
        page = urlopen(url)
        html = page.read().decode("utf-8")
        project_soup = BeautifulSoup(html, 'html.parser')
        priceDict = {'Price_Description': None, 'Price': None, 'Free Trail': None, 'Free version': None}
        try:
            pricing = project_soup.find('div', attrs={'class': 'PricingComponent column pricing'})
            details = pricing.find('div', attrs={'class': 'pricing-details'})
            priceDict['Price_Description'] = self.checkForPricingDescription(details)
            priceDict['Price'] = self.checkForPrice(details)
            priceDict['Free Trail'] = self.checkForFreeTrail(details)
            priceDict['Free version'] = self.checkForFreeVersion(details)
        except:
            print("No Price Details")

        return priceDict

    def checkForPricingDescription(self, div):
        try:
            pricing_Description = div.find('p', attrs={'class': 'small pricing-details__desc'})
            return pricing_Description.text
        except:
            return None

    def checkForPrice(self, div):
        try:
            price = div.find('div', attrs={'class': 'pricing-details__price'})
            return price.contents[1].text
        except:
            return None

    def checkForFreeTrail(self, div):
        try:
            freeTrail = div.find('div', attrs={'class': 'pricing-details__freetrial'})
            return freeTrail.contents[1].text
        except:
            return None

    def checkForFreeVersion(self, div):
        try:
            freeVersion = div.find('div', attrs={'class': 'details__freeversion'})
            return freeVersion.contents[1].text
        except:
            return None

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

    def HTMLreviewPages(self, filepath):
        df = pd.read_csv(filepath)
        title_list = df['Title'].values.tolist()
       #links_list = df['Profile_URL'].values.tolist()
        links_list = df['Profile_link'].values.tolist()
        for title, url in zip(title_list, links_list):
            self.extractHTMLLink(url + 'reviews/', title)

    def extractHTMLLink(self, url, title):
        title = self.trimString(title)
        dir_path = "/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/CRM/HTML/"
        new_dir_path = dir_path + title + '/'
        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path)
        else:
            return
        wait = WebDriverWait(self.driver, 10)
        self.driver.get(url)
        textname = ""
        for i in range(0, 1000):
            try:
                text_element = self.driver.find_element_by_class_name('text-section')
                if text_element.text != textname:
                    textname = text_element.text
                    print(textname)
                    html = self.driver.page_source
                    project_soup = BeautifulSoup(html, 'html.parser')
                    with open(new_dir_path + str(i) + '.html', 'w') as f:
                        f.write(str(project_soup))
                    if self.checkfortotal(textname):
                        break
            except:
                break
            try:
                data = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'next')))
                if data == None:
                    break
                data.click()
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'back')))
            except:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'back')))
                continue

    def checkfortotal(self, text):
        text = text.replace(',', '')
        el = re.findall(r'\d+', text)
        return el[1] == el[2]

    def product_tilte(self, link):
        head = link.rsplit('/', 2)[-2]
        return head.split('-')[0]

    def trimString(self, title):
        return ''.join(char for char in title if char.isalnum())

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

    def getProductId(self, filepath):
        df = pd.read_csv(filepath)
        tilte_list = df['Title'].values.tolist()
        links_list = df['Profile_link'].values.tolist()
        product_details_list = []
        i = 0
        for title, link in zip(tilte_list, links_list):
            try:
                i += 1
                product_dict = {}
                product_dict['Title'] = title
                page = urlopen(link)
                html = page.read().decode("utf-8")
                project_soup = BeautifulSoup(html, 'html.parser')
                section = project_soup.findAll('div', attrs={'class': "column details__bottom"})
                id = section[0].findAll('p', attrs={'class': "small"})
                print(id)
                review_id = id[0].find('a').get('id')
                product_dict['Review_ID'] = review_id.split('reviews-link-')[1]
                product_dict['Profile_URL'] = link
                product_details_list.append(product_dict)
            except:
                print(i)
                continue
        df = pd.DataFrame(product_details_list)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/Accounting/ProductDetailsReviewLinks.csv')

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

    def getNofiles(self, dir_path):
        csv_files = os.listdir(dir_path)
        names_list = []
        for csvfile in csv_files:
            files = os.listdir(dir_path + '/' + csvfile)
            if len(files) == 0:
                names_list.append(csvfile)
        df = pd.DataFrame({'Tilte': names_list})
        df.to_csv('/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/CRM/Norviews.csv')


    def convertToPickleFormt(self, dir_path):
        csv_files = os.listdir(dir_path)
        for csvfile in csv_files:
            name, extension = os.path.splitext(csvfile)
            df = pd.read_csv(dir_path + csvfile)
            with open(dir_path + name + '.pickle', 'wb') as f:
                pickle.dump(df, f)


    def extractReviewsFromHTML(self, HTML_dir_path):
        csv_path = '/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/CRM/CSV/'
        html_dirs = os.listdir(HTML_dir_path)
        for htmlDir in html_dirs:
            if htmlDir is '.DS_Store':
                continue
            if not os.path.exists(csv_path + htmlDir):
                os.makedirs(csv_path + htmlDir)
            else:
                continue
            files = os.listdir(HTML_dir_path + htmlDir)
            if len(files) > 0:
                review_list_dict = []
                for file in files:
                    f = codecs.open(HTML_dir_path + htmlDir + '/' + file, 'r', 'utf-8')
                    soup = BeautifulSoup(f, "html.parser")
                    review_section = soup.find_all('div', attrs={'class': 'review'})
                    reviewwrapperList = review_section[0].find_all('div', attrs={'class': 'reviewItem-wrapper'})
                    for reviewWrapper in reviewwrapperList:
                        dict = {}
                        person = reviewWrapper.find_all('section', attrs = {'class': 'reviewer-information'})
                        person_dict = self.getPersonDetails(person)
                        rating = reviewWrapper.find_all('div', attrs= {'class': 'review-ranking u-hide-mobile-only'})
                        rating_dict= self.getratingDetails(rating)
                        overallrating = reviewWrapper.find_all('div', attrs = {'class': 'review-title review-title-desktop u-mb-32'})
                        overall_rating_dict = self.getOverallrating(overallrating)
                        review_details = reviewWrapper.find_all('div', attrs= {'class': 'review-copy-container'})
                        review_details_dict = self.getReviewDeatails(review_details)
                        review_responsedict = {"Review User Response": None}
                        try:
                            review_response = reviewWrapper.find_all('div', attrs= {'class': 'review-response'})
                            review_responsedict["Review User Response"] = self.getReviewResponse(review_response)
                        except:
                            print("No review repsonse")
                        dict.update(person_dict)
                        dict.update(rating_dict)
                        dict.update(overall_rating_dict)
                        dict.update(review_details_dict)
                        dict.update(review_responsedict)
                        review_list_dict.append(dict)
                df = pd.DataFrame(review_list_dict)
                df.to_csv(csv_path + htmlDir + '/' + htmlDir +'.csv')
                df.to_pickle(csv_path + htmlDir + '/' + htmlDir +'.pickle')

    def getPersonDetails(self, persondiv):
        personDict = {"Profile Name": None,
                      "Reviewer company": None,
                      "Reviewer industry": None,
                      "Time Used": None,
                      "ReviewSource": None}

        profile_name = persondiv[0].find_all('div', attrs= {'class': 'review-profile-user'})
        if len(profile_name) > 0:
            personDict["Profile Name"] = profile_name[0].text
        else:
            personDict["Profile Name"] = None

        compnay = persondiv[0].find_all('div', attrs= {'class': 'review-company'})

        if len(compnay) > 0:
            personDict["Reviewer company"] = compnay[0].text
        else:
            personDict["Reviewer company"] = None

        industry = persondiv[0].find_all('div', attrs= {'class': 'review-gdm-industry'})

        if len(industry) > 0:
            personDict["Reviewer industry"] = industry[0].text
        else:
            personDict["Reviewer industry"] = None

        timeUsed = persondiv[0].find_all('div', attrs= {'class': 'review-profile-time-used'})
        if len(timeUsed) > 0:
            personDict["Time Used"] = timeUsed[0].text
        else:
            personDict["Time Used"] = None

        revewSource = persondiv[0].find_all('div', attrs={'class': 'tooltip ui small'})
        if len(revewSource) > 0:
            personDict["ReviewSource"] = revewSource[0].text
        else:
            personDict["ReviewSource"] = None

        return personDict

    def getratingDetails(self, ratingdiv):
        ratingDict = {'Ease-of-use out of 5': None,
                      'Value for money out of 5': None,
                      'Customer support out of 5': None,
                      'Functionality out of 5': None}
        score_names = []
        scores = []
        try:
            scoreDescription = ratingdiv[0].find_all('section', attrs= {'class': 'score-description'})
            for score in scoreDescription:
                score_names.append(score.text)
        except:
            print("No Score description")

        try:
            actualScore = ratingdiv[0].find_all('section', attrs= {'class': 'score-image'})
            for score in actualScore:
                scores.append(score.text)
        except:
            print("No Scores")

        if len(score_names) > 0 & len(scores) > 0:
            for scorename, score in zip(score_names, scores):
                ratingDict[scorename] = score

        return ratingDict

    def getOverallrating(self, ratingdiv):
        overAllRating = ratingdiv[0].find_all('div', attrs= {'class': 'stars-container'})
        try:
            return {"Product_OverAllRatingScore": overAllRating[0].text}
        except:
            return {"Product_OverAllRatingScore": None}

    def getReviewDeatails(self, reviewDetailsDiv):
        data= {'Review_title': None,
               'Review_Summary': None,
               'hasPros': None,
               'hasCons': None,
               'Pros': None,
               'Cons': None
        }
        for child in reviewDetailsDiv[0].children:
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
        return data

    def getReviewResponse(self, responsediv):
        reviewresponse = responsediv[0].find_all('div', attrs= {'class': 'review-response-body'})
        return reviewresponse.text



if __name__ == '__main__':
    obj = Scrapping('https://www.softwareadvice.com/call-center/')
    #obj.readDriverElement('https://www.softwareadvice.com/call-center/', "View all products")
    #obj.getProductId('/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/CRM/AccountingProductLinks.csv')
    #obj.HTMLreviewPages('/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/CRM/AccountingProductLinks.csv')
    #obj.extractReviewsFromHTML('/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/CRM/HTML/')
    obj.getNofiles('/Users/bhanugollapudi/Documents/Projects/GetApp+projectManagement/CRM/CSV/')

