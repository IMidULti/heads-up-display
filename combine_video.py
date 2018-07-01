#!/usr/bin/python3

import ffmpeg
import argparse

parser = argparse.ArgumentParser(description='Script to combine video files into 1 file')
parser.add_argument('-i', dest='input', help='Video files to combine.', nargs='*')
parser.add_argument('-o', dest='output', help='File to output the new video to.')

args = parser.parse_args()
output_file = args.output
file_list = args.input
ffmpeg_inputs = list()

for file in file_list:
    ffmpeg_inputs.append(ffmpeg.input(file))

(ffmpeg
    .concat(*ffmpeg_inputs)
    .output(output_file)
    .run()
)