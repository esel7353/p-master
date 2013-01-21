def Tabelle(X)
	x=ur"""
	\begin{tabular}{| l | c | r |}
	\hline
	  1 & 2 & 3 \\ \hline
	  4 & 5 & 6 \\ \hline
	  7 & 8 & 9 \\ \hline
	\end{tabular}
	"""
	return x
def write_tex(s,innername="inner.tex",layername="layer.tex"):
	f = open(innername,"w")
	f.write(x)	
	f.close()
	import subprocess
	subprocess.call(["pdflatex",layername])
