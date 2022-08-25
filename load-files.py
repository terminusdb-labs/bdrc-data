#!/usr/bin/env python3
import os
import subprocess
import random

INSTANCE_DIR='/home/gavin/dev/bdrc/instances'
WORKS_DIR='/home/gavin/dev/bdrc/works'

print(random.randint(0,9))


def optimize():
    if random.randint(0,9) == 0:
        print(f"        optimizing...")
        subprocess.run(["terminusdb","optimize","admin/bdrc"])
        subprocess.run(["terminusdb","optimize","admin/bdrc/_meta"])
        subprocess.run(["terminusdb","optimize","admin/bdrc/local/_commits"])

RESTART_AFTER = ['/home/gavin/dev/bdrc/instances','43'] # set to [] to process everything
RESTART_SEEN = False # set to True to process everything
Dirs = [INSTANCE_DIR,WORKS_DIR]
for Dir in Dirs:
    print(f"Loading {Dir}")
    for hash_dir in os.listdir(Dir):
        print(f"  hash_dir: {hash_dir}")
        print(f"{[Dirs,hash_dir]}")
        if len(RESTART_AFTER) > 0 and [Dir,hash_dir] == RESTART_AFTER:
            RESTART_SEEN = True
            continue
        elif RESTART_SEEN == True:
            for filename in os.listdir(f"{Dir}/{hash_dir}"):
                if filename.endswith(".trig"):
                    optimize()
                    print(f"    processing {filename}")
                    p = subprocess.run(["terminusdb", "triples", "load", "admin/bdrc/local/branch/main/instance", f"{Dir}/{hash_dir}/{filename}"])
