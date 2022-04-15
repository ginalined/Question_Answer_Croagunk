import nltk
import stanza
import spacy

stanza.download('en')
# stanza.install_corenlp()
spacy.cli.download("en_core_web_sm")
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('words', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)