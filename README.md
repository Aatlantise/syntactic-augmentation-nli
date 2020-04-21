# qa2

This repository contains the syntactic augmentation dataset to improve robustness in NLI.

## Data

Augmentation datasets are in the [`datasets`](https://github.com/Aatlanties/qa2/datasets) folder. Each file is named using the following abbreviations:

Transformation strategies:
- `inv`: inversion
- `pass`: passivization
- `comb`: combination of inversion and passivization
- `chaos`: random shuffling condition

Sentence pair:
- `orig`: original premise as premise, tranformed hypothesis as hypothesis
- `trsf`: original hypothesis as premise, transformed hypothesis as hypothesis

Label:
- `pos`: augmentation examples whose gold label is entailment
- `neg`: augmentation examples whose gold label is nonentailment

Size:
- `small`: 101 examples
- `medium`: 405 examples
- `large`: 1215 examples

For example, [`pass_orig_pos_small.tsv`](https://github.com/Aatlantise/qa2/datasets/pass_orig_pos_small.tsv) is an set of 101 original premise-passivized hypothesis pair whose labels are entailment. Fields within each file are equivalent to those from the [MultiNLI](https://github.com/nyu-mll/multiNLI) dataset. However, only four fields `index`, `sentence1` (premise), `sentence2` (hypothesis), and `gold_label` are populated.

## Script

The attached `.tsv` data files were used to augment the MultiNLI training set in our experiments. They are randomly selected subsets or unions of subsets of transformations created by running [`qa2.py`](https://github.com/Aatlanties/qa2/qa2.py) on Python 2. It requires MultiNLI's json file to run.

## Config

BERT parameters and other configurations used to train augmented models are included in the [`config`](https://github.com/Aatlanties/qa2/config) folder.

