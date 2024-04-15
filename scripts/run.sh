#!/bin/bash

# This was from last time, to select a blob?
sudo blobfuse /home/azureuser/cloudfiles/code/blobfuse/ovl --tmp-path=/mnt/resource/blobfusetmp --config-file=/home/azureuser/cloudfiles/code/blobfuse/fuse_connection_ovl.cfg -o attr_timeout=3600 -o entry_timeout=3600 -o negative_timeout=3600 -o allow_other -o nonempty

# this is to run the scritp, what has to be specified:
# --in_folder (folder containing all files to tile, can contain subfolders)
# --out_folder (path where to write files to)
# --points_per_iter (number of points to process per iteration, (~40mln per GB RAM))

python3 pipeline.py --in_folder "/home/azureuser/path/to/files/" --out_folder "/home/azureuser/path/to/output/" --points_per_iter 50000000 --delete_small