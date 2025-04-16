# Annotation Standardization
## Introduction
Welcome to the repository for the standardization of text annotation tasks. This document provides an overview of the structure of the respository as well as general formatting specifications for data files. The specifications outlined below are not exhaustive and may vary depending on your annotation task. This repository supports the following annotation tasks:

- UREL (Usage Relatedness)
- LEXSUB (Lexical Substitution)
- WSBEST (Word Sense Best)
- WSSIM (Word Sense Similarity)

## Structure of the repository

Each task follows the structure of the below diagram.

```
task_type
│
└───task_name
        │   README.md
        │   guidelines.md
        │
        └───language
                |
                └───tutorial
                │        uses.tsv
                │        instances.tsv
                │        judgments.tsv
                │		
                └───data
                         uses.tsv
                         instances.tsv
                         judgments.tsv
```

Each `task_type` will be one of the following:
- use single
- use pair
- use tuple
- use rank
- use replace
- sentiment analysis

For each `task_name`, you will find a task-specific README file which contains suggested configurations for data files. Additionally, you will find a Guidelines document containing guidelines for annotators. Each `language` folder contains the folders `tutorial` and `data`. The `tutorial` folder contains a small set of data for training annotators. The `data` file contains a set of real, pre-annotated data. 

## General Format
All data must be provided in the .tsv format. Each annotation task will (at minimum) contain uses.tsv files, instances.tsv files, and judgments.tsv files. The general format for each of these files is described below. However, depending on the task, additional fields and files may be required. The README for each task will specify the format for the instances.tsv and judgments.tsv files as well as any additional files that may be required.
### Uses
A uses.tsv file contains a set of texts to be annotated and has the following fields:

* **dataID**: A unique text ID
* **context**: The context of use in which the target lemma occurs.
* **indices_target_token**: The character indices of the target token in context (Python list ranges used in slicing). Multiple index slices are possible in certain cases. For example, many English phrasal verbs allow an object between the verb and the preposition.
*e.g. switch off: 1) He switched the light off, 2) He switched off the light* 
* **indices_target_sentence**: The index slice containing the sentence in which the target occurs.
* **lemma**: The target lemma.
* **info**: An optional field to provide additional information.
***
### Instances
The instances file contains a set of annotation instances to be judged by the annotator. The instances.tsv file contains the following fields:
* **instanceID**: A unique ID for an annotation instance.
* **dataIDs**: Given in the task-specific README file. The dataIDs column references data needed to perform an annotation task.
* **tag**: An optional tag field.
* **label_set**: The set of labels from which the annotator must select. The label_set is given in the task-specific README file.
* **cannot_annotate**: A special label selected by the user when they are unable to provide an annotation.
* **info**: An optional field to provide additional information for each instance.
***
### Judgments
The judgments.tsv file is the format for representing annotated instances as well as the set of gold standard annotations. The judgments.tsv file contains the following fields:

* **instanceID**: The unique instance ID corresponding to an annotation instance in the instances.tsv file.
* **label**: The label value for a given annotation instance, given in the task-specific README.
* **comment**: A comment field for the annotator.

***
## Scripts
The scripts folder is structured according to the below diagram.
```
scripts
|   
└─── random_annotator
|       annotation_provider.py
|       random_annotate.py
|
└─── dwug_converter
|       convert_dwug.py
|
└─── transform_wssim
|       transform_wssim.py
|
└─── transform_wsbest
|       transform_wsbest.py
|
└─── transform_lexsub
|       transform_lexsub.py         
|
|
└─── evaluation
        evaluation.py
```
The `scripts` folder, contains three directories: `random_annotator` and `dwug_converter`, and `evaluation`. 

The `random_annotator` randomly generates randomly annotated data for a given annotation task. Instructions for running the random_annotate.py script are given in the task-specific README.

The `dwug_converter` downloads pre-annotated Word Usage Graph (WUG) data (https://www.ims.uni-stuttgart.de/en/research/resources/experiment-data/wugs/), and converts it to the standard format outlined in this repository. Instructions for running the convert_dwug.py script can be found in the task-specific README.

The `transform_wssim` script formats pre-annotated data for the WWSIM task according to the standard format outlined in this repository. The data can be found at http://www.dianamccarthy.co.uk/downloads/WordMeaningAnno2012/. Instructions for running the transform_wssim.py script can be found in the task-specific README. 

The `evaluation` script generates an evaluation.tsv file containing results accross various evlalutation metrics given two .tsv files in the judgments format. For example, this script can be used to evaluate automatically annotated data against gold standard annotated data. More information on running the script can be found in the task specific README.


***
### License
This project is licensed under the terms of the MIT license.
