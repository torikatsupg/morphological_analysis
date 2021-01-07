import pandas as pd
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
from graphviz import Digraph

index = [str(i) for i in range(1, 31)]

def read_csv(csv_path: str, range_number: int) -> pd.DataFrame:
  return pd.read_csv(csv_path, usecols=range(range_number), low_memory=False, dtype="object")

def main(df: pd.DataFrame, file_name: str) -> None:
  df = df[index].dropna(subset=[index[0]])
  count = defaultdict(lambda:defaultdict(lambda:0))

  # 品詞の前後関係をカウント
  for loc in df.index.values:
    row = df.loc[loc]
    row_len = len(row)
    for i in range(0, 30):
      current = row[i]
      next    = row[(i + 1)] if i < row_len else None
      count[current][next] += 1
      if type(next) is not str:
        break

  # 確率を算出
  result = pd.DataFrame()
  count_df = pd.DataFrame(count).fillna(0).transpose()
  for loc in count_df.index.values:
    row = count_df.loc[loc]
    sum = row.sum()
    new_row = row.apply(lambda x: round(x / sum, 4) if x != 0 else 0)
    result = pd.concat([result, new_row], axis=1)
  result.to_csv(file_name)

def render_heatmap(csv_path: str, file_name: str):
  df = pd.read_csv(csv_path, index_col=0)
  df.fillna("NaN")
  plt.figure()
  sns.heatmap(df, xticklabels=1, yticklabels=1)
  plt.savefig(file_name)
  plt.close("all")

def render_tree(csv_path: str, file_name: str):
  dg = Digraph(comment='The Round Table')
  df = pd.read_csv(csv_path, index_col=0)
  for column in df.columns:
    for index in df.index:
      value = df.at[index, column]
      if value >= 0.05:
         dg.edge(column, index, label=str(round(value, 3)))
  dg.render(file_name + '.gv', view=True)

def count_record_length():
  class_len =    len(pd.read_csv("../csv/modified/class_morphological.csv",    index_col=0, usecols=range(1), low_memory=False, dtype="object"))
  method_len =   len(pd.read_csv("../csv/modified/method_morphological.csv",   index_col=0, usecols=range(1), low_memory=False, dtype="object"))
  variable_len = len(pd.read_csv("../csv/modified/variable_morphological.csv", index_col=0, usecols=range(1), low_memory=False, dtype="object"))
  print("class", class_len)
  print("method", method_len)
  print("variable", variable_len)
  print("sum", class_len + method_len + variable_len)

def sum_word_length():
  class_df =    pd.read_csv("../csv/modified/class_morphological.csv",    index_col=0, usecols=range(8), low_memory=False)
  method_df =   pd.read_csv("../csv/modified/method_morphological.csv",   index_col=0, usecols=range(8), low_memory=False)
  variable_df = pd.read_csv("../csv/modified/variable_morphological.csv", index_col=0, usecols=range(8), low_memory=False)
  class_words     = class_df["wordLength"].sum()
  method_words    = method_df["wordLength"].sum()
  variable_words  = variable_df["wordLength"].sum()
  print("class", class_words)
  print("method", method_words)
  print("variable", variable_words)
  print("sum", class_words + method_words + variable_words)

#render_tree("../csv/markov/modified/class_markov_modified.csv",      "class_markov_tree")
#render_tree("../csv/markov/modified/method_markov_modified.csv",    "method_markov_tree")
#render_tree("../csv/markov/modified/variable_markov_modified.csv","variable_markov_tree")
#render_tree("../csv/markov/modified/alice_markov_rate_modified.csv", "alice_markov_tree")

# render_heatmap("../csv/markov/modified/class_markov_modified.csv",      "class_markov_heatmap")
# render_heatmap("../csv/markov/modified/method_markov_modified.csv",    "method_markov_heatmap")
# render_heatmap("../csv/markov/modified/variable_markov_modified.csv","variable_markov_heatmap")
# render_heatmap("../csv/markov/modified/alice_markov_rate_modified.csv", "alice_markov_heatmap")

sum_word_length()
