import sympy as sy
import ocd
Werte=ocd.open_csv("tables/table1.csv")
t=sy.Symbol("t")
s1=sy.Symbol("s1")
s2=sy.Symbol("s2")
q=sy.Symbol("q")
f=(s1/t + s2/t )*q
test=ocd.eval_expr(f,[t,s1,s2,q],Werte,"test")
print str(test)
