import csv
import os
from collections import defaultdict
import argparse
import requests
import zipfile
from io import BytesIO
import pandas as pd

'''
Extracts data from DWUG_EN uses.csv file and stores them in python dictionary corresponding to our schema.

INPUT: (str), a path to a directory containing a uses.csv file in the DWUG format
OUTPUT: (dict), a python dictionary containing data for a uses.tsv file per our schema.

'''
def transform_uses(path):
    fn = path
    uses = {}
    with open(os.path.join(fn, 'uses.csv'), 'r') as f:
        reader = csv.DictReader(f, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        for row in reader:
            uses[row['identifier']] = {
                'dataID': row['identifier'],
                'context': row['context'],
                'indices_target_token': row['indexes_target_token'],
                'indices_target_sentence': row['indexes_target_sentence'],
                'lemma': row['lemma'],
            }
        #return the lemma name:
        first_key = list(uses.keys())[0]
        lem = uses[first_key]['lemma']
        return uses, lem
'''
Extracts data from DWUG_EN judgments.csv file and stores them in python dictionary corresponding to our instances.tsv schema.

INPUT: (str), a path to a directory containing a judgments.csv file in the DWUG format
OUTPUT: (dict), a python dictionary containing data for a instances.tsv file per our schema.

'''
def transform_instances(path, lem):
    fn = path
    instances = {}
    inst_count = 0
    label_set = '1,2,3,4'
    non_label = '-'
    with open(os.path.join(fn, 'judgments.csv'), 'r') as f:
        reader = csv.DictReader(f, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        for row in reader:
            data_ids = row['identifier1'] + ',' + row['identifier2']
            instance = inst_count
            found_key = False
            if instances != {}:
                for key in instances.keys():
                    if instances[key]['dataIDs'] == data_ids:
                        found_key = True
            if found_key == False:
                instances[str(inst_count)] = {
                    'instanceID': str(instance) + '_' + lem,
                    'dataIDs': data_ids,
                    'label_set': label_set,
                    'non_label': non_label
                    }
                inst_count+=1
        
        id_dict = defaultdict(lambda: str)
        for inst in instances.values():
            id_dict[inst['dataIDs']]=inst['instanceID']

        return instances, id_dict

'''
Extracts data from DWUG_EN judgments.csv file and stores them in python dictionary corresponding to our judgments.tsv schema.
INPUT: (str), (id_dict): a path to a directory containing a judgments.csv file in the DWUG format and a dictionary matching
instanceIds to dataIDs.
OUTPUT: (dict), a python dictionary containing data for a judgments.tsv file per our schema.
'''
def transform_judgments(path, id_dict):
    fn = path
    judgment_count = 0
    judgments = {}
    with open(os.path.join(fn, 'judgments.csv'), 'r') as f:
        reader = csv.DictReader(f, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        for row in reader:
            data_ids = row['identifier1'] + ',' + row['identifier2']
            judgement = ''
            if row['judgment'] != '0.0':
                judgement = row['judgment']
            else: 
                judgement = '-'
            judgments[str(judgment_count)] = {
                'instanceID': id_dict[data_ids],
                'label': judgement,
                'comment': row['comment'],
                'annotator': row['annotator']
                }
            judgment_count+=1
    
    return judgments



'''
Writes uses.tsv file from python dictionary 

INPUT: (dict, string), python dictionary containing data for uses.tsv file, a directory to write the file
OUTPUT: (None), writes uses.tsv file

'''

def write_uses_tsv(uses_dict, path):
    fn = os.path.join(path, 'uses.tsv')
    keys = ['dataID', 'context', 'indices_target_token', 'indices_target_sentence', 'lemma']
    rows = uses_dict.values()

    with open(fn, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(rows)

'''
Writes instances.tsv file from python dictionary 

INPUT: (dict, string), python dictionary containing data for instances.tsv file, a directory to write the file
OUTPUT: (None), writes instances.tsv file

'''

def write_instances_tsv(instances_dict, path):
    fn = os.path.join(path, 'instances.tsv')
    keys = ['instanceID', 'dataIDs', 'label_set', 'non_label']
    rows = instances_dict.values()

    with open(fn, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(rows)

'''
Writes judgments.tsv file from python dictionary 

INPUT: (dict, string), python dictionary containing data for judgments.tsv file, a directory to write the file
OUTPUT: (None), writes uses.tsv file
'''
def write_judgments_tsv(judgments_dict, path):
    fn = os.path.join(path, 'judgments.tsv')
    keys = ['instanceID', 'label', 'comment', 'annotator']
    rows = judgments_dict.values()

    with open(fn, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(rows)

'''
Accepts a path to a directory containing a uses.csv and judgments.csv file in the DWUG_EN format. Calls write_uses_tsv()
and write_instances_tsv() functions to write uses.tsv and instances.tsv files.

INPUT: (str), a path to a directory containing uses.csv and judments.csv files in DWUG_EN format.
OUTPUT: (None), writes uses.tsv and instances.tsv files per our schema.
'''

def transform_dwug(path):
    uses, lem = transform_uses(path)
    instances, id_dict = transform_instances(path, lem)
    judgments = transform_judgments(path, id_dict)
    write_uses_tsv(uses, path)
    write_instances_tsv(instances, path)
    write_judgments_tsv(judgments, path)

def concat_dwugs(path):
    uses = pd.DataFrame()
    instances = pd.DataFrame()
    judgments = pd.DataFrame()

    for dir in os.listdir(path):
        f = os.path.join(path, dir)

        # Get paths to datafiles
        use_path = os.path.join(f, 'uses.tsv')
        inst_path = os.path.join(f, 'instances.tsv')
        judge_path = os.path.join(f, 'judgments.tsv')

        # Create dataframes from paths
        use_frame = pd.read_csv(use_path, delimiter='\t')
        inst_frame = pd.read_csv(inst_path, delimiter='\t')
        judge_frame = pd.read_csv(judge_path, delimiter='\t')

        # Concat frames
        uses = pd.concat([uses, use_frame])
        instances = pd.concat([instances, inst_frame])
        judgments = pd.concat([judgments, judge_frame])
    
    uses.to_csv(os.path.join(path, 'uses.tsv'), sep='\t', quoting=csv.QUOTE_NONE, index=False)
    instances.to_csv(os.path.join(path, 'instances.tsv'), sep='\t', quoting=csv.QUOTE_NONE, index=False)
    judgments.to_csv(os.path.join(path, 'judgments.tsv'), sep='\t', quoting=csv.QUOTE_NONE, index=False)

def download_dwug(path, lang='en'):
    urls = {'en': 'https://zenodo.org/record/5796878/files/dwug_en.zip', 
            'de': 'https://zenodo.org/record/7295410/files/dwug_de.zip',
            'la': 'https://zenodo.org/record/5255228/files/dwug_la.zip',
            'sv': 'https://zenodo.org/record/5090648/files/dwug_sv.zip',
            'es': 'https://zenodo.org/record/6433667/files/dwug_es.zip'
            }
    url = urls[lang]
    req = requests.get(url)
    zip_file = zipfile.ZipFile(BytesIO(req.content))
    zip_file.extractall(path)

'''
Main function is called from the command line with two arguments: 1) A directory to download the data, and
2) the language code ('en' for english).
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_directory', metavar='start_directory', type=str, help='Enter directory to download data')
    parser.add_argument('language', metavar='language', type=str, help='Enter language code ("en" for English)')
    args = parser.parse_args()
    path = args.start_directory
    lang = args.language

    # Download the data
    download_dwug(path, lang)
    dwug_path = os.path.join(path, 'dwug_' + lang + '/data')

    for dir in os.listdir(dwug_path):
        f = os.path.join(dwug_path, dir)
        transform_dwug(f)
        
        # Cleanup
        for file_name in os.listdir(f):
            if file_name.endswith('.csv'):
                os.remove(os.path.join(f, file_name))
                
    # Concatenate files
    concat_dwugs(dwug_path)
        
if __name__ == '__main__':
    main()
