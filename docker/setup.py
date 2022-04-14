import nltk
import stanza

stanza.download('en')
# stanza.install_corenlp()
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('words', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)