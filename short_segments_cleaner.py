#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: short_segments_cleaner.py
Author: Sylvain Décastel
Version: 1.0
Contact: s.decastel@gmail.com
License: GNU General Public License v3

Description: This script takes one gcode file in parameter and will parse the content to detect and filter the
unnecessary short segments to smoothen the result on the 3D printing FDM machine.
"""

import argparse
import os
import math


def parse_gcode_line(line):
    """
    Parse the G1 gcode line and detect the lines with X Y movements

    :param line: Input line of a gcode file
    :return: (is_valid, x ,y), is_valid : True if the line contains the X Y coordinate. x,y the coordinates.
    """
    is_valid = False
    x = 0.0
    y = 0.0

    tokens = line.strip().split()

    # Check if it's a G1 command
    if len(tokens) >= 3 and tokens[0] == 'G1':
        for token in tokens[1:]:
            # Extract X, Y, and Z coordinates if present
            if token.startswith('X'):
                x = float(token[1:])
            elif token.startswith('Y'):
                y = float(token[1:])

    if x != 0.0 and y != 0.0:
        is_valid = True

    return is_valid, x, y


def parse_gcode_file(input_file, out_file, thresh):
    """
    Parse the content of the gcode file, detect the small segments and write the filtered content in the
     output file.

    :param input_file: Input gcode file
    :param out_file: Output gcode file
    :param thresh: Threshold to detect the short segments
    :return: Number of detect short segments
    """

    last_x = 0.0
    last_y = 0.0
    cnt = 0

    f_o = open(out_file, 'w')

    # Read the G-code file
    with open(input_file, 'r') as f:
        for line in f:

            valid, x, y = parse_gcode_line(line)

            if valid:
                # calculate the distance from the last position
                x_mov = x - last_x
                y_mov = y - last_y
                mov = math.sqrt(x_mov ** 2 + y_mov ** 2)

                # detect the short segments
                if mov < thresh:
                    # add ; in the beginning of the line to comment it
                    line = ";" + line
                    cnt += 1

            # update the last position variables
            last_x = x
            last_y = y

            # write the line to the output file
            f_o.write(line)

    f.close()
    f_o.close()

    return cnt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse G-code and calculate X and Y movement")
    parser.add_argument("-i", "--input", required=True, help="Path to G-code input file")
    parser.add_argument("-t", "--threshold", default="0.08", help="Threshold to filter out the movement,"
                                                                  " default=0.08")
    args = parser.parse_args()

    output_file = os.path.splitext(args.input)[0] + "-fixed.gcode"

    threshold = float(args.threshold)

    count = parse_gcode_file(args.input, output_file, threshold)

    print(f"Nb of detected short segments : {count}")
