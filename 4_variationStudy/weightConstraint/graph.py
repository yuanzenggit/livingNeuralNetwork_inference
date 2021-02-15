import os
import glob
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

path=[]
path.append('./*1, 1, 1, 2,*')
path.append('./*1, 1, 1, 1*')
path.append('./*1, 1, 1, 3,*')

plt.figure()
for i in range (len(path)):
	files=glob.glob(path[i])
	
	#print(files)
	name=str(files[0]).split(",")[3]+str(files[0]).split(",")[4]+str(files[0]).split(",")[5]+str(files[0]).split(",")[6]
	#name=""
	if int(str(files[0]).split(",")[15])==1:
			name+=str("[0, 0.0027]")
	elif int(str(files[0]).split(",")[15])==3:
			name+=str("[-0.005, 0.005]")
	elif int(str(files[0]).split(",")[15])==2:
			name+=str("[0.00045, 0.0018]")
	
	index=[]
	for j in range (len(files)):
		index.append([files[j]])
	
	total=[] 
	for ind in index:
			f=open(ind[0], 'r') 
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
							a.append(float(str(line).split("accuracy: ")[1].strip()))
			
			total.append(a)
			f.close()
	
	total=np.array(total)
	total=total.T
	average=[0]*len(total)
	std=[0]*len(total)
	for j in range (len(total)):
		average[j]=np.mean(total[j])
		std[j]=np.std(total[j])
	
		#if j==99:
		#	print(average[j])
	
	delta=[0]*(len(total)-1)
	for j in range(len(total)-1):
		delta[j]=round(average[j+1]-average[j], 5)
		if(delta[j]>0.002):
			print(j)
	#print(delta)

	if i==0:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='g', fmt='-o', markersize='2', capsize=2, label=name)
	#if i==1:
	#	plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='sienna', fmt='-o', markersize='2', capsize=2, label=name)
	if i==1:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='b', fmt='-o', markersize='2', capsize=2, label=name)
	#if i==3:
	#	plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='black', fmt='-o', markersize='2', capsize=2, label=name)
	if i==2:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='r', fmt='-o', markersize='2', capsize=2, label=name)
	if i==3:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='m', fmt='-o', markersize='2', capsize=2, label=name)
	if i==4:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='c', fmt='-o', markersize='2', capsize=2, label=name)

	print(name,(average[99]+average[98]+average[97]+average[96]+average[95])/5, std[99])
	x_ticks=np.arange(0,110,20)
	y_ticks=np.arange(0,1.2,0.1)
	plt.yticks(y_ticks,fontsize=20)
	plt.xticks(x_ticks,fontsize=20)
	plt.tight_layout()
	
#plt.ylabel('Accuracy (%)', size=14)
#plt.xlabel('Epoch', size=14)
plt.legend(loc=4, ncol=1, fontsize=20)
plt.show()



