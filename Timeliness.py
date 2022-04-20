import pandas as pd
import os

class Timeliness:

    def __init__(self, dir_path, out_dir_path):
        self.dir_path = dir_path
        self.out_dir_path = out_dir_path


    def findIntervalindays(self):
        csv_files = os.listdir(self.dir_path)
        for csvfile in csv_files:
            df = pd.read_csv(self.dir_path + csvfile)
            df['Date_time'] = pd.to_datetime(df['created'])
            df['DiffereceInDays'] =  df['Date_time'] - df['Date_time'].min()
            df.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'], inplace=True)
            df.to_csv(self.out_dir_path + csvfile)



if __name__ == '__main__':
    obj = Timeliness('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Get_app_Sentimetal analysis/',
                     '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Get_app_Timeliness/')
    obj.findIntervalindays()

