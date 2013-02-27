import numpy as np
import matplotlib.pyplot as plt

def gerade(x,y):
    x=np.array(x)
    y=np.array(y)
    b=np.sum((x-np.mean(x))*y)/sum((x-np.mean(x))**2)
    a=np.mean(y)-b*np.mean(x)
    n=len(x)
    sy=np.sqrt(np.sum((y-b*x-a)**2)/(n-2))
    sa=sy*np.sqrt(1./n+np.mean(x)**2/np.sum((x-np.mean(x))**2))
    sb=sy*np.sqrt(1./np.sum((x-np.mean(x))**2))
    return (a,b,sa,sb,sy)

#def expfit(x,y):
#	def func(x, a, b, c):
#	    return c * np.exp(b * x) + a 
#	popt, pcov = curve_fit(func, x, y)
#	(a,b,c)=popt
#	return (a,b,c)
