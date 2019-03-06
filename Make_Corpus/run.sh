#!/bin/bash

# [ USER SETTING ]
# 0: data preprocess
# 1: text extraction

stage=1

# [ PREPROCESS SETTING ]
N_GRAM_DIR=N_gram
DATA_PREPROCESS=Data_preprocess

# [ EXTRACTION SETTING ]
n_jobs=4
max_mora=30
min_mora=20
path_file=path_list.txt

# [ STAGE 0 ]
if echo ${stage} | grep -q 0; then
    echo "########################################"
    echo "#            DATA PREPROCESS           #"
    echo "########################################"

    ./data_preprocess.sh

    # make bigram list
    python make_bigram_list.py \
        --unigram_file ${N_GRAM_DIR}/unigram_list.txt \
        --outdir ${N_GRAM_DIR}/

fi

# [ STAGE 1 ]
if echo ${stage} | grep -q 1; then
    echo "########################################"
    echo "#            TEXT EXTRACTION           #"
    echo "########################################"

    [ -e ${path_file} ] && rm ${path_file}
    find ${DATA_PREPROCESS} | grep txt | head -n1000 > ${path_file}

    python test.py \
        --n_jobs ${n_jobs} \
        --path_file ${path_file} \
        --max_mora ${max_mora} \
        --min_mora ${min_mora} > test.txt
fi
