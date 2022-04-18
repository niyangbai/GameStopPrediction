import pandas as pd
import emoji
from datetime import datetime


def words_clean(dataframe):
    deleted = ['[removed]', '[deleted]', '[deleted by user]']
    df_clean = dataframe.replace(deleted, None)
    df_clean = df_clean.loc[df_clean[['title', 'selftext', 'top_comments']].notna().sum(axis=1) != 0, ]
    df_clean = df_clean.replace(r'\n', ' ', regex=True)

    word_col = ['title', 'selftext', 'top_comments']

    for col in word_col:
        df_clean[col] = df_clean[col].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\!\[img\]\S+', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\[deleted\]', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\[removed\]', '', regex=True)

    return df_clean


def emj_clean(string, delete: bool):

    if delete:
        emoji.replace_emoji(string, replace='')
    else:
        pass



def time_reformat(input_time):
    if isinstance(input_time, str):
        output_time = datetime.strptime(input_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    else:
        output_time = datetime.fromtimestamp(input_time).strftime('%Y-%m-%d')
    return output_time


def main():
    import os

    input_dir = 'D:\\github\\master_thesis_2022\\data\\interim'
    output_dir = 'D:\\github\\master_thesis_2022\\data\\raw'
    df_rdt = pd.read_csv(os.path.join(input_dir, 'df_rdt.csv'), encoding='utf-8-sig')
    df_gme = pd.read_csv(os.path.join(input_dir, 'df_gme.csv'), encoding='utf-8-sig')
    df_sp500 = pd.read_csv(os.path.join(input_dir, 'df_sp500.csv'), encoding='utf-8-sig')

    df_rdt['created_utc'] = df_rdt['created_utc'].apply(time_reformat)
    df_gme['Date'] = df_gme['Date'].apply(time_reformat)
    df_sp500['DATE'] = df_sp500['DATE'].apply(time_reformat)

    df_raw = df_rdt.merge(df_sp500, left_on='created_utc', right_on='DATE').merge(df_gme, left_on='created_utc', right_on='Date')
    df_raw = df_raw.drop(['Date', 'DATE'], axis=1)

    df_raw = words_clean(df_raw)
    df_raw.to_csv(os.path.join(output_dir, 'df_raw.csv'), encoding='utf-8-sig')


if __name__ == '__main__':
    main()
else:
    print('successfully imported')
