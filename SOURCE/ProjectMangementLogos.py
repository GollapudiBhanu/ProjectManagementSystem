import os
import pandas as pd
import json
from statistics import mean
import numpy as np
from sklearn import preprocessing


class Logos:

    def __init__(self):
        pass

    def complteness(self, dir_path):
        csvFiles = os.listdir(dir_path)
        for file in csvFiles:
            if file is '.DS_Store':
                continue
            df = pd.read_csv(dir_path + file)
            Description_Completeness = df['Description_Completeness'].values.tolist()
            pros_list = df['Pros_Completeness'].values.tolist()
            cons_list = df['Cons_Completeness'].values.tolist()

            description_tuple = self.totalScoreCompleteness(Description_Completeness)
            pros_tuple = self.totalScoreCompleteness(pros_list)
            cons_tuple = self.totalScoreCompleteness(cons_list)

            df['Description_Completeness_Score'] = description_tuple[0]
            df['Description_Completeness_Average'] = description_tuple[1]

            df['Pros_Completeness_Score'] = pros_tuple[0]
            df['Pros_Completeness_Average'] = pros_tuple[1]

            df['Cons_Completeness_Score'] = cons_tuple[0]
            df['Cons_Completeness_Average'] = cons_tuple[1]

            df.to_csv(
                '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/' + file)

    def totalScoreCompleteness(self, listCompDict):
        totalScores = []
        totalAverage = []
        for comp_dict in listCompDict:
            comp_dict = comp_dict.replace("'", '"')
            comp_dict = json.loads(comp_dict)
            totalScore = sum(list(comp_dict.values()))
            avg = totalScore / len(list(comp_dict.values()))
            totalAverage.append(avg)
            totalScores.append(totalScore)
        return totalScores, totalAverage

    def getAppTimeliness(self, dir_path):
        csvFiles = os.listdir(dir_path)
        timeDict = {}

        prodcutNameList = []
        updateMeanList = []

        for file in csvFiles:
            if file is '.DS_Store':
                continue
            df = pd.read_csv(dir_path + file)
            days_list = df['DiffereceInDays'].values.tolist()
            update_list = []
            for day in days_list:
                day = day.split(' days')[0]
                update_list.append(int(day))
            m = mean(update_list)
            fileName = self.getProductName(file)
            prodcutNameList.append(fileName)
            updateMeanList.append(m)

        timeDict['ProductName'] = prodcutNameList
        timeDict['TimeLinessMean'] = updateMeanList
        df = pd.DataFrame(timeDict)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Timeliness/OverrviewTimeliness.csv')

    def getProductName(self, fileName):
        fileName = fileName.split('.')
        fileName = fileName[0].split('Reviews')[0]
        return fileName

    def conciseRepresentation(self, dir_path):
        csvFiles = os.listdir(dir_path)
        for file in csvFiles:
            if file is '.DS_Store':
                continue

            df = pd.read_csv(dir_path + file)

            description_list = df['Num Sentences in content'].values.tolist()
            pros_list = df['Num Sentences in pros'].values.tolist()
            cons_list = df['Num Sentences in cons'].values.tolist()
            concise_list = []

            for descriptionscore, proscore, conscore in zip(description_list, pros_list, cons_list):
                concise_list.append(descriptionscore + proscore + conscore)

            df['Total Sentences'] = concise_list
            df.to_csv(
                '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/ConciseRepresentation/' + file)

    def calculateSentimentalAnalysis(self, dir_path):
        csvFiles = os.listdir(dir_path)
        for file in csvFiles:
            if file == '.DS_Store':
                continue
            df = pd.read_csv(dir_path + file)
            df1 = df[
                ['ReviewDescription_score', 'ReviewDescription_Sentiment', 'Pros_score', 'pros_Sentiment', 'cons_score',
                 'cons_Sentiment']]
            sentimentList = []
            for index, row in df1.iterrows():
                description = self.getValue(row['ReviewDescription_Sentiment'], row['ReviewDescription_score'])
                pro = self.getValue(row['pros_Sentiment'], row['Pros_score'])
                con = self.getValue(row['cons_Sentiment'], row['cons_score'])
                sentiment = description + pro + con
                sentimentList.append(sentiment)
            df['Sentiment'] = sentimentList
            df.to_csv(
                '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Sentiment/' + file)

    def getValue(self, status, value):
        if status == 'NEGATIVE':
            return value * -1
        return value

    def calculateOverAllSentiments(self, dir_path):
        csvFiles = os.listdir(dir_path)
        productList = []
        listOfValues = []
        for file in csvFiles:
            if file == '.DS_Store':
                continue
            df = pd.read_csv(dir_path + file)
            value = sum(df['Sentiment'].values.tolist())
            listOfValues.append(value)
            productList.append(file)
        fileName = self.getLastPathComponet(dir_path)
        df = pd.DataFrame({'ProductName': productList,
                           'Sentiment': listOfValues})
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/' + fileName + '.csv')

    def getConciseRepresenation(self, dirpath):
        csvFiles = os.listdir(dirpath)
        productList = []
        listOfValuse = []
        for file in csvFiles:
            if file == '.DS_Store':
                continue
            df = pd.read_csv(dirpath + file)
            listOfValuse.append(sum(df['Total Sentences'].values.tolist()))
            productList.append(file)
        fileName = self.getLastPathComponet(dirpath)
        df = pd.DataFrame({'ProductName': productList,
                           'ConciseRepresntation': listOfValuse})
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/' + fileName + '.csv')

    def getOverallRelevancyScore(self, dirpath):
        csvFiles = os.listdir(dirpath)
        productList = []
        listOfValuse = []
        listOfAvg = []
        for file in csvFiles:
            if file == '.DS_Store':
                continue

            df = pd.read_csv(dirpath + file)
            df1 = df.loc[:, ['Description_website_Score', 'Description_otherWebsite_Score',
                             'Pros_website_Score', 'Pros_otherWebsite_Score',
                             'Cons_website_Score', 'Cons_otherWebsite_Score']]
            df2 = df.loc[:, ['Description_website_Average', 'Description_otherWebsite_Average',
                             'Pros_website_Average', 'Pros_otherWebsite_Average',
                             'Cons_website_Average', 'Cons_otherWebsite_Average']]

            scorevalues = df1.values.tolist()
            avgvalues = df2.values.tolist()
            valuesum = sum(map(np.array, scorevalues))
            avgsum = sum(map(np.array, avgvalues))
            a = sum(np.array(valuesum))
            b = sum(np.array(avgsum))
            listOfValuse.append(a)
            listOfAvg.append(b)
            productList.append(file)

        fileName = self.getLastPathComponet(dirpath)
        df = pd.DataFrame({'ProductName': productList,
                           'Score Sum': listOfValuse,
                           'Avg Sum': listOfAvg})
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/' + fileName + '.csv')

    def getOverallCombinedScore(self, dirpath):
        csvFiles = os.listdir(dirpath)
        productList = []
        listOfValuse = []
        listOfAvg = []
        for file in csvFiles:
            if file == '.DS_Store':
                continue

            df = pd.read_csv(dirpath + file)
            df1 = df.loc[:, ['Description_Completeness_Score',
                             'Pros_Completeness_Score',
                             'Cons_Completeness_Score']]
            df2 = df.loc[:, ['Description_Completeness_Average',
                             'Pros_Completeness_Average',
                             'Cons_Completeness_Average']]

            scorevalues = df1.values.tolist()
            avgvalues = df2.values.tolist()
            valuesum = sum(map(np.array, scorevalues))
            avgsum = sum(map(np.array, avgvalues))
            a = sum(np.array(valuesum))
            b = sum(np.array(avgsum))
            listOfValuse.append(a)
            listOfAvg.append(b)
            productList.append(file)

        fileName = self.getLastPathComponet(dirpath)
        df = pd.DataFrame({'ProductName': productList,
                           'Score Sum': listOfValuse,
                           'Avg Sum': listOfAvg})
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/' + fileName + '.csv')

    def getLastPathComponet(self, lastPath):
        fileName = lastPath.split('/')[-2]
        return fileName

    def calculateRelevancy(self, dir_path):
        csvFiles = os.listdir(dir_path)
        for file in csvFiles:
            if file == '.DS_Store':
                continue

            df = pd.read_csv(dir_path + file)
            # description_prodctName = df['Description_ProductName_relevance'].values.tolist()
            description_website = df['Description_Website_relevance'].values.tolist()
            description_otherProduct = df['Description_OtherProductName_relevance'].values.tolist()

            # pros_prodctName = df['pros_ProductName_relevance'].values.tolist()
            pros_website = df['pros_Website_relevance'].values.tolist()
            pros_otherProduct = df['pros_OtherProductName_relevance'].values.tolist()

            # cons_prodctName = df['Cons_ProductName_relevance'].values.tolist()
            cons_website = df['Cons_Website_relevance'].values.tolist()
            cons_otherProduct = df['Cons_OtherProductName_relevance'].values.tolist()

            # description_product_tuple = self.totalScoreCompleteness(description_prodctName)
            description_website_tuple = self.totalScoreCompleteness(description_website)
            description_other_tuple = self.totalScoreCompleteness(description_otherProduct)

            # pros_product_tuple = self.totalScoreCompleteness(pros_prodctName)
            pros_website_tuple = self.totalScoreCompleteness(pros_website)
            pros_other_tuple = self.totalScoreCompleteness(pros_otherProduct)

            # cons_product_tuple = self.totalScoreCompleteness(cons_prodctName)
            cons_website_tuple = self.totalScoreCompleteness(cons_website)
            cons_other_tuple = self.totalScoreCompleteness(cons_otherProduct)

            # df['Description_product_Score'] = description_product_tuple[0]
            # df['Description_product_Average'] = description_product_tuple[1]

            df['Description_website_Score'] = description_website_tuple[0]
            df['Description_website_Average'] = description_website_tuple[1]

            df['Description_otherWebsite_Score'] = description_other_tuple[0]
            df['Description_otherWebsite_Average'] = description_other_tuple[1]

            # df['Pros_product_Score'] = pros_product_tuple[0]
            # df['Pros_product_Average'] = pros_product_tuple[1]

            df['Pros_website_Score'] = pros_website_tuple[0]
            df['Pros_website_Average'] = pros_website_tuple[1]

            df['Pros_otherWebsite_Score'] = pros_other_tuple[0]
            df['Pros_otherWebsite_Average'] = pros_other_tuple[1]

            # df['Cons_product_Score'] = cons_product_tuple[0]
            # df['Cons_product_Average'] = cons_product_tuple[1]

            df['Cons_website_Score'] = cons_website_tuple[0]
            df['Cons_website_Average'] = cons_website_tuple[1]

            df['Cons_otherWebsite_Score'] = cons_other_tuple[0]
            df['Cons_otherWebsite_Average'] = cons_other_tuple[1]

            df.to_csv(
                '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Relevancy/' + file)

    def mergeDatFrame(self):
        df1 = pd.read_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Completeness.csv')
        df2 = pd.read_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/ConciseRepresentation.csv')
        df3 = pd.read_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Relevancy.csv')
        df4 = pd.read_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Sentiment.csv')
        df = pd.concat([df1, df2, df3, df4], axis=1)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Final_Logos.csv')

    def calculateScoreValues(self, dir_path, outputfilepath):
        csvFiles = os.listdir(dir_path)
        productNamesList = []
        overallRating = []
        ValueForMoney = []
        EaseofUse = []
        Features = []
        CustomerSupport = []
        Likelihoodtorecommned = []
        for file in csvFiles:
            if file == '.DS_Store':
                continue
            df = pd.read_csv(dir_path + file)
            overallRating.append(mean(df['OverAllRating'].values.tolist()))
            ValueForMoney.append(mean(df['Value For Money'].values.tolist()))
            EaseofUse.append(mean(df['Ease of Use'].values.tolist()))
            Features.append(mean(df['Features'].values.tolist()))
            CustomerSupport.append(mean(df['Customer Support'].values.tolist()))
            Likelihoodtorecommned.append(mean(df['Likelihood to recommned'].values.tolist()))
            productNamesList.append(file)
        df2 = pd.read_csv(outputfilepath)
        df2['OverAllRating'] = overallRating
        df2['Value For Money'] = ValueForMoney
        df2['Ease of Use'] = EaseofUse
        df2['Features'] = Features
        df2['Customer Support'] = CustomerSupport
        df2['Likelihood to recommned'] = Likelihoodtorecommned
        df2['OverProductNames'] = productNamesList
        df2.to_csv(outputfilepath)

    def calculateStandardDeviationScore(self, dir_path, outputfilepath):
        csvFiles = os.listdir(dir_path)
        productNamesList = []
        overallRating = []
        ValueForMoney = []
        EaseofUse = []
        Features = []
        CustomerSupport = []
        Likelihoodtorecommned = []
        numberOfReviews = []
        for file in csvFiles:
            if file == '.DS_Store':
                continue
            df = pd.read_csv(dir_path + file)
            overallRatingList = df['OverAllRating'].values.tolist()
            overallRating.append(self.calculateStandardDeviation(overallRatingList))
            ValueForMoney.append(self.calculateStandardDeviation(df['Value For Money'].values.tolist()))
            EaseofUse.append(self.calculateStandardDeviation(df['Ease of Use'].values.tolist()))
            Features.append(self.calculateStandardDeviation(df['Features'].values.tolist()))
            CustomerSupport.append(self.calculateStandardDeviation(df['Customer Support'].values.tolist()))
            Likelihoodtorecommned.append(self.calculateStandardDeviation(df['Likelihood to recommned'].values.tolist()))
            productNamesList.append(file)
            numberOfReviews.append(len(overallRatingList))
        df2 = pd.DataFrame({
            "ProductName": productNamesList,
            "Standard Deviation OverAllRating": overallRating,
            "Standard Deviation Value For Money": ValueForMoney,
            "Standard Deviation Ease of Use": EaseofUse,
            "Standard Deviation Features": Features,
            "Standard Deviation Customer Support": CustomerSupport,
            "Standard Deviation Likelihood to recommned": Likelihoodtorecommned,
            "NumberOfReviews": numberOfReviews
        })
        df2.to_csv(outputfilepath)

    def baseLineScore(self, outputfilepath):
        df = pd.read_csv(outputfilepath)
        OverALlRatingList = df['OverAllRating'].values.tolist()
        valueForMoneyList = df['Value For Money'].values.tolist()
        EaseOfUseList = df['Ease of Use'].values.tolist()
        featuresList = df['Features'].values.tolist()
        CustomerSupportList = df['Customer Support'].values.tolist()
        LikehoodList = df['Likelihood to recommned'].values.tolist()

        baseLineScore = []
        for overall, value, ease, feature, support, likehood in zip(OverALlRatingList, valueForMoneyList, EaseOfUseList,
                                                                    featuresList, CustomerSupportList, LikehoodList):
            score = (overall + value + ease + feature + support + likehood) / 35
            baseLineScore.append(score)
        df['BaseLinescore'] = baseLineScore
        df.to_csv(outputfilepath)

    def trimProductName(self, name):
        return name.split("Reviews")[0]

    def calculateStandardDeviation(self, scorelist):
        score_array = np.array(scorelist)
        return score_array.std()

    def standardDeviationAndNumberOfReviews(self, inputFilepath, outputfilepath):
        df = pd.read_csv(inputFilepath)

        overallRating = df['Standard Deviation OverAllRating'].values.tolist()
        values = df['Standard Deviation Value For Money'].values.tolist()
        uses = df['Standard Deviation Ease of Use'].values.tolist()
        features = df['Standard Deviation Features'].values.tolist()
        support = df['Standard Deviation Customer Support'].values.tolist()
        recommend = df['Standard Deviation Likelihood to recommned'].values.tolist()

        avgSDList = []

        for rating, value, use, feature, support, recommend in zip(overallRating, values, uses, features, support,
                                                                   recommend):
            avgSd = (rating + value + use + feature + support + recommend) / 6
            avgSDList.append(avgSd)

        df2 = pd.read_csv(outputfilepath)
        df2['Avg Standard Deviation'] = avgSDList
        df2['number Of reviews'] = df['NumberOfReviews'].values.tolist()
        df2['Pro'] = df['ProductName'].values.tolist()
        df2.to_csv(outputfilepath)

    def changeDAtaframe(self, outfilepath):
        df = pd.read_csv(outfilepath)
        df.drop(columns=df.columns[0], inplace=True)
        df.columns = ['ProductName', 'OverAllRating', 'Value For Money',
                      'Ease of Use', 'Features', 'Customer Support', 'Likelihood to recommned',
                      'BaseLinescore', 'Avg Standard Deviation', 'number Of reviews', 'Sentiment',
                      'Score Sum', 'Avg Sum', 'CompletenssScore Sum', 'Completeness Avg Sum',
                      'ConciseRepresntation']

        # df.drop(columns=['Unnamed: 0.1'], inplace=True)
        # df.drop(columns=['Unnamed: 0.1.1'], inplace=True)

        # names1 = df['ProductName'].values.tolist()
        # names2 = df['Pro'].values.tolist()

        # if names1 == names2:
        #    df.drop(columns=['Pro'], inplace=True)
        #    print("Both are equal")
        # else:
        #    print("BOth are not equal")

        df.to_csv(outfilepath, index='ProductName')

    def normalizevalues(self, inputFilepath, outfilepath):
        df = pd.read_csv(inputFilepath)
        df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], inplace=True)
        df1 = df.iloc[:, 2:]
        column_list = df1.columns
        df1[column_list] = df1[column_list].apply(pd.to_numeric, errors='coerce')
        for column in df1.columns:
            df1['Normalized' + column] = df1[column] / df1[column].abs().max()

        df1['ProductName'] = df['ProductName'].values.tolist()
        cols = list(df1.columns)
        cols = [cols[-1]] + cols[:-1]
        df1 = df1[cols]
        df1.to_csv(outfilepath, index='ProductName')

    def baselIneRanking(self, inputFilePath):
        df = pd.read_csv(inputFilePath)
        df.drop(columns=['NormalizedPro'], inplace=True)
        df['BaseLine_Rank'] = df['BaseLinescore'].rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormaliseBaselinerank.csv')

    def StandardDeviationRank(self, inputFilePath):
        df = pd.read_csv(inputFilePath)
        df['BaseLinescore + NormalizedAvg Standard Deviation'] = df['BaseLinescore'] + df[
            'NormalizedAvg Standard Deviation']
        df['StandardDeviation Rank'] = (df['BaseLinescore'] + df['NormalizedAvg Standard Deviation']).rank(
            ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormaliseStandardDeviationRank.csv')

    def NormalisedStandardDeviationRank(self, inputFilePath):
        df = pd.read_csv(inputFilePath)
        df['NormalizedBaseLinescore + NormalizedAvg Standard Deviation'] = df['NormalizedBaseLinescore'] + df[
            'NormalizedAvg Standard Deviation']
        df['Normalised StandardDeviation Rank'] = (
                    df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation']).rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormaliseStandardDeviationRank.csv')

    def numberOfReviewsRank(self, inputFilePath):
        df = pd.read_csv(inputFilePath)
        df.drop(columns=['Unnamed: 0.1.1'], inplace=True)
        df['NormalizedBaseLinescore + NormalizedAvg Standard Deviation + Normalizednumber Of reviews'] = df[
                                                                                                             'NormalizedBaseLinescore'] + \
                                                                                                         df[
                                                                                                             'NormalizedAvg Standard Deviation'] + \
                                                                                                         df[
                                                                                                             'Normalizednumber Of reviews']
        df['Normalised Number Of Reviews Rank'] = (
                    df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df[
                'Normalizednumber Of reviews']).rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedNumberOfReviewsRank.csv',
            index='ProductName')

    def sentiRank(self, inputFilePath):
        df = pd.read_csv(inputFilePath)
        df.drop(columns=['Unnamed: 0.1.1'], inplace=True)
        df[
            'NormalizedBaseLinescore + NormalizedAvg Standard Deviation + Normalizednumber Of reviews + NormalizedSentiment + NormalizedAvg Sum'] = \
        df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df['Normalizednumber Of reviews'] + df[
            'NormalizedSentiment']
        df['Normalised Number Of Sentiment Rank'] = (
                    df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df[
                'Normalizednumber Of reviews'] + df['NormalizedSentiment']).rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedSentimentRank.csv',
            index='ProductName')

    def relevancyRank(self, inputFilePath):
        df = pd.read_csv(inputFilePath)
        df.drop(columns=['Unnamed: 0'], inplace=True)
        df[
            'NormalizedBaseLinescore + NormalizedAvg Standard Deviation + Normalizednumber Of reviews + NormalizedSentiment + NormalizedAvg Sum'] = \
        df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df['Normalizednumber Of reviews'] + df[
            'NormalizedSentiment'] + df['NormalizedAvg Sum']
        df['Normalised Relevancy Rank'] = (df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df[
            'Normalizednumber Of reviews'] + df['NormalizedSentiment'] + df['NormalizedAvg Sum']).rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedrelevancyRank.csv',
            index='ProductName')

    def completenssRank(self, inputFilePath):
        df = pd.read_csv(inputFilePath)
        df.drop(columns=['Unnamed: 0.1'], inplace=True)
        df[
            'NormalizedBaseLinescore + NormalizedAvg Standard Deviation + Normalizednumber Of reviews + NormalizedSentiment + NormalizedAvg Sum + NormalizedCompleteness Avg Sum'] = \
            df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df['Normalizednumber Of reviews'] + \
            df[
                'NormalizedSentiment'] + df['NormalizedAvg Sum'] + df['NormalizedCompleteness Avg Sum']
        df['Normalised Completensess Rank'] = (
                    df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df[
                'Normalizednumber Of reviews'] + df['NormalizedSentiment'] + df['NormalizedAvg Sum'] + df[
                        'NormalizedCompleteness Avg Sum']).rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedCompletenessRank.csv',
            index='ProductName')

    def conciseRepresenationRank(self, inputFilePath):
        df = pd.read_csv(inputFilePath)
        df.drop(columns=['Unnamed: 0.1'], inplace=True)
        df[
            'NormalizedBaseLinescore + NormalizedAvg Standard Deviation + Normalizednumber Of reviews + NormalizedSentiment + NormalizedAvg Sum + NormalizedCompleteness Avg Sum + NormalizedConciseRepresntation'] = \
            df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df['Normalizednumber Of reviews'] + \
            df[
                'NormalizedSentiment'] + df['NormalizedAvg Sum'] + df['NormalizedCompleteness Avg Sum'] + df[
                'NormalizedConciseRepresntation']
        df['Normalised ConciseRepresenation Rank'] = (
                    df['NormalizedBaseLinescore'] + df['NormalizedAvg Standard Deviation'] + df[
                'Normalizednumber Of reviews'] + df['NormalizedSentiment'] + df['NormalizedAvg Sum'] + df[
                        'NormalizedCompleteness Avg Sum'] + df['NormalizedConciseRepresntation']).rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedConciseRepresntationRank.csv',
            index='ProductName')

    def trimProductNames(self, inputFilePath):
        df = pd.read_csv(inputFilePath, index_col=[0])
        df.drop(columns=['Unnamed: 0.1'], inplace=True)
        productNames = df['ProductName'].values.tolist()
        updatedProductNmes = [self.trimProductName(name) for name in productNames]
        df['ProductName'] = updatedProductNmes
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/FinalRanking.csv',
            index='ProductName')

    def trimProductnames(self, name):
        name = name.split('.')[0].split('Reviews')[0]
        return name

    def mean(self, filepath):
        df = pd.read_csv(filepath)
        value = mean(df['OverAllRating'].values.tolist())
        return value


if __name__ == '__main__':
    obj = Logos()
    # obj.complteness('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/GetApp_Completeness/')
    # obj.conciseRepresentation('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Concise_Representation/')
    # obj.getAppTimeliness('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Get_app_Timeliness/')
    # obj.calculateRelevancy('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Relevancy/')
    # obj.getOverallCombinedScore('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Completeness/')
    # obj.getLastPathComponet('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Completeness/')
    # obj.getConciseRepresenation('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/ConciseRepresentation/')
    # obj.getOverallRelevancyScore('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Relevancy/')
    # obj.calculateSentimentalAnalysis('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Get_app_Sentimetal analysis/')
    # obj.calculateOverAllSentiments('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Sentiment/')
    # obj.mergeDatFrame()
    # obj.calculateScoreValues('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Concise_Representation/',
    #                         '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/Final_Logos.csv')
    # obj.baseLineScore('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/CombinedScores_1.csv')
    # obj.standardDeviationAndNumberOfReviews('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Ranking_Docs/',
    #                                        '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/CombinedScores_1.csv')
    # obj.calculateStandardDeviationScore('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Concise_Representation/',
    #                               '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/StndardDeviationScore.csv')

    # obj.standardDeviationAndNumberOfReviews('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/StndardDeviationScore.csv',
    #                                        '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/CombinedScores_1.csv')

    # obj.changeDAtaframe('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/CombinedScores_1.csv')
    #obj.normalizevalues(
    #    '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/CombinedScores_1.csv',
    #    '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/GetAppNormalisedScores.csv')

    #obj.baselIneRanking('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/GetAppNormalisedScores.csv')
    #obj.StandardDeviationRank('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/GetAppNormalisedScores.csv')
    #obj.NormalisedStandardDeviationRank(
    #    '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormaliseStandardDeviationRank.csv')
    #obj.numberOfReviewsRank('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormaliseStandardDeviationRank.csv')
    #obj.sentiRank('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedNumberOfReviewsRank.csv')
    #obj.relevancyRank('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedSentimentRank.csv')
    #obj.completenssRank('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedrelevancyRank.csv')
    #obj.conciseRepresenationRank('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/NormalisedCompletenessRank.csv')
    obj.trimProductNames('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_Logos/FinalRanking.csv')