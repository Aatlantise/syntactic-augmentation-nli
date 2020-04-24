# syntactic-augmentation-nli

This repository contains the syntactic augmentation dataset to improve robustness in NLI, used in our ACL 2020 paper, Syntactic Data Augmentation Increases Robustness to Inference Heuristics, by Junghyun Min<sup>1</sup>, Tom McCoy<sup>1</sup>, Dipanjan Das<sup>2</sup>, Emily Pitler<sup>2</sup>, and Tal Linzen<sup>1</sup>.

<sup>1</sup>Department of Cognitive Science, Johns Hopkins University, Baltimore, MD

<sup>2</sup>Google Research, New York, NY

## Data

Augmentation datasets are in the [`datasets`](https://github.com/Aatlantise/syntactic-augmentation-nli/tree/master/datasets) folder. Each file is named using the following abbreviations:

Transformation strategies:
- `inv`: inversion
- `pass`: passivization
- `comb`: combination of inversion and passivization
- `chaos`: random shuffling condition

Sentence pair:
- `orig`: original premise as premise, tranformed hypothesis as hypothesis
- `trsf`: original hypothesis as premise, transformed hypothesis as hypothesis

Label:
- `pos`: augmentation examples whose label is entailment
- `neg`: augmentation examples whose label is nonentailment

Size:
- `small`: 101 examples
- `medium`: 405 examples
- `large`: 1215 examples

For example, [`pass_trsf_pos_small.tsv`](https://github.com/Aatlantise/syntactic-augmentation-nli/tree/master/datasets/pass_trsf_pos_small.tsv) is an set of 101 passivization with transformed hypothesis examples whose labels are entailment. Also, please note that the negative combined transformed-hypothesis nonentailed datasets (`comb_trsf_neg_large.tsv`, etc) are not discussed or reported in our paper.

Fields within each file are equivalent to those from the [MultiNLI](https://github.com/nyu-mll/multiNLI) dataset. However, only four fields `index`, `sentence1` (premise), `sentence2` (hypothesis), and `gold_label` are populated. To finetune BERT with an augmented training set, you can concatenate an augmentation set to an existing training set `train.tsv`, and finetune BERT as you would on an unaugmented set.


## Script

The attached `.tsv` data files were used to augment the MultiNLI training set in our experiments. They are randomly selected subsets or unions of subsets of transformations created by running [`generate_dataset.py`](https://github.com/Aatlantise/syntactic-augmentation-nli/tree/master/generate_dataset.py), which requires MultiNLI's json file, like `multinli_1.0_train.jsonl` to run. Simply modify the MNLI path argument before running `python2 generate_dataset.py`.

This will create four files: `inv_orig.tsv`, `inv_trsf.tsv`, `pass_orig.tsv`, and `pass_trsf.tsv`. From these four files, individual augmentation sets similar to those included in the `datasets` folder can be created by concatenating and / or subsetting using commands like `cat` and `shuf -n`.

## Config

In the [`config`](https://github.com/Aatlantise/syntactic-augmentation-nli/tree/master/config) folder, `bert_config.json` contains BERT configurations, while `bert_mnli.sh` contains training parameters when BERT's [`run_classifier.py`](https://github.com/google-research/bert/blob/master/run_classifier.py) runs.

## License

This repository is licenced under the MIT [license](https://github.com/Aatlantise/syntactic-augmentation-nli/tree/master/LICENSE.md).

