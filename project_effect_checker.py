import pandas as pd

MODIFIED_CSV_DIRETORY = "../../data/csv/modified/"
EXPORT_DIRECTORY = "../../data/csv/split/"

CLASS_CSV_PATH    = MODIFIED_CSV_DIRETORY + "class_morphological.csv"
METHOD_CSV_PATH   = MODIFIED_CSV_DIRETORY + "method_morphological.csv"
VARIABLE_CSV_PATH = MODIFIED_CSV_DIRETORY + "variable_morphological.csv"

CLASS_RANGE = 72
METHOD_RANGE = 73
VARIABLE_RANGE = 74

BIG_REPOSITORIES = ["Azure/azure-sdk-for-java", "aws/aws-sdk-java", "aliyun/aliyun-openapi-java-sdk"]

def read_class_csv():
  return pd.read_csv(CLASS_CSV_PATH, usecols=range(72), low_memory=False)

def read_method_csv():
  return pd.read_csv(METHOD_CSV_PATH, usecols=range(73), low_memory=False)

def read_variable_csv():
  return pd.read_csv(VARIABLE_CSV_PATH, usecols=range(74), low_memory=False)

# でかいやつだけを抽出
def extract_big_project(df: pd.DataFrame):
  return df.query('repository in @BIG_REPOSITORIES')

# でかいやついがいを抽出
def exclude_big_project(df: pd.DataFrame):
  return df.query('not repository in @BIG_REPOSITORIES')

def split_csv_with_big():
  # read csv
  class_df = read_class_csv()
  method_df = read_method_csv()
  variable_df = read_variable_csv()
  # create csv only big
  extract_big_project(class_df).to_csv(EXPORT_DIRECTORY + "class_only_big.csv")
  extract_big_project(method_df).to_csv(EXPORT_DIRECTORY + "method_only_big.csv")
  extract_big_project(variable_df).to_csv(EXPORT_DIRECTORY + "variable_only_big.csv")
  # create csv without big
  exclude_big_project(class_df).to_csv(EXPORT_DIRECTORY + "class_without_big.csv")
  exclude_big_project(method_df).to_csv(EXPORT_DIRECTORY + "method_without_big.csv")
  exclude_big_project(variable_df).to_csv(EXPORT_DIRECTORY + "variable_without_big.csv")

# split_csv_with_bigの結果を確認
def check():
  df_all = read_class_csv()
  df_without_big = pd.read_csv(EXPORT_DIRECTORY + "class_without_big.csv", usecols=range(1))
  df_only_big = pd.read_csv(EXPORT_DIRECTORY + "class_only_big.csv", usecols=range(1))
  print(len(df_all) == (len(df_only_big) + len(df_without_big)))

  df_all = read_method_csv()
  df_without_big = pd.read_csv(EXPORT_DIRECTORY + "method_without_big.csv", usecols=range(1))
  df_only_big = pd.read_csv(EXPORT_DIRECTORY + "method_only_big.csv", usecols=range(1))
  print(len(df_all) == (len(df_only_big) + len(df_without_big)))

  df_all = read_variable_csv()
  df_without_big = pd.read_csv(EXPORT_DIRECTORY + "variable_without_big.csv", usecols=range(1))
  df_only_big = pd.read_csv(EXPORT_DIRECTORY + "variable_only_big.csv", usecols=range(1))
  print(len(df_all) == (len(df_only_big) + len(df_without_big)))