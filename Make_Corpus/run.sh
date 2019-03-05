#!/bin/bash

# [ USER SETTING ]
# 0: data preprocess

stage=1

# [ PREPROCESS SETTING ]
N_GRAM_DIR=N_gram


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

