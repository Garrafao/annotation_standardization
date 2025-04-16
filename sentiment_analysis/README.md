# Sentiment Analysis
## Introduction
The sentiment analysis annotation tasks asks annotators to label the emotional valence of a text. The guidelines.md file contains instructions for annotators.

Each `language` folder contains tutorial data for training annotators.
## Data Format
Please provide uses.tsv files in the general format outlined in the README for this repository.
### instances.tsv
**dataIDs**: A dataID, corresponding to a text to be annotated.
**label_set**: A set of labels corresponding to emotional valence (0,1,2) where 0 is 'negative', 1 is 'neutral' and 2 is 'positive'.

### judgments.tsv
**label**: A single integer value from the **label_set** or '-' for non-label.


## Evaluation
The evaluation.py script can be found in the `scripts/evlauation` folder. The script can be run from the command line and accepts 3 positional arguments: 1) A directory containing folder `data` which holds sub directories for each lemma in you data set, each with a uses.tsv, intances.tsv, judgments.tsv, and an auto_annotated.tsv* file. 2) The naming convention for the auto-annotated.tsv file (e.g. random_judgments.tsv). 3) Chosen evaluation functions (e.g. "krip" for Krippendorf's alpha or "sp" for Spearman or "krip, sp" for both). It is advised to create a virtual Python environment and pip install the requirements.txt file located in the `scripts/evaluation` folder:

To install requirements:
`$ pip install -r requirements.txt`

To run evaluation.py script:
`$ python3 evaluation.py your_path random_judgments.tsv "krip, sp"`


\* The naming convention for this file will be specified by the user

## References
[TweetEval: Unified Benchmark and Comparative Evaluation for Tweet Classification](https://aclanthology.org/2020.findings-emnlp.148) (Barbieri et al., Findings 2020)