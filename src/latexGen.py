
import sys


def genPlotLatex(name, decr):
    out  = "\\begin{figure}[htbp]\n"
    out += "    \\centering\n"
    out += "    \\includegraphics[width=.9\\textwidth]{./" + name + ".png}\n"
    out += "    \\caption{" + decr + "}\n"
    out += "    \\label{fig:" + name + "}\n"
    out += "\\end{figure}" 
    return out

def genTableLatex(file):
    return ""

def genPlot(file):
    # TODO: create image
    return genPlotLatex(file, "decr")


dirlist = os.listdir('.')
rawFiles = [rawFile for rawFile in dirlist if dirlist[:-8] == ".raw.tex"]

for file in rawFiles:
    outName = file[:-8] + ".tex"
    out     = open(outName, 'w')
    sys.stdout = out
    for line in open(file, 'r'):
        if line[1] == '#':
            
            # Plot marker
            if line[:6] == '#PLOT ':
                print genPlot(line[6:])
                continue
            
            # Table marker
            if line[:7] == '#TABLE ':
                print genTable(line[7:])
                continue
        
            # Python marker
            if line[:4] == '#PY ':
                runPython(line[4:])
                continue
            
            # unknown marker
            print line
            
        else:
            print line
        