# WSBSEST Annotation Task
## Introduction
In the WSBEST annotation task, annotators are shown a target lemma in context as well as a set of senses which may or may not apply to the target lemma. Annotators must decide which sense description **best** reflects the meaning of the usage in the target sentence. 

Each `language` folder contains tutorial data for training annotators as well as real, pre-annotated sample data.
## Data Format
Please provide uses.tsv files in the general format outlined in the README for this repository.
### senses.tsv
The senses.tsv file contains the set of senses for each target lemma. The senses in the `data` folder were extracted from Wordnet3.0. The columns are structured as follows:
**senseID**: An ID corresponding to a sense for a given lemma (e.g. a Wordnet sense).

**definition**: The definition of corresponding to the sense.

**lemma**: The lemma for each sense.
### instances.tsv
**dataIDs**: A data ID corresponding to the the dataID in uses and a senseID from the senses.tsv file.

**label_set**: A binary judgment (0,1) where 1 is 'yes' and 0 is 'no'.

### judgments.tsv
**label**: A single value (0 or 1) **label_set** or '-' for non-label.

## Download Data
The data for this task can be downloaded using the transform_wsbest.py script, found in the `scripts/transform_wsbest` directory of the repository. To run the script, you will first need to install the requirements.txt file located in the same directory. This can be done from the command line:

`$ pip install -r requirements.txt`

To run transform_wsbest.py, you will need to specify a directory to which you would like to download the external data as well as the directory to which you would like the transformed data. To run the script:

`$ python3 transform_wsbest.py your_path1 your_path2`

## Random Annotator
To randomly generate annotations for the instances.tsv files, you can use the random_annotate.py script found in the `scripts` folder. This script iterates over a directory in the formate of the `data` folder in this directory. The script generates a `random_judgments.tsv` file for each `instances.tsv` file in the directory. The random annotator can be run from the command line. The argument is the absolue path to the directory where the instances.tsv files can be found. The script outputs the `random_judgments.tsv` file to the same folder as the `instances.tsv` file.

`$ python3 random_annotate.py your_path`

## Evaluation


To install requirements:
`$ pip install -r requirements.txt`

To run evaluation.py script:
`$ python3 evaluation.py your_path random_judgments.tsv sp`

## References

Erk, Katrin, Diana McCarthy, and Nicholas Gaylord. 2013. Measuring word meaning in context.

http://www.dianamccarthy.co.uk/downloads/WordMeaningAnno2012/