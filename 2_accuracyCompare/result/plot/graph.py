import os
import glob
import matplotlib.pyplot as plt
import numpy as np

path=[]
path.append('./*Biophysical_*')
path.append('./*Biophysical1*')
path.append('./*Computational_*')
path.append('./*Computational1*')

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
			a=[]
			count=[]
			n=0
			for line in f:
					if n==101:
						break
					n+=1
					count.append(n)
					if str(files[0]).split("_")[0].strip('./[],_')=='Biophysical' or str(files[0]).split("_")[0].strip('./[],_')=='Biophysical1':
							a.append(float(str(line).split("accuracy:")[1].strip())/100)
					else:
							a.append(float(str(line).split("accuracy:")[1].strip()))

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
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='dodgerblue', fmt='--o', markersize='4', capsize=0, label=name)
	elif str(files[0]).split("_")[0].strip('./[],_')=='Biophysical1':
		name='Biophysical_Val_optimized'
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='dimgray', fmt='--o', markersize='4', capsize=0, label=name)
	elif str(files[0]).split("_")[0].strip('./[],_')=='Computational1':
		name='Computational_Val_optimized'
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='mediumaquamarine', fmt='--o', markersize='4', capsize=0, label=name)
	else:
		name='Computational_Val'
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='firebrick', fmt='--o', markersize='4', capsize=4, label=name)

	x_ticks=np.arange(0,110,20)
	y_ticks=np.arange(0,1.2,0.1)
	plt.yticks(y_ticks, fontsize=18)
	plt.xticks(x_ticks, fontsize=18)
	plt.legend(loc=4, ncol=1, fontsize=17)

plt.show()




