
import rdkit.Chem.inchi as inchi
import rdkit.Chem.rdmolops as rdmolops
import rdkit.Chem as chem
import molvs
from molvs import Standardizer
from pprint import pprint
import psycopg2
import sys
import re
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

chembl_new = []
chembl_help = []
conn2 = psycopg2.connect('dbname=chembl user=data host=/tmp/')
curs2 = conn2.cursor()
curs2.execute("select doi, pubmed_id, patent_id, authors, journal from (((((target_dictionary T INNER JOIN target_components TC on T.tid = TC.tid) INNER JOIN component_sequences CSEQ on TC.component_id = CSEQ.component_id) INNER JOIN assays A on T.tid = A.tid) INNER JOIN activities AC on A.assay_ID = AC.assay_ID) INNER JOIN docs D on AC.doc_id = D.doc_id) INNER JOIN compound_structures CS on AC.molregno = CS.molregno where CSEQ.accession IN ('P10827', 'P10828', 'P10276', 'P10826', 'P13631', 'Q07869', 'Q03181', 'P37231', 'P20393', 'Q14995', 'P35398', 'Q92753', 'P51449', 'P55055', 'Q13133', 'Q96RI1', 'P11473', 'O75469', 'Q14994', 'P41235', 'Q14541', 'P19793', 'P28702', 'P48443', 'P13056', 'P49116', 'Q9Y466', 'Q9Y5X4', 'P10589', 'P24468', 'P10588', 'P03372', 'Q92731', 'P11474', 'O95718', 'P62508', 'P04150', 'P08235', 'P06401', 'P10275', 'P22736', 'P43354', 'Q92570', 'Q13285', 'O00482', 'Q15406', 'P51843', 'Q15466');")
chembl = curs2.fetchall()

#pprint (len(chembl))

i = 0
while i < len(chembl):
	delete = False
	for lig in chembl_help:
		if chembl[i][0] == lig[0]:
			delete = True
	if delete == True:
		i = i + 1
		continue
	chembl_help.append(chembl[i])
	i = i + 1

#pprint (len(chembl_help))



bdb_help = []
list_help = []
conn = psycopg2.connect('dbname=bdb user=data host=/tmp/')
curs = conn.cursor()
curs.execute("select bdb_17_article_doi, bdb_18_pmid, bdb_19_pubchem_aid, bdb_20_patent_number, bdb_21_authors, bdb_22_institution from bdb_base B FULL OUTER JOIN bdb_extend E ON B.bdb_0_bindingdb_reactant_set_id = E.bdb_0_bindingdb_reactant_set_id where bdb_40_uniprot__swissprot__entry_name_of_target_chain IN ('THA_HUMAN', 'THB_HUMAN', 'RARA_HUMAN', 'RARB_HUMAN', 'RARG_HUMAN', 'PPARA_HUMAN', 'PPARD_HUMAN', 'PPARG_HUMAN', 'NR1D1_HUMAN', 'NR1D2_HUMAN', 'RORA_HUMAN', 'RORB_HUMAN', 'RORG_HUMAN', 'NR1H2_HUMAN', 'NR1H3_HUMAN', 'NR1H4_HUMAN', 'VDR_HUMAN', 'NR1I2_HUMAN', 'NR1I3_HUMAN', 'HNF4A_HUMAN', 'HNF4G_HUMAN', 'RXRA_HUMAN', 'RXRB_HUMAN', 'RXRG_HUMAN', 'NR2C1_HUMAN', 'NR2C2_HUMAN', 'NR2E1_HUMAN', 'NR2E3_HUMAN', 'COT1_HUMAN', 'COT2_HUMAN', 'NR2F6_HUMAN', 'ESR1_HUMAN', 'ESR2_HUMAN', 'ERR1_HUMAN', 'ERR2_HUMAN', 'ERR3_HUMAN', 'GCR_HUMAN', 'MCR_HUMAN', 'PRGR_HUMAN', 'ANDR_HUMAN', 'NR4A1_HUMAN', 'NR4A2_HUMAN', 'NR4A3_HUMAN', 'STF1_HUMAN', 'NR5A2_HUMAN', 'NR6A1_HUMAN', 'NR0B1_HUMAN', 'NR0B2_HUMAN') OR bdb_41_uniprot__swissprot__primary_id_of_target_chain IN ('P10827', 'P10828', 'P10276', 'P10826', 'P13631', 'Q07869', 'Q03181', 'P37231', 'P20393', 'Q14995', 'P35398', 'Q92753', 'P51449', 'P55055', 'Q13133', 'Q96RI1', 'P11473', 'O75469', 'Q14994', 'P41235', 'Q14541', 'P19793', 'P28702', 'P48443', 'P13056', 'P49116', 'Q9Y466', 'Q9Y5X4', 'P10589', 'P24468', 'P10588', 'P03372', 'Q92731', 'P11474', 'O95718', 'P62508', 'P04150', 'P08235', 'P06401', 'P10275', 'P22736', 'P43354', 'Q92570', 'Q13285', 'O00482', 'Q15406', 'P51843', 'Q15466');")
bdb = curs.fetchall()

#pprint (bdb)
#pprint (len(bdb))

i = 0
while i < len(bdb):
	delete = False
	for lig in bdb_help:
		if bdb[i][0] == lig[0]:
			delete = True
	if delete == True:
		i = i + 1
		continue
	bdb_help.append(bdb[i])
	i = i + 1

#pprint (len(bdb_help))

#test of lenght
bdb_tester = []
for k in bdb_help:
	bdb_tester.append(k[0])

chembl_tester = []
for l in chembl_help:
	chembl_tester.append(l[0])

#pprint (len(set(chembl_tester) | set(bdb_tester)))


#making final
final = []
i = 0
counter = 0
bdb_counter = 0
while i < 1:
	#existing in chembl
	help = []
	help.append(counter)
	chembl_counter = 0
	exister = 0
	if (len(bdb_help)!=0) & (len(chembl_help)!=0):
		for j in chembl_help:
			if bdb_help[0][0] == j[0]:
				exister = 1
				break
			chembl_counter = chembl_counter + 1



	#if in chembl
	if (exister == 1) & (len(bdb_help)!=0):
		if bdb_help[0][0] != '':
			help.append(bdb_help[0][0])
		else:
			help.append('Unknown doi')
		if bdb_help[0][1] == '':
			if (chembl_help[chembl_counter][1] != '') and (chembl_help[chembl_counter][1] != 'None') and (chembl_help[chembl_counter][1] != None):
				help.append(chembl_help[chembl_counter][1])
			else: 
				help.append('0')
		else:
			help.append(bdb_help[0][1])
		if bdb_help[0][2] != '':
			help.append(bdb_help[0][2])
		else:
			help.append("Unknown")
		if bdb_help[0][3] == '':
			help.append(chembl_help[chembl_counter][2])
		else:
			help.append(bdb_help[0][3])
		if bdb_help[0][4] == '':
			authors = chembl_help[chembl_counter][3]
		else:
			authors = bdb_help[0][4]
		if authors != '' and authors != None:
			authors = authors.replace("'", '')
		else:
			authors = "Unknown"
		help.append(authors)
		if bdb_help[0][5] == '':
			help.append(chembl_help[chembl_counter][4])
		else:
			help.append(bdb_help[0][5])
		bdb_help.remove(bdb_help[0])
		chembl_help.remove(chembl_help[chembl_counter])
	elif (exister == 0) & (len(bdb_help)!=0):
		if bdb_help[0][0] != '':
			help.append(bdb_help[0][0])
		else:
			help.append('Unknown doi')
		if (bdb_help[0][1] == '') or (bdb_help[0][1] == 'None') or (bdb_help[0][1] == None):
			help.append('0')
		else:
			help.append(bdb_help[0][1])
		if bdb_help[0][2] != '':
			help.append(bdb_help[0][2])
		else:
			help.append('Unknown')
		help.append(bdb_help[0][3])
		authors = bdb_help[0][4]
		if authors != '' and authors != None:
			authors = authors.replace("'", '')
		else:
			authors = "Unknown"
		help.append(authors)
		help.append(bdb_help[0][5])
		bdb_help.remove(bdb_help[0])

	#rest of chembl
	elif len(chembl_help) != 0:
		if chembl_help[0][0] != '':
			help.append(chembl_help[0][0])
		else:
			help.append('Unknown doi')
		if (chembl_help[0][1] != '') and (chembl_help[0][1] != 'None') and (chembl_help[0][1] != None):
			help.append(chembl_help[0][1])
		else:
			help.append('0')
		help.append('Unknown')
		help.append(chembl_help[0][2])
		authors = chembl_help[0][3]
		if authors != '' and authors != None:
			authors = authors.replace("'", '')
		else:
			authors = "Unknown"
		help.append(authors)
		help.append(chembl_help[0][4])
		chembl_help.remove(chembl_help[0])

	#pprint (help)
	final.append(help)
	#pprint (final)
	del help
	if (len(chembl_help)==0) & (len(bdb_help)==0):
		i = 2
	counter = counter + 1

#pprint (final)

for line in final:
	for x in range(7):
		if '\'' in str(line[x]):
			line[x] = line[x].replace('\'','')
	statement = 'insert into source values (' + str(line[0]) + ', \''  + str(line[1]) + '\', ' + str(line[2]) + ', \'' + str(line[3]) + '\', \'' + str(line[4]) + '\', \'' + str(line[5]) + '\', \'' + str(line[6]) + '\');'
	#print (statement)
	conn3 = psycopg2.connect('dbname=chembdb_update user=data host=/tmp/')
	curs3 = conn3.cursor()
	curs3.execute(statement)
	conn3.commit()

