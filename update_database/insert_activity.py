
import rdkit.Chem.inchi as inchi
import rdkit.Chem.rdmolops as rdmolops
import rdkit.Chem as chem
import molvs
import math
from molvs import Standardizer
from pprint import pprint
import psycopg2
import sys
import re
from io import StringIO
from decimal import Decimal
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


#CHEMBL preparing
chembl = []
conn2 = psycopg2.connect('dbname=chembl user=data host=/tmp/')
curs2 = conn2.cursor()
curs2.execute("select doi, accession, standard_inchi, standard_type, standard_relation, standard_value, standard_units, pchembl_value, confidence_score from (((((target_dictionary T INNER JOIN target_components TC on T.tid = TC.tid) INNER JOIN component_sequences CSEQ on TC.component_id = CSEQ.component_id) INNER JOIN assays A on T.tid = A.tid) INNER JOIN activities AC on A.assay_ID = AC.assay_ID) INNER JOIN docs D on AC.doc_id = D.doc_id) INNER JOIN compound_structures CS on AC.molregno = CS.molregno where CSEQ.accession IN ('P10827', 'P10828', 'P10276', 'P10826', 'P13631', 'Q07869', 'Q03181', 'P37231', 'P20393', 'Q14995', 'P35398', 'Q92753', 'P51449', 'P55055', 'Q13133', 'Q96RI1', 'P11473', 'O75469', 'Q14994', 'P41235', 'Q14541', 'P19793', 'P28702', 'P48443', 'P13056', 'P49116', 'Q9Y466', 'Q9Y5X4', 'P10589', 'P24468', 'P10588', 'P03372', 'Q92731', 'P11474', 'O95718', 'P62508', 'P04150', 'P08235', 'P06401', 'P10275', 'P22736', 'P43354', 'Q92570', 'Q13285', 'O00482', 'Q15406', 'P51843', 'Q15466');")
chembl_help = curs2.fetchall()
i = 0
while i < len(chembl_help):
	#check if foreign keys from Chembl exist
	if chembl_help[i][0] == '' or chembl_help[i][1] == '' or chembl_help[i][2] == '':
		i = i + 1
		continue
	chembl.append(list(chembl_help[i]))
	i = i + 1






#BDB preparing
bdb = []
conn = psycopg2.connect('dbname=bdb user=data host=/tmp/')
curs = conn.cursor()
curs.execute("select bdb_17_article_doi,  bdb_41_uniprot__swissprot__primary_id_of_target_chain, bdb_2_ligand_inchi, bdb_8_ki__nm_, bdb_9_ic50__nm_, bdb_10_kd__nm_, bdb_11_ec50__nm_, bdb_12_kon__m_1_s_1_, bdb_13_koff__s_1_, bdb_14_ph, bdb_15_temp__c_, bdb_15_temp__c_, bdb_15_temp__c_, bdb_15_temp__c_ from bdb_base B FULL OUTER JOIN bdb_extend E ON B.bdb_0_bindingdb_reactant_set_id = E.bdb_0_bindingdb_reactant_set_id where bdb_40_uniprot__swissprot__entry_name_of_target_chain IN ('THA_HUMAN', 'THB_HUMAN', 'RARA_HUMAN', 'RARB_HUMAN', 'RARG_HUMAN', 'PPARA_HUMAN', 'PPARD_HUMAN', 'PPARG_HUMAN', 'NR1D1_HUMAN', 'NR1D2_HUMAN', 'RORA_HUMAN', 'RORB_HUMAN', 'RORG_HUMAN', 'NR1H2_HUMAN', 'NR1H3_HUMAN', 'NR1H4_HUMAN', 'VDR_HUMAN', 'NR1I2_HUMAN', 'NR1I3_HUMAN', 'HNF4A_HUMAN', 'HNF4G_HUMAN', 'RXRA_HUMAN', 'RXRB_HUMAN', 'RXRG_HUMAN', 'NR2C1_HUMAN', 'NR2C2_HUMAN', 'NR2E1_HUMAN', 'NR2E3_HUMAN', 'COT1_HUMAN', 'COT2_HUMAN', 'NR2F6_HUMAN', 'ESR1_HUMAN', 'ESR2_HUMAN', 'ERR1_HUMAN', 'ERR2_HUMAN', 'ERR3_HUMAN', 'GCR_HUMAN', 'MCR_HUMAN', 'PRGR_HUMAN', 'ANDR_HUMAN', 'NR4A1_HUMAN', 'NR4A2_HUMAN', 'NR4A3_HUMAN', 'STF1_HUMAN', 'NR5A2_HUMAN', 'NR6A1_HUMAN', 'NR0B1_HUMAN', 'NR0B2_HUMAN') OR bdb_41_uniprot__swissprot__primary_id_of_target_chain IN ('P10827', 'P10828', 'P10276', 'P10826', 'P13631', 'Q07869', 'Q03181', 'P37231', 'P20393', 'Q14995', 'P35398', 'Q92753', 'P51449', 'P55055', 'Q13133', 'Q96RI1', 'P11473', 'O75469', 'Q14994', 'P41235', 'Q14541', 'P19793', 'P28702', 'P48443', 'P13056', 'P49116', 'Q9Y466', 'Q9Y5X4', 'P10589', 'P24468', 'P10588', 'P03372', 'Q92731', 'P11474', 'O95718', 'P62508', 'P04150', 'P08235', 'P06401', 'P10275', 'P22736', 'P43354', 'Q92570', 'Q13285', 'O00482', 'Q15406', 'P51843', 'Q15466');")
bdb_help = curs.fetchall()
i = 0
while i < len(bdb_help):
	#check if foreign keys from BDB exist
	if bdb_help[i][0] == '' or bdb_help[i][1] == '' or bdb_help[i][2] == '':
		i = i + 1
		continue
	helper = 0
	numbers = []
	if bdb_help[i][3] != '':
		helper = helper + 1
		numbers.append(3)
	if bdb_help[i][4] != '':
		helper = helper + 1
		numbers.append(4)
	if bdb_help[i][5] != '':
		helper = helper + 1
		numbers.append(5)
	if bdb_help[i][6] != '':
		helper = helper + 1
		numbers.append(6)
	if bdb_help[i][7] != '':
		helper = helper + 1
		numbers.append(7)
	if bdb_help[i][8] != '':
		helper = helper + 1
		numbers.append(8)
	if helper > 1:
		m = 0
		while m < len(numbers):
			var = list(bdb_help[i])
			k = 1
			while k < len(numbers):
				var[numbers[k]] = ''
				k = k + 1
			bdb.append(var)
			numbers.append(numbers[0])
			del numbers[0]
			m = m + 1
	else:
		bdb.append(list(bdb_help[i]))
	i = i + 1

x = 0
while x < len(bdb):
	y = 0
	while y < len(bdb[x]):
		new = bdb[x][y].replace(" ", "")
		bdb[x][y] = new
		if (bdb[x][y] != '') and (y == 3 or y == 4 or y == 5 or y == 6 or y == 7 or y == 8):
			if "<" in bdb[x][y]:
				a = bdb[x][y].replace("<", "")
				bdb[x][y] = float(a)
				bdb[x][11] = "<"
			elif ">" in bdb[x][y]:
				a = bdb[x][y].replace(">", "")
				bdb[x][y] = float(a)
				bdb[x][11] = ">"
			else:
				bdb[x][y] = float(bdb[x][y])
				bdb[x][11] = "="
			if y == 3:
				bdb[x][12] = "Ki"
				bdb[x][13] = "nM"
			if y == 4:
				bdb[x][12] = "IC50"
				bdb[x][13] = "nM"
				bdb[x][3] = bdb[x][4]
				bdb[x][4] = ""
			if y == 5:
				bdb[x][12] = "Kd"
				bdb[x][13] = "nM"
				bdb[x][3] = bdb[x][5]
				bdb[x][5] = ""
			if y == 6:
				bdb[x][12] = "EC50"
				bdb[x][13] = "nM"
				bdb[x][3] = bdb[x][6]
				bdb[x][6] = ""
			if y == 7:
				bdb[x][12] = "kon"
				bdb[x][13] = "M-1 s-1"
				bdb[x][3] = bdb[x][7]
				bdb[x][7] = ""
			if y == 8:
				bdb[x][12] = "koff"
				bdb[x][13] = "s-1"
				bdb[x][3] = bdb[x][8]
				bdb[x][8] = ""
		y = y + 1
	x = x + 1	


#ChemBDB preparing
conn3 = psycopg2.connect('dbname=chembdb_update user=data host=/tmp/')


source = []
curs_source = conn3.cursor()
curs_source.execute("select source_id, article_doi from source;")
source_help = curs_source.fetchall()
i = 0
while i < len(source_help):
	source.append(list(source_help[i]))
	i = i + 1

ligand = []
curs_ligand = conn3.cursor()
curs_ligand.execute("select ligand_id, inchi_bdb, inchi_chembl from ligand;")
ligand_help = curs_ligand.fetchall()
i = 0
while i < len(ligand_help):
	ligand.append(list(ligand_help[i]))
	i = i + 1

receptor = []
curs_receptor = conn3.cursor()
curs_receptor.execute("select receptor_id, uniprot_id, uniprot_name, uniprot_short_name, chembl_number from receptor;")
receptor_help = curs_receptor.fetchall()
i = 0
while i < len(receptor_help):
	receptor.append(list(receptor_help[i]))
	i = i + 1



#replace Chembl
for line in chembl:
	for s in source:
		if s[1] == line[0]:
			line[0] = s[0]
	for l in ligand:
		if l[2] == line[2]:
			line[2] = l[0]
	for r in receptor:
		if r[1] == line[1]:
			line[1] = r[0]


#replace BDB
for line in bdb:
        for s in source:
                if s[1] == line[0]:
                        line[0] = s[0]
        for l in ligand:
                if l[1] == line[2]:
                        line[2] = l[0]
        for r in receptor:
                if r[1] == line[1]:
                        line[1] = r[0]

#pprint (chembl)


#making final
final = []
counter = 0
i = 0
while i < 1:
	#existing in chembl
	help = []
	help.append(counter)
	chembl_counter = 0
	exister = 0
	if (len(bdb)!=0) & (len(chembl)!=0):
		for j in chembl:
			if (bdb[0][0] == j[0]) and (bdb[0][1] == j[1]) and (bdb[0][2] == j[2]) and (bdb[0][3] == j[5]) and (bdb[0][12] == j[3]) and (bdb[0][11] == j[4]) and (bdb[0][13] == j[6]):
				exister = 1
				break
			chembl_counter = chembl_counter + 1
		#print (exister)	

#if in chembl
	if (exister == 1) & (len(bdb)!=0):
		if bdb[0][0] != None and str(bdb[0][0]) != '':
			help.append(bdb[0][0])
		else:
			help.append(-1)
		help.append(bdb[0][1])
		help.append(bdb[0][2])
		if bdb[0][12] != '':
			help.append(bdb[0][12])
		else:
			help.append("Unknown")
		if bdb[0][11] != '':
			help.append(bdb[0][11])
		else:
			help.append("---")
		if bdb[0][3] != None and str(bdb[0][3]) != '':
			help.append(bdb[0][3])
		else:
			help.append('NULL')
		if bdb[0][13] != '':
			help.append(bdb[0][13])
		else:
			help.append("Unknown")
		if chembl[chembl_counter][7] != None:
			help.append(float(chembl[chembl_counter][7]))
		else:
			help.append('NULL')
		if chembl[chembl_counter][8] != None and str(chembl[chembl_counter][8]) != '':
			help.append(chembl[chembl_counter][8])
		else:
			help.append('NULL')
		if bdb[0][9] != None and str(bdb[0][9]) != '':
			help.append(bdb[0][9])
		else:
			help.append('NULL')
		if bdb[0][10] != '':
			help.append(bdb[0][10])
		else:
			help.append("Unknown")
		help.append("Chembl, BDB")

		bdb.remove(bdb[0])
		chembl.remove(chembl[chembl_counter])
	
	elif (len(bdb)!=0):
		if bdb[0][0] != None and str(bdb[0][0]) != '':
			help.append(bdb[0][0])
		else:
			help.append(-1)
		help.append(bdb[0][1])
		help.append(bdb[0][2])
		if bdb[0][12] != '':
			help.append(bdb[0][12])
		else:
			help.append("Unknown")
		if bdb[0][11] != '':
			help.append(bdb[0][11])
		else:
			help.append("---")
		if bdb[0][3] != None and str(bdb[0][3]) != '':
			help.append(bdb[0][3])
		else:
			help.append('NULL')
		if bdb[0][13] != '':
			help.append(bdb[0][13])
		else:
			help.append("Unknown")
		if (bdb[0][3] != None) and (bdb[0][3] != 0) and (str(bdb[0][3]) != ''):
			#print ("a" + str(bdb[0][3]) + "a")
			help.append(-math.log(float(bdb[0][3]) * float(0.000000001), 10))
		else:
			help.append('NULL')
		help.append('NULL')
		if bdb[0][9] != None and str(bdb[0][9]) != '':
			help.append(bdb[0][9])
		else:
			help.append('NULL')
		if bdb[0][10] != '':
			help.append(bdb[0][10])
		else:
			help.append("Unknown")
		help.append("BDB")

		bdb.remove(bdb[0])
	
	elif (len(chembl)!=0):
		if chembl[0][0] != None and str(chembl[0][0]) != '':
			help.append(chembl[0][0])
		else:
			help.append(-1)
		help.append(chembl[0][1])
		help.append(chembl[0][2])
		if chembl[0][3] != '':
			help.append(chembl[0][3])
		else:
			help.append("Unknown")
		if chembl[0][4] != '':
			help.append(chembl[0][4])
		else:
			help.append("---")
		if chembl[0][5] != None and str(chembl[0][5]) != '':
			help.append(float(chembl[0][5]))
		else:
			help.append('NULL')
		if chembl[0][6] != '':
			help.append(chembl[0][6])
		else:
			help.append("Unknown")
		if chembl[0][7] != None:
			help.append(float(chembl[0][7]))
		else:
			help.append('NULL')
		if chembl[0][8] != None or  str(chembl[0][8]) != '':
			help.append(chembl[0][8])
		else:
			help.append('NULL')
		help.append('NULL')
		help.append("Unknown")
		help.append("Chembl")

		chembl.remove(chembl[0])

	#pprint (help)
	final.append(help)
	#print (final)
	del help
	if (len(chembl)==0) and (len(bdb)==0):
		i = 2
	counter = counter + 1

for line in final:
	#last check
	if (str(line[0]) == '') or (str(line[1]) == '') or (str(line[2]) == '') or (str(line[3]) == ''):
		continue
	for x in range(13):
		if '\'' in str(line[x]):
			line[x] = line[x].replace('\'','')
	statement = 'insert into activity values (' + str(line[0]) + ', '  + str(line[1]) + ', ' + str(line[2]) + ', ' + str(line[3]) + ', \'' + str(line[4]) + '\', \'' + str(line[5]) + '\', ' + str(line[6]) + ', \'' + str(line[7]) + '\', ' +  str(line[8]) + ', ' + str(line[9]) + ', ' + str(line[10]) + ', \'' + str(line[11]) + '\', \'' + str(line[12]) + '\');'
	print (statement)
	conn_final = psycopg2.connect('dbname=chembdb_update user=data host=/tmp/')
	curs_final = conn_final.cursor()
	curs_final.execute(statement)
	conn_final.commit()

