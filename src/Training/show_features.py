import os
import sys

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import src
from src.Dataset import get_dataset_file
from src.Dataset.waves_dataset import WavesDataset
import matplotlib.pylab as plt

from src.Models import BasicModel

def run_network(batch_size = 10):

	# train_dataset_stream,
	# 				validation_dataset_stream,
	# 				net,
	# 				loss,
	# 				cuda_dev = None,
	# 				learning_rate = 0.001,
	# 				start_epoch = None,
	# 				max_epoch = 100,
	# 				batch_size = 10,
	# 				model_save_period = 10,
	# 				model_save_dir = None,
	# 				logger = None,
	# 				test_visualization = True

	cuda_dev = 0

	torch.manual_seed(42)
	#torch.cuda.set_device(cuda_dev)
	#print 'Current device = ', torch.cuda.current_device()

	net = BasicModel()
	net = net.cuda()

	epoch = 190
	state_dict = torch.load('/home/nina/ML/WavesProject/models/TestCode/net_epoch_%d.pth'%(epoch))
	net.load_state_dict(state_dict)

	w = list(net.parameters())
	#print(w)

	data_folder = get_dataset_file('data_folder')
	dataset = WavesDataset(data_folder, "/home/nina/ML/WavesProject/dataset/training.csv")

	paths, x, y = dataset.__getitem__(10)
	x, y = Variable(x.cuda()), Variable(y.cuda())
	
	#there are some parameters that are not fixed during training
	#this function fixes them 
	net.eval()

	#this function basically runs the network on the batch
	#however, you can run it on a single example just passing 
	#one input without changing anything to the model
	result = net(x[1,:,:,:])

	#and see the output dimension
	print result.size()
				
run_network()