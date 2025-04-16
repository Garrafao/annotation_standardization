# UREL Annotation Task
## Introduction
The usage relatedness annotation tasks asks annotators to rate the degree of semantic relatedness between two uses of a word. The guidelines.md file contains instructions for annotators.

Each `language` folder contains tutorial data for training annotators as well as real, pre-annotated sample data.
## Data Format
Please provide uses.tsv files in the general format outlined in the README for this repository.
### instances.tsv
**dataIDs**: A pair of dataIDs, corresponding to the dataID column in the uses.tsv file, for which the lemma is the same.
**label_set**: A scale (1,2,3,4).

### judgments.tsv
**label**: A single integer value from the **label_set** or '-' for non-label.

## Download Data
The convert_dwug.py file, found in the `scripts` folder will automatically download pre-annotated data from the DWUG (Diachronic Word Usage Graphs) resource: https://www.ims.uni-stuttgart.de/en/research/resources/experiment-data/wugs/.

The code can be run from the command line and accepts two arguments: 1) The absolute path to the directory in which you would like to download the data, and 2) The language code corresponding to your chosen language:

* 'en' for English
* 'de' for German
* 'la' for Latin
* 'sv' for Swedish
* 'es' for Spanish

`$ python3 convert_dwug.py your_path en`

The data can be found in the directory `your_path/dwug_en/data`.
## Random Annotator
To randomly generate annotations for the instances.tsv files, you can use the random_annotate.py script found in the `scripts` folder. This script iterates over a directory in the formate of the `data` folder in this directory. The script generates a `random_judgments.tsv` file for each `instances.tsv` file in the directory. The random annotator can be run from the command line. The argument is the absolue path to the directory where the instances.tsv files can be found. The script outputs the `random_judgments.tsv` file to the same folder as the `instances.tsv` file.

`$ python3 random_annotate.py your_path`

## Evaluation
The evaluation.py script can be found in the `scripts/evlauation` folder. The script can be run from the command line and accepts 3 positional arguments: 1) A directory containing folder `data` which holds sub directories for each lemma in you data set, each with a uses.tsv, intances.tsv, judgments.tsv, and an auto_annotated.tsv* file. 2) The naming convention for the auto-annotated.tsv file (e.g. random_judgments.tsv). 3) Chosen evaluation functions (e.g. "krip" for Krippendorf's alpha or "sp" for Spearman or "krip, sp" for both). It is advised to create a virtual Python environment and pip install the requirements.txt file located in the `scripts/evaluation` folder:

To install requirements:
`$ pip install -r requirements.txt`

To run evaluation.py script:
`$ python3 evaluation.py your_path random_judgments.tsv "krip, sp"`


\* The naming convention for this file will be specified by the user
## References
Dominik Schlechtweg, Nina Tahmasebi, Simon Hengchen, Haim Dubossarsky, Barbara McGillivray. 2021. DWUG: A large Resource of Diachronic Word Usage Graphs in Four Languages.


Erk, Katrin, Diana McCarthy, and Nicholas Gaylord. 2013. Measuring word meaning in context.

Schlechtweg, Dominik, Sabine Schulte im Walde, and Stefanie Eckmann. 2018. Diachronic Usage Relatedness (DURel): A framework for the annotation of lexical semantic change.