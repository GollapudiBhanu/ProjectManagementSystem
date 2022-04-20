from transformers import pipeline
import os
import pandas as pd

class Analysis:

  def __init__(self):
    self.classifier = pipeline('sentiment-analysis')

  def calucalteSentiment(self, dirpath):
    csv_files = os.listdir(dirpath)
    for csvfile in csv_files:
      if csvfile == '.DS_Store':
        continue
      df = pd.read_csv(dirpath + csvfile)
      sentiment = []
      combinedStringList = df['combinedString'].values.tolist()
      for combinedString in combinedStringList:
        senti = self.classifier(combinedString)
        sentiment.append(senti)



if __name__ == '__main__':
    obj = Analysis()
    obj.calucalteSentiment('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/GETAPP_Senti')
