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
		if a1==1:
				index.append([0, files[j], 'f=2,s=2,p=0'])
		elif a1==2:
				index.append([1, files[j], 'f=3,s=3,p=7'])
		elif a1==3:
				index.append([2, files[j], 'f=4,s=2,p=1'])
		elif a1==4:
				index.append([3, files[j], 'f=6,s=2,p=2'])
		elif a1==5:
				index.append([4, files[j], 'f=8,s=2,p=3'])
		#index.append([str(files[j]).split(" ")[18].strip('],'), files[j]])
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
	#plt.legend(loc=4,ncol=3, fontsize=14)	
	plt.legend(loc=4, bbox_to_anchor=(1,0), ncol=1, fontsize=19)
	#plt.tight_layout()

	#plt.subplot(122)
	#for i in range (len(total)):
	#	plt.plot(count,spike[i],label=name[i])
		#plt.ylabel('Nf_hidden (%)', size=20)
		#plt.xlabel('Epoch', size=20)
	#	y_ticks=np.arange(0,110,10)
	#	plt.xticks(fontsize=20)
	#	plt.yticks(y_ticks, fontsize=20)
	#plt.legend(loc=4,ncol=1, fontsize=20)
	#plt.tight_layout()

	plt.show()




