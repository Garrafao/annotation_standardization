import krippendorff
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import os 
import argparse
from collections import defaultdict
from csv import DictWriter
from tqdm import tqdm

'''
Loads and aggregates judgments data/calculates median value of judgment. Returns
grouped judgements with median value and target lemma.
INPUT[str]: A path to a folder containing a judgments.tsv file.

OUTPUT[str, pandas.DataFrame]: The target lemma and a pandas dataframe object containing
judgments with calculated median values.
'''
def load_judgments(path):
    df = pd.DataFrame()
    judge_path = path + '/judgments.tsv'
    df = pd.read_csv(judge_path, delimiter='\t')


    # Replace null judgments with nan
    df['label'] = df['label'].replace('-', np.NaN)
    # Cast labels to floats
    df['label'] = df['label'].astype(float)


    # Aggregate use pairs and extract median column
    df = df.groupby(['instanceID'])['label'].apply(list).reset_index(name='label')
    df['median_judgment'] = df['label'].apply(lambda x: np.nanmedian(list(x)))

    # nan median
    df = df[~df['median_judgment'].isnull()]

    # Get target lemma name from uses.tsv file
    use_path = path + '/uses.tsv'
    uses = pd.read_csv(use_path, delimiter='\t')
    lemma = uses.iloc[0]['lemma']

    return df, lemma

'''
Loads auto annotated data file to a pandas dataframe object.

INPUT[str]: A path to a file containing auto annotated data.

OUTPUT[pandas.DataFrame]: A pandas dataframe object containing auto
annotated data.
'''
def load_auto_annotation(path):
    df = pd.DataFrame()
    fn = path
    df = pd.read_csv(fn, delimiter='\t')

    # Replace non labels with np.Nans
    df['label'] = df['label'].replace('-', np.NaN)
    # Cast labels to floats
    df['label'] = df['label'].astype(float)

    return df
'''
Builds arrays to pass to evaluation functions.

INPUT[pandas.DataFrame, pandas.DataFrame]: The dataframe containing the aggregated
data and the dataframe containing the auto-annotated data.

OUTPUT[list, list]: A list of median label values for aggregated judgments (gold_list) and
a list containing automatically generated label values (auto_list)
'''
def make_arrays(auto_df, gold_df):
    gold_list = gold_df['median_judgment'].tolist()
    auto_list = auto_df['label'].tolist()
    return gold_list, auto_list
'''
Builds reliability data (a 2d list) from the gold_list and auto_list output from the make_arrays()
function. Calculates Krippendorf's alpha for ordinal data using krippendorff.alpha(): 
https://github.com/pln-fing-udelar/fast-krippendorff.

INPUT[list, list]: A list of median label values for aggregated judgments (gold_list) and
a list containing automatically generated label values (auto_list).

OUTPUT[float]: Calculated alpha from reliability data. 
'''

def krip(gold_list, auto_list):
    reliability_data = [gold_list, auto_list]
    k = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement='ordinal')
    return k

'''
Calculates a Spearman correlation coefficient from the gold_list and auto_list output 
from the make_arrays() function. Spearman calculated using scipy.stats.spearmanr.

INPUT[list, list]: A list of median label values for aggregated judgments (gold_list) and
a list containing automatically generated label values (auto_list).

OUTPUT[float]: Calculated correlation coefficient from input data. 
'''
def spearman(gold_list, auto_list):
    spearman = spearmanr(gold_list, auto_list, nan_policy='omit')
    return spearman.correlation

'''
Writes dictionary of results to an evaluation.tsv file.

INPUT[dict, str]: Dictionary containing results of evaluation metrics where
the key is the target lemma. Ex. {'target_lemma': {krip: -.530328, sp: 0.000190},...}

OUTPUT[None]: Writes dictionary to evaluation.tsv file. 
'''
def write_results(res_dict, path):
    fn = os.path.join(path, 'evaluation.tsv')
    keys = ['lemma', 'krip', 'sp']
    rows = res_dict.values()

    with open(fn, 'w') as f:
        dict_writer = DictWriter(f, fieldnames=keys, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(rows)

'''
Main evalutation function. The script can be run from the comman line with 3 positional
arguments: start_directory, auto_annotator_name (name convention for auto-annotated.tsv file),
metrics (e.g. "krip, sp" for Krippendorf's alpha and Spearman correlation).

INPUT[str, str, str]: 1) Path to main directory to start evaluation. This directory must contain a
file called data which holds subfolders containing (at minimum) judgments.tsv files, uses.tsv
files, and auto-annotated data in the .tsv format. 2) Naming convention for auto annotated .tsv files
(e.g. auto_annotation.tsv). 3) Selected evalutation metrics separated by commas (e.g. "krip, sp" for
Krippendorf and Spearman).

OUTPUT[None]: Writes dictionary to evaluation.tsv file. 
'''

def main():
    # Getting positional arguments from argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('start_directory', metavar='start_directory', type=str, help='Enter directory with uses and instances files')
    parser.add_argument('auto_annotator_name', metavar='auto_annotator_name', type=str, help='Enter the file name with auto-annotated data (e.g. random_judgments.tsv')
    parser.add_argument('metrics', metavar='metrics', type=str, help='Enter your preferred evluation metrics separated by commas (e.g. "sp, krip")')
    args = parser.parse_args()
    path = args.start_directory
    auto_fn = args.auto_annotator_name

    # Extract metrics from metrics string and put in list
    metrics = [x.strip() for x in args.metrics.split(',')]

    # Initialse metric_dict to false for all metrics. If metric is included
    # in metrics argument, value is set to true.
    metric_dict = {'sp': False, 'krip': False}

    for metric in metrics:
        if metric in metric_dict.keys():
            metric_dict[metric] = True
        else:
            print(metric + ' not a valid option')

    # Initialize results dictionary as defaultdict()
    res_dict = defaultdict(lambda: {'krip': None, 'sp': None})

    # Open path to /data/ file and iterated over the sub folders
    data_path = os.path.join(path, 'data')
    for dir in tqdm(os.listdir(data_path)):
        f = os.path.join(data_path, dir)
        # Get judgments, lemma, and auto annotated data at each sub folder
        judgments, lemma = load_judgments(f)
        auto_annotations = load_auto_annotation(os.path.join(f, auto_fn))
        # Make arrays to pass to evaluation functions
        gold_lst, auto_lst = make_arrays(auto_annotations, judgments)

        res_dict[lemma]['lemma']=lemma
        
        # Perform metric evaluation if metric in metric_dict and put results in res_dict
        if metric_dict['krip'] == True:
            k = krip(gold_lst, auto_lst)
            res_dict[lemma]['krip'] = k
        
        if metric_dict['sp'] == True:
            sp = spearman(gold_lst, auto_lst)
            res_dict[lemma]['sp'] = sp

    # Write res_dict to evaluation.tsv file one directory above the /data/ folder
    write_results(res_dict, path)


if __name__ == '__main__':
    main()