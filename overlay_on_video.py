#!/usr/bin/python3

import sys
import csv
import ffmpeg
import argparse
from pprint import pprint
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from datetime import datetime
from datetime import timedelta

pprint( sys.getrecursionlimit())
sys.setrecursionlimit(30000)
parser = argparse.ArgumentParser(description='script to combine video files into 1 file')
parser.add_argument('-i', dest='input', help='video files to combine.', nargs='*')
parser.add_argument('-o', dest='output', help='file to output the new video to.')
parser.add_argument('-csv', dest='csv', help='CSV file to gather overlay data.')

args = parser.parse_args()
output_file = args.output
file_list = args.input
csv_file = args.csv

ffmpeg_inputs = list()
video_time = dict()

first_time = None
last_time = None

for file in file_list:
    ffmpeg_input = ffmpeg.input(file)
    ffmpeg_inputs.append(ffmpeg_input['v'])
    ffmpeg_inputs.append(ffmpeg_input['a'])

    probe = ffmpeg.probe(file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    creation_time = datetime.strptime(video_stream['tags']['creation_time'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(seconds=280)
    end_time = creation_time + timedelta(seconds=int(float(video_stream['duration'] ))) + timedelta(seconds=280)
    video_time[file] = {'creation_time': creation_time, 'end_time': end_time}

    if not first_time or creation_time < first_time:
        first_time = creation_time
    if not last_time or end_time > last_time:
        last_time = end_time

concated = ffmpeg.concat(*ffmpeg_inputs, v=1, a=1)
joined = concated.node
v = joined[0]
#v= joined[0].overlay(import_image, x=500, y=500, enable='between(t,0,20)')

#data = list()
#with open(csv_file) as f:
#    reader = csv.DictReader(f)
#    data = [r for r in reader]

def parser_func(x):
    return datetime.strptime(x, '%d-%b-%Y %H:%M:%S.%f')

series = read_csv(csv_file, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser_func)

resample = series.resample('S')
secondly_mean_values = resample.mean()
dataset = secondly_mean_values.to_dict()
#secondly_mean_values.plot()
#pyplot.show()

processing_time = 0
for time, speed in dataset['Speed (OBD)(mph)'].iteritems():
    if time > first_time and time < last_time:
        pprint(speed)
        v = v.drawtext(text=speed, fontsize=100, enable='between(t,' + str(int(float(processing_time))) + ',' + str(int(float(processing_time + 1))) + ')')
        processing_time += 1


a = joined[1]
out = ffmpeg.output(v, a, output_file, vcodec="h264_nvenc", preset="default",
                    pixel_format="yuva444p", video_bitrate="30M",  bufsize="30M")
#print(' '.join(out.compile()))
out.run()