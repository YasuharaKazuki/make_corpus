#!/bin/bash

# [ USER SETTING ]
# 0: data preprocess
# 1: text extraction
# 2: select text

stage=2

# [ PREPROCESS SETTING ]
N_GRAM_DIR=N_gram
DATA_PREPROCESS=Data_preprocess
# [ EXTRACTION SETTING ]
n_jobs=4
max_mora=30
min_mora=20
path_file=path_list.txt
output_dir=mora_${min_mora}_${max_mora}
extraction_text=extraction_text.txt
# [ SELECTION SETTING ]
SELECT_DIR=Select_text_data
selected_text=selected_text.txt
select_num=5000

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
    find ${DATA_PREPROCESS} | grep txt > ${path_file}

    [ ! -e ${output_dir} ] && mkdir ${output_dir}

    python extraction_text.py \
        --n_jobs ${n_jobs} \
        --path_file ${path_file} \
        --max_mora ${max_mora} \
        --min_mora ${min_mora} \
        --output_file ${output_dir}/${extraction_text}

    sed 's/、//g' ${output_dir}/${extraction_text} > tmp.txt
    sort tmp.txt | uniq > ${output_dir}/${extraction_text}
    rm tmp.txt

    python make_id_list.py \
        --text_file ${output_dir}/${extraction_text} \
        --output_file ${output_dir}/${extraction_text}
fi

# [ STAGE 2 ]
if echo ${stage} | grep -q 2; then
    echo "########################################"
    echo "#            SERECT TEXT               #"
    echo "########################################"

    [ ! -e ${output_dir}/${SELECT_DIR} ] && mkdir ${output_dir}/${SELECT_DIR}

    if [ -f ${output_dir}/${SELECT_DIR}/${selected_text} ]; then
        cat ${output_dir}/${extraction_text} ${output_dir}/${SELECT_DIR}/${selected_text} | \
            sort | uniq -u > ${output_dir}/${SELECT_DIR}/candidate_text.txt
    fi

    for bigram in `cat ${N_GRAM_DIR}/bigram_list.txt`; do
        shuf ${output_dir}/${SELECT_DIR}/candidate_text.txt | \
            grep ${bigram} | \
            head -n1 >> ${output_dir}/${SELECT_DIR}/tmp.txt
    done

    sort ${output_dir}/${SELECT_DIR}/tmp.txt | \
        uniq > ${output_dir}/${SELECT_DIR}/select_text.txt

    for bigram in `cat ${N_GRAM_DIR}/bigram_list.txt`; do
        shuf ${output_dir}/${SELECT_DIR}/select_text.txt | \
            grep ${bigram} | \
            head -n1 >> ${output_dir}/${SELECT_DIR}/tmp.txt
    done

    sort ${output_dir}/${SELECT_DIR}/tmp.txt | \
        uniq > ${output_dir}/${SELECT_DIR}/select_text.csv

    python calculate_bigram.py \
        --csv_file ${output_dir}/${SELECT_DIR}/select_text.csv \
        --bigram_file ${N_GRAM_DIR}/bigram_list.txt \
        --output_file ${output_dir}/${SELECT_DIR}/select_text.txt \
        --select_num ${select_num}

    rm ${output_dir}/${SELECT_DIR}/tmp.txt
fi

ls
