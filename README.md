# BDRC in TerminusDB

This repository contains programs and schema for porting BDRC to TerminusDB.

## Install TerminusDB command line

The best way to do this is to install the
[snap](https://snapcraft.io/terminusdb) if on linux. If you're not on
linux you will have to make do with the
[bootstrap](https://github.com/terminusdb/terminusdb-bootstrap) which
lives in a docker file. The terminusdb command lines will have to be
slightly altered if using the docker (SEE BELOW).

### Bootstrap instructions...

Follow the directions in the bootstrap page for installation. In these
scripts if using the bootstrap, uses of `terminusdb` should be
replaced with `./terminusdb-container cli`.

## Add BDRC database to local storage

We need to create the terminusdb storage. You should run this command
in the folder you intend to keep the local storage.

`terminusdb db create admin/bdrc --schema=false`

We create it without schema checking, because BDRC has elements which
we do not want to check for referential integrity. We can still impose
a schema to allow us to recover and insert documents, but we will not
be checking referential integrity when we do this.

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

After setting the appropriate paths etc. you can run the import with: 

```shell
python3 load-files.py
```

It will now report some information regarding import.

NOTE: TerminusDB does not currently support EDTF. We will have to come
up with a solution for dealing with EDTF.

## Schema Import

Now we can import the schema, so that we can view the documents

`cat bdrc-schema.json | terminusdb doc insert -f -g schema admin/bdrc`

## View Documents

The documents can now be viewed in the document explorer. We can start
up a terminusdb server (in the same directory as the local storage) as
follows:

```shell
terminusdb serve
```
Now open a browser and go to `http://127.0.0.1:6363`

## Sharing

We can share the data with others by setting a remote. TerminusX will
allow you to have several data products as a remote for free, but BDRC
has a special agreement for hosting large datasets.

First, make an account on TerminusX. Then create a team in which you
will share data products. Now create a data product. You could call it
`bdrc`. Navigate to the main data product overview. On the side panel
there will be a clone address. Copy this address, it should look
something like:

```
https://cloud.terminusdb.com/TerminatorsX/TerminatorsX/bdrc
```

Now we can add that URL as a remote to our repository:

```shell
terminusdb remote add admin/bdrc origin 'https://cloud.terminusdb.com/TerminatorsX/TerminatorsX/bdrc'
```

We need to get a machine access token from TerminusX as well, so we
can authenticate our communications. Go to TerminusX and obtain a new
machine access token from the profile page. Copy this key and put it
in a file called `~/.bdrc-access-key`.


First we fetch the (*empty*) repository to our local storage.

```shell
terminusdb fetch admin/bdrc --token=$(cat ~/.bdrc-access-key)
```

Now we can push to the remote...

```shell
terminusdb push admin/bdrc --token=$(cat ~/.bdrc-access-key)
```

We will now have a copy of the database in TerminusX that others can
clone and begin work on.

