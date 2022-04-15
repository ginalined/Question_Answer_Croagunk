import sys
import nltk
from nltk import CFG
from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch
import numpy as np
import logging
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

logging.disable(logging.CRITICAL)
# model_name = "cointegrated/rubert-tiny"
# model = AutoModelForMaskedLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)
model_id = "gpt2-medium"
model = GPT2LMHeadModel.from_pretrained(model_id)
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)


class NLTKProcessor:
    def __init__(self, article=None):
        if article != None:
            self.article = open(article).read()
        # self.skip = set(nltk.corpus.stopwords.words('english'))

    def sentence_segmentation(self):
        self.sentences = nltk.sent_tokenize(self.article)
        return self.sentences

    def word_tokenize(self):
        self.tokenizes = []
        for sentence in self.sentences:
            self.tokenizes.append(nltk.word_tokenize(sentence))
        return self.tokenizes

    def pos_tag(self):
        self.poss = []
        for sentence in self.tokenizes:
            self.poss.append(nltk.pos_tag(sentence))
        return self.poss

    def process(self):
        self.sentence_segmentation()
        self.word_tokenize()
        self.pos_tag()
        self.ner()


if __name__ == "__main__":
    article = sys.argv[1]
    aa = NLTKProcessor(article)
    aa.process()
    print("1. Sentence Segmentation: ", aa.sentences)
    print("2. Word Tokenization: ", aa.tokenizes)
    print("3. POS: ", aa.poss)
    print("4. NER: ", aa.ners)

# https://stackoverflow.com/questions/70464428/how-to-calculate-perplexity-of-a-sentence-using-huggingface-masked-language-mode
def get_score(sentence):
    input_ids = torch.tensor(tokenizer.encode(sentence)).unsqueeze(0) 
    with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
    loss, logits = outputs[:2]
    return np.exp(loss)
    # tensor_input = tokenizer.encode(sentence, return_tensors="pt")
    # repeat_input = tensor_input.repeat(tensor_input.size(-1) - 2, 1)
    # mask = torch.ones(tensor_input.size(-1) - 1).diag(1)[:-2]
    # masked_input = repeat_input.masked_fill(mask == 1, tokenizer.mask_token_id)
    # labels = repeat_input.masked_fill(masked_input != tokenizer.mask_token_id, -100)
    # with torch.inference_mode():
    #     loss = model(masked_input, labels=labels).loss
    # return np.exp(loss.item())
