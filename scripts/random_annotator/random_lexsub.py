import annotation_provider as ap
import pandas as pd
import os
import random
import argparse

def get_labels(path):
    df = pd.read_csv(os.path.join(path, 'vocab.tsv'), delimiter='\t')
    return df['lemma'].to_list()

def random_annotate(path, vocab):
    annotation_provider = ap.AnnotationProvider(path)
    for instance in annotation_provider.get_instances_iterator():
        print(f"Annotating instance: {instance}")
        # Adding a random judgment from the label set
        annotation_provider.add_judgement({'instanceID': instance['instanceID'], 'label':random.choice([*vocab, instance['non_label']]), 'comment': '-'})
    # Result is output to file 'random_judgments.tsv'
    annotation_provider.flush_judgement(path, filename='random_judgments.tsv')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_directory', metavar='start_directory', type=str, help='Enter directory with uses and instances files')
    args = parser.parse_args()
    # The start directory where the instances.tsv files can by found.
    path = args.start_directory

    vocab = get_labels(path)
    random_annotate(path, vocab)

if __name__ == '__main__':
    main()