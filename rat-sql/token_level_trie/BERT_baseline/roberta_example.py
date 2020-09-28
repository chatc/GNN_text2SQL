import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from input_classification.config import *

if __name__ == '__main__':

    tokenizer = AutoTokenizer.from_pretrained("roberta-large")
    model = AutoModelForSequenceClassification.from_pretrained("roberta-large")

    classes = ["not paraphrase", "is paraphrase"]

    sequence_0 = "The company HuggingFace is based in New York City"
    sequence_1 = "Apples are especially bad for your health"
    sequence_2 = "HuggingFace's headquarters are situated in Manhattan"

    paraphrase = tokenizer.encode_plus(sequence_0, sequence_2, return_tensors="pt")
    not_paraphrase = tokenizer.encode_plus(sequence_0, sequence_1, return_tensors="pt")

    cfg = CONFIG()

    criterion = nn.CrossEntropyLoss(reduction='mean')
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)

    for i in range(100):
        paraphrase_classification_logits = model(**paraphrase)[0]
        not_paraphrase_classification_logits = model(**not_paraphrase)[0]

        paraphrase_results = torch.softmax(paraphrase_classification_logits, dim=1).tolist()[0]
        not_paraphrase_results = torch.softmax(not_paraphrase_classification_logits, dim=1).tolist()[0]

        logits = torch.cat((paraphrase_classification_logits, not_paraphrase_classification_logits), dim=0)
        labels = torch.LongTensor([1, 0])
        loss = criterion(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"round:{i}, loss:{loss}")


        print("Should be paraphrase")
        for i in range(len(classes)):
            print(f"{classes[i]}: {round(paraphrase_results[i] * 100)}%")

        print("\nShould not be paraphrase")
        for i in range(len(classes)):
            print(f"{classes[i]}: {round(not_paraphrase_results[i] * 100)}%")