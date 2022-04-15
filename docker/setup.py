import nltk
import stanza
import spacy
from transformers import AutoModelForMaskedLM, AutoTokenizer
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

stanza.download('en')
# stanza.install_corenlp()
spacy.cli.download("en")
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('words', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
model_id = "gpt2-medium"
model = GPT2LMHeadModel.from_pretrained(model_id)
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
# model_name = 'cointegrated/rubert-tiny'
# model = AutoModelForMaskedLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)