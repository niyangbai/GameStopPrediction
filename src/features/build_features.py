import pandas as pd
from datetime import datetime


def data_clean(df):
    deleted = ['[removed]', '[deleted]', '[deleted by user]']
    df_clean = df.replace(deleted, None)
    df_clean = df_clean.loc[df_clean[['title', 'selftext', 'top_comments']].notna().sum(axis=1) != 0, ]
    df_clean = df_clean.replace(r'\n', ' ', regex=True)

    word_col = ['title', 'selftext', 'top_comments']

    for col in word_col:
        df_clean[col] = df_clean[col].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\!\[img\]\S+', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\[deleted\]', '', regex=True)
        df_clean[col] = df_clean[col].replace(r'\[removed\]', '', regex=True)

    return df_clean


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
    df_rdt = pd.read_csv(os.path.join(input_dir, 'df_rdt.csv'))
    df_gme = pd.read_csv(os.path.join(input_dir, 'df_gme.csv'))
    df_sp500 = pd.read_csv(os.path.join(input_dir, 'df_sp500.csv'))

    df_rdt['created_utc'] = df_rdt['created_utc'].apply(time_reformat)
    df_gme['Date'] = df_gme['Date'].apply(time_reformat)
    df_sp500['DATE'] = df_sp500['DATE'].apply(time_reformat)

    df_raw = df_rdt.merge(df_sp500, left_on='created_utc', right_on='DATE').merge(df_gme, left_on='created_utc', right_on='Date')
    df_raw = df_raw.drop(['Date', 'DATE'], axis=1)
    df_raw.to_csv(os.path.join(output_dir, 'df_sp500.csv'))


if __name__ == '__main__':
    main()
else:
    print('successfully imported')
