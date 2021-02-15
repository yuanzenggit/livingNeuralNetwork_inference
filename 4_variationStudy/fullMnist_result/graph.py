import os
import glob
import matplotlib.pyplot as plt
import numpy as np

path=[]
path.append('./*100*[1, 0,*')
path.append('./*100*[1, 1,*')
path.append('./*500*[1, 0,*')
path.append('./*500*[1, 1,*')
path.append('./*2000*[1, 0,*')
path.append('./*2000*[1, 1,*')

plt.figure(figsize=(6,8))
for i in range (len(path)):
	files=glob.glob(path[i])
	
	print (files[0])
	print (str(files[0]).split(" ")[13].strip('[]./,'))
	if int(str(files[0]).split(" ")[13].strip('[]./,'))==0:
		name=str(files[0]).split(" ")[1].strip('[]./,')+str(' hidden, no Est op')
	else:
		name=str(files[0]).split(" ")[1].strip('[]./,')+str(' hidden, with Est op')

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

		if j==99:
			print (average[j])
	
	if i==0:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='g', fmt='-o', markersize='2', capsize=2, label=name)
	if i==1:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='sienna', fmt='-o', markersize='2', capsize=2, label=name)
	if i==2:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='b', fmt='-o', markersize='2', capsize=2, label=name)
	if i==3:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='black', fmt='-o', markersize='2', capsize=2, label=name)
	if i==4:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='r', fmt='-o', markersize='2', capsize=2, label=name)
	if i==5:
		plt.errorbar(count, average, yerr=std, elinewidth=1, ecolor='orange', color='gray', fmt='-o', markersize='2', capsize=2, label=name)
	
	print (name,average[99], std[99])
	x_ticks=np.arange(0,110,20)
	y_ticks=np.arange(0,1.2,0.1)
	plt.yticks(y_ticks,fontsize=20)
	plt.xticks(x_ticks,fontsize=20)
	plt.tight_layout()
	
#plt.ylabel('Accuracy (%)', size=14)
#plt.xlabel('Epoch', size=14)
plt.legend(loc=4, ncol=1, fontsize=22)
plt.show()



