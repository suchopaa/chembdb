#!/bin/sh
conda activate my-rdkit-env

#!!!!!!!!!!write names of databases WITHOUT type of file (so "chembl.tar.gz" will be "chembl" only)
CHEMBL="NAME_OF_CHEMBL"
BDB="NAME_OF_BINDING_DB"
#!!!!!!!!!!



#unzipping and running dump of chembl
tar -xf $CHEMBL".tar.gz"
CHEM=${CHEMBL%_postgresql} 
CHEMBL_PATH="./"$CHEM"/"$CHEMBL"/"$CHEMBL".dmp"
pg_restore -c -d chembl $CHEMBL_PATH
rm -r $CHEM

#unzipping and creating BindingDB database
unzip $BDB".tsv.zip"
mv $BDB".tsv" BindingDB_All.tsv
python BDB_base_create_script.py
python BDB_extend_create_script.py
python BDB_all_insert_script.py
rm BindingDB_All.tsv

#making ChemBDB database
psql -U data -d chembdb_update -f create_script.sql
python insert_ligand.py
python insert_receptor.py
python insert_source.py
python insert_activity.py
psql -U data -d chembdb_update -f similarity_script.sql



