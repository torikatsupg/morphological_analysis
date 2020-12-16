import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import re

pd.set_option('isplay.max_rows', 500)
pd.set_option('display.max_columns', 500)

CLASS_CSV_PATH = '/Users/toriikatsuya/Desktop/experiment/csv/modified/class_morphological.csv'
METHOD_CSV_PATH = '/Users/toriikatsuya/Desktop/experiment/csv/modified/method_morphological.csv'
VARIABLE_CSV_PATH = '/Users/toriikatsuya/Desktop/experiment/csv/modified/variable_morphological.csv'

def create_pairplot():
    df = read_csv(CLASS_CSV_PATH, True)
    plt.figure()
    pg = sns.pairplot(df)
    pg.savefig('./pairplot_class.png')
    plt.close('all')

    df = read_csv(METHOD_CSV_PATH, True)
    plt.figure()
    pg = sns.pairplot(df)
    pg.savefig('./pairplot_method.png')
    plt.close('all')

    df = read_csv(VARIABLE_CSV_PATH, True)
    plt.figure()
    pg = sns.pairplot(df)
    pg.savefig('./pairplot_variable.png')
    plt.close('all')
# ===============================================================================================
def read_csv(path, isAll):
    usecols = range(0)
    if isAll:
        if   path == CLASS_CSV_PATH:
            usecols = range(72)
        elif path == METHOD_CSV_PATH:
            usecols = range(73)
        elif path == VARIABLE_CSV_PATH:
            usecols = range(74)
    else:
        if   path == CLASS_CSV_PATH:
            usecols = range(4, 42)
        elif path == METHOD_CSV_PATH:
            usecols = range(4, 44)
        elif path == VARIABLE_CSV_PATH:
            usecols = range(4, 43)
    return pd.read_csv(path, usecols=usecols, low_memory=False)


#　基礎統計量の出力
def export_describe():
    class_df = read_csv(CLASS_CSV_PATH, False)
    class_df.describe(include="all").to_csv("./describe/class_describe.csv")

    method_df = read_csv(METHOD_CSV_PATH, False)
    method_df.describe(include="all").to_csv("./describe/method_describe.csv")

    variable_df = read_csv(VARIABLE_CSV_PATH, False)
    variable_df.describe(include="all").to_csv("./describe/variable_describe.csv")

# 合計値の出力
def export_sum():
    class_df = read_csv(CLASS_CSV_PATH, False)
    class_df.sum().to_csv("./sum/class_sum.csv")

    method_df = read_csv(METHOD_CSV_PATH, False)
    method_df.sum().to_csv("./sum/method_sum.csv")

    variable_df = read_csv(VARIABLE_CSV_PATH, False)
    variable_df.sum().to_csv("./sum/variable_sum.csv")

# Rankの出力(publicのみ)
def export_count_public():
    count_morph(CLASS_CSV_PATH, "./count/class_count_public.csv", True)
    count_morph(METHOD_CSV_PATH, "./count/method_count_public.csv", True)
    count_morph(VARIABLE_CSV_PATH, "./count/variable_count_public.csv", True)

# Rankの出力(privateのみ)
def export_count_private():
    count_morph(CLASS_CSV_PATH, "./count/class_count_private.csv", False)
    count_morph(METHOD_CSV_PATH, "./count/method_count_private.csv", False)
    count_morph(VARIABLE_CSV_PATH, "./count/variable_count_private.csv", False)

# Rankの出力(全て)
def export_count_all():
    count_morph(CLASS_CSV_PATH, "./count/class_count_all.csv", None)
    count_morph(METHOD_CSV_PATH, "./count/method_count_all.csv", None)
    count_morph(VARIABLE_CSV_PATH, "./count/variable_count_all.csv", None)

# 位置ごとの品詞を数える
def count_morph(data_path, output_path, isPublic):
    df = read_csv(data_path, True)
    df = df.astype({ "isPublic": "str" })
    if isPublic == None:
        df = df
    elif isPublic == True:
        df = df[df["isPublic"].str.contains("TRUE", flags=re.IGNORECASE, regex=True)]
    elif isPublic == False:
        df = df[df["isPublic"].str.contains("FALSE", flags=re.IGNORECASE, regex=True)]
    result = pd.DataFrame()
    for i in range(1, 31):
        new_series = df[str(i)].value_counts()
        result = pd.concat([result, new_series], axis=1)
    result.to_csv(output_path)

# repositoryを数える
def count_repository():
    result = pd.DataFrame()
    paths = [ CLASS_CSV_PATH, METHOD_CSV_PATH, VARIABLE_CSV_PATH ]
    for path in paths:
        df = read_csv(path, True)
        new_series = df["repository"].value_counts()
        result = pd.concat([ result, new_series ], axis=1)
    result.to_csv("./count/repository_count.csv")

def count_word_length():
    df = read_csv(VARIABLE_CSV_PATH, False)
    df = df["wordLength"].value_counts()
    df.to_csv("./wordLength.csv")

# 数えれそうなものを数える
def sum_something():
    paths = [ CLASS_CSV_PATH, METHOD_CSV_PATH, VARIABLE_CSV_PATH ]
    for i in range(len(paths)):
        df = read_csv(paths[i], False)
        df = df.sum()
        path = "./sum/" + str(i) + ".csv"
        df.to_csv(path)

ORDER = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP',
                'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH',
                'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', 'other']

def test():
    print('test')

print('start')
df = read_csv(VARIABLE_CSV_PATH, True)
df = df.astype({ "isPublic": "str", "name": "str" })
df = df[df["isPublic"].str.contains("FALSE", flags=re.IGNORECASE, regex=True)]
df = df[df["name"].str.match("..+")]
df = df["wordLength"]
print(df.mean())
print(df.median())
print(df.mode().to_list())
print('end')
