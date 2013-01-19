import sympy as sy
import groesse as gr
Werte=[gr.Groesse("x","mm",10,1),gr.Groesse("y","kg",100,2),gr.Groesse("z","s",1,0.1)]
x=sy.Symbol("x")
y=sy.Symbol("y")
f=x*y
gr.eval_expr(f,[x,y],Werte)
