#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
import numpy as np
from pprint import pprint
import re


def main():

    np.set_printoptions(threshold=np.inf)
    parser = argparse.ArgumentParser()

    parser.add_argument('--csv_file', nargs='?',
                        help='Csv-file')
    parser.add_argument('--bigram_file', type=str,
                        help='Bigram-file')
    parser.add_argument('--output_file', type=str,
                        help='Output_file')
    parser.add_argument('--select_num', type=int,
                        help='Select number of text')
    args = parser.parse_args()

    # read csv-file
    text_csv = pd.read_csv(args.csv_file, header=None).values

    # read data
    id_list = text_csv[:, 0]
    real_text_list = text_csv[:, 1]
    read_text_list = text_csv[:, 2]

    # make dictionary for text
    text_dict = {}
    text_index = 0
    for id, read_text, real_text in zip(id_list, read_text_list, real_text_list):
        text_dict.update({text_index: (id, read_text, real_text,)})
        text_index += 1

    # make dictionary for bigram
    bigram_dict = {}
    bigram_index = 0
    with open(args.bigram_file, 'r') as f:
        for line in f:
            bigram_dict.update({line.rstrip(): bigram_index})
            bigram_index += 1

    # difine vecter of bigram
    bigram_vecter = np.zeros((len(bigram_dict), len(text_dict)))

    select_text_dict = {}

    # count mora
    for read_text_index, read_text_value in text_dict.items():
        vecter = np.array([len(re.findall('(?={0})'.format(re.escape(bigram_key)),
                                          read_text_value[1])) for bigram_key in bigram_dict])
        bigram_vecter[:, read_text_index] = vecter

    while len(select_text_dict) < args.select_num:
        # sum bigram
        sum_vecter = np.sum(bigram_vecter, axis=1)

        # get after index (except sum = 0)
        sum_vecter_sort_index = np.argsort(sum_vecter)
        sum_vecter_except_zero = np.where(sum_vecter > 0)
        sum_vecter_sort_index = sum_vecter_sort_index[len(sum_vecter) - len(sum_vecter_except_zero[0]):]

        # index of mora
        index = sum_vecter_sort_index[0]

        # get text index including mora
        index_serch = np.where(bigram_vecter[index] > 0)[0]

        # get text
        for text_index in index_serch:
            select_text_dict.update({text_index: text_dict[text_index]})
            bigram_vecter[:, text_index] = 0
            del text_dict[text_index]

    with open(args.output_file, 'w') as f:
        for select in select_text_dict.values():
            pprint(select[0] + ',' + select[2] + ',' + select[1], stream=f)


if __name__ == '__main__':
    main()
