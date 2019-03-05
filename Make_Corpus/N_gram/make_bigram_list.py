#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--unigram_file', type=str,
                        help='unigram-file')
    args = parser.parse_args()

    with open(args.unigram_file, 'r') as unigram_file:
        unigram = [line.rstrip() for line in unigram_file]

    with open('bigram.txt', 'w') as w_file:
        for unigram1 in unigram:
            for unigram2 in unigram:
                w_file.write(unigram1 + unigram2 + '\n')


if __name__ == '__main__':
    main()
