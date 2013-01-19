import numpy as np
import sympy as sy
class Groesse:
        def __init__(self,name,einheit,x,Sx):
                self.x=float(x)
                self.Sx=float(Sx)
                self.name=name
                self.einheit=einheit
        def __str__(self):
                return str(self.x)+" +- "+str(self.Sx)
        def __repr__(self):
                return self.__str__()
from sympy.parsing.sympy_parser import parse_expr
import sympy as sy
import sympy.physics.units as u
def eval_expr(expr,variables,container):
        vals={}
        for k in container:
                vals[k.name]=k.x
                vals["S"+k.name]=k.Sx
        x = expr.evalf(subs=vals)
        print x
        #little workaround
        leer=sy.Symbol("leer")
        f=0*leer

        for k in variables:
                f=f+ (sy.diff(expr,k))**2*sy.Symbol("S"+k.__str__())
        f=sy.sqrt(f)
        print f
        Sx= f.evalf(subs=vals)
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
