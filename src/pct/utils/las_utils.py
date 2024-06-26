# PointCloud_Tiling, GPL-3.0 license

""" 
Laspy utility methods - Module (Python)

The module is adapted from:
https://github.com/Amsterdam-AI-Team/Urban_PointCloud_Processing
"""

import re
import os
import glob
import laspy
import pathlib

import pycc
import cccorelib

import numpy as np
from tqdm import tqdm

from ..utils.math_utils import get_octree_level

FILE_TYPES = ('.LAS', '.las', '.LAZ', '.laz')


def get_bbox_from_tile_code(tile_code, padding=0, width=50, height=50):
    """Get bbox for a given tilecode: ((x_min, y_max), (x_max, y_min))"""
    tile_split = tile_code.split('_')

    # The tile code of each tile is defined as
    # 'X-coordinaat/50'_'Y-coordinaat/50'
    x_min = int(tile_split[0]) * 50
    y_min = int(tile_split[1]) * 50

    return ((x_min - padding, y_min + height + padding),
            (x_min + height + padding, y_min - padding))


def get_tilecode_from_filename(filename):
    """Extract the tile code from a file name."""
    return re.match(r'.*(\d{4}_\d{4}).*', filename)[1]


def get_tilecodes_from_folder(las_folder, las_prefix='', extension='.laz'):
    """Get a set of unique tilecodes for the LAS files in a given folder."""
    files = pathlib.Path(las_folder).glob(f'{las_prefix}*{extension}')
    tilecodes = set([get_tilecode_from_filename(file.name) for file in files])
    return tilecodes


def tile_las_file(in_file, out_folder, prefix='', tile_size=50, points_per_iter=40_000_000):
    """Processes a single LAS file to generate multiple tiled LAS files based on specified tile dimensions.

    This function opens a LAS file and partitions its point cloud data into smaller, geospatially defined
    tiles. It saves each tile as a new LAS file in the specified output folder. The tiling is based on 
    a grid defined by `tile_size`, with the number of points processed per iteration controlled by
    `points_per_iter`. This allows handling of large point clouds efficiently.

    Args:
        in_file: The path to the input LAS file.
        out_folder: The directory where the tiled LAS files will be saved.
        prefix: An optional prefix for the output file names. Defaults to an empty string.
        tile_size: The size of each spatial tile, in the same units as the point coordinates. Defaults to 50.
        points_per_iter: The maximum number of points to process in each iteration. Defaults to 40,000,000.

    Raises:
        FileNotFoundError: If the input LAS file does not exist.
        Exception: If there is an error during the reading or writing of LAS files.

    """
    
    if not os.path.isdir(out_folder):
        pathlib.Path(out_folder).mkdir(parents=True, exist_ok=True)
    
    with laspy.open(in_file) as in_las:
        x_bins = np.arange(in_las.header.x_min//tile_size - 1, 2 + in_las.header.x_max//tile_size, dtype=int) * tile_size
        y_bins = np.arange(in_las.header.y_min//tile_size - 1, 2 + in_las.header.y_max//tile_size, dtype=int) * tile_size
        
        with tqdm(total=in_las.header.point_count//points_per_iter + 1, leave=False) as pbar: 
            
            for points in in_las.chunk_iterator(points_per_iter):
                tile_codes = np.vstack([np.digitize(points.x, x_bins), np.digitize(points.y, y_bins)]).T - 1
                for x_ in range(len(x_bins)):
                    xm_ = np.where(tile_codes[:,0] == x_)[0]
                    for y_ in np.unique(tile_codes[xm_,1]):
                        if y_ in range(len(y_bins)):
                            
                            clip_idx = xm_[tile_codes[xm_,1] == y_]
                            
                            if len(clip_idx) > 0:
                                tile_code = f"{int(x_bins[x_]//tile_size)}_{int(y_bins[y_]//tile_size)}"
                                tile_points = points[clip_idx]
                                output_path = pathlib.Path(out_folder) / f"{prefix}{tile_code}.laz"
                                
                                # write or append
                                if not output_path.is_file():
                                    with laspy.open(output_path, mode="w", header=in_las.header) as out_las:
                                        out_las.write_points(tile_points)
                                else:
                                    with laspy.open(output_path, mode="a") as out_las:
                                        tile_points.change_scaling(offsets=out_las.header.offsets)
                                        out_las.append_points(tile_points)
                pbar.update()
  
                                    
def tile_las_folder(in_folder, out_folder, out_prefix='filtered_', glob_pattern='**/*.laz',
                    points_per_iter=40_000_000, tile_size=50):
    """Tiles all LAS files within a specified directory based on the given tiling parameters.

    This function scans a directory for LAS files matching a specific pattern, then processes each file
    to generate smaller, tiled LAS files. Each output file contains a subset of points from the original,
    organized into tiles of specified size. It handles large files by iterating through points in manageable
    chunks.

    Args:
        in_folder: The path to the input directory containing LAS files.
        out_folder: The path to the output directory where tiled LAS files will be saved.
        out_prefix: A prefix to append to the names of the output files. Defaults to 'filtered_'.
        glob_pattern: The pattern used to find LAS files in the input directory. Defaults to '**/*.laz'.
        points_per_iter: The number of points to process in each iteration. Defaults to 40,000,000.
        tile_size: The size of each tile, in units consistent with the LAS file coordinates. Defaults to 50.

    Raises:
        Exception: If an error occurs during the tiling process for any file.

    """
    
    # Create out_folder
    if not os.path.isdir(out_folder):
        pathlib.Path(out_folder).mkdir(parents=True, exist_ok=True)
    
    files = [file for file in pathlib.Path(in_folder).glob(glob_pattern)]
    print(f'Tiling Folder. Found {len(files)} files.')
    
    for in_file in tqdm(files, unit="file"):
        try:
            tile_las_file(in_file, out_folder, out_prefix, tile_size=tile_size, points_per_iter=points_per_iter)
        except Exception as e:
            print(f"Failed to tile file: {in_file.name}")
            print(e)


def subsample_las_file(in_file, out_file, grid_size=0.01):
    """Subsamples a LAS file to reduce the number of points based on a specified grid size.

    This function reads a LAS file, extracts the points, and applies a subsampling process using an octree structure. The subsampling aims to reduce the point cloud density by selecting the nearest point to the cell center within each grid cell defined by the specified grid size. The output is a new LAS file with the subsampled point cloud.

    Args:
        in_file: The path to the input LAS file that will be subsampled.
        out_file: The path where the subsampled LAS file will be saved.
        grid_size: The size of the grid cell used in the subsampling process. Defaults to 0.01.

    Raises:
        AssertionError: If there is a mismatch between the points array and the points in the point cloud after creation.
        Exception: If there are issues during the reading, processing, or writing of the LAS files.

    """
        
    las = laspy.read(in_file)

    xs = np.asarray(las.x - las.header.x_min).astype(pycc.PointCoordinateType)
    ys = np.asarray(las.y - las.header.y_min).astype(pycc.PointCoordinateType)
    zs = np.asarray(las.z - las.header.z_min).astype(pycc.PointCoordinateType)
    pc = pycc.ccPointCloud(xs, ys, zs)

    assert np.all(xs == pc.points()[..., 0])

    # Or give the values directly
    idx1 = pc.addScalarField("intensity", las.intensity)
    idx2 = pc.addScalarField("red", las.red)
    idx3 = pc.addScalarField("green", las.green)
    idx4 = pc.addScalarField("blue", las.blue)

    # Subsample 
    octree_level = get_octree_level(las.xyz, grid_size)
    submethod = cccorelib.CloudSamplingTools.NEAREST_POINT_TO_CELL_CENTER
    refCloud = cccorelib.CloudSamplingTools.subsampleCloudWithOctreeAtLevel(pc, octree_level, submethod)
    sampledPc = pc.partialClone(refCloud)

    # Export
    header = laspy.LasHeader(point_format=las.header.point_format, version=las.header.version)
    header.offset = las.header.offset
    header.scales = las.header.scale

    out_las = laspy.LasData(header)
    out_las.xyz = (sampledPc.points().astype(np.float64) + las.header.mins)
    out_las.intensity = sampledPc.getScalarField(idx1).asArray()
    out_las.red = sampledPc.getScalarField(idx2).asArray()
    out_las.green = sampledPc.getScalarField(idx3).asArray()
    out_las.blue = sampledPc.getScalarField(idx4).asArray()

    # 3. Export
    out_las.write(out_file)


def subsample_las_folder(in_folder, out_folder=None, out_prefix='filtered_', grid_size=0.01, resume=False, 
                         min_points=2_000_000):
    
    
    file_types = ('.LAS', '.las', '.LAZ', '.laz') # valid pointcloud file types
    
    if out_folder and not os.path.isdir(out_folder):
        pathlib.Path(out_folder).mkdir(parents=True, exist_ok=True)
        
    files = [f for f in glob.glob(os.path.join(in_folder, '*'))
            if f.endswith(file_types)]
    
    # Find which files have already been processed.
    if resume:
        done = set([get_tilecode_from_filename(file.name) for file
                    in pathlib.Path(out_folder).glob('*.laz')])
        files = [f for f in files if get_tilecode_from_filename(f) not in done]
    
    
    def get_points_in_file(file):
        with laspy.open(file, 'r') as las:
            file_points = las.header.point_count
        return file_points
        
    if min_points is not None:
        files = [f for f in files if get_points_in_file(f) > min_points]

    print(f"Subsampling {len(files)} files.")

    for in_file in tqdm(files, unit="file"):
        try:
            if out_folder is None:
                out_file = in_file
            else:
                tilecode = get_tilecode_from_filename(in_file)
                out_file = os.path.join(out_folder, out_prefix + tilecode + ".laz")
            subsample_las_file(in_file, out_file, grid_size)
        except:
            print(f"Failed to subsample file: {in_file.name}")