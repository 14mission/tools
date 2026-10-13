from pypxlib import Table
import sys,re,glob

def cleanval(val):
    val = str(val)
    val = re.sub(r'\s*[\t\n]\s*','; ',val)
    return val


def db2tsv(dbfn,tsvfn=None):
    if tsvfn == None:
        tsvfn = re.sub(r'\.\w+$','',dbfn)+".tsv" 
    print(f"read {dbfn}")
    tbl = Table(dbfn)
    print(f" write {tsvfn}")
    tsv = open(tsvfn,"w")
    fields = tbl.fields
    print(f" fields: "+", ".join([field for field in fields]))
    print("#"+"\t".join(fields), file=tsv)
    numrows = len(tbl)
    print(" len: "+str(numrows))
    for row in tbl:
        print("\t".join(cleanval(row[field]) for field in fields),file=tsv)

for arg in sys.argv[1:]:
    for dbfn in glob.glob(arg):
        try:
            db2tsv(dbfn)
        except:
            print("FAILED TO CONVERT: "+dbfn)

print("ok")
