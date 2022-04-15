# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 08:38:36 2022
https://machinelearningmastery.com/develop-word-embedding-model-predicting-movie-review-sentiment/
@author: baini
"""

import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for token in doc:
    print(token.text, token.pos_, token.dep_)