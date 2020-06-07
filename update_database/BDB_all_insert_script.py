import psycopg2

with open("BindingDB_All.tsv") as input:
	for i, line in enumerate(input):
#now preparing data
		strip = line.strip()
		#print strip
		pom = strip.split('\t')
		pom = [y.replace('\'', '') for y in pom]
		if i ==0:
			delka = len(pom)
			continue
		actual = len(pom)
		cut = int(((actual - 38)/12) + 1)
#now insert base data
		statement = "insert into BDB_base values ("
		num = 0
		for x in pom:
			statement = (statement + "'" + x + "',")
			if num==36:
				break
			num = num + 1
		statement = statement[:-1] + ");"
		conn = psycopg2.connect('dbname=bdb user=data host=/tmp/')
		curs = conn.cursor()
		curs.execute(statement)
		conn.commit()
#now I have to delete base data
		del pom[1:37]
		#print pom
#now insert extend data
		k = 0
		while k<cut:
			statement = "insert into BDB_extend values ('" + pom[0] + "',"
			num = 0
			if len(pom)<13:
				while len(pom)!=13:
					pom.append('')
			for x in pom:
				if num!=0:
					statement = (statement + "'" + x + "',")
				if num==12:
					break
				num = num + 1
			statement = statement[:-1] + ");"
			del pom[1:13]
			conn = psycopg2.connect('dbname=bdb user=data host=/tmp/')
			curs = conn.cursor()
			curs.execute(statement)
			#print statement
			conn.commit()
			k = k + 1



