
class Table:
    def __init__(self):
        self.data
        self.usedFormulas = []
        
    def latex(self, includeFormula=True):
        pass
    
    def readFromFile(fileName):
        pass
    
class Plot:
    def __init__(self, caption):
        self.caption        = caption
        self.description    = ""
        self.imageName      = ""
        self.usedFormulas   = []
        self.name           = ""
    
    def makeImage(self):
        pass
    
    def latex(self, includeFormula=True):
        out  = "\\begin{figure}[htbp]\n"
        out += "    \\centering\n"
        out += "    \\includegraphics[width=.9\\textwidth]{./" + self.imageName + "}\n"
        out += "    \\caption{" + self.description + "}\n"
        out += "    \\label{fig:" + self.name + "}\n"
        out += "\\end{figure}" 
        return out
    
    def readFromFile(fileName):
        pass
    

        
class NoSuchException(Exception): pass
        
class Environment:
    
    def __init__(self, tables={}, plots={}, formula={} ):
        self.tables     = tables
        self.plots      = plots
        self.formulas   = formula
        
    def addTable(self, name, table):
        self.tables[name] = table
        
    def addPlot(self, name, plot):
        self.plots[name] = plot
        plot.name         = name
        
    def addFormula(self, name, formula):
        self.formulas[name] = formula    
    
    def getTable(self, name):
        if name in self.tables:
            return self.tables[name]
        else:
            raise NoSuchException("No table named " + name + "!")
        
    def getPlot(self, name):
         if name in self.plots:
            return self.plots[name]
         else:
            raise NoSuchException("No plot named " + name + "!")
    
    def getFormula(self, name):
        if name in self.formulas:
            return self.formulas[name]
        else:
            raise NoSuchException("No formula named " + name + "!")