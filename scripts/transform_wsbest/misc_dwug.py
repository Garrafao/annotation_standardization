import requests
import zipfile
from io import BytesIO
import os
import csv
import pandas as pd
import argparse
import shutil
from tqdm import tqdm

'''
DOWNLOAD THE DATA
'''
def download_dwug(path):
    url = 'https://zenodo.org/record/7441645/files/dwug_de.zip?download=1'
    req = requests.get(url)
    zip_file = zipfile.ZipFile(BytesIO(req.content))
    zip_file.extractall(path)
#--------------------------------------------------------------------------------------------------------
'''
TRANSFORM DATA TO OUR FORMAT AS DICTIONARIES
'''
# Extract the uses data
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
# Extract senses data
def transform_senses(path, lemma):
    fn = path
    senses = {}
    with open(os.path.join(fn, 'senses.csv'), 'r') as f:
        reader = csv.DictReader(f, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
        for row in reader:
            senses[row['identifier_sense']] = {
                'senseID': row['identifier_sense'],
                'definition': row['description_sense'],
                'lemma': lemma
            }
    return senses

# Extract instances data
def make_instance(path, senses):
    judge_path = os.path.join(path, 'judgments_senses.csv')
    judgments = pd.read_csv(judge_path, delimiter='\t')
    judgments = judgments.loc[judgments['annotator'] == 'annotatorA']
    # get unique use ids
    ids = judgments['identifier'].to_list()

    res = pd.DataFrame(columns=['instanceID', 'dataIDs', 'label_set', 'non_label'])

    for use_id in ids:
        for sense in senses:
            instanceID = sense + '-' + use_id
            dataIDs = sense + ',' + use_id
            label_set = '0,1'
            non_label = '-'
            res.loc[len(res)] = [instanceID, dataIDs, label_set, non_label]
    
    res.to_csv(os.path.join(path, 'instances.tsv'), sep='\t', index=False)

# Extract judgments data

def make_judgments(path):
    judge_path = os.path.join(path, 'judgments_senses.csv')
    inst_path = os.path.join(path, 'instances.tsv')
    j_df = pd.read_csv(judge_path, delimiter='\t')
    inst = pd.read_csv(inst_path, delimiter='\t')

    annotators = list(set(j_df['annotator'].tolist()))
    annotators.sort()
    res = pd.DataFrame(columns=['instanceID', 'label', 'comment', 'annotator'])
    for annotator in annotators:
        for id in inst['dataIDs'].tolist():
            data_id = id.split(',')[1]
            by_id = j_df.loc[(j_df['identifier'] == data_id) & (j_df['annotator'] == annotator)]
            chosen_sense = by_id['identifier_sense'].to_list()[0]
            label = ''
            comment = '-'
            if chosen_sense == 'None':
                label = '-'
                comment = by_id['comment'].tolist()[0]
            elif chosen_sense == id.split(',')[0]:
                label = 1
                comment = by_id['comment'].tolist()[0]
                if comment == ' ' or comment == '':
                    comment = '-'
            else:
                label = 0
            
            new_row = [id, label, comment, annotator]
            res.loc[len(res)] = new_row
            
    res.to_csv(os.path.join(path, 'judgments.tsv'), sep='\t', index=False)

#--------------------------------------------------------------------------------------------------------
'''
WRITE DATA TO .TSV FILES
'''

# MAKE uses.tsv
def write_uses_tsv(uses_dict, path):
    fn = os.path.join(path, 'uses.tsv')
    keys = ['dataID', 'context', 'indices_target_token', 'indices_target_sentence', 'lemma']
    rows = uses_dict.values()

    with open(fn, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(rows)

# MAKE senses.tsv
def write_senses_tsv(senses_dict, path):
    fn = os.path.join(path, 'senses.tsv')
    keys = ['senseID', 'definition', 'lemma']
    rows = senses_dict.values()

    with open(fn, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(rows)


def transform_dwug(path):
    uses, lem = transform_uses(path)
    senses = transform_senses(path, lem)
    
    sense_set = list(senses.keys())
    sense_set.sort()

    #instances = transform_instances(path, label_set)
    #judgments = transform_sense_judgments(path, instances)

    write_uses_tsv(uses, path)
    write_senses_tsv(senses, path)
    make_instance(path, sense_set)
    make_judgments(path)

    pass
#--------------------------------------------------------------------------------------------------------
'''CONCATENATE DATA'''
def concat_dwugs(path):
    uses = pd.DataFrame()
    senses = pd.DataFrame()
    instances = pd.DataFrame()
    judgments = pd.DataFrame()

    for dir in os.listdir(path):
        f = os.path.join(path, dir)

        # Get paths to datafiles
        use_path = os.path.join(f, 'uses.tsv')
        sense_path = os.path.join(f, 'senses.tsv')
        inst_path = os.path.join(f, 'instances.tsv')
        judge_path = os.path.join(f, 'judgments.tsv')

        # Create dataframes from paths
        use_frame = pd.read_csv(use_path, delimiter='\t')
        sense_frame = pd.read_csv(sense_path, delimiter='\t')
        inst_frame = pd.read_csv(inst_path, delimiter='\t')
        judge_frame = pd.read_csv(judge_path, delimiter='\t')

        # Concat frames
        uses = pd.concat([uses, use_frame])
        senses = pd.concat([senses, sense_frame])
        instances = pd.concat([instances, inst_frame])
        judgments = pd.concat([judgments, judge_frame])
    
    uses.to_csv(os.path.join(path, 'uses.tsv'), sep='\t', index=False)
    senses.to_csv(os.path.join(path, 'senses.tsv'), sep='\t', index=False)
    instances.to_csv(os.path.join(path, 'instances.tsv'), sep='\t', index=False)
    judgments.to_csv(os.path.join(path, 'judgments.tsv'), sep='\t', index=False)
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
'''MAIN FUNCTION'''

def main():
    print('''DOWNLOADING DATA...''')
    parser = argparse.ArgumentParser()
    parser.add_argument('start_directory', metavar='start_directory', type=str, help='Enter directory to download data')
    parser.add_argument('destination', metavar='destination', type=str, help='Where new data folder will be')
    args = parser.parse_args()
    path = args.start_directory
    new_path = args.destination

    # Download the data
    download_dwug(path)
    dwug_path = os.path.join(path, 'dwug_de/misc/dwug_de_sense/data')

    for dir in tqdm(os.listdir(dwug_path)):
        f = os.path.join(dwug_path, dir)

        # remove extra files (maj_2, maj_3)
        maj2 = os.path.join(f, 'maj_2')
        maj3 = os.path.join(f, 'maj_3')
        shutil.rmtree(maj2)
        shutil.rmtree(maj3)

        # transform dwug data
        transform_dwug(f)
        
        # Cleanup
        for file_name in os.listdir(f):
            if file_name.endswith('.csv'):
                os.remove(os.path.join(f, file_name))
                
    # Concatenate files
    concat_dwugs(dwug_path)
    
    original = dwug_path
    new = new_path
    shutil.move(original, new)
    shutil.rmtree(os.path.join(path, 'dwug_de'))
        
if __name__ == '__main__':
    main()