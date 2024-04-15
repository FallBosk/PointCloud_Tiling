#!/usr/bin/python
# command: python tile.py --in_folder '..' --out_folder '..'

# Helper script to allow importing from parent folder.
import set_path  # noqa: F401

import os
import sys
import argparse
from pathlib import Path

from pct.utils.las_utils import tile_las_folder

MIN_FILE_SIZE = 1 # threshold for deleting small tiles

if __name__ == '__main__':
    global args

    desc_str = '''This script tiles a point cloud.'''
    parser = argparse.ArgumentParser(description=desc_str)
    parser.add_argument('--in_folder', metavar='path', action='store',
                        type=str, required=True)
    parser.add_argument('--out_folder', metavar='path', action='store',
                        type=str, required=True)
    parser.add_argument('--out_prefix', type=str, default="filtered_")
    parser.add_argument('--tile_size', type=int, default=50)
    parser.add_argument('--points_per_iter', type=int, default=30_000_000)
    parser.add_argument('--delete_small', action='store_true')
    args = parser.parse_args()
    
    if not os.path.isdir(args.in_folder):
        print('The input path does not exist')
        sys.exit()
    
    if not os.path.isdir(args.out_folder):
        Path(args.out_folder).mkdir(parents=True, exist_ok=True)
    
    tile_las_folder(args.in_folder, args.out_folder, args.out_prefix,
                    points_per_iter=args.points_per_iter, tile_size=args.tile_size)
    
    print("Success.")
    
    if args.delete_small:
        print(f"Deleting small tiles less than {MIN_FILE_SIZE} MB..")
        for f in Path(args.out_folder).glob(f'{args.out_prefix}*.laz'):
            if os.stat(f).st_size / (1024 * 1024) < MIN_FILE_SIZE:
                f.unlink()
    
    print("Done. Exit.")