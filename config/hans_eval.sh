export BERT_BASE_DIR=path/to/base/model/like/uncased_L-12_H-768_A-12
export HANS_DIR=path/to/hans
export TRAINED_CLASSIFIER=path/to/trained/classifier
export OUTPUT_DIR=path/to/output/folder

#Record trained model's predictions on HANS

python run_classifier.py \
  --task_name=MNLI \
  --do_predict=true \
  --data_dir=$HANS_DIR \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$TRAINED=CLASSIFIER \
  --max_seq_length=128 \
  --output_dir=$OUTPUT_DIR
