#!/bin/bash

#replace databases
psql -c 'alter database chembdb rename to chembdb_help;' chembdb_update
psql -c 'alter database chembdb_update rename to chembdb;' chembdb_help
psql -c 'alter database chembdb_help rename to chembdb_update;' chembdb

#deleting pictures of ligands
rm -rf ../web/static/web/inchi/{*,.*}

