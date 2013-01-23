
import os
import sys
from Environment import *

def runPython(*args):
    global env          # external python files have access to env
    global markerTypes  # and can add more marker types
    ns = {'env': env, 'markerTypes': markerTypes}
    if len(args) == 1:
        execfile(args[0], ns)
        return
    if len(args) == 2:
	asd= args[1].replace("\r", "")
	print >>stdout, repr(asd)
        exec(asd, ns)

def printPlot(*args):
    if len(args) == 1:
        print env.getPlot(args[0]).latex()
    if len(args) == 2:
        p = Plot.createFromText(args[1])
        env.addPlot(args[0], p)
        print p.latex()

def printTable(*args):
    if len(args) == 1:
        print env.getTable(args[0]).latex()
    if len(args) == 2:
        t = Table.createFromText(args[1])
        env.addTable(args[0], t)
        print t.latex()

def printFormula(*args):
    pass
def printMean(arg):
    pass
def printLinReg(arg):
    pass

def getFilesByExtention(extention):
    dirlist = os.listdir('.')
    l       = len(extention)
    return [file for file in dirlist if file[-l:] == extention]

env = Environment()

###############################################################
# build in marker
markerTypes = {}
markerTypes['PY'] 	    = runPython     #single and multi line
markerTypes['PLOT']	    = printPlot     #single and multi line
markerTypes['TABLE']	= printTable    #single and multi line
markerTypes['FORMULA']  = printFormula  #single and multi line
markerTypes['MEAN']     = printMean     #single line only
markerTypes['LINREG']   = printLinReg   #single line only

###############################################################
# load fuc

###############################################################
# load tables

csvFiles = getFilesByExtention('.raw.csv')
for csv in csvFiles:
    name = csv[-8:]
    env.addTable(name, Table.createFromFile(csv))


###############################################################
# load plots

plotFiles = getFilesByExtention('.plot')
for plot in plotFiles:
    name    = csv[-5:]
    env.addPlot(name, Plot.createFromFile(plot))

###############################################################
# parse raw tex files

rawFiles  = getFilesByExtention('.raw.tex')
done      = []

stdout = sys.stdout

for file in rawFiles:
    outName = file[:-8] + ".tex"
    out     = open(outName, 'w')
    sys.stdout = out
    print >>stdout, "Writing to " + outName
    fObj = open(file, 'r')
    multimode = False
    for line in fObj:
        # handle multiline mode
        if multimode:
            if line.strip()== '%---':
                markerTypes[marker](arg, content)
		multimode = False
                continue
	    else:
                content += line
		continue
	# handle normal mode
        if len(line) > 2 and line[0] == '%':
            if " " in line[2:]:
                pos    = line.index(" ")  
                marker = line[2:pos].strip() 
                arg    = line[pos:].strip()
            else:
                arg    = ""
                marker = line[2:].strip()
            if marker in markerTypes:
                if line[1] == '%':
                    markerTypes[marker](arg)
		    continue
		if line[1] == '-':
		    content = ""
		    multimode = True
		    continue
        
	# if not continued...
        print line.strip()
    
    
    # one .raw.tex file done
    out.close()
    done.append(outName)
    
    # run multiline marker, if %--- was omitted at end of file
    if multimode:
        markerTypes[marker](arg, content)

print >>stdout, "\nIn total ", len(done), " .tex files created!"

###############################################################
# make pdf

for tex in done:
    pdfout = os.popen("pdflatex -interaction=nonstopmode " + os.path.abspath(tex) , 'r')
    #print >>stdout, str(pdfout) 
    for l in pdfout:
        print >>stdout, l.strip()

