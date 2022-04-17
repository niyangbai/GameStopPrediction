# -*- coding: utf-8-sig -*-
import time
import pandas as pd

def data_clean(path, encoding = 'utf-8-sig'):
    df = pd.read_csv(path, encoding = encoding)
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
    return df_clean




