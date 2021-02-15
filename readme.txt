Code for "Undersanding the impact of neural variations and random connection on inference"
Requirement:
1) Install NEURON simulator: https://neuron.yale.edu/neuron/
2) Tensorflow: https://www.tensorflow.org

Reproduce the result:
1) Computational model parameters fitting experiment under: 1_distirbution 
	 -> python3 ./1_distirbution/distribution.py to generate the raw data for Fig 4(a)
	 -> python3 ./1_distirbution/normalFit.py to generate the raw data for Fig 4(b)

2) Accuracy comparison between biophysical and computational model experiment under: 2_accuracyCompare 
	 -> python3 ./2_accuracyCompare/result/plot/graph.py to generate Fig 4(c)

3) Computational model optimization experiment under: 3_optimization
	 -> python3 ./3_optimization/result/sparse/graph.py to generate Fig 5(a)
	 -> python3 ./3_optimization/result/nin_b/graph.py to generate Fig 5(b)
	 -> python3 ./3_optimization/result/weight/graph.py to generate Fig 5(c)
	 -> python3 ./3_optimization/result/compression/graph.py to generate Fig 5(d)
	 -> python3 ./3_optimization/result/estimator/graph.py to generate Fig 5(e)

4) Neural variation study experiment under: 4_variationStudy
   -> python3 ./4_variationStudy/fullMnist_result/graph.py to generate Fig 6(a)
   -> python3 ./4_variationStudy/thVariaition/graph.py to generate Fig 6(b)
   -> python3 ./4_variationStudy/weightVariation/graph.py to generate Fig 6(c)
   -> python3 ./4_variationStudy/weightConstraint/graph.py to generate Fig 6(d)

