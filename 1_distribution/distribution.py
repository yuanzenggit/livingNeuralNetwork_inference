from neuron import h,gui
import numpy 
import random as random
import sys
from sys import argv
from matplotlib import pyplot
from random import randint

###############################################################
#            Initial the Network and Parameters               #
###############################################################
#Parameters with variation

#light parameters
light_on=0
light_off=5
N_CHR2=[1500,2000,1480,1400] 
e_CHR2_pre=10
e_CHR2_post=0

#cell parameters
cap=[10,8,10,15,15,10,8,8,10] 
e_pas=[-45,-40,-45,-35,-45,-56,-50,-60,-60]
g_pas=[1.1E-3,8.5E-4,1.48E-3,1.15E-3,1.48E-3,2.1E-3,8E-4,7E-4,1.1E-3]
gmax_nafPR=[8E-2,6E-2,1.5E-1,2.9E-1,2.5E-1,9E-2,7E-2,8E-2,1.1E-1]
gmax_kdr=[2E-2,2E-2,0.5E-2,2E-2,1E-2,9.9E-2,2E-2,6E-2,12E-2]
gmax_rkq=[1E-2,9E-3,1E-3,4.5E-3,1E-3,3E-2,5E-3,12E-2,5E-3]
gmax_cal=[8E-3,8E-3,8E-3,8E-3,8E-3,8E-3,8E-3,8E-3,8E-3]
gmax_kcRT03=[2E-2,2E-2,2E-2,2.5E-2,1E-1,2E-1,2E-2,1E-1,2E-2]

#synapse parameters
dlist=[1.8,2,1.3,1.4,2,2,1.3,2,2,2,2,2] 
glist=[0.00072,0.00041,0.00228,0.00117,0.00021,0.00115,0.00063,0.00069,0.00073,0.00034,0.00059,0.00059] 
tlist=[4.5,6.99,4.75,4.4,6,5.95,6.96,5.75,7.8,4.55,5.7,4.9]

###############################################################
resultlist=[]
for cellnum in range (0,9): #different post synaptic neuron 
	spikelist=[0]*20
	for time in range (0,1000): #number of experiment
				
				lightlist=[]
				celllist=[]
				synapselist=[]
				for i in range (20):
						lightlist.append(randint(0,3))
						celllist.append(randint(0,7))
						synapselist.append(randint(0,11)) 

				for num in range (2,20): #number of pre synaptic neurons

						#network parameters
						Numin,Numhidden=num,1
						Numtotal=Numin+Numhidden

						h('''
						inputNum=0
						hiddenNum=0
						outputNum=0
						totalSyn=0
						totalNeuron=0
						density=0
						''')

						h.inputNum=Numin
						h.hiddenNum=Numhidden
						h.totalSyn=h.inputNum*h.hiddenNum
						h.totalNeuron=h.inputNum+h.hiddenNum
						h.density=100
						
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

						delay=0
						double weights1[totalSyn]
						double tau[totalSyn]
						''')

						#1. light initial
						h.light_on=light_on
						h.light_off=light_off
						for i in range (Numtotal):
								indexCurrent=lightlist[i]
								h.in_N_CHR2[i]=N_CHR2[indexCurrent]
								if i<Numin: #pre
										h.in_e_CHR2[i]=e_CHR2_pre
								else: #post
										h.in_e_CHR2[i]=e_CHR2_post
						
						#2. neuron initial
						for i in range (Numtotal):
								if i<Numin: #pre
										indexCurrent=celllist[i]
										h.in_cap[i]=cap[indexCurrent]
										h.in_e_pas[i]=e_pas[indexCurrent]
										h.in_g_pas[i]=g_pas[indexCurrent]
										h.in_gmax_nafPR[i]=gmax_nafPR[indexCurrent]
										h.in_gmax_kdr[i]=gmax_kdr[indexCurrent]
										h.in_gmax_rkq[i]=gmax_rkq[indexCurrent]
										h.in_gmax_cal[i]=gmax_cal[indexCurrent]
										h.in_gmax_kcRT03[i]=gmax_kcRT03[indexCurrent]
								else: #post
										indexCurrent=cellnum
										h.in_cap[i]=cap[indexCurrent]
										h.in_e_pas[i]=e_pas[indexCurrent]
										h.in_g_pas[i]=g_pas[indexCurrent]
										h.in_gmax_nafPR[i]=gmax_nafPR[indexCurrent]
										h.in_gmax_kdr[i]=gmax_kdr[indexCurrent]
										h.in_gmax_rkq[i]=gmax_rkq[indexCurrent]
										h.in_gmax_cal[i]=gmax_cal[indexCurrent]
										h.in_gmax_kcRT03[i]=gmax_kcRT03[indexCurrent]


						#3. weight initial
						weights1=[[numpy.random.randn() for row in range(0,Numin)] for col in range(0,Numhidden)]
						tau=[[numpy.random.randn() for row in range(0,Numin)] for col in range(0,Numhidden)]
						delay=[[numpy.random.randn() for row in range(0,Numin)] for col in range(0,Numhidden)]
						for j in range (Numhidden):
								for i in range (Numin):
										indexCurrent=synapselist[i]
										weights1[j][i]=glist[indexCurrent]
										tau[j][i]=tlist[indexCurrent]
										delay[j][i]=dlist[indexCurrent]

						for j in range (Numhidden):
								for i in range (Numin):
										h.weights1[i+j*Numin]=weights1[j][i]
										h.tau[i+j*Numin]=tau[j][i]
										h.delay[i+j*Numin]=delay[j][i]

						#4. initial the network
						h('''
						load_file("nrngui.hoc")
						load_file("net_new.hoc")
						objref snn
						snn=new fullynet(inputNum, hiddenNum, light_on, light_off, &in_N_CHR2, &in_e_CHR2, &in_cap, &in_e_pas, &in_g_pas, &in_gmax_nafPR, &in_gmax_kdr, &in_gmax_rkq, &in_gmax_cal, &in_gmax_kcRT03, &weights1, &tau, delay, density)

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

						def annot_max(x,y, ax=None):
								xmax = x[numpy.argmax(y)]
								ymax = numpy.array(y).max()
								text= "x={:.4f}, y={:.4f}".format(xmax, ymax)
								if not ax:
										ax=pyplot.gca()
								bbox_props = dict(boxstyle="square,pad=0.4", fc="w", ec="k", lw=0.8)
								arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
								kw = dict(xycoords='data',textcoords="axes fraction",
										arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
								ax.annotate(text, fontsize=12, xy=(xmax, ymax), xytext=(0.94,1), **kw)

						post_v=[0]*Numhidden
						t_vec=[0]*Numhidden
						pre_v=[0]*Numin
						gsyn0_v=[0]*Numin
						gsyn1_v=[0]*Numin

						for i in range (Numhidden):
							t_vec[i]=h.Vector()
							t_vec[i].record(h._ref_t)
							post_v[i]=h.Vector()
							post_v[i].record(h.snn.post[0].soma(0.5)._ref_v)
							
						for i in range (Numin):	
							pre_v[i]=h.Vector()
							pre_v[i].record(h.snn.pre[0].soma(0.5)._ref_v)
							gsyn0_v[i]=h.Vector()
							gsyn0_v[i].record(h.snn.outputSyn[0]._ref_g)
							gsyn1_v[i]=h.Vector()
							gsyn1_v[i].record(h.snn.outputSyn[1]._ref_g)

						h.tstop=200
						h.run()
						
						if max(post_v[0])>0:
							spikelist[num]+=1
							with open(argv[1], "a") as f:
									data = f.write("cellnum:%f " % cellnum)
									data = f.write("exp time:%f " % time)
									data = f.write("spikelist:%s \n" % spikelist)

							break
	
	with open(argv[1], "a") as f:
			data = f.write("finallist:%s \n" % spikelist)
	resultlist.append(spikelist)
print (resultlist)

