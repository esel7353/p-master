import numpy as np
class Errorclass:
        def __init__(self,x,Sx=0):
                self.x=np.array(x)
                self.Sx=np.array(Sx)
        # + 
        def __add__(self,other):
                if isinstance(other,Errorclass):
                        x=self.x+other.x
                        Sx= np.sqrt(self.Sx**2+other.Sx**2)
                        return Errorclass(x,Sx)
                else:
                        x=self.x+other
                        return Errorclass(x,self.Sx)
        def __radd__(self,other):
                 if isinstance(other,Errorclass):
                        x=self.x+other.x
                        Sx= np.sqrt(self.Sx**2+other.Sx**2)
                        return Errorclass(x,Sx)
                 else:
                         try:
                                 x=self.x+other
                                 return Errorclass(x,self.Sx)
                         except:
                                 print "adding failed"
                                 return NotImplemented
        # -        
        def __sub__(self,other):
                if isinstance(other,Errorclass):
                        x=self.x-other.x
                        Sx= np.sqrt(self.Sx**2+other.Sx**2)
                        return Errorclass(x,Sx)
                else:
                        x=self.x-other
                        return Errorclass(x,self.Sx)
        def __rsub__(self,other):
                 if isinstance(other,Errorclass):
                        x=-self.x+other.x
                        Sx= np.sqrt(self.Sx**2+other.Sx**2)
                        return Errorclass(x,Sx)
                 else:
                         try:
                                 x=-self.x+other
                                 return Errorclass(x,self.Sx)
                         except:
                                 print "adding failed"
                                 return NotImplemented
# *
        def __mul__(self,other):
                if isinstance(other,Errorclass):
                        x=self.x*other.x
                        Sx= x*np.sqrt(self.Sx**2/self.x**2+other.Sx**2/other.x**2)
                        return Errorclass(x,Sx)
                else:
                        x=self.x*other
                        Sx=self.Sx*other
                        return Errorclass(x,Sx)
        def __rmul__(self,other):
                 if isinstance(other,Errorclass):
                        x=self.x*other.x
                        Sx= x*np.sqrt(self.Sx**2/self.x**2+other.Sx**2/other.x**2)
                        return Errorclass(x,Sx)
                 else:
                         try:
                                 x=self.x*other
                                 Sx=self.Sx*other
                                 return Errorclass(x,Sx)
                         except:
                                 print "adding failed"
                                 return NotImplemented
 
        def __div__(self,other):
                if isinstance(other,Errorclass):
                        x=self.x/other.x
                        Sx= x*np.sqrt(self.Sx**2/self.x**2+other.Sx**2/other.x**2)
                        return Errorclass(x,Sx)
                else:
                        x=self.x/other
                        Sx=self.Sx/other
                        return Errorclass(x,Sx)
        def __rdiv__(self,other):
                 if isinstance(other,Errorclass):
                        x=other.x/self.x
                        Sx= x*np.sqrt(self.Sx**2/self.x**2+other.Sx**2/other.x**2)
                        return Errorclass(x,Sx)
                 else:
                         try:
                                 x=other/self.x
                                 Sx=other*self.Sx/self.x**2
                                 return Errorclass(x,Sx)
                         except:
                                 print "adding failed"
                                 return NotImplemented
 
        def __pow__(self,other):
                if isinstance(other,Errorclass):
                        return NotImplemented

                else:
                        x=self.x**other
                        Sx=abs(x)*abs(other)*self.Sx/abs(self.x)
                        return Errorclass(x,Sx)
        def __rpow__(self,other):
                return NotImplemented
        
        def __str__(self):
                return str(self.x)+" +- "+str(self.Sx)
        def __repr__(self):
                return self.__str__()
