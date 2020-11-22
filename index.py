import nltk
import re
import csv

def main():
    analyze('../origin java files/class.csv', './reports/class_morphological.csv')
    analyze('../origin java files/method.csv', './reports/method_morphological.csv')
    analyze('../origin java files/variable.csv', './reports/variable_morphological.csv')

def analyze(read_path, write_path):
    with open(read_path) as f:
        reader = csv.reader(f, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        for row in reader:
            write_csv(write_path, create_row(row, 2))

def write_csv(csv_path, row):
    with open(csv_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row);

def create_row(row, name_index):
    parsed_row = [x for x in row if row != None and x != '']
    morphs = [nltk.pos_tag([x])[0] for x in split_name(row[name_index])]
    morphs_dict = count_morph(morphs)
    pos_tag_num_list = [morph[1] for morph in morphs]
    return parsed_row + [len(morphs)] + dict_to_list(morphs_dict) + pos_tag_num_list

def split_name(name):
    if "_" in name: # スネークケースの場合
        return [x for x in name.split("_") if x != None and x != '']
    else: # キャメルケースの場合
        return [x for x in re.split('([a-z]+)([A-Z][a-z]+)|([A-Z][a-z]+)', name) if x != None and x != '']

def count_morph(morphs):
    pos_tag_dict = create_pos_tag_dict()
    for morph in morphs:
        if morph[1] in pos_tag_dict:
            pos_tag_dict[morph[1]] += 1
        else:
            pos_tag_dict['other'] += 1
    return pos_tag_dict

def create_pos_tag_dict():
    return {
        'CC'  : 0, 'CD'  : 0, 'DT'  : 0, 'EX'  : 0, 'FW'  : 0, 'IN'  : 0, 'JJ'  : 0, 'JJR' : 0,
        'JJS' : 0, 'LS'  : 0, 'MD'  : 0, 'NN'  : 0, 'NNS' : 0, 'NNP' : 0, 'NNPS': 0, 'PDT' : 0,
        'POS' : 0, 'PRP' : 0, 'PRP$': 0, 'RB'  : 0, 'RBR' : 0, 'RBS' : 0, 'RP'  : 0, 'SYM' : 0,
        'TO'  : 0, 'UH'  : 0, 'VB'  : 0, 'VBD' : 0, 'VBG' : 0, 'VBN' : 0, 'VBP' : 0, 'VBZ' : 0,
        'WDT' : 0, 'WP'  : 0, 'WP$' : 0, 'WRB' : 0, 'other':0
    }

def dict_to_list(pos_tag_dict):
    ORDER = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP',
                'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH',
                'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', 'other']
    return [pos_tag_dict[key] for key in ORDER if key in pos_tag_dict]

def convert_tag_to_universal(tag):
    return nltk.map_tag('en_ptb', 'universal', tag)

main()
