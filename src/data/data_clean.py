# -*- coding: utf-8-sig -*-
import time
import pandas as pd

df = pd.read_csv('api.csv', encoding = 'utf-8-sig')
deleted = ['[removed]', '[deleted]', '[deleted by user]']
df_clean = df.replace(deleted, None)
df_clean = df_clean.loc[df_clean[['title', 'selftext', 'top_comments']].notna().sum(axis = 1) != 0,]
df_clean = df_clean.replace(r'\n',' ', regex = True) 

word_col = ['title', 'selftext', 'top_comments']

for col in word_col:
    df_clean[col] = df_clean[col].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
    df_clean[col] = df_clean[col].replace(r'\!\[img\]\S+', '', regex = True)
    df_clean[col] = df_clean[col].replace(r'\[deleted\]', '', regex = True)
    df_clean[col] = df_clean[col].replace(r'\[removed\]', '', regex = True)
    
df_clean['created_utc'] = df_clean['created_utc'].apply(lambda x: time.strftime('%m-%d-%y', time.localtime(x)))

df_clean.to_csv('clean.csv', encoding = 'utf-8-sig', index = False)




