Code for "Undersanding the impact of neural variations and random connection on inference"
Requirement:
1) Install NEURON simulator: https://neuron.yale.edu/neuron/
2) Tensorflow: https://www.tensorflow.org
3) Other libraries: numpy, matplotlib, scipy

Reproduce the result:
1) Computational model parameters fitting experiment under: 1_distirbution 
	 cd 1_distirbution
	 -> python3 distribution.py log.txt to generate the raw data for Fig 4(a)
	 -> python3 normalFit.py to generate the raw data for Fig 4(b)

2) Accuracy comparison between biophysical and computational model experiment under: 2_accuracyCompare 
	 cd 2_accuracyCompare/result/plot
	 -> python3 graph.py to generate Fig 7
	    comment out line 8 and line 10 in graph.py to generate 4(c)
	 -> To generate the raw data
	  cd 2_accuracyCompare 
	  -> python3 tensorflow_compModel.py to get computational model result
	  cd 2_accuracyCompare/biophy
	  -> ./run.sh to get biophysical model result

3) Algorithm and network optimization experiment under: 3_optimization
	 -> python3 ./3_optimization/result/sparse/graph.py to generate Fig 5(a)
	 -> python3 ./3_optimization/result/nin_b/graph.py to generate Fig 5(b)
	 -> python3 ./3_optimization/result/weight/graph.py to generate Fig 5(c)
	 -> python3 ./3_optimization/result/compression/graph.py to generate Fig 5(d)
	 -> python3 ./3_optimization/result/estimator/graph.py to generate Fig 5(e)
	 -> To generate the raw data
	  -> python3 ./3_optimization/tensorflow_compModel.py, set the parameters according to each experiment

4) Neural variation study experiment under: 4_variationStudy
	 -> python3 ./4_variationStudy/fullMnist_result/graph.py to generate Fig 6(a)
	 -> python3 ./4_variationStudy/thVariaition/graph.py to generate Fig 6(b)
	 -> python3 ./4_variationStudy/weightVariation/graph.py to generate Fig 6(c)
	 -> python3 ./4_variationStudy/weightConstraint/graph.py to generate Fig 6(d)
	 -> To generate the raw data
	  -> python3 ./4_variationStudy/tensorflow_compModel.py, set the parameters according to each experiment

