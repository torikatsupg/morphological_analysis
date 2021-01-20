from matplotlib.pyplot import xcorr
import pandas as pd
from collections import defaultdict

MARKOV_PATH = "../csv/markov/modified/"
MORPH_SUM_PATH = "../csv/sum/"

# CSV読み込み
def read_markov_csv(csv_path: str) -> pd.DataFrame:
  return pd.read_csv(csv_path, usecols=range(35), index_col=0, low_memory=False)

def read_sum_csv(csv_path: str) -> pd.DataFrame:
  return pd.read_csv(csv_path, usecols=range(2), index_col=0, low_memory=False)

# カイ2乗値の算出
#|     ||      tag |      tag_|      sum |
#| --- || -------- | -------- | -------- |
#| ali ||       a  |   c(j-a) |      lf1 |
#| ide ||       b  |   d(k-b) |      lf2 |
#| --- || -------- | -------- | -------- |
#| sum || pf1(a+b) | pf2(b+d) |   N(j+k) |
#
def compute_chi2(alice_tag, identifier_tag, alice_sum, identifier_sum):
  # c, dの値算出
  a = alice_tag * alice_sum
  b = identifier_tag * identifier_sum
  c = alice_sum - a
  d = identifier_sum - b

  # 全体の標本数
  N = alice_sum + identifier_sum

  # 列周辺度数(Line premiter Frequency)
  lf1 = alice_sum
  lf2 = identifier_sum

  # 列周辺度数(Peripheral Frequency)
  pf1 = a + b
  pf2 = c + d

  # 期待値
  ea = pf1 * lf1 / N if not N == 0 else 0
  eb = pf1 * lf2 / N if not N == 0 else 0
  ec = pf2 * lf1 / N if not N == 0 else 0
  ed = pf2 * lf2 / N if not N == 0 else 0

  # (実測値 - 期待値) ^ 2 / 期待値
  x = (a - ea) ** 2 / ea if not ea == 0 else 0
  y = (b - eb) ** 2 / eb if not eb == 0 else 0
  z = (c - ec) ** 2 / ec if not ec == 0 else 0
  w = (d - ed) ** 2 / ed if not ed == 0 else 0

  # カイ2乗値
  chi = x + y + z + w
  return chi

# メイン関数
def main():
  # csv読み込み
  alice = read_markov_csv(MARKOV_PATH + "alice_markov_rate_modified.csv").fillna(0)
  identifier = read_markov_csv(MARKOV_PATH + "variable_markov_modified.csv").fillna(0)
  alice_total = read_sum_csv(MORPH_SUM_PATH + "alice_modified.csv")
  identifier_total = read_sum_csv(MORPH_SUM_PATH + "variable.csv")

  # 配列の作成
  result = defaultdict(lambda:defaultdict(lambda:0))

  # 各カイ2乗値を計算
  for row in identifier.index:
    for col in identifier.columns:
      result[row][col] = compute_chi2(
        alice.at[row, col],
        identifier.at[row, col],
        alice_total.at[col, "value"],
        identifier_total.at[col, "value"],
      )

  # csvファイルの出力
  pd.DataFrame.from_dict(result, orient='index').to_csv("variable.csv")

main()