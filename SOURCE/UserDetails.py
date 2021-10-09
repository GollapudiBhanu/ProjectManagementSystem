import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import os
from ProjectManagementSoftware.Utilities import Reusable
import re

class GetUserDetails:

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        # self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def getUserDetails(self, review_pages_list):
        review_list = []
        for review_page in review_pages_list:
            review_ranking_dict = {}
            for div in review_page.findAll('div', attrs={'class': 'review'}):
                ratingdict = self.getRating(div)
                try:
                    div = div.findAll('div', attrs={'class': 'review-person Grid-cell Grid-cell--3of12'})
                    subdiv = div[0].findAll('div', attrs={'class': 'content'})
                    children = subdiv[0].children
                    for subchildren in children:
                        data = {}
                        try:
                            className = " ".join(subchildren.attrs['class'])
                            if className == 'review-ranking':
                                review_ranking_dict = self.getReviewRanking(subchildren)
                            else:
                                textlist = Reusable.splitString(subchildren.text, ':')
                                if len(textlist) == 1:
                                    if textlist[0] == 'Verified Reviewer':
                                        data['Verified Reviewer'] = True
                                    else:
                                        data['UserName'] = data[0] 
                                elif len(textlist) > 1:
                                    data[textlist[0]] = textlist[1]
                        except:
                            continue
                        ratingdict = {**data, **ratingdict}
                except:
                    print('Error')
                final_dict = {**ratingdict, **review_ranking_dict}
                review_list.append(final_dict)
        return review_list

    def getRating(self, div):
        data = {}
        try:
            subdiv = div.findAll('div', attrs={'class': 'review-title review-title-tablet Grid'})
            for children in subdiv[0].children:
                className = " ".join(children.attrs['class'])
                if className == 'Grid-cell':
                    data['ReviewDate'] = children.text
                else:
                    rating = self.getRatingscore(className)
                    data['ReviewRating'] = rating
        except:
            print('No review ratings')
        return data

    def getReviewRanking(self, subchildren):
        data = {}
        for schild in subchildren.children:
            textlist = Reusable.getRating(schild.text)
            data[textlist[0]] = textlist[1]
        return data

    def getReviews(self, url, title):
        review_pages_list = []
        for i in range(1, 100):
            request_url = url + 'reviews/?review.page=' + str(i)
            response = requests.get(request_url)
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
        final_list = self.getUserDetails(review_pages_list)
        print(final_list)

    def getRatingscore(self, className):
        if className == 'new-stars new-stars-x2 new-stars-rank new-stars-rank__20':
            return 1
        elif className == 'new-stars new-stars-x2 new-stars-rank new-stars-rank__40':
            return 2
        elif className == 'new-stars new-stars-x2 new-stars-rank new-stars-rank__60':
            return 3
        elif className == 'new-stars new-stars-x2 new-stars-rank new-stars-rank__80':
            return 4
        elif className == 'new-stars new-stars-x2 new-stars-rank new-stars-rank__100':
            return 5
        else:
            return 0

obj = GetUserDetails()
obj.getReviews('https://www.softwareadvice.com/project-management/moovila-profile/', 'Bhanu')