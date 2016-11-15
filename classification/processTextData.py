# coding: utf-8

# ------ IMPORTS -----
import pandas as pd
from loadAndCleanData import LoadCleanData
from utilNormalizer import normaliz
import warnings
warnings.filterwarnings("ignore")

# ------ IMPORTS -----
df_open_ff, df_open_bf = LoadCleanData().load_clean_data()


# ------ PROCESS DATA -----
def clean_text_data(df):
    """ Uniformize a column in a DataFrame """
    df['merge_cols_simpl'] = df['merge_col'].map(lambda x: normaliz(x))
    return df

df_open_ff = clean_text_data(df_open_ff)

print df_open_ff.merge_cols_simpl.head()
