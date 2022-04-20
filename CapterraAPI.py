import requests
import pandas as pd
import json

class ExtractJson:

    def __init__(self):
        pass

    def extractJSON(self, urlTuple):
        hitsList = []
        product_id = urlTuple[0]
        product_name = urlTuple[1]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        intial_URL = 'https://www.capterra.com/spotlight/rest/reviews?apiVersion=2&productId='
        i = 0
        intialvalue = 0
        finalValue = 100
        while(i <= 30):
            review_URL = intial_URL + str(product_id) + '&from=' + str(intialvalue) + '&size=' + str(finalValue)
            response = requests.get(review_URL, headers=headers)
            if response.status_code == 200:
                hitsList.append(response.json()['hits'])
            else:
                break
            intialvalue = finalValue
            finalValue += finalValue
            i += 1
        self.save(product_name, hitsList)

    def save(self, fileName, hitsList):
        fileName = self.trim(fileName)
        dir_path = '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/Capterra/'
        if len(hitsList) > 0:
            with open(dir_path + fileName + '.txt', 'a', encoding='utf-8') as f:
                for hit in hitsList:
                    json.dump(hit, f)
                    f.write('\n')


    def trim(self, filename):
        return ''.join(char for char in filename if char.isalnum())



    def splitString(self, url):
        urllist = url.split('/')
        return (urllist[2], urllist[3])

    def readCSV(self):
        df = pd.read_csv('/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Datafinal_links_Bhanu.csv')
        review_links = df['Reviews'].values.tolist()
        for reviewURL in review_links:
            urlTuple = self.splitString(reviewURL)
            self.extractJSON(urlTuple)


if __name__ == '__main__':
    obj = ExtractJson()
    obj.readCSV()



