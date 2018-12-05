#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pykakasi import kakasi

import argparse


def read_path_list(path_file_name):
    '''
    Read file-path  and Make path list

    Parameters
    ---------
    path_file_name: string
        file name of file-path

    Returns
    --------
    path_list: list of string
        path list
    '''
    with open(path_file_name) as f:
        # read file path and make list
        path_list = [line.rstrip() for line in f]

    return path_list


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--path_file', type=str,
                        help='File of path')
    parser.add_argument('--max_mora', type=int, default=30,
                        help='max number of mora')
    parser.add_argument('--min_mora', type=int, default=25,
                        help='min number of mora')
    args = parser.parse_args()

    # get path list
    path_list = read_path_list(args.path_file)

    # define converter
    converter = kakasi()

    # define list
    text_list = []

    for path in path_list:
        # set converter Kanji > Hiragana
        converter.setMode("J", "H")
        conv = converter.getConverter()

        # read text file
        with open(path, 'r') as f:
            # read text
            text_lines = [line.strip() for line in f.readlines()]
        # convert Kanji to Hiragana
        conv_j2h_lines = [conv.do(line) for line in text_lines]

        # set converter Hiragana > Katakana
        converter.setMode("H", "K")
        conv = converter.getConverter()

        # convert Hiragana to Kanji
        conv_h2k_lines = [conv.do(line) for line in conv_j2h_lines]

        # get text from min mora to max mora
        for text, conv_text in zip(text_lines, conv_h2k_lines):
            if len(conv_text) >= args.min_mora and len(conv_text) <= args.max_mora:
                text_list.append((text, conv_text))
    id_num = 1

    output_file = 'mora_' + str(args.min_mora) + '_' + str(args.max_mora) + '.csv'
    with open(output_file, 'w') as f:
        for text in text_list:
            f.write('ID' + str(id_num).zfill(7) + ',')
            f.write(text[0] + ',' + text[1] + '\n')
            id_num += 1


if __name__ == '__main__':
    main()
