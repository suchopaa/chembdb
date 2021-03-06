import csv, ast, psycopg2, array, re
from itertools import islice

conn = psycopg2.connect('dbname=bdb user=data host=/tmp/')
curs = conn.cursor()
curs.execute('drop table BDB_extend')
conn.commit()


f = open('BindingDB_All.tsv', 'r')

reader = csv.reader(f, delimiter='\t')

longest = 15000
headers = list()

def dataType(val):
    try:
        int(val)
    except ValueError:
        try:
            float(val)
        except ValueError:
            return "varchar"
        return "float"
    return "int"


headers = next(reader)
statement = "create table BDB_extend ("
#u = len(headers)
#u = 40
k = [x.replace(' ', '_') for x in headers]
o = [y.replace('(', '_') for y in k]
p = [z.replace(')', '_') for z in o]
n = [x.replace('-', '_') for x in p]
e = [x.replace('/', '_') for x in n]
headers_no_gap = [x.replace('>', 'more') for x in e]
cislo = 0
for i in headers_no_gap:
    znak = str(cislo)
    i = re.sub("^", 'BDB_'+znak+'_', i)
    headers_no_gap[cislo] = i
    cislo = cislo + 1

u = 37
statement = (statement + "{} varchar({}),").format(headers_no_gap[0].lower(), str(longest))
while u<49:
    statement = (statement + "{} varchar({}),").format(headers_no_gap[u].lower(), str(longest))
    u = u + 1
statement = statement[:-1] + ");"


conn = psycopg2.connect('dbname=bdb user=data host=/tmp/')
curs = conn.cursor()
curs.execute(statement)
conn.commit()


