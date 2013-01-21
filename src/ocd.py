<<<<<<< HEAD
#usage: 
# x = open_csv("tables/table1.csv")
# now all the variables are stored in x
import numpy as np
import csv 
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
                from quantities import *
                self.x=np.array(x)*eval(einheit)
                self.Sx=np.array(Sx)*eval(einheit)
                self.name=name
        def __str__(self):
                return str(self.x)+" +- "+str(self.Sx)
        def __repr__(self):
                return self.__str__()
from sympy.parsing.sympy_parser import parse_expr
import sympy as sy
import sympy.utilities.lambdify as lambdify
def eval_expr(expr,variables,container,name):
        vals={}
        for k in container:
                vals[k.name]=k.x
                vals["S"+k.name]=k.Sx
        #x = expr.evalf(subs=vals)
        f=lambdify(tuple(vals.keys()),expr)
        x = f(**vals)
        #little workaround
        leer=sy.Symbol("leer")
        f=0*leer

        for k in variables:
                f=f+ (sy.diff(expr,k))**2*sy.Symbol("S"+k.__str__())**2
        f=sy.sqrt(f)
        #Sx= f.evalf(subs=vals)
        gf = lambdify(tuple(vals.keys()),f)
        Sx = gf(**vals)
        return Groesse(name,x.dimensionality.string,x.magnitude,Sx.magnitude)
=======
#usage: 
# x = open_csv("tables/table1.csv")
# now all the variables are stored in x
import numpy as np
import csv 
import errorclass as er
import numpy as np
def open_csv(name,errorfy=False):
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
                result={}
                variables=[]
                errors=[]
                for k in data_.keys():
                        if k[0]!="S":
                                variables+=[k]
                        else:
                                errors+=[k]
                for k in variables:
                        if k[-3::]!="std":
                                if "S"+k in errors:
                                        result[k]=er.Errorclass(data_[k],data_["S"+k])
                                else:
                                        result[k]=data_[k]
                        else:
                                ss=np.array(data_[k]).std()
                                result[k]=er.Errorclass(data_[k],ss)
                return Bunch(result)
>>>>>>> 0d2e864e0c7347985f113a96f77ad36cad7f8c85
