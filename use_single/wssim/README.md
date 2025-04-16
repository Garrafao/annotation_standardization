# WSSIM Annotation Task
## Introduction
In the WSSIM annotation task, users are shown a target lemma in context as well as a set of senses which may or may not apply to the target lemma. Annotators must rate each sense on how well it matches the meaning of the target lemma in its given context.

Each `language` folder contains tutorial data for training annotators as well as real, pre-annotated sample data. The "gold_annotator" judgments provided in the judgments.tsv file in the `tutorial` folder are the rounded averages of the judgments from the pre-annotated data in the `data` folder.
## Data Format
Please provide uses.tsv files in the general format outlined in the README for this repository.
### senses.tsv
The senses.tsv file contains the set of senses for each target lemma. The senses in the `data` folder were extracted from Wordnet3.0. The columns are structured as follows:
**senseID**: An ID corresponding to a sense for a given lemma (e.g. a Wordnet sense).

**definition**: The definition of corresponding to the sense.

**lemma**: The lemma for each sense.
### instances.tsv
**dataIDs**: A data ID corresponding to the the dataID in uses and a senseID from the senses.tsv file.

**label_set**: A scale (1,2,3,4,5).

### judgments.tsv
**label**: A single integer value from the **label_set** or '-' for non-label.

## Download Data
The data for this task can be downloaded using the transform_wssim.py script, found in the `scripts/transform_wssim` directory of the repository. To run the script, you will first need to install the requirements.txt file located in the same directory. This can be done from the command line:

`$ pip install -r requirements.txt`

To run transform_wssim.py, you will need to specify a directory to which you would like to download the external data as well as the directory to which you would like the transformed data. To run the script:

`$ python3 transform_wssim.py your_path1 your_path2`

## Random Annotator
To randomly generate annotations for the instances.tsv files, you can use the random_annotate.py script found in the `scripts` folder. This script iterates over a directory in the formate of the `data` folder in this directory. The script generates a `random_judgments.tsv` file for each `instances.tsv` file in the directory. The random annotator can be run from the command line. The argument is the absolue path to the directory where the instances.tsv files can be found. The script outputs the `random_judgments.tsv` file to the same folder as the `instances.tsv` file.

`$ python3 random_annotate.py your_path`

## Evaluation
The evaluation.py script can be found in the `scripts/evlauation` folder. The script can be run from the command line and accepts 3 positional arguments: 1) A directory containing folder `data` which holds sub directories for each lemma in you data set, each with a uses.tsv, intances.tsv, judgments.tsv, and an auto_annotated.tsv* file. 2) The naming convention for the auto-annotated.tsv file (e.g. random_judgments.tsv). 3) Chosen evaluation functions (e.g. "krip" for Krippendorf's alpha or "sp" for Spearman or "krip, sp" for both). It is advised to create a virtual Python environment and pip install the requirements.txt file located in the `scripts/evaluation` folder:

To install requirements:
`$ pip install -r requirements.txt`

To run evaluation.py script:
`$ python3 evaluation.py your_path random_judgments.tsv "krip, sp"`

## References

Erk, Katrin, Diana McCarthy, and Nicholas Gaylord. 2013. Measuring word meaning in context.

http://www.dianamccarthy.co.uk/downloads/WordMeaningAnno2012/