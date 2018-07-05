#!/usr/bin/python3

import csv
import argparse

parser = argparse.ArgumentParser(description='script to output ')
parser.add_argument('-i', dest='input', help='video files to combine.', nargs='*')
parser.add_argument('-o', dest='output', help='file to output the new video to.')