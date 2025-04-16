import csv
import xml.etree.ElementTree as et 
import pandas as pd
import regex as re
import os
import argparse
import nltk
from nltk.corpus import wordnet as wn
import requests
from io import BytesIO
import tarfile

#******************************************************#
#DOWNLOAD DATA

def get_mc_data(url, path):
    req = requests.get(url)
    f = BytesIO(req.content)
    file = tarfile.open(fileobj=f, mode='r')
    file.extractall(path)
    xml_file = os.path.join(path, 'Data/lexsub_wcdata.xml')
    with open(xml_file, 'r') as f:
        filedata = f.read()
        filedata = filedata.replace('&#8221 ;','&#8221;')
    with open(xml_file,'w') as f:
        f.write(filedata)

#******************************************************#
#USES

def clean_use(use):
    xmlstr = et.tostring(use, encoding='unicode', method='xml')
    xml_lst = re.split('<(.*?)>', xmlstr)
    return [xml_lst[4].strip(), xml_lst[6].strip(), xml_lst[8].strip(), xml_lst[10].strip(), xml_lst[12].strip()]

def get_context(txt_lst):
    return ' '.join(txt_lst)

def get_targ_idx(txt_lst):
    start = len(txt_lst[0]) + len(txt_lst[1]) + 2
    end = start + len(txt_lst[2]) + 1
    return str(start) + ':' + str(end)

def get_targ_sent(txt_lst):
    targ_sent = txt_lst[1] + ' ' + txt_lst[2] + ' ' + txt_lst[3]
    start = len(txt_lst[0]) + 1
    end = start + len(targ_sent)
    return str(start) + ':' + str(end)


def make_uses(xml_file, file_path):
    tree = et.parse(xml_file)
    root = tree.getroot()
    cols = ['dataID', 'context', 'indices_target_token', 'indices_target_sentence', 'lemma']
    rows = []

    for i in root:
        lemma = i.attrib['item']
        for use in i.findall('instance'):
            dataID = use.attrib['id']
            txt_lst = clean_use(use)
            context = get_context(txt_lst)
            indices_target_token = get_targ_idx(txt_lst)
            indices_target_sentence = get_targ_sent(txt_lst)
            rows.append({'dataID': dataID, 'context': context, 'indices_target_token': indices_target_token, 
            'indices_target_sentence': indices_target_sentence, 'lemma': lemma})
            
    
    df = pd.DataFrame(rows, columns=cols)
    lemmas = sorted(list(set(df['lemma'].tolist())))

    for lem in lemmas:
        rslt_df = df[df['lemma'] == lem]
        os.mkdir(os.path.join(file_path, lem))
        output_dir = os.path.join(file_path, lem, 'uses.tsv')
        rslt_df.to_csv(output_dir, sep='\t', quoting=csv.QUOTE_NONE, index=False)

#******************************************************#
# JUDGMENTS

def make_judgments(csv_file, file_path):
    # read csv file
    judgments = pd.read_csv(csv_file)
    # get instance ids
    use_sense_map = list(zip(judgments['lexsub_id'].tolist(),judgments['sense_id'].tolist()))
    inst_ids = [(str(x[0]) + '-' + x[1]) for x in use_sense_map]
    # get labels, comments, annotators, and lemmas
    labels = judgments['judgment'].to_list()
    comments = ['-' for i in range(len(labels))]
    annotator = judgments['user_id'].to_list()

    '''
    for i in range(len(annotator)):
        if annotator[i] == 'avg':
            annotator[i] = 'gold_annotator'
    '''

    lemmas = judgments['lemma'].to_list()
    # initialize column names
    names = ['instanceID', 'label', 'comment', 'annotator', 'lemma']
    # make transformed dataframe
    transformed = pd.DataFrame(list(zip(inst_ids, labels, comments, annotator, lemmas)), columns=names)

    # Drop 'averages'
    transformed = transformed[transformed.annotator != 'avg']

    # Make all uses judgments ints
    transformed.label = transformed.label.apply(int)

    # write subsets of dataframe to corresponding lemma folder
    for lemma in list(set(transformed['lemma'].to_list())):
        # filter by lemma
        filtered_df = transformed[transformed['lemma'] == lemma]
        # drop lemma column
        filtered_df = filtered_df.drop('lemma', axis=1)
        # write judgments.tsv file to lemma folder
        output_dir = os.path.join(file_path, lemma, 'judgments.tsv')
        filtered_df.to_csv(output_dir, sep='\t', quoting=csv.QUOTE_NONE, index=False)

#******************************************************#
# SENSES
def extract_senses(path):
    fn = path
    senses = {}
    with open(fn, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            senses[row['sense_id']] = {
                'senseID': row['sense_id'],
                'definition': wn.lemma_from_key(row['sense_id']).synset().definition(),
                'lemma': row['lemma']
                }
    return senses

def make_senses(csv_file, file_path):
    nltk.download('omw-1.4')
    senses = extract_senses(csv_file)
    transformed = pd.DataFrame(senses.values())
    for lemma in list(set(transformed['lemma'].to_list())):
        # filter by lemma
        filtered_df = transformed[transformed['lemma'] == lemma]
        # write senses.tsv file to lemma folder
        output_dir = os.path.join(file_path, lemma, 'senses.tsv')
        filtered_df.to_csv(output_dir, sep='\t', quoting=csv.QUOTE_NONE, index=False)


#*****************************************************************************
# INSTANCES

def make_instances(path):
    label_set = '5,4,3,2,1'
    cols = ['instanceID', 'dataIDs', 'label_set', 'non_label']
    for dir in os.listdir(path):
        f = os.path.join(path, dir)
        df = pd.read_csv(os.path.join(f, 'judgments.tsv'), sep='\t', quoting=csv.QUOTE_NONE)

        # get data for instance df
        instance_ids = df['instanceID'].to_list()
        non_label = ['-' for i in range(len(instance_ids))]
        labels = [label_set for i in range(len(instance_ids))]
        data_ids = []
        for inst in instance_ids:
            inst_lst = inst.split('-')
            data_ids.append(inst_lst[0] + ',' + inst_lst[1])

        new_df = pd.DataFrame(list(zip(instance_ids, data_ids, labels, non_label)), columns=cols)
        new_df = new_df.drop_duplicates(subset=['instanceID'])
        new_df.to_csv(os.path.join(f, 'instances.tsv'), sep='\t', quoting=csv.QUOTE_NONE, index=False)

#####################################################################################################################
# Concat data to single files
def concat_mc(path):
    uses = pd.DataFrame()
    instances = pd.DataFrame()
    judgments = pd.DataFrame()
    senses = pd.DataFrame()

    for dir in os.listdir(path):
        f = os.path.join(path, dir)

        # Get paths to datafiles
        use_path = os.path.join(f, 'uses.tsv')
        inst_path = os.path.join(f, 'instances.tsv')
        judge_path = os.path.join(f, 'judgments.tsv')
        sense_path = os.path.join(f, 'senses.tsv')

        # Create dataframes from paths
        use_frame = pd.read_csv(use_path, delimiter='\t', quoting=csv.QUOTE_NONE)
        inst_frame = pd.read_csv(inst_path, delimiter='\t', quoting=csv.QUOTE_NONE)
        judge_frame = pd.read_csv(judge_path, delimiter='\t', quoting=csv.QUOTE_NONE)
        sense_frame = pd.read_csv(sense_path, delimiter='\t', quoting=csv.QUOTE_NONE)

        # Concat frames
        uses = pd.concat([uses, use_frame])
        instances = pd.concat([instances, inst_frame])
        judgments = pd.concat([judgments, judge_frame])
        senses = pd.concat([senses, sense_frame])
    
    uses.to_csv(os.path.join(path, 'uses.tsv'), sep='\t', quoting=csv.QUOTE_NONE, index=False)
    instances.to_csv(os.path.join(path, 'instances.tsv'), sep='\t', quoting=csv.QUOTE_NONE, index=False)
    judgments.to_csv(os.path.join(path, 'judgments.tsv'), sep='\t', quoting=csv.QUOTE_NONE, index=False)
    senses.to_csv(os.path.join(path, 'senses.tsv'), sep='\t', quoting=csv.QUOTE_NONE, index=False)



#*****************************************************************************
# MAIN

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_to_format', metavar='data_to_format', type=str, help='directory to download cl-meaningincontext data')
    parser.add_argument('start_directory', metavar='start_directory', type=str, help='Enter directory to download transformed data')
    args = parser.parse_args()
    original_data = args.data_to_format
    start_path = args.start_directory

    # download cl-meaninngincontext data
    get_mc_data('http://www.dianamccarthy.co.uk/downloads/WordMeaningAnno2012/cl-meaningincontext.tgz', original_data)

    # transform uses
    xml_file = os.path.join(original_data, 'Data/lexsub_wcdata.xml')
    make_uses(xml_file, start_path)
    # path to judgments csv
    judge_csv = os.path.join(original_data, 'Markup/WordSenseSimilarity/wssim2ratings.csv')
    # transform judgments
    make_judgments(judge_csv, start_path)
    # make senses
    make_senses(judge_csv, start_path)
    # make instances
    make_instances(start_path)
    # concat data
    concat_mc(start_path)



if __name__ == '__main__':
    main()
