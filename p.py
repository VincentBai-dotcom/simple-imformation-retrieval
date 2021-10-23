from stop_list import *
import numpy as np
import string
import math
from functools import cmp_to_key
def wordFilter(word):
    if word[len(word)-1] in string.punctuation:
        word = word[:len(word)-1]
    if word == "":
        return word
    if word[0] in string.punctuation:
        word = word[1:]
    if word in closed_class_stop_words:
        return ""
    if word.isnumeric():
        return ""
    return word

def IDF(queries):
    dict = {}
    for sentence in queries:
        sentence = sentence.split()
        words = set()
        for word in sentence:
            word = wordFilter(word)
            if word != "":
                words.add(word)
        for word in words:
            dict[word] = dict.get(word,0)+1
    return dict


def TF(queries):
    TF = [dict() for x in range(len(queries))]
    i = 1
    while i < len(queries):
        words = queries[i].split()
        for word in words:
            word = wordFilter(word)
            if(word != ""):
                TF[i][word] = TF[i].get(word,0)+1
        i+=1
    return TF

def comparator(a,b):
    if a[1] < b[1]:
        return 1
    if a[1] > b[1]:
        return -1
    return 0



queries = open("cran.qry", 'r',encoding='UTF-8').read().split(".I")
docs = open("cran.all.1400", 'r',encoding='UTF-8').read().split(".I")
output = open("output.txt", 'w', newline='\n')
queryIDF = IDF(queries)
docIDF = IDF(docs)
queryTF = TF(queries)
docTF = TF(docs)

i = 1
while i < len(queryTF):
    j = 1
    solution = []
    while j < len(docTF):
        product = 0
        querySqaure = 0
        docSqaure = 0
        for key in queryTF[i].keys():
            queryScore = queryTF[i][key]*np.log(225/queryIDF[key])
            idf = 0
            if docIDF.get(key,0) != 0:
                idf = np.log(1400/docIDF[key])
            docScore = docTF[j].get(key,0)*idf
            product += queryScore*docScore
            querySqaure+= queryScore**2
            docSqaure+=docScore**2
        
        similarity = 0
        if querySqaure*docSqaure != 0:
            similarity = product/math.sqrt(querySqaure*docSqaure)
        solution.append([j,similarity])
        j+=1
    solution = sorted(solution,key=cmp_to_key(comparator))
    for data in solution:
        if data[1] != 0:
            output.write(str(i)+" "+str(data[0])+" "+str(data[1])+" \n")
    i+=1

output.close

