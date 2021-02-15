from __future__ import print_function
import tensorflow as tf
import os
import scipy.io as sio
import numpy as np
import sys

# Set report level//////////////////////////////////////////////////
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
old_v = tf.compat.v1.logging.get_verbosity()

# Parameters///////////////////////////////////////////////////////
preprocessingOn, estimatorOn, adlrOn, privatewOn, seed, sparsity = 1, 1, 1, 1, 0, 40
display_step = 1  #0: print each figure result, 1: print epoch result
training_epochs, batch_size = 1, 1
train_cap, test_cap = 60000, 10000
datalen_train, datalen_test, dim = 60000, 10000, 14
n_input, n_hidden_1, n_classes = dim*dim, 2000, 10
Vth_mean, Vth_std = 0.0066, 0.0019 #0.0062, 0.0018 #0.0058, 0.0017
w1_mean, w1_std = 0.0009, 0.0009 #0.0009, 0.0009 #0.0007, 0.0007
w2_mean, w2_std = 0.0009, 0.03 
learning_rate1, learning_rate2, decay = 0.00001, 0.1, -0.2
estimatorL, estimatorU = 0.0057, 0.0075
expect_ones=26.0
last_accuracy=0.0

# Import MNIST data////////////////////////////////////////////////
if preprocessingOn:
		# Preprocessing
		name_train='../MNIST/pre_processing/MNIST/'+'S_train_ones'+str(expect_ones)+'_dim'+str(dim)+'_datalength'+str(train_cap)
		name_test='../MNIST/pre_processing/MNIST/'+'S_test_ones'+str(expect_ones)+'_dim'+str(dim)+'_datalength'+str(test_cap)

else:
		# Original compression
		name_train='../MNIST/input196_training.mat'
		name_test='../MNIST/input196_testing.mat'

vals=sio.loadmat(name_train)
images1, indexs1 = vals['images'], vals['indexs']
images_train=np.reshape(images1,(train_cap,dim*dim))
indexs_train=np.reshape(indexs1,(train_cap,10))
vals=sio.loadmat(name_test)
images2, indexs2 = vals['images'], vals['indexs']
images_test=np.reshape(images2,(test_cap,dim*dim))
indexs_test=np.reshape(indexs2,(test_cap,10))

param=[[n_input,n_hidden_1,n_classes],[Vth_mean,Vth_std],[w1_mean,w1_std],[w2_mean,w2_std],[learning_rate1,learning_rate2,decay],[preprocessingOn,estimatorOn,adlrOn,privatewOn,seed,sparsity],[estimatorL,estimatorU],expect_ones]
with open("./result/" + str(param), "a") as f:
		data = f.write("epochs:%d" % training_epochs)
		data = f.write(" train length:%d" % datalen_train)
		data = f.write(" test length:%d\n" % datalen_test)
		data = f.write("network size/Vth/w1/w2/lr/[preprocessing, estimator, addlr, privatew, seed, sparsity]/estimator range/ones/:\n")
		data = f.write("%s\n" % param)

print ("prarm:", param)
print ("actual num of ones:", np.count_nonzero(images1)/float(datalen_train))
# Parameters///////////////////////////////////////////////////////

# tf Graph Input//////////////////////////////////////////////////////
x = tf.compat.v1.placeholder(tf.float64, [n_input, None]) 
y = tf.compat.v1.placeholder(tf.float64, [n_classes, None]) 

np.random.seed(seed)
if privatewOn:
		w1 = tf.clip_by_value(w1_mean+np.random.randn(n_hidden_1, n_input) * w1_std, 0, float('Inf'))
else:
		w1 = tf.clip_by_value(w1_mean+np.random.randn(n_hidden_1, n_input) * w1_std, 0, 0.0014)
Min_w1, Max_w1 = w1 * 0.5, w1 * 2.0                  
np.random.seed(seed)
w2 = w2_mean+np.random.randn(n_classes, n_hidden_1) * w2_std
np.random.seed(seed)
Vth = Vth_mean+np.random.randn(n_hidden_1, 1) * Vth_std

weights = {
		'h1': tf.Variable(w1, dtype=tf.float64),
		'out': tf.Variable(w2, dtype=tf.float64)
}

learning_rate={
		'h1': tf.Variable(learning_rate1, dtype=tf.float64),
		'out': tf.Variable(learning_rate2, dtype=tf.float64)
}

# Construct model//////////////////////////////////////////////////////
def sparse (x):
		np.random.seed(seed)
		mask = np.random.randint(0,100,size=x.shape).astype(np.int)
		mask[mask<sparsity] = 1
		mask[mask>=sparsity] = 0
		masks = tf.Variable(mask, dtype=tf.float64)
		connect = x * masks
		return connect

def binary_layer(x):
		result = tf.less(x, tf.Variable(Vth, dtype=tf.float64))
		binaryOut = tf.where(result, tf.zeros(tf.shape(x)), tf.ones(tf.shape(x)))
		binaryOut = tf.cast(binaryOut, dtype=tf.float64)
		return binaryOut

def estimator(x):
		mask1 = tf.less(x, tf.Variable(estimatorL, dtype=tf.float64))
		mask2 = tf.less(x, tf.Variable(estimatorU, dtype=tf.float64))
		mask1 = tf.where(mask1, tf.zeros(tf.shape(mask1)), tf.ones(tf.shape(mask1)))
		mask2 = tf.where(mask2, tf.ones(tf.shape(mask2)), tf.zeros(tf.shape(mask2)))
		mask = mask1 * mask2
		mask = tf.cast(mask, dtype=tf.float64)
		return mask

def weight_constraint(x, Min_w1, Max_w1):
		mask1 = tf.less(Min_w1, x)
		mask2 = tf.greater(Max_w1, x)
		y = tf.where(mask1, x, Min_w1)
		y = tf.where(mask2, y, Max_w1)
		return y

# Front propagation
w1_sparse = sparse(weights["h1"])
layer1 = tf.matmul(w1_sparse, x)
layer1b = binary_layer(layer1)
layer2 = tf.matmul(weights['out'], layer1b)
out_softmax = tf.nn.softmax(tf.transpose(layer2))

pred = tf.argmax(out_softmax,1)
label = tf.argmax(tf.transpose(y),1)
cost = -tf.reduce_sum(tf.transpose(y) * tf.math.log(tf.clip_by_value(out_softmax,1e-200,float('Inf'))), 1)

# Back propagation
grad_layer2 = tf.add(tf.transpose(out_softmax), -y)
grad_w2 = tf.matmul(grad_layer2, tf.transpose(layer1b))
w2_new = weights['out'].assign(weights['out'] - learning_rate['out'] * grad_w2)

grad_layer1b = tf.matmul(tf.transpose(weights['out']), grad_layer2)
if estimatorOn:
	grad_layer1 = grad_layer1b * estimator(layer1)
else:
	grad_layer1 = grad_layer1b
grad_w1 = tf.matmul(grad_layer1, tf.transpose(x))
if privatewOn:
		constraintW = weight_constraint(weights['h1'] - learning_rate['h1'] * grad_w1, Min_w1, Max_w1)
else:		
		constraintW = tf.clip_by_value(weights['h1'] - learning_rate['h1'] * grad_w1, 0, 0.0014)
w1_new = weights['h1'].assign(constraintW)

spike=tf.math.count_nonzero(layer1b)
# Run /////////////////////////////////////////////////////////////////
init = tf.compat.v1.global_variables_initializer()
with tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(allow_soft_placement=True,gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.05))) as sess:
		sess.run(init)

		# Training
		for epoch in range(training_epochs):
				correct_num = 0.
				avg_cost = 0
				avg_ones = 0
				correct_num1 = 0.
				avg_cost1 = 0
				for i in range(datalen_train):
						
						# Input
						batch_xs, batch_ys = images_train[i].reshape(n_input,1), indexs_train[i].reshape(10,1)
						
						# Run optimization op (backprop) 
						_, _, c, p, t= sess.run([w1_new, w2_new, cost, pred, label],
																				 feed_dict={x: batch_xs,y: batch_ys})
						

						# Compute average loss
						avg_cost += c / datalen_train
						#avg_ones += float(s) / datalen_train

						# Accuracy for each images 
						if p==t:
								correct_num+=1
								if display_step==0:
									print ("predict/label:", p, t, "correct", correct_num)
						elif display_step==0:
								print ("predict/label:", p, t, "wrong", correct_num)
						
				# Accuracy for each epoch
				accuracy = correct_num / datalen_train
				if display_step:
						#print ("Training Epoch:", epoch+1, "Cost:", avg_cost, "Accuracy:", accuracy)
						with open("./result/" + str(param), "a") as f:
								data = f.write("train epochs: %d " % epoch)
								data = f.write(" avg_cost: %f " % avg_cost)
								data = f.write(" avg_ones: %f " % avg_ones)
								data = f.write(" accuracy: %f\n" % accuracy)

		 		#Test model
				#correct_prediction = tf.equal(pred, label)
				#accur = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
				#accuracy=accur.eval({x: images_train.transpose(), y: indexs_train.transpose()})
				#with open("./result/" + str(param), "a") as f:
				#		data = f.write("test  epochs: %d " % epoch)
				#		data = f.write(" accuracy: %f\n" % accuracy)
				
				############################################################################################
				for i in range(datalen_test):
						
						# Input
						batch_xs, batch_ys = images_test[i].reshape(n_input,1), indexs_test[i].reshape(10,1)
						
						# Run optimization op (backprop) 
						c, p, t= sess.run([cost, pred, label],
																				 feed_dict={x: batch_xs,y: batch_ys})
						

						# Compute average loss
						avg_cost1 += c / datalen_test
						#avg_ones += float(s) / datalen_test

						# Accuracy for each images 
						if p==t:
								correct_num1+=1
								if display_step==0:
									print ("predict/label:", p, t, "correct", correct_num1)
						elif display_step==0:
								print ("predict/label:", p, t, "wrong", correct_num1)
						
						
				# Accuracy for each epoch
				accuracy1 = correct_num1 / datalen_test
				if display_step:
						#print ("Testing Epoch:", epoch+1, "Cost:", avg_cost, "Accuracy:", accuracy)
						with open("./result/" + str(param), "a") as f:
								data = f.write("test epochs: %d " % epoch)
								data = f.write(" avg_cost: %f " % avg_cost1)
								#data = f.write(" avg_ones: %f " % avg_ones)
								data = f.write(" accuracy: %f\n" % accuracy1)

				############################################################################################
				#Adaptive learning rate
				if adlrOn:
						if  accuracy< last_accuracy:
								lr1 = learning_rate['h1'].assign(learning_rate['h1'] * tf.cast(tf.exp(decay), dtype=tf.float64))
								lr2 = learning_rate['out'].assign(learning_rate['out'] * tf.cast(tf.exp(decay), dtype=tf.float64))
								ll1, ll2 = sess.run([lr1, lr2])
						last_accuracy=accuracy
				

