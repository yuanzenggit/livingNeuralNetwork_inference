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
		index.append([str(files[j]).split(" ")[20].strip('],'), files[j]])
		index=sorted(index)
	#index1=[0]*len(index)
	#index1[0]=index[0]
	#index1[1:9]=index[2:]
	#index1[9]=index[1]
		
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
							if n==199:
									name.append([int(float(str(ind[0]))),int(float(str(line).split(" ")[8].strip()))])
			total.append(a)
			spike.append(b)
			#name.append(ind[0])
			f.close()

	plt.figure(figsize=(5,8))
	#plt.subplot(121)
	for i in range (len(total)):
		plt.plot(count,total[i],label=name[i])
		#plt.ylabel('Accuracy (%)', size=20)
		#plt.xlabel('Epoch', size=20)
		plt.xticks(fontsize=20)
		#x_ticks=np.arange(0,22,1)
		y_ticks=np.arange(0,1.2,0.1)
		#y_ticks=np.arange(0,100,5)
		#plt.xticks(x_ticks)
		plt.yticks(y_ticks, fontsize=20)
	plt.legend(loc=4, bbox_to_anchor=(0.9,0), ncol=1, fontsize=20)	

	#plt.subplot(122)
	#for i in range (len(total)):
		#plt.plot(count,spike[i],label=name[i])
		#plt.ylabel('Nf_hidden (%)', size=20)
		#plt.xlabel('Epoch', size=20)
		#y_ticks=np.arange(0,110,10)
		#plt.xticks(fontsize=20)
		#plt.yticks(y_ticks, fontsize=20)
	#plt.legend(loc=4,ncol=1, fontsize=20)
	#plt.tight_layout()

	plt.show()




