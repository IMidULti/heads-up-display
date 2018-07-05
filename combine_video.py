#!/usr/bin/python3

import ffmpeg
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(description='script to combine video files into 1 file')
parser.add_argument('-i', dest='input', help='video files to combine.', nargs='*')
parser.add_argument('-o', dest='output', help='file to output the new video to.')

args = parser.parse_args()
output_file = args.output
file_list = args.input
ffmpeg_inputs = list()

for file in file_list:
    #ffmpeg_input = ffmpeg.input(file).filter_multi_output('split').trim(start_frame=0, end_frame=100
    ffmpeg_input = ffmpeg.input(file)
    ffmpeg_inputs.append(ffmpeg_input['v'])
    ffmpeg_inputs.append(ffmpeg_input['a'])

    #probe = ffmpeg.probe(file)
    #video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    #pprint(video_stream['tags']['creation_time'])

#video_count = len(file_list)

joined = ffmpeg.concat(*ffmpeg_inputs, v=1, a=1).node
v = joined[0]
a = joined[1]
out = ffmpeg.output(v, a, output_file)
#out = ffmpeg.output(joined, output_file)
#print(' '.join(ffmpeg.compile(out)))
out.run()