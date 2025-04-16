from annotation_provider import AnnotationProvider
import os 
import argparse
import random
'''
Given a directory as its argument in the command line, this function automatically generates random_judgments.tsv files
with annotations based on the label set provided in the instances.tsv files.
'''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_directory', metavar='start_directory', type=str, help='Enter directory with uses and instances files')
    args = parser.parse_args()
    # The start directory where the instances.tsv files can by found.
    path = args.start_directory

    # Initializes the AnnotationProvider class
    annotation_provider = AnnotationProvider(path)
    # Loop over the instances in instances.tsv
    for instance in annotation_provider.get_instances_iterator():
        print(f"Annotating instance: {instance}")
        # Adding a random judgment from the label set
        annotation_provider.add_judgement({'instanceID': instance['instanceID'], 'label':random.choice([*instance['label_set'], instance['non_label']]), 'comment': '-'})
    # Result is output to file 'random_judgments.tsv'
    annotation_provider.flush_judgement(path, filename='random_judgments.tsv')


if __name__ == '__main__':
    main()