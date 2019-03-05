#!/bin/bash

last_character='s/[！？。「」]/h/g'
old_character='[ゝヱゑゐヰ]'
all_symbol='s/[、。，．・：；？！゛゜´｀¨＾￣＿ヽヾゝゞ〃仝々〆〇ー―‐／＼～∥｜…‥‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＋－±×÷＝≠＜＞≦≧∞∴♂♀°′″℃￥＄￠￡％＃＆＊＠§☆★○●◎◇◆□■△▲▽▼※〒→←↑↓〓∈∋⊆⊇⊂⊃∪∩∧∨￢⇒⇔∀∃∠⊥⌒∂∇≡≒≪≫√∽∝∵∫∬Å‰♯♭♪]//g'
aozora_dir=Aozorabunko
preprocess_dir=Data_preprocess

[ ! -e ${preprocess_dir} ] && mkdir ${preprocess_dir}

for file_path in `find ${aozora_dir} | grep txt`; do

    text_tail=`cat -n ${file_path} | grep 底本：| awk '{print $1}'`
    if [ -z "${text_tail}" ];then
        text_tail=`cat ${file_path} | wc -l`
    else
        text_tail=`expr ${text_tail} - 1`
    fi

    text_head=`cat -n ${file_path} | grep -E '\-\-\-\-\-\-\-\-\-\-' | awk '{print $1}' | tail -n1`
    if [ -z "${text_head}" ];then
        text_head=0
    else
        text_head=`expr ${text_head} + 1`
    fi

    [ -e temp.txt ] && rm temp.txt

    cat ${file_path} | head -${text_tail} | tail -`expr ${text_tail} - ${text_head} + 1` > temp.txt


    preprocess_file=`basename ${file_path}`

    [ -e ${preprocess_dir}/${preprocess_file} ] && rm ${preprocess_dir}/${preprocess_file}

    old_flug=`grep -E ${old_character} temp.txt | wc -l`
    if [ ${old_flug} -eq 0 ];then
        sed 's/（[^\）]*）//g' temp.txt | \
            sed 's/《[^\》]*》//g' | \
            sed 's/〔[^\〕]*〕//g' | \
            sed 's/［＃[^\]*］//g' | \
            sed ${last_character} | \
            tr 'h' '\n' | \
            tr '\r' 'h' | \
            sed 's/——/h/g' | \
            sed ${all_symbol} | \
            sed 's/h//g' | \
            grep -v -E '[a-zA-Z0-9０-９ａ-ｚＡ-Ｚ]' | \
            grep -v '^\s*$'| \
            sed 's/　//g' > ${preprocess_dir}/${preprocess_file}
    fi
done

rm temp.txt
