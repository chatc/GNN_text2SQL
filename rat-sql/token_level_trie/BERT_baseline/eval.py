import torch.nn as nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn import metrics
from config import *
from utils import *
from model import TransformerMultiClassifier
import time

os.environ['CUDA_VISIBLE_DEVICES'] = '2,3'
time_stamp = time.strftime("%m%d%H%M", time.localtime())


def eval(model, test_loader, cfg):
    # evaluation
    model.eval()
    eval_labels = []
    eval_results = []
    for batch in test_loader:
        # move batch to GPU
        if torch.cuda.is_available() and cfg.use_gpu is True:
            batch = [x.cuda(cfg.device) for x in batch]

        # forward
        classification_logits = model(batch[0], batch[1])[0]
        batch_results = torch.argmax(classification_logits, dim=1).cpu().numpy()

        # add to list
        eval_labels += batch[2].cpu().tolist()
        eval_results += batch_results.tolist()

    f1_micro = metrics.f1_score(eval_labels, eval_results, average='micro')
    f1_macro = metrics.f1_score(eval_labels, eval_results, average='macro')
    f1_weighted = metrics.f1_score(eval_labels, eval_results, average='weighted')
    model.train()

    print(f"[test], f1: micro:{f1_micro}, macro:{f1_macro}, weighted:{f1_weighted}")
    print(batch_results)

if __name__ == '__main__':
    # load config
    cfg = CONFIG()

    # load dataset
    print("Loading dataset...")
    test_data = load_data(cfg.test_path)
    large_testset = get_5type_sequences(test_data)

    # tokenize
    print("Tokenizing...")
    large_testset_token_dict = {x: tokenize_sequences(*y, cfg.pretrain_model_name, cfg.max_input_len,
                                                      label_overwrite=int(cfg.label_dict[x]))
                                for x, y in large_testset.items()}

    # load model and the others
    model = TransformerMultiClassifier(cfg.pretrain_model_name)
    criterion = nn.CrossEntropyLoss(reduction='mean')
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)

    # multi GPU
    if cfg.multi_GPU and torch.cuda.device_count() > 1:
        print(f"Using {torch.cuda.device_count()} GPUs")
        model = nn.DataParallel(model)

    # load model parameters
    if cfg.load_model:
        print("Loading model...")
        params = torch.load(cfg.model_path)
        model.load_state_dict(torch.load(cfg.model_path))

    # move to gpu
    if torch.cuda.is_available() and cfg.use_gpu is True:
        model.cuda(cfg.device)
        criterion.cuda(cfg.device)

    # use data loader (not in GPU)
    larger_test_loader = {x: DataLoader(TensorDataset(*y[0].values(), y[1]),
                                        batch_size=cfg.batch_size, shuffle=False, num_workers=4)
                          for x, y in large_testset_token_dict.items()}
    # start training
    print("starting evaluation")
    for type, loader in larger_test_loader.items():
        print(f"evaluating on type: \"{type}\", size {len(large_testset[type][0])}")
        eval(model, loader, cfg)
