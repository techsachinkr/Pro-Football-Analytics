#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 10:49:48 2018

@author: michaelkowolenko
"""

import nltk
import re
from nltk import ne_chunk
from nltk.tree import *
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
import pprint as pp
import pandas as pd
from nltk.tag import RegexpTagger
import numpy as np
data = open('salary_name').read()
sent=sent_tokenize(data)

type(sent)
iso=[]
names=[]
salary=[]
noise_list=['Indianapolis','Colts','Ameritrade','Oakland','Raiders','NFL','QBs','is','a','this','the','to','and','from','TD','BodyArmor',
            'in','not','has','still','his','in','while','but','will','NFLâ€™s']
for line in sent:
    words = line.split() 
    noise_free_words = [word for word in words if word not in noise_list] 
    noise_free_text = " ".join(noise_free_words) 
    result=re.search('\w.*\$.*\.',noise_free_text)
    if result:
        iso.append(result.group())

for line in iso:
    breakdown=(pos_tag(word_tokenize(line)))
    #print(breakdown)

   

    find_names=nltk.RegexpParser('NAMES:{<NNP><NNP>}')
    listing = (find_names.parse(breakdown))
    #print(listing)
    find_salaries =nltk.RegexpParser('Salary:{<JJ><CD><NNS><\$><CD><CD>|<NNP>+<\(><\$><CD><CD>}|<NNP><\$><CD><CD>')
    listing2 = (find_salaries.parse(breakdown))
    #type(listing)
    
    for term in listing.subtrees():
        if term.label()=='NAMES':
           names.append(term)
    for term in listing2.subtrees():
        if term.label()=='Salary':
           salary.append(term[len(term)-2:])
    
for values in range(len(names)):
    nameStr1=names[values][0][0]
    nameStr2=names[values][1][0]

    salaryStr1=salary[values][0][0]
    salaryStr2=salary[values][1][0]
    print(nameStr1," ",nameStr2," "," earning ",salaryStr1,salaryStr2)



        