#!/usr/bin/python3

import ffmpeg
import argparse

parser = argparse.ArgumentParser(description='Script to combine video files into 1 file')
parser.add_argument('-i', dest='input', help='Video files to combine.', nargs='*')
parser.add_argument('-o', dest='output', help='File to output the new video to.', nargs='*')

args = parser.parse_args()
file_list = args.input
ffmpeg_inputs = list()

for file in file_list:
    ffmpeg_inputs.append(ffmpeg.input(file).trim(start_frame=0, end_frame=100))

(ffmpeg
    .concat(*ffmpeg_inputs)
    .output('test.mp4')
    .run()
)