import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet 

AUX_VERBS = [
        'am','is','are',
        'was','were',
        'being','been','be',
        'has','have','had',
        'did','do','does',
        'shall',
        'will','would',
        'should',
        'may','might',
        'must',
        'can','could',
        'need',
        'ought to',
        'dare',
        'going to',
        'be able to',
        'have to',
        'had better',
]
SPACE_AFTER = [
        "}" , ")" , "]" , ">" , ".",
        "," , ";" , ":", "'s",
]
NO_SPACE = ["-",]
# Determiner or Personal pronoun or Preposition or subordinating conjunction
DEPS = ["DT", "IN", "PRP"]
LEADING_VERBS = {
    "VBP":"do",
    "VBZ":"does",
    "VBD":"did",
}

class YesNoQuestion:

    def __init__(self, source):
        self.source = source
        self.questions = []

    def ask(self):
        self.dep()

    # get string made from leaf recursively
    # https://stackoverflow.com/questions/21004181/how-to-get-leaf-nodes-of-a-tree-using-python
    def get_leaf_string(self, root, skip=None):
        leafs = []
        self._collect_leaf_nodes(root,leafs)
        text = ""
        store = ""
        for leaf in leafs:
            if leaf == skip:
                continue
            if leaf == "–" or leaf == "-":
                store = leaf
            elif leaf in SPACE_AFTER or leaf[:1] == '–' or leaf[:1] == "-" or leaf[-1] == "'":
                text += leaf
            else:
                if store != "":
                    text += store + leaf
                    store = ""
                else:
                    text += " " + leaf
        return text.strip(), leafs

    def _collect_leaf_nodes(self, node, leafs):
        if node is not None:
            if not hasattr(node, 'children') or len(node.children) == 0:
                leafs.append(str(node))
            else:
                for n in node.children:
                    self._collect_leaf_nodes(n, leafs)
    
    def dep(self):
        for sent in self.source.sentences:
            question = ''
            np = ''
            aux = ''
            for child in sent.constituency.children[0].children:
                # noun phrase
                if child.label == "NP":
                    for grandchild in child.children:
                        con = grandchild.label
                        text,_ = self.get_leaf_string(grandchild)
                        if con in DEPS:
                            np += text.lower()
                            if np == "i":
                                np = np.upper()
                        else:
                            np += " "+ text
                    np += " "
                # verb phrase
                elif child.label == "VP":
                    for i in range(len(child.children)):
                        grandchild = child.children[i]
                        con = grandchild.label
                        leading = ""
                        aux, arr = self.get_leaf_string(grandchild)
                        if con == "MD" or arr[0] in AUX_VERBS:
                            leading = aux
                        elif con in LEADING_VERBS.keys():
                            leading = LEADING_VERBS[con]
                        else:
                            continue
                        question = leading + " " + np.strip()
                        for j in range(i, len(child.children)):
                            replace = child.children[j]
                            if replace.label == con:
                                word = replace.children[0]
                                lemma = WordNetLemmatizer().lemmatize(str(word), wordnet.VERB)
                                child.children[j] = lemma
                        break
                    
                    text, _ = self.get_leaf_string(child, skip=aux)
                    question += " " + text + "?"
                    question = question.replace(".","").strip()
                    question = question[:1].upper() + question[1:]
                    self.questions.append(question)
