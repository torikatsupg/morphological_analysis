import re
import pprint as pp
import nltk
import pandas as pd
from collections import defaultdict

def tokenize() -> list:
  with open("../data/alice_only_paragraph.txt", "r") as f:
    text = f.read()
    modified = text.lower()
    modified = spread_shorthand(modified)
    modified = trim_symbols(modified)
    sentences = re.split('[.!?]', modified)
    result = []
    for line in sentences:
      if len(line) != 0:
        words = [word for word in line.lstrip().split(" ") if len(word) != 0]
        result.append(words)
    return result

def trim_symbols(text: str) -> str:
    modified = re.sub('[\n“”—_＿;,:：()（）]', " ", text)
    modified = re.sub("( ‘)|(‘ )", " ", modified)
    modified = re.sub("( ’)|(’ )", " ", modified)
    modified = re.sub("( ')|(' )", " ", modified)
    return re.sub("  +", " ", modified)

def spread_shorthand(text: str) -> str:
  shortened = {
      '\'m': ' am',
      '\'re': ' are',
      'don\'t': 'do not',
      'doesn\'t': 'does not',
      'didn\'t': 'did not',
      'won\'t': 'will not',
      'wanna': 'want to',
      'gonna': 'going to',
      'gotta': 'got to',
      'hafta': 'have to',
      'needa': 'need to',
      'outta': 'out of',
      'kinda': 'kind of',
      'sorta': 'sort of',
      'lotta': 'lot of',
      'lemme': 'let me',
      'gimme': 'give me',
      'getcha': 'get you',
      'gotcha': 'got you',
      'letcha': 'let you',
      'betcha': 'bet you',
      'shoulda': 'should have',
      'coulda': 'could have',
      'woulda': 'would have',
      'musta': 'must have',
      'mighta': 'might have',
      'dunno': 'do not know',
  }
  shortened_re = re.compile('(?:' + '|'.join(map(lambda x: '\\b' + x + '\\b', shortened.keys())) + ')')
  return shortened_re.sub(lambda x: shortened[x.group(0)], text)

def to_tag_transitions(arr: list) -> list:
  result = defaultdict(lambda:defaultdict(lambda:0))
  for row in arr:
    tags = nltk.pos_tag(row)
    tag_len = len(tags)
    for i in range(tag_len):
      next_index = i + 1
      current = tags[i][1]
      next    = tags[next_index][1] if next_index < tag_len else None
      result[current][next] += 1
  return result

def to_transition_matrix(tag_transitions: dict) -> pd.DataFrame:
  df = pd.DataFrame.from_dict(tag_transitions)
  return df

def create_transition_matrix_from_alice():
  tokens = tokenize()
  tag_transitions = to_tag_transitions(tokens)
  to_transition_matrix(tag_transitions).fillna(0).to_csv('./alice_transition.csv')