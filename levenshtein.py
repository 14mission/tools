#!/usr/bin/env python3
import sys,re

def normstr(s):
  s = s.lower()
  s = re.sub(r'^\W*|\W*$|\'','',s)
  return s

def align(origvseq,orighseq,norm=False,joiner=":"):
  hseq = [ "NULL", *orighseq, "NULL" ]
  vseq = [ "NULL", *origvseq, "NULL" ]
  costgrid = []
  costgrid.append(list(range(len(hseq))))
  for v in range(1,len(vseq)): costgrid.append(list(map(lambda h: 0, range(0,len(hseq))))); costgrid[v][0] = v
  for v in range(1,len(vseq)-1):
    for h in range(1,len(hseq)-1):
      diagonalcost = costgrid[v-1][h-1] + (
        0 if norm and normstr(vseq[v]) == normstr(hseq[h])
        else 0 if vseq[v] == hseq[h]
        else 1 )
      bestcost = diagonalcost
      downcost = costgrid[v-1][h] + 1
      if downcost < bestcost:
        bestcost = downcost
      overcost = costgrid[v][h-1] + 1
      if overcost < bestcost:
        bestcost = overcost
      costgrid[v][h] = bestcost
  edits = costgrid[-2][-2]
  v = len(vseq)-2
  h = len(hseq)-2
  alignment = []
  while v > 0 or h > 0:
    diagonalcost = costgrid[v-1][h-1] if v > 0 and h > 0 else sys.maxsize
    downcost = costgrid[v-1][h] if v > 0 else sys.maxsize
    overcost = costgrid[v][h-1] if h > 0 else sys.maxsize
    if diagonalcost <= downcost and diagonalcost <= overcost:
      if diagonalcost == costgrid[v][h]:
        if norm and vseq[v] != hseq[h]:
          alignment.append(vseq[v]+joiner+hseq[h])
        else:
          alignment.append(vseq[v])
      else:
        alignment.append(vseq[v]+joiner+hseq[h])
      v -= 1
      h -= 1
    elif downcost < overcost:
      alignment.append(vseq[v]+joiner+"NULL")
      v -= 1
    else:
      alignment.append("NULL"+joiner+hseq[h])
      h -= 1
  alignment.reverse()
  return edits, alignment


if __name__ == "__main__":
  av = sys.argv
  ac = 1
  hseq = None
  vseq = None
  donorm = False
  infn = None
  joiner = ":"
  usage = av[0] + " -n(orm) -s \"hseq\" \"vseq\""
  while ac < len(av):
    if av[ac][0] != '-':
      raise Exception("?"+av[ac]+"; "+usage)
    elif av[ac] == "-n":
      donorm = True
    elif av[ac] == "-p":
      joiner = "|"
    elif ac+1 >= len(av) or av[ac+1][0] == '-':
      raise Exception("?"+av[ac]+" NOVAL; "+usage)
    elif av[ac] == "-i":
      ac += 1
      infn = av[ac]
      inh = open(infn)
      totaltoks = 0
      totaledits = 0
      for ln in inh:
        cols = ln.strip().split("\t")
        if len(cols) < 2: raise Exception("need >= 2 cols: "+ln)
        refseq = list(filter(None,cols[-2].split()))
        hypseq = list(filter(None,cols[-1].split()))
        edits, alignment = align(refseq,hypseq,norm=donorm,joiner=joiner)
        totaltoks += len(refseq)
        totaledits += edits
        cols.append(" ".join(alignment))
        cols.append(str(edits))
        print("\t".join(cols))
      print("toks="+str(totaltoks)+"; edits="+str(totaledits)+"; wer="+str(100.0*totaledits/totaltoks))
    elif av[ac] == "-s" and ac+2 < len(av) and av[ac+1][0] != '-' and av[ac+2][0] != '-':
      ac += 1
      hseq = list(filter(None,av[ac].split()))
      ac += 1 
      vseq = list(filter(None,av[ac].split()))
      edits, alignment = align(hseq,vseq,norm=donorm,joiner=joiner)
      print("edits="+str(edits))
      print("alignment="+" ".join(alignment))
    else:
      raise Exception("?"+av[ac]+"; "+usage)
    ac += 1
