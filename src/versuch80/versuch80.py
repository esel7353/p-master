import ocd
Werte=ocd.open_csv("versuch80/tabelle2.csv")
s_unten=sy.Symbol("s_unten")
s_oben=sy.Symbol("s_oben")
r_unten=sy.Symbol("r_unten")
r_oben=sy.Symbol("r_oben")
I=sy.Symbol("I")
U=sy.Symbol("U")
alpha_offset=sy.Symbol("alpha_offset")
alpha=sy.Symbol("alpha")

B=0.78*10**(-3)*I
import scipy.constants as c
wz=c.e/c.m_e*B/(2*sy.pi)
test=ocd.eval_expr(wz,[s_unten,s_oben,r_oben,I,U,alpha_offset,alpha],Werte,"test")
print str(test)
