#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--text_file', type=str,
                        help='File of path')
    parser.add_argument('--output_file', type=str,
                        help='output file name')
    args = parser.parse_args()

    # get text_list
    with open(args.text_file, 'r') as f:
        text_list = [line.rstrip() for line in f]

    with open(args.output_file, 'w') as f:
        for index in range(len(text_list)):
            f.write('ID' + str(index + 1).zfill(7) + ',')
            f.write(text_list[index] + '\n')


if __name__ == '__main__':
    main()
