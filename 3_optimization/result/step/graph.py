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
		a1=int(str(files[j]).split(" ")[12].strip('[],'))
		a2=int(str(files[j]).split(" ")[13].strip('[],'))
		a3=int(str(files[j]).split(" ")[14].strip('[],'))
		if a1 and a2 and a3:
				index.append([3, files[j], 'Pt+Adpp+Est+Adplr'])
		elif a1 and a2:
				index.append([2, files[j], 'Pt+Adpp+Est'])
		elif a1:
				index.append([1, files[j], 'Pt+Adpp'])
		else:
				index.append([0, files[j], 'Pt'])

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
			name.append(ind[2])
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




