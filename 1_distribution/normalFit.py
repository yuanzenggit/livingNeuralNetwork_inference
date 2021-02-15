import scipy.io as sio
import sys
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.spatial import distance

#distribution
Vth=0.0066

#experiment
goal = [0,0,2,14,48,131,197,255,194,102,39,13,3,1,0,0,0,0,0,0]
minError = 50
minResult = [0]*20
minU = ''
minS = '' 
for a in range (880,910,1):
	for b in range (880,910,1):
		inital_u=0.000001*a 
		inital_s=0.000001*b
		
		result=[0]*20
		for i in range (1000):
			for j in range (20):	
				synlist=inital_u+np.random.randn(j,1)*inital_s

				if sum(synlist) > Vth:
					result[j]+=1
					break
			
		error=distance.euclidean(result,goal)
		if error<minError:
			minError = error
			minResult = result
			minU = str(inital_u)
			minS = str(inital_s)
			print 
			print ("u,s:", inital_u, inital_s)
			print ("target", goal)
			print ("result", result)
			print (error)

outputStr = "N(" + minU + "," + minS + ")"
titleStr = "Error: "+str(minError)

x = range(0,20)
plt.plot(x,goal,x,minResult)
plt.legend(['Biophysical',str(outputStr)])
plt.title(titleStr)
plt.xticks(np.arange(min(x), max(x)+1, 1.0))
plt.show()



