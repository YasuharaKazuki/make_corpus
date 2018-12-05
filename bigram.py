#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--monogram_file', type=str,
                        help='Monogram-file')
    args = parser.parse_args()

    with open(args.monogram_file, 'r') as r_file:
        monogram = [line.rstrip() for line in r_file]

    with open('kasu.txt', 'w') as w_file:
        for monogram1 in monogram:
            for monogram2 in monogram:
                w_file.write(monogram1 + monogram2 + '\n')


if __name__ == '__main__':
    main()
