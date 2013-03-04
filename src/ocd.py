# -*- coding: utf-8 -*-
#usage: 
# x = open_csv("tables/table1.csv")
# now all the variables are stored in x
import matplotlib.pyplot as plt
import csv 
import numpy as np
import sympy as sy
import sympy.utilities.lambdify as lambdify
import quantities as qs
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
                
class Groesse:
        def __init__(self,name,einheit,x,Sx):
                self.x=np.array(x)*eval("qs."+einheit)
                self.Sx=np.array(Sx)*eval("qs."+einheit)
		self.x=self.x.simplified
		self.Sx=self.Sx.simplified
                if len(self.Sx)==1:
                        self.Sx=self.x*0+self.Sx
                self.name=name
        def __str__(self):
                return str(self.x)+" +- "+str(self.Sx)
        def __repr__(self):
                return self.__str__()
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
        #print "Formel:"
        #print ur"\begin*{equation}"
        #print sy.latex(expr)
        #print ur"\end{equation}"
        #print "Fehler:"
        #print ur"\begin*{equation}"
	#print sy.latex(f)
        #print ur"\end{equation}"
        gf = lambdify(tuple(vals.keys()),f,"numpy")
        Sx = gf(**vals)
	if give_formula==True:
		return (Groesse(name,x.dimensionality.string,x.magnitude,Sx.magnitude),expr,f)
	else:
		return Groesse(name,x.dimensionality.string,x.magnitude,Sx.magnitude)
def get_error(expr,variables):
        leer=sy.Symbol("leer")
        f=0*leer
        for k in variables:
                f=f+ (sy.diff(expr,k))**2*sy.Symbol("S"+k.__str__())**2
        return sy.sqrt(f)
        return (Groesse(name,x.dimensionality.string,x.magnitude,Sx.magnitude),expr,f)
def get_error(expr,variables):
	leer=sy.Symbol("leer")
        f=0*leer

        for k in variables:
                f=f+ (sy.diff(expr,k))**2*sy.Symbol("S"+k.__str__())**2
        f=sy.sqrt(f)
	return f
def table_groesse(expr,variables,container,name,formula=False):
        (X,expr,Sexpr)=eval_expr(expr,variables,container,name)
        x=ur"\bigskip"
        if formula==True:
                x+=ur"\begin{equation*} "+name+" = "+sy.latex(expr)+"\end{equation*}"
                x+=ur"\begin{equation*} S"+name+" = "+sy.latex(Sexpr)+"\end{equation*}"
        s=ur""
        s2=ur""
        if X.x.dimensionality.string != "dimensionless":
                x+=ur"S"+name+" = "+sy.latex(Sexpr)+ur"\\"
        s=ur""
        s2=ur""
        if X.x.dimensionality.string != "dimensionless":
                s+=name+" in "+str(X.x.dimensionality.string)
        else: 
                s+=name
        for k in X.x.magnitude:
                s+="& %.3f " % k
                s2+="r|"
        s+=ur"\\ \hline "
        if X.Sx.dimensionality.string!= "dimensionless":
                s+="S"+name+" in "+str(X.Sx.dimensionality.string)
        else:
                s+="S"+name
        for k in X.Sx.magnitude:
                s+="& %.3f " % k
        s+=ur"\\ \hline"       
        x+=ur"""\normalsize \vspace{3 mm}
	\begin{tabular}{| l | """+s2+"""}
	\hline
        """+s+ur"""
	\end{tabular} \\ """
	return x
def write_tex(s,innername="inner.tex",layername="layer.tex"):
	f = open(innername,"w")
	f.write(s)	
	f.close()
	import subprocess
	subprocess.call(["pdflatex",layername])

def plot_var(expr1,expr2,variables,container,fitted=False):
        groesse1=eval_expr(expr1,variables,container,"dummy1")
        if expr2!=0:
                groesse2=eval_expr(expr2,variables,container,"dummy2")
                return plot_groessen(groesse1,groesse2,fitted=fitted)
        else:
                return plot_groessen(groesse1)

def plot_groessen(A,B=0,fitted=False):
        X=A.x.magnitude
        plt.xlabel(A.name+" ("+str(A.x.dimensionality)+")")
	plt.grid(True)
        SX=A.Sx.magnitude
        print X,SX
        if B!=0:
                Y=B.x.magnitude
                SY=B.Sx.magnitude
                plt.ylabel(B.name+" ("+str(B.x.dimensionality)+")")

		plt.errorbar(X,Y,xerr=SX,yerr=SY, fmt=".")
		if fitted==True:
			(a,b,Sa,Sb,Sy)=gerade(X,Y)
			t=np.linspace(0,max(Y),1000)
			plt.plot(t,b*t+a)
			plt.plot(t,(b+Sb)*t+a+Sa,"m--")
			plt.plot(t,(b-Sb)*t+a-Sa,"c--")
			return (a,b,Sa,Sb,Sy)	
		else:
			return True
        else:
                plt.errorbar(range(len(X)),X,yerr=SX )
		return True
def gerade(x,y):
    x=np.array(x)
    y=np.array(y)
    b=np.sum((x-np.mean(x))*y)/sum((x-np.mean(x))**2)
    a=np.mean(y)-b*np.mean(x)
    n=len(x)
    sy=np.sqrt(np.sum((y-b*x-a)**2)/(n-2))
