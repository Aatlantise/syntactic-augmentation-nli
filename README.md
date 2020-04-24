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

Fields within each file are equivalent to the MNLI datasets downloadable from [GLUE](https://github.com/nyu-mll/GLUE-baselines). However, only four fields `index`, `sentence1` (premise), `sentence2` (hypothesis), and `gold_label` are populated. 

## Script

The attached `.tsv` data files were used to augment the MultiNLI training set in our experiments. They are randomly selected subsets or unions of subsets of transformations created by running [`generate_dataset.py`](https://github.com/Aatlantise/syntactic-augmentation-nli/tree/master/generate_dataset.py), which requires MultiNLI's json file `multinli_1.0_train.jsonl` to run. Simply modify the MNLI path argument before running `python2 generate_dataset.py`.

This will create four files: `inv_orig.tsv`, `inv_trsf.tsv`, `pass_orig.tsv`, and `pass_trsf.tsv`. From these four files, individual augmentation sets similar to those included in the `datasets` folder can be created by concatenating and / or subsetting using commands like `cat` and `shuf -n`.

## Config

In the [`config`](https://github.com/Aatlantise/syntactic-augmentation-nli/tree/master/config) folder, `bert_config.json` contains BERT configurations, while `train.sh` and `hans_pred.sh` contain training, evaluation, and prediction parameters for running BERT's [`run_classifier.py`](https://github.com/google-research/bert/blob/master/run_classifier.py).

## Training and evaluating on MNLI and HANS

If you already haven't downloaded MNLI data, now is the time. You can do so by running [download_glue_data.py](https://github.com/nyu-mll/GLUE-baselines/blob/master/download_glue_data.py). It includes files mentioned below like `train.tsv` and `test_matched.tsv`:

```
python download_glue_data.py --data_dir ~/download/path --tasks MNLI
```

To finetune BERT with an augmented training set, you can concatenate an augmentation set to training set `train.tsv`:

```
shuf -n1215 inv_trsf.tsv > inv_trsf_large.tsv
mv train.tsv train_orig.tsv
cat train_orig.tsv inv_trsf_large.tsv > train.tsv
```

and finetune BERT as you would on an unaugmented set:
```
bash train.sh
```

Once the model is trained, it will also be evaluated on MNLI, and the results will be recorded in `eval_results.txt` in your output folder. It'll look something like this:

```
eval_accuracy = 0.8471727
eval_loss = 0.481841
global_step = 36929
loss = 0.48185167
```

Along with the results file, you'll also see checkpoint files starting with `model.ckpt-some-number`. They are model weights at a particular point in training, the higher the number, the closer it is to completion of training. If you used large augmentation, you'll have `model.ckpt-36929` as your trained model.

To evaluate the model on HANS, you'll need to have downloaded scripts and datasets from [HANS](https://github.com/tommccoy1/hans). And, format `heuristics_evaluation_set.txt` to resemble `test_matched.tsv` and have fields `sentence1` (premise) and `sentence2` (hypothesis) as 9th and 10th fields. Other fields can be filled with dummy fillers. The formatted file will also need to be named `test_matched.tsv`, so it is a good idea to keep MNLI and HANS directories separate.

Then, you can create the model's predictions on HANS:
```
bash hans_pred.sh
```

Once it is finished, it will produce `test_results.tsv` in your output folder. To analyze it, you need to process the results:

```
python process_results.py
python evaluate_heur_output.py preds.txt
```

This will output HANS performance by heuristic, by subcase, and by template.

## License

This repository is licenced under the MIT [license](https://github.com/Aatlantise/syntactic-augmentation-nli/tree/master/LICENSE.md).

