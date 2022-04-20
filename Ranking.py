import os
import pandas as pd
import json
import numpy as np

class Ranking:

    def __init__(self, dir_path):
        self.dirpath = dir_path

    def ranking(self):
        csv_files = os.listdir(self.dirpath)
        for csv_file in csv_files:
            print(csv_file)
            df = pd.read_csv(self.dirpath + '/' + csv_file)
            if len(df.columns) == 1:
                continue
            rating_dict_values = df['rating'].values
            score_list = self.getScore(rating_dict_values)
            df['BaseLine_Score'] = score_list
            df.to_csv(
                '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/New_Get_App/' + csv_file)

    def getScore(self, rating_dict_list):
        score_list = []
        for rating_dict in rating_dict_list:
            rating_dict = rating_dict.replace("\'", "\"")
            final_dict = json.loads(rating_dict)
            score = self.calculateScore(final_dict)
            score_list.append(score)
        return score_list

    def calculateScore(self, rating_dict):
        dict1 = rating_dict['by_field']
        dict1['total_rounded'] = rating_dict['total_rounded']
        value = sum(dict1.values())
        score = value / 35
        return score

    def rename_filename(self):
        csv_files = os.listdir(self.dirpath)
        new_dir_path = '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/New_Get_App/'
        for csv_file in csv_files:
            name, extension = os.path.splitext(csv_file)
            new_name = self.trim(name)
            os.renames(self.dirpath + '/' + name + '.csv', new_dir_path + '/' + new_name + '.csv')

    def trim(self, filename):
        return ''.join(char for char in filename if char.isalnum())

    def assignRank(self):
        dir_path = '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/New_Get_App/'
        csv_files = os.listdir(dir_path)
        for csv_file in csv_files:
            df = pd.read_csv(dir_path + '/' + csv_file)
            if len(df.columns) == 1:
                continue
            df['BaseLine_Rank'] = df['BaseLine_Score'].rank(ascending=False)
            df.to_csv(
                '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/Ranking_Docs/' + csv_file)

    def rankProducts(self):
        dir_path = '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Ranking_Docs/'
        csv_files = os.listdir(dir_path)
        total_list = []
        for csv_file in csv_files:
            df = pd.read_csv(dir_path + '/' + csv_file)
            score_list = df['BaseLine_Score'].values.tolist()
            avgScore = self.calcuateOverallProductScore(score_list)
            name, extension = os.path.splitext(csv_file)
            name = self.trimProductName(name)
            overall_dict = {}
            overall_dict['Product Name'] = name
            overall_dict['Average BaseLine Score'] = avgScore
            overall_dict['Number Of Reviews'] = len(score_list)
            overall_dict['Standard Deviation'] = self.calculateStandardDeviation(score_list)
            total_list.append(overall_dict)
        df = pd.DataFrame(total_list)
        df.to_csv(dir_path + 'Overallscore_prodcuts.csv')

    def finalranking(self, columnName):
        df = pd.read_csv('/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Ranking_Docs/Overallscore_prodcuts.csv')
        df[columnName + 'Rank'] = df[columnName].rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/' + 'Final_ranking'+ columnName +'.csv')

    def calcuateOverallProductScore(self, score_list):
        total_elements = len(score_list)
        total_score = sum(score_list)
        avgScore = total_score / total_elements
        return avgScore

    def trimProductName(self, name):
        return name.split("Reviews")[0]

    def calculateStandardDeviation(self, scorelist):
        score_array = np.array(scorelist)
        return score_array.std()

    def overAllRanking(self):
        df = pd.read_csv('/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Ranking_Docs/Overallscore_prodcuts.csv')
        df['BaseLineScore' + 'Rank'] = df['Average BaseLine Score'].rank(ascending=False)
        df['NumberOfReviews' + 'Rank'] = df['Number Of Reviews'].rank(ascending=False)
        df['StandardDeviation' + 'Rank'] = df['Standard Deviation'].rank(ascending=False)
        df.to_csv(
            '/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/ScoreRanking/' + 'CombinedRanking.csv')

if __name__ == '__main__':
    obj = Ranking('/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/Data/Get_APP_docs')
    #obj.finalranking('Average BaseLine Score')
    #obj.finalranking('Standard Deviation')
    #obj.finalranking('Number Of Reviews')
    #obj.rankProducts()
    #obj.overAllRanking()
    #obj.finalOverAllRank('/Users/bhanugollapudi/Documents/Ding_Proj/ProjectManagementSoftware/ScoreRanking/CombinedRanking.csv')
