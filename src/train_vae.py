import os
import sys
import torch
import argparse
from Training import VAETrainer
from Models import VAEModel, VAELossModel
from Dataset import get_stream_vae
from tqdm import tqdm
from torch import nn
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src import DATA_DIR, MODELS_DIR, LOG_DIR

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Train deep protein folder')
	parser.add_argument('-experiment', default='VAETest', help='Experiment name')
	
	parser.add_argument('-image_model', default='Simple', help='Image prediction model')
	parser.add_argument('-dataset_dir', default='data5/pkls', help='Image prediction model')
			
	parser.add_argument('-lr', default=0.0001, help='Learning rate', type=float)
	parser.add_argument('-max_epoch', default=100, help='Max epoch', type=int)
	parser.add_argument('-save_interval', default=10, help='Model saving interval in epochs', type=int)

	args = parser.parse_args()

	torch.cuda.set_device(0)
	
	EXP_DIR = os.path.join(LOG_DIR, args.experiment)
	MDL_DIR = os.path.join(MODELS_DIR, args.experiment)
	try:
		os.mkdir(EXP_DIR)
	except:
		pass
	try:
		os.mkdir(MDL_DIR)
	except:
		pass

	
	image_model = VAEModel().cuda()
	loss_model = VAELossModel().cuda()

	trainer = VAETrainer(	image_model = image_model,
							loss_model = loss_model,
							lr=float(args.lr))
		
	
		
	
	data_path = os.path.join(DATA_DIR, args.dataset_dir)
	if not os.path.exists(data_path):
		raise(Exception("dataset not found", data_path))
		
	stream_train = get_stream_vae(data_path, 'training_set.dat')
	stream_valid = get_stream_vae(data_path, 'validation_set.dat')
	

	for epoch in xrange(args.max_epoch):
		loss_train = []
		loss_valid = []
		
		trainer.new_log(os.path.join(EXP_DIR,"training_loss%d.dat"%epoch))
		for data in tqdm(stream_train):
			loss_train.append(trainer.optimize(data))
		
		trainer.new_log(os.path.join(EXP_DIR,"validation_loss%d.dat"%epoch))
		for data in tqdm(stream_valid):
			loss_valid.append(trainer.predict(data))
		
		print 'Loss train = %f\n Loss valid = %f\n'%(np.mean(loss_train), np.mean(loss_valid))

		if (epoch+1)%args.save_interval==0:
			trainer.save_models(epoch, MDL_DIR)
		