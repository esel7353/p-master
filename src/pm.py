
import sys
import os
from Environment import *

env = Environment()

def runPython(file):
    global env          # external python files have access to env
    global markerTypes  # and can add more marker types
    execfile(file)
def printPlot(name):
    print env.getPlot(name).latex()
def printTable(name):
    print env.getTable(name).latex()

dirlist = os.listdir('.')
rawFiles = [rawFile for rawFile in dirlist if rawFile[-8:] == ".raw.tex"]

markerTypes = {}
markerTypes['PY'] 	= runPython
markerTypes['PLOT']	= printPlot
markerTypes['TABLE']	= printTable

	

for file in rawFiles:
    outName = file[:-8] + ".tex"
    out     = open(outName, 'w')
    sys.stdout = out
    print >>sys.stderr, "Writing to " + outName
    for line in open(file, 'r'):
        if len(line) > 0:
            if line[0] == '#':
                if " " in line:
                    pos    = line.index(" ") 
                    marker = line[1:pos].strip() 
                    arg    = line[pos:].strip()
                else:
                    arg    = ""
                    marker = line[1:].strip()     
                if marker in markerTypes:
                    markerTypes[marker](arg)
                else:
                    #unknown marker
                    print line 
            else:
                print line
            
