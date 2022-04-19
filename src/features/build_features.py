import pandas as pd
import emoji
from datetime import datetime
import string


class DataClean:
    def __init__(self, column):
        self.col = column

    def table_clean(self, dataframe):
        deleted = ['[removed]', '[deleted]', '[deleted by user]']
        df_clean = dataframe.replace(deleted, None)
        #df_clean = df_clean.replace(r'', None, regex=True)
        #df_clean = df_clean.loc[df_clean[['title', 'selftext', 'top_comments']].notna().sum(axis=1) != 0, ]
        df_clean = df_clean.replace(r'\n', ' ', regex=True)
        df_clean = df_clean.fillna('')

        for col in self.col:
            df_clean[col] = df_clean[col].replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)
            df_clean[col] = df_clean[col].replace(r'\!\[img\]\S+', '', regex=True)
            df_clean[col] = df_clean[col].replace(r'\[deleted\]', '', regex=True)
            df_clean[col] = df_clean[col].replace(r'\[removed\]', '', regex=True)

        return df_clean

    def emj_clean(self, dataframe, delete=True):

        for col in self.col:
            if delete:
                dataframe[col] = dataframe[col].apply(lambda x: emoji.replace_emoji(x, replace=''))
            else:
                dataframe[col] = dataframe[col].apply(lambda x: emoji.demojize(x))

        return dataframe

    def text_clean(self, dataframe, punctuation=True, lower=True):

        for col in self.col:
            if punctuation:
                dataframe[col] = dataframe[col].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
            if lower:
                dataframe[col] = dataframe[col].apply(lambda x: x.lower())

        return dataframe


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

    df_gme['close_diff'] = df_gme['Close'].diff()
    df_sp500['sp500_diff'] = df_sp500['sp500'].diff()
    df_gme = df_gme.drop(['Open', 'High', 'Low', 'Volume', 'Close'], axis=1)
    df_rdt = df_rdt.drop(['url'], axis=1)
    df_sp500 = df_sp500.drop(['sp500'], axis=1)

    df_raw = df_gme.merge(df_sp500,
                          left_on='Date',
                          right_on='DATE').merge(df_rdt,
                                                 left_on='Date',
                                                 right_on='created_utc')

    df_raw = df_raw.drop(['DATE', 'created_utc'], axis=1)

    clean_col = ['title', 'selftext', 'top_comments']
    clean = DataClean(clean_col)

    df_raw = clean.table_clean(df_raw)
    df_raw = clean.emj_clean(df_raw)
    df_raw = clean.text_clean(df_raw, punctuation=True)

    df_raw['text'] = df_raw['title'] + df_raw['selftext'] + df_raw['top_comments']
    df_raw = df_raw.drop(['title', 'selftext', 'top_comments'], axis=1)
    df_raw = df_raw.replace(r'', None, regex=True)
    df_raw = df_raw.dropna()
    df_raw.to_csv(os.path.join(output_dir, 'df_raw.csv'), encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    main()
else:
    print('successfully imported')
