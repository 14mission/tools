#!/usr/bin/env python
from math import log2
explenlist = [ 0.02, 0.25, 0.5, 1.0 ]
fstoplist = [ 16, 22, 36 ]
for filmiso in [ 100, 200, 400 ]:
  print("\tfilmiso: "+str(filmiso))
  print("\t"+"\t".join("f"+str(fstop) for fstop in fstoplist))
  for explen in explenlist:
    evlist = []
    for fstop in fstoplist:
      filmspeedmod = filmiso / 100
      ev = log2( fstop*fstop / (explen * filmspeedmod) )
      evlist.append(ev)
    print(str(explen) + "s\t" + "\t".join(str(round(ev,1)) for ev in evlist))
print("15\tsunny\n"\
  +"14\thazy\n"\
  +"13\tcloudy\n"\
  +"12\tshady\n"\
  +"12\tsunset\n"\
  +"9-11\tdusk\n"\
  +"9-10\tneon\n"\
  +"7-8\tnight streets\n"\
  +"4-6\tindoors/lighting\n"\
  +"3\tdim-window-lit\n")
