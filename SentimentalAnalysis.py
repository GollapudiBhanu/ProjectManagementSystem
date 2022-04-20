import os
import nltk
import numpy as np
import pandas as pd
from contractions import CONTRACTION_MAP as cMap
import re
import spacy
from nltk.tokenize.toktok import ToktokTokenizer

sp = spacy.load('en', parse=True, tag=True, entity=True)
tokenizer = ToktokTokenizer()
stopwords_list = nltk.corpus.stopwords.words('english')

class Analysis:

    def __init__(self):
        pass

    def basicPreprocessing(self, dir_path):
        csv_files = os.listdir(dir_path)
        for csvfile in csv_files:
            if csvfile == '.DS_Store':
                continue
            df = pd.read_csv(dir_path + csvfile)
            preprocessed_List = []
            combinedStringList = df['combinedString'].values.tolist()
            for combinedString in combinedStringList:
                text = self.expandContractions(combinedString)
                text = self.removeSpecialCharcters(text)
                text = self.lemmatizeText(text)
                text = self.removeSpecialCharcters(text)
                preprocessed_List.append(text)
            df['preprocessed CombinedString'] = combinedStringList
            df.to_csv('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/GETAPP_Senti/'+')

    def expandContractions(self, combinedText):
        words = combinedText.split()
        expanded_words_list = [cMap[word] if word in cMap else word for word in words]
        expanded_text = ' '.join(expanded_words_list)
        return expanded_text

    def removeSpecialCharcters(self, combinedText):
        try:
            pattern = r'[^a-zA-Z0-9\s]'
            combinedText = re.sub(pattern, '', combinedText)
        except TypeError:
            pass
        return combinedText

    def lemmatizeText(self, combinedText):
        try:
            combinedText = sp(combinedText)
            combinedText = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in combinedText])
        except TypeError:
            pass
        return combinedText

    def get_tokens(self, combinedText):
        tokens = tokenizer.tokenize(combinedText)
        tokens = [token.strip() for token in tokens]
        return tokens

    def remove_stopwords(self, combinedText):
        tokens = self.get_tokens(combinedText)
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords_list]
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text


    def combineText(self, dir_path):
        csv_files = os.listdir(dir_path)
        for csvfile in csv_files:
            if csvfile == '.DS_Store':
                continue
            df = pd.read_csv(dir_path + csvfile)
            df['title'].replace(np.nan, '', inplace=True)
            df['content'].replace(np.nan, '', inplace=True)
            df['pros'].replace(np.nan, '', inplace=True)
            df['cons'].replace(np.nan, '', inplace=True)
            df['combinedString'] = df['title'] + df['content'] + df['pros'] + df['cons']
            df.to_csv('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/GETAPP_Senti/'+ csvfile)

if __name__ == '__main__':
    obj = Analysis()
    #obj.combineText('/Users/bhanugollapudi/Documents/Projects/Ding_Proj/ProjectManagementSoftware/Ranking_Docs/')
    #obj.expandContractions('you\'re happy now')

