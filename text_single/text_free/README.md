# Lexical Substitution (LEXSUB) Annotation Task
## Introduction
In the LEXSUB annotation task, annotators are presented a series of sentences, each containing a target lemma. Users are asked to provide a synonym to replace the target lemma in the context of the sentence in which it appears. The substitute word should preserve the meaning of the target as closely as possible.

Each `language` folder contains tutorial data for training annotators as well as real, pre-annotated sample data.
## Data Format
Please provide uses.tsv files in the general format outlined in the README for this repository.

### Vocabulary
A txt file containing the vocabulary used for random annotation and evaluation.

### instances.tsv
**dataIDs**: A data ID corresponding to the the dataID in uses and a senseID from the senses.tsv file.

**label_set**: Empty label set

### judgments.tsv
**label**: A single integer value from the **label_set** or '-' for non-label.

## Download Data
The data for this task can be downloaded using the transform_wssim.py script, found in the `scripts/transform_lexsub` directory of the repository. To run the script, you will first need to install the requirements.txt file located in the same directory. This can be done from the command line:

`$ pip install -r requirements.txt`

To run transform_wssim.py, you will need to specify a directory to which you would like to download the external data as well as the directory to which you would like the transformed data. To run the script:

`$ python3 transform_lexsub.py your_path1 your_path2`

## Random Annotator


## Evaluation


To install requirements:
`$ pip install -r requirements.txt`

To run evaluation.py script:
`$ python3 evaluation.py your_path random_judgments.tsv "krip, sp"`

## References

Erk, Katrin, Diana McCarthy, and Nicholas Gaylord. 2013. Measuring word meaning in context.

http://www.dianamccarthy.co.uk/downloads/WordMeaningAnno2012/