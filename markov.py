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

# test
render_tree("../csv/markov/class_markov.csv",     "class_markov_graph")
render_tree("../csv/markov/method_markov.csv",    "method_markov_graph")
render_tree("../csv/markov/variable_markov.csv",  "variable_markov_graph")