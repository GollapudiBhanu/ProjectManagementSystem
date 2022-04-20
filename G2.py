import requests
from selenium.webdriver.chrome.options import Options
import os
import codecs
import urllib
import urllib.request
import json
from bs4 import BeautifulSoup
import pandas as pd
import re

class G2:

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        #self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def scrapeData(self):
        for i in range(1, 14):
            request_url = 'https://www.g2.com/categories/project-management?order=g2_score&page='+str(i) +'#product-list'
            response = requests.get(request_url)
            if response.status_code == 404:
                break
            self.driver.get(request_url)
            html = self.driver.page_source
            project_soup = BeautifulSoup(html, 'html.parser')
            with open('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/G2/' + str(i) + ".html", "w") as file:
                file.write(str(project_soup))


    def readHTML(self, dirpath):
        f=codecs.open(dirpath, 'r', 'utf-8')
        soup = BeautifulSoup(f, "html.parser")
        for tag in soup.find_all():
            header = tag.find_all('span')
            print(header)
            break


    def ExtractImageURL(self, dir_path):
        HTMLFiles = os.listdir(dir_path)
        imageLinks = []
        for HTMLFile in HTMLFiles:
            if HTMLFile == '.DS_Store':
                continue
            f = codecs.open(dir_path + HTMLFile, 'r', 'utf-8')
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text('\n')
            links = re.findall(r'(https?://[^\s]+)', text)
            for link in links:
                if 'https://images.g2crowd.com/uploads/product/' in link:
                    if ('.svg' in link) or ('.png' in link):
                        imageLinks.append(link)
        imageLinks = list(set(imageLinks))
        df = pd.DataFrame({'ImageLinks': imageLinks})
        df.to_csv('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/G2/ImageLinks.csv')

    def ExtractOneFile(self, filePath):
        imageLinks = []
        f = codecs.open(filePath, 'r', 'utf-8')
        soup = BeautifulSoup(f, "html.parser")
        text = soup.get_text('\n')
        links = re.findall(r'(https?://[^\s]+)', text)
        for link in links:
            if 'https://images.g2crowd.com/uploads/product/' in link:
                if ('.svg' in link) or ('.png' in link):
                    imageLinks.append(link)

        imageLinks = list(set(imageLinks))
        df = pd.DataFrame({'ImageLinks': imageLinks})
        df.to_csv('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/G2/ImageLinks1.csv')


    def filterUrls(self, csvFilepath):
        df = pd.read_csv(csvFilepath, index_col=None)
        urls = df['ImageLinks'].values.tolist()
        urlDict = {}
        for url in urls:
            productName = self.extractproductName(url).split('.')[0]
            if productName in urlDict.keys():
                values = urlDict[productName]
                values.append(url)
                urlDict[productName] = values
            else:
                urlDict[productName] = [url]

        a_file = open("/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/G2/ImageLinks2.json", "w")
        json.dump(urlDict, a_file)
        a_file.close()

    def extractproductName(self, url):
        productName = url.split("/")[-1]
        return productName

if __name__ == '__main__':
    obj = G2()
    #obj.scrapeData()
    #obj.readHTML('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/G2/1.html')
    #obj.ExtractImageURL('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/G2/')
    #https://www.g2.com/categories/project-management?order=g2_score#product-list

    #obj.ExtractOneFile('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/G2/5.html')
    obj.filterUrls('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/G2/ImageLinks.csv')
