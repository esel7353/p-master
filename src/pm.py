
import sys
import os
from Environment import *

env = Environment()

def runPython(file):
    global env
    execfile(file)

dirlist = os.listdir('.')
rawFiles = [rawFile for rawFile in dirlist if rawFile[-8:] == ".raw.tex"]


for file in rawFiles:
    outName = file[:-8] + ".tex"
    out     = open(outName, 'w')
    sys.stdout = out
    for line in open(file, 'r'):
        if len(line) > 0:
            if line[0] == '#':
                
                # Plot marker
                if line[:6] == '#PLOT ':
                    name = line[6:].strip() 
                    print env.getPlot(name).latex()
                    continue
                
                # Table marker
                if line[:7] == '#TABLE ':
                    name = line[7:] .strip()
                    print env.getTable(name).latex()
                    continue
            
                # Python marker
                if line[:4] == '#PY ':
                    runPython(line[4:].strip())
                    continue
                
                # unknown marker
                print line
                
            else:
                print line
            