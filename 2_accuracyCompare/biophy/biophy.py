from neuron import h
import scipy.io as sio
import numpy as np
import random 
import math
import sys
from sys import argv
#from matplotlib import pyplot
from random import randint
import time
start_time = time.time()

###############################################################
#                    Separate Model														#
###############################################################
def softmax(x):
		e_x = np.exp(x - np.max(x))
		return e_x / e_x.sum()

def sparse (x):
		np.random.seed(2)
		mask = np.random.randint(0,100,size=x.shape).astype(np.int)
		mask[mask<sparsity] = 1
		mask[mask>=sparsity] = 0
		connect = x * mask
		return connect

def weight_constraint(x, Min_w1, Max_w1):
		mask1 = np.less(Min_w1, x)
		mask2 = np.greater(Max_w1, x)
		y = np.where(mask1, x, Min_w1)
		y = np.where(mask2, y, Max_w1)
		return y

matname=argv[2]
print (matname)
iteration=int(argv[3])
datalength=int(argv[4])
iterat=int(argv[5])
cur=int(argv[6])
correct=int(argv[7])
cost=float(argv[8])
trainSign=int(argv[9])
seed2=int(argv[10]) #task number
seed1=int(argv[11]) #run number
spikeNum=float(argv[12])
if not (iterat==0 and cur==0 and trainSign):
		all_vals=sio.loadmat(matname)
		input_weights1=all_vals['input_weights1']
		input_weights2=all_vals['input_weights2']
		input_copyweights1=all_vals['copy_weights1']
		printout0=all_vals['figure']
		printout1=printout0.tolist()
else:
		printout1=[]
###############################################################
#                          Dataset                            #
###############################################################
name='../../MNIST/input196_training.mat'
vals=sio.loadmat(name)
images=vals['images']
labels=vals['labels']
indexs=vals['indexs']
nimages=images[cur]
nindex=indexs[cur]
nlabels=labels[0][cur]

###############################################################
#            Initial the Network and Parameters               #
###############################################################
batch=1
Numin,Numhidden,Numout=196,100,10
Numtotal=Numin+Numhidden
Numsyn=Numin*Numhidden
LearningRate1=0.0001
LearningRate2=0.01
initialW_u2=0.00075
initialW_s2=0.00077
sparsity=40

#layer two weight
if iterat==0 and cur==0 and trainSign:
		np.random.seed(2)
		weights2=[[initialW_s2*np.random.randn()+initialW_u2 for row in range(0,Numhidden)] for col in range(0,Numout)]
else:
		weights2=input_weights2

#read figure 
h('numInputs=1')
h.numInputs=len(images[0])
h('double img[numInputs]')

#network parameters that changes
h('''
inputNum=0
hiddenNum=0
outputNum=0
totalSyn=0
totalNeuron=0

figureNum=0
currentFig=-1
''')

h.inputNum=Numin
h.hiddenNum=Numhidden
h.totalSyn=Numsyn
h.totalNeuron=h.inputNum+h.hiddenNum

h('''
light_on=0
light_off=0
double in_N_CHR2[totalNeuron]
double in_e_CHR2[totalNeuron]

double in_cap[totalNeuron]
double in_e_pas[totalNeuron]
double in_g_pas[totalNeuron]
double in_gmax_nafPR[totalNeuron]
double in_gmax_kdr[totalNeuron]
double in_gmax_rkq[totalNeuron]
double in_gmax_cal[totalNeuron]
double in_gmax_kcRT03[totalNeuron]

double weights1[totalSyn]
double tau[totalSyn]
double delay[totalSyn]
''')

###############################################################
#Parameters with variation, layer one
#light parameters
light_on=0
light_off=5
N_CHR2=[1500,2000,1480,1400] 
e_CHR2_pre=10

#cell parameters
cap=[10,8,10,15,15,10,8,8] 
e_pas=[-45,-40,-45,-35,-45, -56,-50,-60]
g_pas=[1.1E-3,8.5E-4,1.48E-3,1.15E-3,1.48E-3, 2.1E-3,8E-4,7E-4]
gmax_nafPR=[8E-2,6E-2,1.5E-1,2.9E-1,2.5E-1,9E-2,7E-2,8E-2]
gmax_kdr=[2E-2,2E-2,0.5E-2,2E-2,1E-2,9.9E-2,2E-2,6E-2]
gmax_rkq=[1E-2,9E-3,1E-3,4.5E-3,1E-3,3E-2,5E-3,12E-2]
gmax_cal=[8E-3,8E-3,8E-3,8E-3,8E-3,8E-3,8E-3,8E-3]
gmax_kcRT03=[2E-2,2E-2,2E-2,2.5E-2,1E-1,2E-1,2E-2,1E-1]

#synapse parameters
dlist=[1.8,2,1.3,1.4,2,2,1.3,2,2,2,2,2] 
glist=[0.00072,0.00041,0.00228,0.00117,0.00021,0.00115,0.00063,0.00069,0.00073,0.00034,0.00059,0.00059] 
tlist=[4.5,6.99,4.75,4.4,6,5.95,6.96,5.75,7.8,4.55,5.7,4.9]

#select those will be used in the experiment
#add variation for all the parameters
s=[seed1, seed1+100, seed1+200, seed1+200]
np.random.seed(seed1)
inputNeuronList=np.random.randint(0,8,size=Numin) #0-8,23
np.random.seed(seed1+100)
outputNeuronList=np.random.randint(0,8,size=Numhidden) #0-8, 23
np.random.seed(seed1+200)
synapseList=np.random.randint(0,12,size=Numsyn) #0-12, 01
np.random.seed(seed1+200)
delayList=np.random.randint(0,12,size=Numsyn) #0-12, 01

if iterat==0 and cur==0 and trainSign:
		with open(argv[1], "a") as f:
				data = f.write("seed:")
				for item in s:
						data = f.write("%s " % item)
				data = f.write("\nneuron pre:")
				for item in inputNeuronList:
						data = f.write("%s " % item)
				data = f.write("\nneuron post:")
				for item in outputNeuronList:
						data = f.write("%s " % item)
				data = f.write("\nsynapse:")
				for item in synapseList:
						data = f.write("%s " % item)
				data = f.write("\ndelay:")
				for item in delayList:
						data = f.write("%s " % item)
				data = f.write("\n")

#1. light initial
h.light_on=light_on
h.light_off=light_off
for i in range (Numtotal):
	indexCurrent=0 
	h.in_N_CHR2[i]=N_CHR2[indexCurrent]
	h.in_e_CHR2[i]=0

#2. neuron initial
for i in range (Numtotal):
	if i<Numin: #pre
			indexCurrent=inputNeuronList[i]
			h.in_cap[i]=cap[indexCurrent]
			h.in_e_pas[i]=e_pas[indexCurrent]
			h.in_g_pas[i]=g_pas[indexCurrent]
			h.in_gmax_nafPR[i]=gmax_nafPR[indexCurrent]
			h.in_gmax_kdr[i]=gmax_kdr[indexCurrent]
			h.in_gmax_rkq[i]=gmax_rkq[indexCurrent]
			h.in_gmax_cal[i]=gmax_cal[indexCurrent]
			h.in_gmax_kcRT03[i]=gmax_kcRT03[indexCurrent]
	else: #post
			indexCurrent=outputNeuronList[i-Numin]
			h.in_cap[i]=cap[indexCurrent]
			h.in_e_pas[i]=e_pas[indexCurrent]
			h.in_g_pas[i]=g_pas[indexCurrent]
			h.in_gmax_nafPR[i]=gmax_nafPR[indexCurrent]
			h.in_gmax_kdr[i]=gmax_kdr[indexCurrent]
			h.in_gmax_rkq[i]=gmax_rkq[indexCurrent]
			h.in_gmax_cal[i]=gmax_cal[indexCurrent]
			h.in_gmax_kcRT03[i]=gmax_kcRT03[indexCurrent]

#3. weight initial
weights1=[[np.zeros for row in range(0,Numin)] for col in range(0,Numhidden)]
tau=[[np.zeros for row in range(0,Numin)] for col in range(0,Numhidden)]
delay=[[np.zeros for row in range(0,Numin)] for col in range(0,Numhidden)]

for j in range (Numhidden):
	for i in range (Numin):
			indexCurrent=synapseList[i+j*Numin]
			weights1[j][i]=glist[indexCurrent]
			tau[j][i]=tlist[indexCurrent]

for j in range (Numhidden):
	for i in range (Numin):
			indexCurrent=delayList[i+j*Numin]
			delay[j][i]=dlist[indexCurrent]

# weight constraint, sparsity
weights1=np.array(weights1)
weights1 = sparse(weights1)

if iterat==0 and cur==0 and trainSign:	
		weights1=np.clip(weights1, 0, float('Inf'))
		copyweight1 = np.copy(weights1)
else:
		weights1 = weight_constraint(input_weights1, 0.5*input_copyweights1, 2*input_copyweights1)
		copyweight1 = input_copyweights1

for j in range (Numhidden):
	for i in range (Numin):
			h.weights1[i+j*Numin]=weights1[j][i]
			h.tau[i+j*Numin]=tau[j][i]
			h.delay[i+j*Numin]=delay[j][i]

###############################################################
#initial the network
h('''
load_file("stdgui.hoc")
load_file("network.hoc")
objref snn
''')

if iterat==0 and cur==0 and trainSign:
		print ("iteration:",iteration, " batch:", batch)
		print ("Numin:",Numin," Numhidden:",Numhidden, " Numout:",Numout)
		print ("LearningRate:",LearningRate1, " LearningRate1:",LearningRate2)
		print ("initial weight2:",initialW_u2, initialW_s2)

		with open(argv[1], "a") as f:
				data = f.write("Iteration:%d" % iteration)
				data = f.write(" datalength:%d" % datalength)
				data = f.write(" batch:%d" % batch)
				data = f.write(" sparsity%d\n" %sparsity)
				data = f.write("Numin:%d" % Numin)
				data = f.write(" Numhidden:%d" % Numhidden)
				data = f.write(" Numout:%d" % Numout)
				data = f.write(" LearningRate1:%f" % LearningRate1)
				data = f.write(" LearningRate2:%f" % LearningRate2)
				data = f.write(" initialW_u2:%f" % initialW_u2)
				data = f.write(" initialW_s2:%f\n" % initialW_s2)
		
######################## Front Propogation ########################
#A.light inputs
for i in range (Numin):
		h.in_e_CHR2[i]=e_CHR2_pre*nimages[i]

#intial the network
h.currentFig+=1
h('''
snn=new fullynet(inputNum, hiddenNum, light_on, light_off, &in_N_CHR2, &in_e_CHR2, &in_cap, &in_e_pas, &in_g_pas, &in_gmax_nafPR, &in_gmax_kdr, &in_gmax_rkq, &in_gmax_cal, &in_gmax_kcRT03, &weights1, &tau, &delay)

celsius=37
gc=8
pp= 0.5
forall Ra=1
global_Ra = (1e-6/(gc/pp * (area(0.5)*1e-8) * 1e-3))/(2*ri(0.5))
forall { Ra=global_Ra}

proc init() {
	cvode = new CVode()
	for i=0, totalNeuron-1  {
		forsec snn.slist[i] {v=in_e_pas[i] cm=in_cap[i]}
	}
	finitialize()
	fcurrent()

	if (cvode.active()) {
		cvode.re_init()
	} else {
		fcurrent()
	}
	frecord_init()
}

''')

#record the output
post_v=[0]*Numhidden
t_vec=[0]*Numhidden
for i in range (Numhidden):
		t_vec[i]=h.Vector()
		t_vec[i].record(h._ref_t)
		post_v[i]=h.Vector()
		post_v[i].record(h.snn.post[i].soma(0.5)._ref_v)

h.tstop=200
h.run()

#import matplotlib.ticker as plticker
#time=np.arange(8001)
#pyplot.figure(figsize=(10,3))
#pyplot.plot(time,post_v[3],label='fitted data')
#pyplot.xticks(time[::1000], (np.arange(8001)/40)[::1000], size=15)
#pyplot.yticks(size=15)
#pyplot.ylim([-60, 10])
#pyplot.show()

#B.first layer
spike=[0]*Numhidden
printout=[] #for the figure
for i in range (Numhidden):
		if max(post_v[i])>0:
			spike[i]=1
			printout.append(i)
		else:
			printout.append(0)

#C.second layer
outputs2=[0]*Numout
for i in range (Numout):
		outputs2[i]=0
		for j in range (Numhidden):
				outputs2[i] += spike[j] * weights2[i][j]
outputs=softmax(outputs2)

spikeNum+=sum(spike)
##########################   Prediction   ######################### 
#D.prediction
maxIndex=outputs2.index(max(outputs2))
if maxIndex==nlabels:
		correct+=1
		#print (iterat, cur, maxIndex, nlabels, "correct", correct)
		#with open(argv[1], "a") as f:
		#		data = f.write("iterat/cur/pre/nlabels/correct %d" % iterat)
		#		data = f.write(" %d" % cur)
		#		data = f.write(" %d" % maxIndex)
		#		data = f.write(" %d" % nlabels)
		#		data = f.write(" %d" % sum(spike))
		#		data = f.write(" %d\n" % correct)
#else:
		#print (iterat, cur, maxIndex, nlabels, "wrong  ", correct)
		#with open(argv[1], "a") as f:
		#		data = f.write("iterat/cur/pre/nlabels/wrong  %d" % iterat)
		#		data = f.write(" %d" % cur)
		#		data = f.write(" %d" % maxIndex)
		#		data = f.write(" %d" % nlabels)
		#		data = f.write(" %d" % sum(spike))
		#		data = f.write(" %d\n" % correct)

######################### Back Propogation ########################
if (trainSign):
		cost += (-1 * np.sum(np.dot(nindex, np.log(outputs))))/float(datalength)
		loss2=[0]*Numout
		for i in range (Numout):
				if i==nlabels:
						loss2[i]=1-outputs[i]
				else:
						loss2[i]=0-outputs[i]
		
		loss1=[0]*Numhidden
		for i in range (Numout):
				for j in range(Numhidden):
						loss1[j] += loss2[i] * weights2[i][j]
						weights2[i][j] += LearningRate2 * loss2[i] * spike[j]
		
		for i in range (Numhidden):
				for j in range (Numin):
						weights1[i][j] += LearningRate1 * loss1[i] * nimages[j]

#save weights to a file
all_vals = {'input_weights1': weights1, 'input_weights2': weights2, 'copy_weights1': copyweight1, 'correct':correct, 'cost': cost, 'spike': spikeNum, 'figure':printout1}
sio.savemat(matname, all_vals)

#print to file
if cur==datalength-1 and trainSign:
		with open(argv[1], "a") as f:
			data = f.write("train iter: %d" % iterat)
			data = f.write(" acuracy: %d" % correct)
			data = f.write(" spike: %d" % spikeNum)
			data = f.write(" cost: %f\n" % cost)
			print("train iter:", iterat, "accuracy:", correct, "spike:", spikeNum, "cost:", cost)
elif cur==datalength-1:
		with open(argv[1], "a") as f:
			data = f.write("test  iter:                               %d" % iterat)
			data = f.write(" accuracy: %d\n" % correct)
			print("test iter:                                          ", iterat, "accuracy:", correct)

print ("finished")
print (time.time() - start_time)
