#!/usr/bin/python3

import csv
import argparse

from pprint import pprint

parser = argparse.ArgumentParser(description='script to read a CSV file')
parser.add_argument('-i', dest='input', help='video files to combine.')

args = parser.parse_args()
file_input = args.input
data = list()

with open(file_input) as f:
    reader = csv.DictReader(f)
    data = [r for r in reader]

pprint(data)