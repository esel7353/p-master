# -*- coding: utf-8 -*-
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
                        if "S"+k in errors:
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
		self.x=self.x.simplified
		self.Sx=self.Sx.simplified
                self.name=name
        def __str__(self):
                return str(self.x)+" +- "+str(self.Sx)
        def __repr__(self):
                return self.__str__()
import sympy as sy
import sympy.utilities.lambdify as lambdify
def eval_expr(expr,variables,container,name):
        vals={}
        for k in container:
                vals[k.name]=k.x
                vals["S"+k.name]=k.Sx
        #x = expr.evalf(subs=vals)
        f=lambdify(tuple(vals.keys()),expr,"numpy")
        x = f(**vals)
        #little workaround
        leer=sy.Symbol("leer")
        f=0*leer

        for k in variables:
                f=f+ (sy.diff(expr,k))**2*sy.Symbol("S"+k.__str__())**2
        f=sy.sqrt(f)
	print f
        #Sx= f.evalf(subs=vals)
        gf = lambdify(tuple(vals.keys()),f,"numpy")
        Sx = gf(**vals)
        return Groesse(name,x.dimensionality.string,x.magnitude,Sx.magnitude)
import matplotlib.pyplot as plt
import mylib as mm
def plot_groessen(A,B):
	(a,b,Sa,Sb,Sy)=mm.gerade(A.x,B.x)
	t=np.linspace(min(A.x),max(A.x),1000)
		
	plt.figure()
	plt.xlabel(A.name+" ("+str(A.x.dimensionality)+")")
	plt.ylabel(B.name+" ("+str(B.x.dimensionality)+")")
	plt.errorbar(A.x,B.x,xerr=A.Sx,yerr=B.Sx, fmt=".")
	plt.plot(t,b*t+a)
	plt.plot(t,(b+Sb)*t+a+Sa,"m--")
	plt.plot(t,(b-Sb)*t+a-Sa,"c--")
	plt.legend([ur"Messwerte",ur"Ausgleichsgerade $a+b\cdot l$",ur"Obere Grenze $a+Sa+(b+Sb)\cdot l$",ur"Untere Grenze $a-Sa+(b-Sb)\cdot l$"],loc=2)
	
	plt.grid()
	plt.show()	
