import os
import pandas as pd

class MergeFiles:


    def __init__(self, source_dir, output_dir):
        self.source_dir = source_dir
        self.output_dir = output_dir


    def merge(self):
        csvFiles = []
        dfList = []
        csvDirs = os.listdir(self.source_dir)
        for dir in csvDirs:
            if dir is '.DS_Store':
                continue
            files = os.listdir(self.source_dir + dir + '/')
            if len(files) > 0:
                csvFile = [filename for filename in files if filename.endswith('.csv')]
                df = pd.read_csv(self.source_dir + dir + '/' + csvFile[0],index_col=None)
                df.drop(columns=['Unnamed: 0'], inplace=True)
                df["productName"] = self.getProductNameList(csvFile[0], df.shape[0])
                csvFiles.append(self.source_dir + dir + '/' + csvFile[0])
                dfList.append(df)
        df = pd.concat(dfList)
        df.to_csv('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Bhanu_new_J/ProjectManagement_Combined.csv')

    def getProductNameList(self, fileName, rows):
        productName = fileName.split('.')
        return [productName[0]] * rows





if __name__ == '__main__':
    obj = MergeFiles('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Project_management_data_csv/',
                     '')
    obj.merge()

