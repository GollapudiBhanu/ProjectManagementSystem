import os
import pandas as pd
import json
import numpy as np

class Comparison:

    def __init__(self):
        pass

    def compareThreeRankingMethods(self, dir_path, file_path):
        df = pd.read_csv(dir_path + file_path)
        df['BaseLines Vs NumberOfReviews'] = np.where(df["BaseLineScoreRank"] == df["NumberOfReviewsRank"], True, False)
        df['BaseLines Vs StandardDeviationRank'] = np.where(df["BaseLineScoreRank"] == df["StandardDeviationRank"], True, False)
        df['NumberOfReviewsRank Vs StandardDeviationRank'] = np.where(df["NumberOfReviewsRank"] == df["StandardDeviationRank"], True, False)
        df["BaseLines Vs NumberOfReviews Vs StandardDeviationRank"] = df.apply(lambda x: x.BaseLineScoreRank == x.NumberOfReviewsRank == x.StandardDeviationRank, axis=1)

        df.to_csv(dir_path + 'RankingComparsion.csv')

    def extarctRankingProducts(self,  dir_path, file_path):
        df = pd.read_csv(dir_path + file_path)
        BNList = df[df['BaseLines Vs NumberOfReviews'] == True]['Product Name'].tolist()
        BSDList = df[df['BaseLines Vs StandardDeviationRank'] == True]['Product Name'].tolist()
        NSDLISt = df[df['NumberOfReviewsRank Vs StandardDeviationRank'] == True]['Product Name'].tolist()
        BNSDList = df[df['BaseLines Vs NumberOfReviews Vs StandardDeviationRank'] == True]['Product Name'].tolist()
        print(BNList)
        print(BSDList)
        print(NSDLISt)
        print(BNSDList)

    def comapreTwoProductRanking(self, filepath1, filepath2):
        df1 = pd.read_csv(filepath1)
        df2 = pd.read_csv(filepath2)
        df1.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'], inplace=True)
        df2.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'], inplace=True)
        commonProductNames = df1[df1['Product Name'].isin(df2['Product Name'])]['Product Name'].values.tolist()

        getapplist = df1[df1['Product Name'].isin(commonProductNames)].to_dict('records')
        getapplist = sorted(getapplist, key=lambda i: i['Product Name'])
        projectmanagementdictList = df2[df2['Product Name'].isin(commonProductNames)].to_dict('records')
        projectmanagementdictList = sorted(projectmanagementdictList, key=lambda i: i['Product Name'])

        combinedList = []
        for getapp, projectmanagementdict in zip(getapplist, projectmanagementdictList):
            combinedDict = {}
            combinedDict['Products'] = getapp['Product Name']
            combinedDict['GetApp_AverageBaseLineScore'] = getapp['Average BaseLine Score']
            combinedDict['SoftwareAdvice_AverageBaseLineScore'] = projectmanagementdict['Average BaseLine Score']
            combinedDict['GetApp_BaseLineScoreRank'] = getapp['BaseLineScoreRank']
            combinedDict['SoftwareAdvice_BaseLineScoreRank'] = projectmanagementdict['BaseLineScoreRank']

            combinedDict['GetApp_NumberOfReviews'] = getapp['Number Of Reviews']
            combinedDict['SoftwareAdvice_NumberOfReviews'] = projectmanagementdict['Number Of Reviews']
            combinedDict['GetApp_NumberOfReviewsRank'] = getapp['NumberOfReviewsRank']
            combinedDict['SoftwareAdvice_NumberOfReviewsRank'] = projectmanagementdict['NumberOfReviewsRank']

            combinedDict['GetApp_StandardDeviation'] = getapp['Standard Deviation']
            combinedDict['SoftwareAdvice_StandardDeviation'] = projectmanagementdict['Standard Deviation']
            combinedDict['GetApp_StandardDeviationRank'] = getapp['StandardDeviationRank']
            combinedDict['SoftwareAdvice_StandardDeviationRank'] = projectmanagementdict['StandardDeviationRank']

            combinedList.append(combinedDict)

        combiedDF = pd.DataFrame(combinedList)
        combiedDF.to_csv('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/RankingCompProducts/CombinedProducts.csv')
        #df4.to_csv('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/RankingCompProducts/df2.csv')

if __name__ == '__main__':
    obj = Comparison()
    #obj.compareThreeRankingMethods('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ScoreRanking/',
    #                               'CombinedRanking.csv')
    #obj.extarctRankingProducts('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ScoreRanking/',
    #                           'RankingComparsion.csv')
    obj.comapreTwoProductRanking('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ScoreRanking/CombinedRanking.csv',
                                   '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_combined/ProjectManagement_CombinedRanking.csv')

    #obj.compareThreeRankingMethods('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_combined/',
    #                               'ProjectManagement_CombinedRanking.csv')
    #obj.extarctRankingProducts('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/ProjectManagement_combined/',
    #                           'RankingComparsion.csv')