import os
import glob
import matplotlib.pyplot as plt
import numpy as np

path=[]
path.append('./*0.0066*')

for i in range (len(path)):
	files=glob.glob(path[i])

	index=[]
	for j in range (len(files)):
		a1=int(str(files[j]).split(" ")[16].strip('[],'))
		index.append([str(files[j]).split(" ")[18].strip('[],'), files[j], str(files[j]).split(" ")[19].strip('[],') ])
		index=sorted(index)
		
	total=[] 
	spike=[]
	name=[]
	for ind in index:
			f=open(ind[1], 'r') 
			next(f)
			next(f)
			next(f)
			a=[]
			b=[]
			count=[]
			n=0
			for line in f:
					if n==201:
						break
					n+=1
					if n%2==0:
							count.append(n/2)
							a.append(float(str(line).split(" ")[8].strip()))
					else:		
							b.append(float(str(line).split(" ")[8].strip()))
			total.append(a)
			spike.append(b)
			if float(ind[2])==1000:
					name.append([str("L: ")+ind[0]+str(" H: inf")])
			else:
					name.append([str("L: ")+ind[0]+str(" H: ")+ind[2]])
			f.close()

	plt.figure(figsize=(5,8))
	for i in range (len(total)):
		plt.plot(count,total[i],label=name[i])
		#plt.ylabel('Accuracy (%)', size=20)
		#plt.xlabel('Epoch', size=20)
		plt.xticks(fontsize=20)
		y_ticks=np.arange(0,1.2,0.1)
		plt.yticks(y_ticks, fontsize=20)
	plt.legend(loc=4, bbox_to_anchor=(1,0), ncol=1, fontsize=19)

	plt.show()




