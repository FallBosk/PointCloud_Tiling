#!/usr/bin/python

# PointCloud_Tiling, GPL-3.0 license
# command: python subsample.py --in_folder '..' [--out_folder '..']

# Helper script to allow importing from parent folder.
import set_path  # noqa: F401

import os
import sys
import argparse
from pathlib import Path

from pct.utils.las_utils import subsample_las_folder

MIN_FILE_SIZE = 1 # threshold for deleting small tiles

if __name__ == '__main__':
    global args

    desc_str = '''This script preprocesses a dataset.'''
    parser = argparse.ArgumentParser(description=desc_str)
    parser.add_argument('--in_folder', metavar='path', action='store',
                        type=str, required=True)
    parser.add_argument('--out_folder', metavar='path', action='store',
                        type=str)
    parser.add_argument('--grid_size', type=float, default=0.01)
    parser.add_argument('--out_prefix', type=str, default="filtered_")
    args = parser.parse_args()
    
    if not os.path.isdir(args.in_folder):
        print('The input path does not exist')
        sys.exit()
    
    if args.out_folder and not os.path.isdir(args.out_folder):
        Path(args.out_folder).mkdir(parents=True, exist_ok=True)
    
    subsample_las_folder(args.in_folder, args.out_folder, out_prefix=args.out_prefix,
                         grid_size=args.grid_size)
    
    print("Done. Exit.")