import os
import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow.keras import regularizers
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

input_dir = 'D:\\github\\master_thesis_2022\\data\\raw'
output_dir = 'D:\\github\\master_thesis_2022\\data\\processed'

num_words = 20000

tokenizer = Tokenizer(num_words=num_words, oov_token="unk")
tokenizer.fit_on_texts(train_data['text'].tolist())

df_raw = pd.read_csv(os.path.join(input_dir, 'df_raw.csv'), encoding='utf-8-sig', index_col='id')
df_raw = df_raw.drop(['Date'], axis=1)

X_train, X_valid, y_train, y_valid = train_test_split(df_raw.loc[:, df_raw.columns != 'close_diff'],
                                                      df_raw['close_diff'],
                                                      test_size=0.33)

