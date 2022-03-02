import pandas as pd
import os
from stanfordcorenlp import StanfordCoreNLP
from nltk import sent_tokenize
import csv
from engine import *

#source :https://www.geeksforgeeks.org/python-save-list-to-csv/
nlp = StanfordCoreNLP('http://localhost', 9000)
def read(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    
def per_count(sentence):
    
    count = 0
    for i, token in enumerate(sentence):
        if token[1] != 'O' and (i == 0 or token[1] != sentence[i-1][1]):
            count += 1

    return count

result = []
for one_set in ['set1', 'set2', 'set3','set4']:
    dirc = r"articles/"+ one_set
    for file in os.listdir(dirc):
        if file.endswith(".txt"): 
            
            aa = ArticleAnalysis(os.path.join(dirc, file))
            sent_len = len(aa.sentence_segmentation())
            aa.word_tokenize()
            token_len =  sum([len(x) for x in aa.tokenizes])
            ner = aa.ner()
            count = sum([per_count(x) for x in ner])

            result.append([one_set,file, sent_len, token_len, count])




header = ['set','name', 'sentence_number', 'token_number', 'per_count'] 
      
with open('stats.csv', 'w') as f:
      
    write = csv.writer(f)
      
    write.writerow(header)
    for row in result:
        write.writerow(row)

nlp.close()
            
    # # Check whether file is in text format or not
    # if file.endswith(".txt"):
    #     file_path = f"{path}\{file}"
  
    #     # call read text file function
    #     read_text_file(file_path)