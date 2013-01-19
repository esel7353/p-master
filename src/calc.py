
import math

"""
Contexts in which the MathObjects str() or latex() methods are called.
"""
C_LINE      = -1
C_PARENTH     = 0
C_SUM       = 1
C_MINUS     = 1.5
C_PRODUCT   = 2
C_DIVISOR   = 2.5
C_POWER     = 3

class MathException():
    def __init__(self, data):
        self.data = data
       
class NoNumericalValueFound(MathException):
    def str(self):
        return "No numerical value for variable " + self.data + " found."
    
    
"""
Parent class
"""
class MathObject:
    def __init__(self):
        pass
    
    """
    Plugs in numbers for the values.
    The argument has to be a dictionary. The keys represent the values
    and the values represent the values, which will be plugged in.
    The Return values is an instance of Number.
    """
    def eval(**vars):
        raise NotImplementedError()
    
    """
    Returns a internal representation of the MathObject. For example
    Sum( [Number(1)], [Product( [2, Variable(x)] ) ] )
    """
    def repr(self):
        raise NotImplementedError()
    
    """
    Returns a string representation of the MathObject. The context argument
    determines in which the current Math object is located. This is important
    for propper parenthesis.
    """   
    def str(self, context=0):
        raise NotImplementedError()
    
    """
    Returns a latex representation of the MathObject. See str()
    """   
    def latex(self, context=0):
        raise NotImplementedError()
    
    """
    Simplifies the expression. This affects internal structure as well as
    the mathematical. For example Number(1) + Number(2) = Number(3)
    """
    def simplify(self):
        raise NotImplementedError()
    
    """
    Returns True (False) if the MathObject does (not) depend on the given
    Variable. The argument can be a string.
    """
    def dependsOn(self, var):
        raise NotImplementedError()

    """
    Returns the derivative of the MathObject. The variable must a string.
    The argument total determines whether it should be the total derivative
    or the partial.
    """ 
    def derivate(self, var, total=False):
        raise NotImplementedError()


    def __add__(self, operand):
        return Sum([self, operand])
    
    def __sub__(self, operand):
        return Sum([self], [operand]) 
    
    def __mul__(self, operand):
        return Product([self, operand])
      
    def __div__(self, operand):
        return Product([self], [operand]) 
    
    def __pow__(self, exponent):
        return Pow(self, exponent)


"""
Represents fixed numbers, such as constants, results if eval, ...
"""
class Number(MathObject):
    """
    Constructor of Number. Argument must be one of python build in
    numerical types.
    """
    def __init__(self, number):
        self.number = number
    def eval(self, **vars):
        return self.number
    def repr(self):
        return "Number(" + self.number + ")"        
    def str(self, context=C_PARENTH):
        return latex(self.number).replace(".", ",")
    def latex(self, context=C_PARENTH):
        return latex(self.number).replace(".", ",")
    def dependsOn(self, var):
        return False
    def derivate(self, var):
        return Number(0)

"""
Eulers number
"""
class E(Number):
    def eval(self, **vars):
        return math.e
    def repr(self):
        return "E()"
    def str(self, context=C_PARENTH):
        return "e"
    def latex(self, context=C_PARENTH):
        return "e"

class Pi(Number):
    def eval(self, **vars):
        return math.pi
    def repr(self):
        return "Pi()"
    def str(self, context=C_PARENTH):
        return "pi"
    def latex(self, context=C_PARENTH):
        return "\pi"    
      
"""
Represents a mathematical function. This relevant for the total/partial derivative.
In addition a function offers a fixed argument list, on which it depends on.
A function depends ONLY on the variables in its argument list.
"""
class Function(MathObject):
    """
    First argument is the name of the function.
    Second argument must be a list with all variables on which the function depends.
    Third argument is the inner MathObject of the function.
    """
    def __init__(self, name, argumentSet, inner):
        self.name  = name
        self.inner = inner
        self.argumentSet = argumentSet
    
    def eval(self, vars):
        return self.inner.eval(vars)
    
    """
    The call method is the analogue to a function call. The arguments of this
    method are the values for the variables of the functions argument list.
    The method returns the eval result if the inner MathObject. 
    """
    def call(self, *arguments):
        vars = dict(zip(self.argumentSet, arguments))
        return self.eval(**vars)
    
    def repr(self):
        return "Function(" + self.name + ", " + str(self.argumentSet) + ", " + self.inner.repr() + ")"

    def str(self, context=C_LINE):
        # make args list
        args = ""
        if len(self.argumentSet) > 0:
            args = self.argumentSet[0]
            for arg in self.argumentSet[1:]:
                args += ", " + arg
                
        # in a C_LINE context the function will be displayed as
        #     <name>( <args> ) = <inner>.str()
        # but in any other context the function will be displayed as
        #    <name>( <args> )
        if context == C_LINE:
            return self.name  + "(" + args + ") = " + self.inner.str()
        else:
            return self.name  + "(" + args + ") "
        
    def latex(self, context= C_LINE):
        # make args list
        args = ""
        if len(self.argumentSet) > 0:
            args = self.argumentSet[0]
            for arg in self.argumentSet[1:]:
                args += ", " + arg
                
        # see str()
        if context == C_LINE:
            return "\\textrm{" + self.name + "}" + "(" + args + ") = " + self.inner.latex()      
        else:
            return "\\textrm{" + self.name + "}" + "(" + args + ")" 
    
    """
    Tells whether the function depends on the given variable. The variable name
    has to be a string.
    NOTE: the function depends only on the variable in its argument list!
    """    
    def dependsOn(self, var):
        return var in self.argumentSet
    
    """
    If the argument newName is omitted, the method will simply calculate the
    derivative of the inner MathObject and return the result.
    If the argument newName is not omitted, the method will return a new function
    named after newName, whichs inner MathObject is the derivative of the inner
    MathObject.
    For example:
        x  = Variable('x')
        f  = Function("f", ['x'], Square(x))
        df = f.derivate('x', "f'")
    Now f' is a new function, the derivative of f.    
    
    """
    def derivate(self, var, total=False, newName=""):
        if newName == "":
            if self.dependsOn(var):
                return self.inner.derivate(var, total)
            else:
                return Number(0)
        else:
            return Function(newName, self.argumentSet, self.derivate(var, total))
        

"""
This class represents a variable.
"""
class Variable(MathObject):
    
    """
    The argument determines the name of the variable. All
    variables are identified by their name (string).
    """
    def __init__(self, name):
        self.name = name
    
    """
    Raises an exception if there is no values given for this variable.
    """
    def eval(self, **vars):
        if self.name in vars.keys():
            return vars[self.name]
        else:
            raise NoNumericalValueFound(self.name)
        
    def repr(self):
        return "Variable(" + self.name + ")"
    def str(self, context=C_PARENTH):
        return self.name
    def latex(self, context=C_PARENTH):
        return self.name
    
    def dependsOn(self, var):
        return  var == self.name
    
    def derivate(self, var):
        if var == self.name:
            return Number(1)
        else:
            return Number(0)
    
    
class Sum(MathObject):
    def __init__(self, summands=[], subtrahends=[]):
        self.summands   = summands
        self.subtrahends = subtrahends
    
    def __add__(self, operand):
        self.summands.append(operand)
        return self
    def __radd__(self, operand):
        self.summands.append(operand)
        
    def __sub__(self, operand):
        self.subtrahends.append(operand)
        return self
    def __rsub__(self, operand):
        self.subtrahends.append(operand)
    
    def eval(self, **vars):
        sum=0
        for summand in self.summands:
            sum += summand.eval(**vars)
        for subtrahend in self.subtrahends:
            sum -= subtrahend.eval(**vars)
        return sum
    def str(self, context=C_PARENTH):
        str = ""
        if context > C_SUM:  str += "("
        str += self.summands[0].str(C_SUM)
        for term in self.summands[1:]:
            str += " + " + term.str()
        for term in self.subtrahends:
            str += " - " + term.str(C_SUM)
        if context > C_SUM:  str += ")"
        return str
    
    def latex(self, context=C_PARENTH):
        str = ""
        if context > C_SUM:  str += "\\left("
        str += self.summands[0].latex()
        for term in self.summands[1:]:
            str += " + " + term.latex(C_SUM)
        for term in self.subtrahends:
            str += " - " + term.latex(C_SUM)
        if context > C_SUM:  str += "\\right)"
        return str
    def dependsOn(self, var):
        for summand in self.summands:
            if summand.dependsOn(var): return True
        for subtrahend in self.subtrahends:
            if subtrahend.dependsOn(var): return True
        return False
    def derivate(self, var):
        derivative = Sum()
        
        for summand in self.summands:
            if summand.dependsOn(var):
                derivative += summand.derivate(var)
        for subtrahend in self.subtrahends:
            if subtrahend.dependsOn(var):
                derivative -= derivative.derivate(var)
        return False
        

class Product(MathObject):
    def __init__(self, factors=[], divisors=[]):
        self.factors   = factors
        self.divisors  = divisors
    
    def ___mul__(self, operand):
        self.factors.append(operand)
        return self
        
    def __rmul__(self, operand):
        self.factors.append(operand)
    
    def __truediv__(self, operand):
        self.divisors.append(operand)
        return self
    def __rtruediv__(self, operand):
        self.divisors.append(operand)

    def eval(self, **vars):
        prod=1
        for factor in self.factors:
            prod *= factor.eval(**vars)
        for divisor in self.divisors:
            prod *= divisor.eval(**vars)
        return prod
    
    def str(self, context=C_PARENTH):
        str = ""
        if context > C_PRODUCT:  str += "("
        str += self.factors[0].str(C_PRODUCT)
        for term in self.factors[1:]:
            str += " * " + term.str(C_PRODUCT)
        if str == "": str = "1"
        
        for term in self.divisors:
            str += " / "
            str +=  term.str(C_DIVISOR)

        if context > C_PRODUCT:  str += ")"
        return str
    
    def latex(self, context=C_PARENTH):
        
        fraction = (len(self.divisors) > 0)       
        if fraction:
            chieldContext = C_PARENTH
        else:
            chieldContext = C_PRODUCT
        
        numerator = ""
        for term in self.factors:
            numerator += " " + term.latex(chieldContext)
        if numerator == "": numerator = "1"
        
        denominator = ""
        for term in self.divisors:
            denominator += " " + term.latex(chieldContext)
 
        str = ""
        if context>C_DIVISOR: str = "\\left("
        
        if not fraction:
            str += numerator
        else:
            str += "\\frac{" + numerator + "}{" + denominator + "}"
        if context>C_DIVISOR: str += "\\right)"
        
        return str    
    
    def numeratorDependsOn(self, var):
        for factor in self.factors:
            if factor.dependsOn(var): return True
        return False        
    def denominatorDependsOn(self, var):
        for factor in self.factors:
            if factor.dependsOn(var): return True
        return False
        
    def dependsOn(self, var):
        return self.numeratorDependsOn(var) or self.denominatorDependsOn(var)
    
    def derivateHalf(self, var, terms):
        dependent   = []
        constants   = []
        for term in self.terms:
            if term.dependsOn(var): dependent.append(term)
            else:                   constants.append(term)
        
        cProd = Product(constants)
        
        if len(dependent) == 0:
            return Number(0)
        if len(dependent) == 1:
            return cProd * dependent[0].derivate(var)
        if len(dependent) == 2:
            return cProd * (dependent[0].derivate(var) * dependent[1] + dependent[0] * self.factors[1].derivate(var))
        
        residual = Product(self.factors[1:])
        return cProd(self.factors[0].derivate(var) * residual + self.factors[0] * residual.derivate(var))
    def derivateNumerator(self, var):
        return self.derivateHalf(var, self.factors)
    def derivateDenominator(self, var):
        return self.derivateHalf(var, self.divisors)
    
    def derivate(self, var):
        if(not self.numeratorDependsOn(var) and not self.denominatorDependsOn(var)):
            return Number(0)
        
        if(self.numeratorDependsOn(var) and not self.denominatorDependsOn(var)):
            return self.derivateNumerator(var) / Product(self.divisors)
        
        if(self.numeratorDependsOn(var) and not self.denominatorDependsOn(var)):
            return  Minus(Product(self.factors) * self.derivateDenominator(var) / Square(Product(self.divisors)))
        
        if(self.numeratorDependsOn(var) and self.denominatorDependsOn(var)):
            return  (Product(self.divisors) * self.derivateDenominator(var)  - Product(self.factors) * self.derivateNumerator(var) )/ Square(Product(self.divisors))

            
class Minus(MathObject):
    def __init__(self, funct):
        self.inner = funct
    def eval(self, **vars):
        return -self.inner.eval(**vars)
    def str(self, context=C_PARENTH):
        if context > C_PARENTH:
            return "(-" + self.inner.str(C_MINUS) + ")"
        else:
            return "-" + self.inner.str(C_MINUS) 
    def latex(self, context=C_PARENTH):
        if context > C_PARENTH:
            return "\\left(-" + self.inner.latex(C_MINUS) + "\\right)"
        else:
            return "-" + self.latex.str(C_MINUS) 
    def dependsOn(self, var):
        return self.inner.dependsOn(var)
    def derivate(self, var):
        return Minus(self.inner.derivate(var))

class OneOver(MathObject):
    def __init__(self, funct):
        self.inner = funct
    def eval(self, **vars):
        return 1/self.inner.eval(**vars)
    def str(self, context=C_PARENTH):
        if context > C_DIVISOR:
            return "(1/" + self.inner.str(C_DIVISOR) + ")"
        else:
            return "1/" + self.inner.str(C_DIVISOR) 
    def latex(self, context=C_PARENTH):
        if context > C_DIVISOR:
            return "\\left(\\frac{1}{" + self.inner.latex(C_DIVISOR) + "}\\right)"
        else:
            return "(\\frac{1}{" + self.inner.latex(C_DIVISOR) + "})"
    def dependsOn(self, var):
        return self.inner.dependsOn(var)
    def derivate(self, var):
        return Minus(self.inner.derivate(var) / Square(self.inner) )

   
class Sqrt(MathObject):
    def __init__(self, funct):
        self.inner = funct
    def eval(self, **vars):
        return math.sqrt(self.inner.eval(**vars))
    def str(self, context=C_PARENTH):
        return "sqrt(" + self.inner.str(C_PARENTH) + ")"
    def latex(self):
        return "\\sqrt{" + self.inner.latex(C_PARENTH) + "}"
    def dependsOn(self, var):
        return self.inner.dependsOn(var)
    def derivate(self, var):
        return OneOver(Number(2)) * self.inner(self.inner.derivate(var) / Square(self.inner) )     
     
class Log(MathObject):
    def __init__(self, funct, base=Number(10)):
        self.inner = funct
        self.base  = base
    def eval(self, **vars):
        return math.log(self.inner.eval(**vars), self.base.eval(**vars))
    def str(self, contex=C_PARENTH):
         if self.base == Number(10):
             return "log(" + self.inner.str(C_PARENTH) + ")"
         else:
             return "log(" + self.inner.str(C_PARENTH) + ", " + self.base.str() + ")"
    def latex(self, context=C_PARENTH):
         if self.base == Number(10):
             return "\\log \left(" + self.inner.latex(C_PARENTH) + "\\right)"
         else:
             return "\\log_{" + self.base.latex(C_PARENTH) + "} \left(" + self.inner.latex(C_PARENTH) +  "\\right)" 
                 
class Ln(MathObject):
    def __init__(self, funct):
        self.inner = funct
    def eval(self, **vars):
        return math.log(self.inner.eval(**vars))
    def str(self, context=C_PARENTH):
         return "ln(" + self.inner.str(C_PARENTH) + ")"
    def latex(self, context=C_PARENTH):
         return "\\ln \left(" + self.inner.latex(C_PARENTH) + "\\right)"
    
class Root(MathObject):
    def __init__(self, n, funct):
        self.inner  = funct
        self.n      = n
    def eval(self, **vars):
        return math.pow(self.inner.eval(**vars), OneOver(self.n).eval(**vars))
    def str(self, context=C_PARENTH):
         return "root(" + self.n.str(C_PARENTH) + ", " + self.inner.str(C_PARENTH) + ")"
    def latex(self, context=C_PARENTH):
         return "\\sqrt[" +  self.n.latex(C_PARENTH) + "]{" + self.inner.latex(C_PARENTH) + "}"
        
class Pow(MathObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def eval(self, **vars):
        return math.pow(self.x.eval(**vars), self.y.eval(**vars))
    def str(self, context=C_PARENTH):
        if context>C_DIVISOR:
            return "(" + self.x.str(C_POWER) + "^" +  self.y.str(C_POWER) + ")"
        else:
            return self.x.str(C_POWER) + "^" +  self.y.str(C_POWER)
    def latex(self, context=C_PARENTH):
        if context>C_DIVISOR:
            return "\\left(" + self.x.latex(C_POWER) + "^{" + self.y.latex(C_PARENTH) + "}\\right)"
        else:
            return  self.x.latex(C_POWER) + "^{" + self.y.latex(C_PARENTH) + "}"
     
class Square(MathObject):
    def __init__(self, x):
        self.x = x
    def eval(self, **vars):
        return math.pow(self.x.eval(**vars), 2)
    def str(self, context=C_PARENTH):
        if context>C_DIVISOR:
            return "(" + self.x.str(C_POWER) + "^2)"
        else:
            return self.x.str(C_POWER) + "^2"
        
    def latex(self, context=C_PARENTH):
        if context > C_DIVISOR:
            return "\\left(" + self.x.latex(C_POWER) + "^2\\right)"
        else:
            return "" + self.x.latex(C_POWER) + "^2"
        

class Exp(MathObject):
    def __init__(self, funct):
        self.inner = funct
    def eval(self, **vars):
        return math.exp(self.inner.eval(**vars))
    def str(self, context=C_PARENTH):
         return "exp(" + self.inner.str(C_PARENTH) + ")"  
    
    def latex(self, context=C_PARENTH):
         return "e^{" + self.inner.latex(C_PARENTH) + "}"    



class Cos(MathObject):
    def __init__(self, inner):
        self.inner = inner
    def eval(self, **vars):
        return math.cos(self.inner.eval(**vars))
    def str(self, context=C_PARENTH):
        return "cos(" + self.inner.str(C_PARENTH) + ")"
    def latex(self, context=C_PARENTH):
        return "\\cos\\left(" + self.inner.latex(C_PARENTH) + "\\right)"
    
    def dependsOn(self, var):
        return self.inner.dependsOn(var)
    
    def derivate(self, var):
        if self.inner.dependsOn(var):
            if type(self.inner) == Variable:
                return Sin(self.inner)
            else:
                return Product([Sin(self.inner), self.inner.derivate(var)])
        else:
            return Number(0)
        
        
class Sin(MathObject):
    def __init__(self, inner):
        self.inner = inner
    def eval(self, **vars):
        return math.sin(self.inner.eval(**vars))
    def str(self, context=C_PARENTH):
        return "sin(" + self.inner.str(C_PARENTH) + ")"
    def latex(self, context=C_PARENTH):
        return "\\sin\\left(" + self.inner.latex(C_PARENTH) + "\\right)"
    


if __name__ == "__main__":
    x = Variable("x")
    s = Square(x)

    f = Function("f", ['x'], ( (s-x) / Number(5) + s)**(x + Number(2) ) )

    print(f.str())
    print(f.latex())
    
    
    print(Cos(f).str())
    
    print(Cos(Cos(x)).derivate('x').str())
