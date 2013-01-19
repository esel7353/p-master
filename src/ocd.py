#usage: 
# x = open_csv("tables/table1.csv")
# now all the variables are stored in x
import numpy as np
import csv 
import numpy as np
def open_csv(name,errorfy=True):
        class Bunch(object):
          def __init__(self, adict):
            self.__dict__.update(adict)
        data_={}
        with open(name,"rb") as csvfile:
                data= csv.reader(csvfile, delimiter=",", quotechar="|")
                names=data.next()
                for k in names:
                        data_[k]=[]
                for row in data:
                        for k in xrange(len(row)):
                                try:
                                        number=float(str(row[k]))
                                        data_[names[k]]+=[number]
                                except:
                                        pass
        if errorfy==False:
                return Bunch(data_)
        else:
                result=[]
                variables=[]
                errors=[]
                for k in data_.keys():
                        if k[0]!="S":
                                variables+=[k]
                        else:
                                errors+=[k]
                for k in variables:
                        r=k.split(" in ")
                        name=r[0]
                        einheit=r[1]
                        if "S"+name in errors:
                                result+=[Groesse(name,einheit,data_[k],data_["S"+k])]
                        else:
                                result+=[Groesse(name,einheit,data_[k],np.array(data_[k])*0)]
                #return Bunch(result)
                return result
                
import sympy as sy
class Groesse:
        def __init__(self,name,einheit,x,Sx):
                self.x=np.array(x)
                self.Sx=np.array(Sx)
                self.name=name
                self.einheit=einheit
        def __str__(self):
                return str(self.x)+" +- "+str(self.Sx)
        def __repr__(self):
                return self.__str__()
from sympy.parsing.sympy_parser import parse_expr
import sympy as sy
import sympy.physics.units as u
import sympy.utilities.lambdify as lambdify
def eval_expr(expr,variables,container):
        vals={}
        for k in container:
                vals[k.name]=k.x
                vals["S"+k.name]=k.Sx
        #x = expr.evalf(subs=vals)
        f=lambdify(tuple(vals.keys()),expr)
        print vals.keys()
        x = f(**vals)
        print x
        #little workaround
        leer=sy.Symbol("leer")
        f=0*leer

        for k in variables:
                f=f+ (sy.diff(expr,k))**2*sy.Symbol("S"+k.__str__())
        f=sy.sqrt(f)
        print f
        #Sx= f.evalf(subs=vals)
        gf = lambdify(tuple(vals.keys()),f)
        Sx = gf(**vals)
        print x,"+-",Sx
        #units
        unit_dict={}
        for k in container:
                unit_dict[k.name]=k.einheit
                print k.name,"has unit",k.einheit
        units=[]
        for k in variables:
                units+=[(k,u.__dict__[unit_dict[k.__str__()]])]
        unit_expr=expr.subs(units)
        print expr
        print unit_expr
