import subprocess
import scipy.io as sio
from sys import argv

iteration=1
datalength=100
name=argv[1]
seed1=argv[2] #task number
seed2=argv[3] #run number
for iterat in range (iteration):
		correct=0
		cost=0
		spikeNum=0
		for cur in range (datalength):
				print ("train fig:", iterat, cur, correct)
				#train
				subprocess.call(["python3", name+".py", "./result/"+name+"_"+seed2, "./weights/"+name+seed2+".mat", str(iteration), str(datalength), str(iterat), str(cur), str(correct), str(cost), str(1), str(seed1), str(seed2), str(spikeNum)])
				all_vals=sio.loadmat('./weights/'+name+seed2+".mat")
				correct=int(all_vals['correct'][0])
				cost=float(all_vals['cost'][0])
				spikeNum=float(all_vals['spike'][0])
				printout1=all_vals['figure']

		correct=0
		cost=0
		spikeNum=0
		for cur in range (datalength):
				print ("test fig:", iterat, cur, correct)
				#test
				subprocess.call(["python3", name+".py", "./result/"+name+"_"+seed2, "./weights/"+name+seed2+".mat", str(iteration), str(datalength), str(iterat), str(cur), str(correct), str(cost), str(0), str(seed1), str(seed2), str(spikeNum)])
				all_vals=sio.loadmat('./weights/'+name+seed2+".mat")
				correct=int(all_vals['correct'][0])
				cost=float(all_vals['cost'][0])
				spikeNum=float(all_vals['spike'][0])

