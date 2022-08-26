# BDRC in TerminusDB

This repository contains programs and schema for porting BDRC to TerminusDB.

## Install TerminusDB command line

The best way to do this is to install the [snap]() if on linux. If you're
not on linux you will have to make do with the bootstrap.

## Process of Import

The file `load-files.py` is a python script which uses the BDRC
repositories to load the data into TerminusDB.

First, we clone the relevant BDRC repositories.

```shell
mkdir bdrc-data
cd bdrc-data
git clone git@gitlab.com:bdrc-data/instances
git clone git@gitlab.com:bdrc-data/works
```

Now, we edit the `load-files.py` to contain the correct path
information for loading.

```python
INSTANCE_DIR='/home/gavin/dev/bdrc/instances'
WORKS_DIR='/home/gavin/dev/bdrc/works'
```

In order to restart the process which takes a *long* time, it's nice
to start over where you left off. Just put in the last completed hash
directory and repository.

```python
RESTART_AFTER = ['/home/gavin/dev/bdrc/instances','90'] # set to [] to process everything
```

### Once we have imported we can load a (partial) schema
terminusdb 
