import pandas as pd
import os
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import string
import statistics
import json

nltk.download('punkt')

class ConciseRepr:

    def __init__(self, dir_path, out_dir_path):
        self.dir_path = dir_path
        self.out_dir_path = out_dir_path

    def conciseRepresentation(self):
        csv_files = os.listdir(self.dir_path)
        for csvfile in csv_files:

            df = pd.read_csv(self.dir_path + csvfile)

            df['content'].replace(np.nan, '', inplace=True)
            df['pros'].replace(np.nan, '', inplace=True)
            df['cons'].replace(np.nan, '', inplace=True)

            df['Overall_conciseRepresentation_Content'] = self.findaveragelengthofsentences(df['content'].values.tolist())
            df['Overall_conciseRepresentation_Pros'] = self.findaveragelengthofsentences(df['pros'].values.tolist())
            df['Overall_conciseRepresentation_Cons'] = self.findaveragelengthofsentences(df['cons'].values.tolist())

            df.drop(columns=['Unnamed: 0.1.1'], inplace=True)
            df.to_csv(self.out_dir_path + csvfile, index= None)

    def _remove_punctuation_and_tokenize(self, sentence):
        return word_tokenize(sentence.translate(str.maketrans({a: None for a in string.punctuation})))

    def findSentences(self, sentList):
        avgList = []
        for sent in sentList:
            totalSent = sent_tokenize(sent)
            avgList.append(len(totalSent))
        return avgList

    def findAverageSentenceLength(self, length_list):
        if len(length_list) == 0:
            return np.nan
        return float(format(statistics.mean(length_list), '.2f'))

    def findStadardDeviation(self, length_list):
        if len(length_list) < 2:
            return np.nan
        return float(format(statistics.stdev(length_list), '.2f'))


    def findaveragelengthofsentences(self, sentList):
        avgList = []
        for sent in sentList:
            totalSent = sent_tokenize(sent)
            word_list = [self._remove_punctuation_and_tokenize(words) for words in totalSent]
            length_list = [len(word) for word in word_list]
            avgList.append({
                "Average Sentence Length": self.findAverageSentenceLength(length_list),
                "number_of_sentences": len(totalSent),
                "longest": max(length_list) if len(length_list) > 0 else 0,
                "shortest": min(length_list) if len(length_list) > 0 else 0,
                "stdDev": self.findStadardDeviation(length_list)
            })
        return avgList

if __name__ == '__main__':
    obj = ConciseRepr('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Get_app_Timeliness/',
                      '/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/OverAll_Concise_Representation/' )
    obj.conciseRepresentation()


