# URANK Annotation Task
## Introduction
The Usage Rank annotation tasks asks annotators to rank a set of uses according to a specified criteria. The `guidelines.md` file provides instructions for annotators.

Each `language` folder contains tutorial data for training annotators.
## Data Format
Please provide uses.tsv files in the general format outlined in the README for this repository.
### instances.tsv
**dataIDs**: A pair of dataIDs, corresponding to the dataID column in the uses.tsv file, for which the lemma is the same.
**label_set**: Numbered list of the set of uses to be ranked. For example, if there are 3 uses to rank, the label set will be `1,2,3`

### judgments.tsv
**label**: A single integer value from the **label_set** or '-' for non-label.

## Evaluation
The evaluation.py script can be found in the `scripts/evlauation` folder. The script can be run from the command line and accepts 3 positional arguments: 1) A directory containing folder `data` which holds sub directories for each lemma in you data set, each with a uses.tsv, intances.tsv, judgments.tsv, and an auto_annotated.tsv* file. 2) The naming convention for the auto-annotated.tsv file (e.g. random_judgments.tsv). 3) Chosen evaluation functions (e.g. "krip" for Krippendorf's alpha or "sp" for Spearman or "krip, sp" for both). It is advised to create a virtual Python environment and pip install the requirements.txt file located in the `scripts/evaluation` folder:

To install requirements:
`$ pip install -r requirements.txt`

To run evaluation.py script:
`$ python3 evaluation.py your_path random_judgments.tsv "krip"`


\* The naming convention for this file will be specified by the user