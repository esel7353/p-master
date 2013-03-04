import matplotlib.pyplot as plt
import mylib as mm
import numpy as np
sina=[0.741,0.740,0.717,0.629]
lambd=np.array([579.100,577.000,546.100,435.800])*10**-9
Ssina=[0.000920,0.000922,0.000956,0.001066]

def plot11():
	(a,b,Sa,Sb,Sy)=mm.gerade(lambd,sina)
	print "a:",a,"+-",Sa
	print "b:",b,"+-",Sb
	t=np.linspace(min(lambd),max(lambd),1000)
	plt.figure()
	plt.title(ur"$sin(\alpha)$ als Funktion der Beugungsordnung")
	plt.xlabel(ur"Ordnung $k$")
	plt.ylabel(ur"$sin(\alpha)$")
	plt.plot(t,b*t+a)
	plt.plot(t,(b+Sb)*t+a+Sa,"m--")
	plt.plot(t,(b-Sb)*t+a-Sa,"c--")
	plt.errorbar(lambd,sina,fmt=".",yerr=Ssina)
	plt.grid()
	plt.show()
#plot11()

sina=[0.159,0.159,0.150,0.120]
Ssina=[0.001,0.001,0.001,0.001]
#plot11()
lambd=[1,2,3,4]
sina=[0.120,0.237,0.346,0.535]
Ssina=[0.001,0.001,0.001,0.001]
plot11()
