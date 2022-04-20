import os
import pandas as pd
import numpy as np

class Relevancy:

    def __init__(self, dir_path, out_dir_path):
        self.dir_path = dir_path
        self.out_dir_path = out_dir_path
        self.productNames = self.getOtherProductNames()
        self.webisteNames = self.getWebsiteNames()

    def relevancyRepresentation(self):
        csv_files = os.listdir(self.dir_path)
        for csvfile in csv_files:
            if csvfile == '.DS_Store':
                continue
            productName = self.getProductName(csvfile)
            df = pd.read_csv(self.dir_path + csvfile)
            df['reviewDescription'].replace(np.nan, '', inplace=True)
            df['pros'].replace(np.nan, '', inplace=True)
            df['cons'].replace(np.nan, '', inplace=True)
            descriptionList = df['reviewDescription'].values.tolist()
            prosList = df['pros'].values.tolist()
            consList = df['cons'].values.tolist()
            relevance_productNamelist = []
            relevance_websiteList =[]
            relevance_otherproductNameList = []

            prosrelevance_productNamelist = []
            prosrelevance_websiteList = []
            prosrelevance_otherproductNameList = []

            consrelevance_productNamelist = []
            consrelevance_websiteList = []
            consrelevance_otherproductNameList = []

            for description, pro, cons in zip(descriptionList, prosList,consList):
                description_prodcutNameDict = self.calculateProductNameRelevance(description, productName)
                description_websiteDict = self.calculateWebsiteRelevance(description)
                description_OtherprodcutNameDict =  self.calculateOtherProductNamesRelevance(description)

                relevance_productNamelist.append(description_prodcutNameDict)
                relevance_websiteList.append(description_websiteDict)
                relevance_otherproductNameList.append(description_OtherprodcutNameDict)

                pro_prodcutNameDict = self.calculateProductNameRelevance(pro, productName)
                pro_websiteDict = self.calculateWebsiteRelevance(pro)
                pro_OtherprodcutNameDict = self.calculateOtherProductNamesRelevance(pro)

                prosrelevance_productNamelist.append(pro_prodcutNameDict)
                prosrelevance_websiteList.append(pro_websiteDict)
                prosrelevance_otherproductNameList.append(pro_OtherprodcutNameDict)

                cons_prodcutNameDict = self.calculateProductNameRelevance(cons, productName)
                cons_websiteDict = self.calculateWebsiteRelevance(cons)
                cons_OtherprodcutNameDict = self.calculateOtherProductNamesRelevance(cons)

                consrelevance_productNamelist.append(cons_prodcutNameDict)
                consrelevance_websiteList.append(cons_websiteDict)
                consrelevance_otherproductNameList.append(cons_OtherprodcutNameDict)


            df['Description_ProductName_relevance'] = relevance_productNamelist
            df['Description_Website_relevance'] = relevance_websiteList
            df['Description_OtherProductName_relevance'] = relevance_otherproductNameList

            df['pros_ProductName_relevance'] = prosrelevance_productNamelist
            df['pros_Website_relevance'] = prosrelevance_websiteList
            df['pros_OtherProductName_relevance'] = prosrelevance_otherproductNameList

            df['Cons_ProductName_relevance'] = consrelevance_productNamelist
            df['Cons_Website_relevance'] = consrelevance_websiteList
            df['Cons_OtherProductName_relevance'] = consrelevance_otherproductNameList

            df.to_csv(self.out_dir_path + csvfile, index=None)

    def calculateRelevance(self, text, productName):
        productName_rel = self.calculateProductNameRelevance(text, productName)
        website_rel = self.calculateWebsiteRelevance(text)
        otherProductName_rel = self.calculateOtherProductNamesRelevance(text)
        return  (productName_rel, website_rel, otherProductName_rel)

    def calculateWebsiteRelevance(self, text):
        countDict = {}
        for websiteName in self.webisteNames:
            countDict[websiteName] = text.lower().count(websiteName.lower())
        return countDict

    def calculateOtherProductNamesRelevance(self, text):
        countDict = {}
        for websiteName in self.productNames:
            countDict[websiteName] = text.lower().count(websiteName.lower())
        return countDict

    def calculateProductNameRelevance(self, text, productname):
        return text.lower().count(productname.lower())

    def getProductName(self, fileName):
        filename = fileName.split('.')
        return filename[0].split('Reviews')[0]

    def getWebsiteNames(self):
        return ['Getapp', 'SoftwareAdvice', 'Capterra']

    def getOtherProductNames(self):
        df = pd.read_csv('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/GetappDocs/CombinedRanking.csv')
        return df['Product Name'].values.tolist()

if __name__ == '__main__':
    obj = Relevancy('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Concise_Representation/',
                      '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Relevancy/' )
    obj.relevancyRepresentation()


