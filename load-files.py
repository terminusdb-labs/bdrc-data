#!/usr/bin/env python3
import os
import subprocess

INSTANCE_DIR='/home/gavin/dev/bdrc/instances'
WORKS_DIR='/home/gavin/dev/bdrc/works'

Dirs = [INSTANCE_DIR,WORKS_DIR]
for Dir in Dirs:
    print(f"Loading {Dir}")
    for hash_dir in os.listdir(Dir):
        print(f"  hash_dir: {hash_dir}")
        for filename in os.listdir(f"{Dir}/{hash_dir}"):
            if filename.endswith(".trig"):
                print(f"    processing {filename}")
                p = subprocess.run(["terminusdb", "triples", "load", "admin/bdrc/local/branch/main/instance", f"{Dir}/{hash_dir}/{filename}"])

