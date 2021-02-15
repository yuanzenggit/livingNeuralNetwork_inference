import os
import glob
import matplotlib.pyplot as plt
import numpy as np

path=[]
path.append('./*Biophysical*')
path.append('./*Computational*')

#path.append('./*Biophysical_Fix*')
#path.append('./*Computational_Fix*')

plt.figure(figsize=(6,10))

for i in range (len(path)):
	files=glob.glob(path[i])

	index=[]
	
	for j in range (len(files)):
		index.append([str(files[j]).split("_")[0].strip('./[],_'), files[j], str(files[j]).split("_")[1].strip('./[],_')])
		index=sorted(index)

	total=[] 
	for ind in index:
			print (ind)
			f=open(ind[1], 'r') 
			#next(f)
			#next(f)
			#next(f)
			a=[]
			count=[]
			n=0
			for line in f:
					if n==101:
						break
					n+=1
					count.append(n)
					if str(files[0]).split("_")[0].strip('./[],_')=='Biophysical':
							a.append(float(str(line).split("accuracy:")[1].strip())/100)
					else:
							a.append(float(str(line).split(" ")[4].strip()))

			total.append(a)
			f.close()

	total=np.array(total)
	total=total.T
	average=[0]*len(total)
	std=[0]*len(total)
	for j in range (len(total)):
			average[j]=np.mean(total[j])
			std[j]=np.std(total[j])
	
	print (average[99])
	if str(files[0]).split("_")[0].strip('./[],_')=='Biophysical':
		name='Biophysical_Val'
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', fmt='--o', markersize='4', capsize=0, label=name)
	else:
		name='Computational_Val'
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='firebrick', fmt='--o', markersize='4', capsize=4, label=name)

	x_ticks=np.arange(0,110,20)
	y_ticks=np.arange(0,1.2,0.1)
	plt.yticks(y_ticks, fontsize=24)
	plt.xticks(x_ticks, fontsize=24)
	plt.legend(loc=4, ncol=1, fontsize=24)

plt.show()




