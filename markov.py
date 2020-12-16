import pandas as pd
from collections import defaultdict
from pandas.core.frame import DataFrame

index = [str(i) for i in range(1, 31)]

def read_csv(csv_path: str, range_number: int) -> DataFrame:
  return pd.read_csv(csv_path, usecols=range(range_number), low_memory=False, dtype="object")

def main(df: DataFrame, file_name: str) -> None:
  df = df[index]
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
  count_df = pd.DataFrame(count).fillna(0)
  for loc in count_df.index.values:
    row = count_df.loc[loc]
    sum = row.sum()
    new_row = row.apply(lambda x: round(x / sum, 4) if x != 0 else 0)
    result = pd.concat([result, new_row], axis=1)

  result.to_csv(file_name)

main(read_csv("../csv/modified/class_morphological.csv", 72), "./class_markov.csv")
main(read_csv("../csv/modified/method_morphological.csv", 73), "./method_markov.csv")
main(read_csv("../csv/modified/variable_morphological.csv", 74), "./variable_markov.csv")
