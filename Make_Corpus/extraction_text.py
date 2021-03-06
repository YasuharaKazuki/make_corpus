#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import MeCab
from itertools import chain
import re
from pykakasi import kakasi
from joblib import Parallel, delayed

def read_path_list(path_file):
    """READ FILE PATH AND MAKE PATH LIST

    Parameter
    ---------
    path_file: str
        file name of path

    Return
    ---------
    path_list: list of str
        path list
    """
    with open(path_file) as f:
        # read files and make list
        path_list = [line.rstrip() for line in f]

    return path_list


def read_text_file(path):
    """READ TEXT FILE

    Parameter
    ---------
    path: str
        path of text file

    Return
    ---------
    text_list: list of str
        text list
    """

    with open(path, 'r') as f:
        # read text file and make text list
        text_list = [line.strip() for line in f.readlines()]

    return text_list


def analysis_text(text_list):
    """ANALYZE TEXT USING MECAB AND PYKAKASI

    Parameter
    ---------
    text_list: list of str
        text list

    Return
    ---------
    analysis_list: list of str
        analyzed text list
    """
    # define MeCab
    mecab = MeCab.Tagger("-Oyomi")

    # analyze text using MeCab
    analysis_list = [re.sub(r'\n', '', mecab.parse(line)) for line in text_list]

    # define converter
    converter = kakasi()

    # set converter Kanji > Katakana
    converter.setMode('J', 'K')
    conv = converter.getConverter()

    # analyze text using Pykakasi
    try:
        analysis_list = [conv.do(line) for line in analysis_list]
    except Exception:
        print('pykakasi error')

    return analysis_list


def extract_text(pair_text, max_mora, min_mora):
    """EXTRACT TEXT

    Parameter
    ---------
    pair_text: tuple of str
        pair text
    max_mora: int
        max length of mora
    min_mora: int
        min length of mora

    Return
    ---------
    pair_text: tuple of str
        pair text
    """
    if len(pair_text[1]) >= min_mora and len(pair_text[1]) <= max_mora:
        return pair_text


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--n_jobs', type=int, default=1,
                        help='number of using CPU')
    parser.add_argument('--path_file', type=str,
                        help='File of path')
    parser.add_argument('--max_mora', type=int, default=30,
                        help='max number of mora')
    parser.add_argument('--min_mora', type=int, default=20,
                        help='minimum number of mora')
    parser.add_argument('--output_file', type=str,
                        help='output file name')
    args = parser.parse_args()

    # get path_list
    path_list = read_path_list(args.path_file)

    # get all text
    all_text_list = Parallel(n_jobs=args.n_jobs)([delayed(read_text_file)
                                                  (path) for path in path_list])
    # analyze all text
    analysis_list = Parallel(n_jobs=args.n_jobs)([delayed(analysis_text)
                                                  (text_list) for text_list in all_text_list])
    # flatten list
    all_text_list = list(chain.from_iterable(all_text_list))
    analysis_list = list(chain.from_iterable(analysis_list))

    # make pair list
    pair_text_list = list(zip(all_text_list, analysis_list))

    # extraction text
    text_list = Parallel(n_jobs=args.n_jobs)([delayed(extract_text)
                                              (pair_text, args.max_mora, args.min_mora)
                                              for pair_text in pair_text_list])
    # remove None data
    text_list = list(filter(None.__ne__, text_list))

    with open(args.output_file, 'w') as f:
        for text in text_list:
            f.write(text[0] + ',' + text[1] + '\n')


if __name__ == '__main__':
    main()
