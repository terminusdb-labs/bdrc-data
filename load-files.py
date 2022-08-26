#!/usr/bin/env python3
import os
import subprocess
import random

INSTANCE_DIR='/home/gavin/dev/bdrc/instances'
WORKS_DIR='/home/gavin/dev/bdrc/works'

def optimize():
    if random.randint(0,9) == 0:
        print(f"        optimizing...")
        subprocess.run(["terminusdb","optimize","admin/bdrc"])
        subprocess.run(["terminusdb","optimize","admin/bdrc/_meta"])
        subprocess.run(["terminusdb","optimize","admin/bdrc/local/_commits"])

RESTART_AFTER = ['/home/gavin/dev/bdrc/instances','90'] # set to [] to process everything
RESTART_SEEN = False if len(RESTART_SEEN) > 0 else True
Dirs = [INSTANCE_DIR,WORKS_DIR]
for Dir in Dirs:
    print(f"Loading {Dir}")
    hash_dirs = os.listdir(Dir)
    for hash_dir in hash_dirs:
        print(f"  hash_dir: {hash_dir}")
        if (not RESTART_SEEN
            and len(RESTART_AFTER) == 2
            and Dirs.index(Dir) >= Dirs.index(RESTART_AFTER[0])
            and hash_dirs.index(hash_dir) >= hash_dirs.index(RESTART_AFTER[1])):
            RESTART_SEEN = True
            continue
        elif RESTART_SEEN == True:
            for filename in os.listdir(f"{Dir}/{hash_dir}"):
                if filename.endswith(".trig"):
                    optimize()
                    print(f"    processing {filename}")
                    CMD = ["terminusdb", "triples", "load", "admin/bdrc/local/branch/main/instance", f"{Dir}/{hash_dir}/{filename}"]
                    print(f"Running {CMD}")
                    p = subprocess.run(CMD)
        else:
            print(f"Skipping {Dir} and {hash_dir}")

