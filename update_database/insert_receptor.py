
import rdkit.Chem.inchi as inchi
import rdkit.Chem.rdmolops as rdmolops
import rdkit.Chem as chem
import molvs
from molvs import Standardizer
from pprint import pprint
import psycopg2
import sys
import re
import csv
from io import StringIO
chem.WrapLogs()
#sio = sys.stderr = StringIO()
import logging
#reload(logging)
logging.basicConfig(filename='logging.log', level=logging.DEBUG, format="[%(asctime)s %(levelname)-8s] %(message)s", datefmt="%Y/%b/%d %H:%M:%S")
from standardiser import standardise
s = Standardizer()

from rdkit import RDLogger
lg = RDLogger.logger()
lg.setLevel(RDLogger.ERROR)

dictionary = ["C", "H", "O", "N", "S", "P", "F", "Cl", "Br", "I"]






with open('receptors.csv', 'r', encoding='utf-8') as receptor:
	reader = csv.reader(receptor, delimiter=',', )
	final = list(reader)

#pprint (final)
final[0][0] = '1'
#pprint (final)

for line in final:
	statement = 'insert into receptor values (' + str(line[0]) + ', \''  + str(line[1]) + '\', \'' + str(line[2]) + '\', \'' + str(line[3]) + '\', \'' + str(line[4]) + '\', \'' + str(line[5]) + '\', \'' + str(line[6]) + '\', \'' + str(line[7]) + '\');'
	#print (statement)
	conn = psycopg2.connect('dbname=chembdb_update user=data host=/tmp/')
	curs = conn.cursor()
	curs.execute(statement)
	conn.commit()

