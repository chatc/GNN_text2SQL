import os
import torch

class CONFIG(object):
    def __init__(self):
        # params for train.py(or shared)
        self.learning_rate = 2e-5
        self.max_input_len = 256
        self.batch_size = 32
        self.epoch = 100
        self.data_max_size = 1e9 # use 100 if debuging

        self.pretrain_model_name = "roberta-base"
        self.data_path = "/home/dxy/datasets/output.json"
        # self.model_path = "./checkpoints/07270039_params13.pkl"
        # self.model_path = "../input_classification/params2.pkl"
        self.model_path = "./checkpoints/07301738_params10.pkl"
        self.use_gpu = True
        self.device = 0
        self.save = True
        self.load_model = True
        self.multi_GPU = True

        # params only for eval.py
        self.test_path = "./dataset/type12_trainset.json"

        self.label_dict = {
            'answerable': 0,
            'small talk': 1,
            'ambiguous' : 2,
            'lack data' : 3,
            'unanswerable by sql' : 4
        }

