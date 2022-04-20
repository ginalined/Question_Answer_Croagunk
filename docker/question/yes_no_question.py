from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

AUX_VERBS = [
    "am",
    "is",
    "are",
    "was",
    "were",
    "being",
    "been",
    "be",
    "has",
    "have",
    "had",
    "did",
    "do",
    "does",
    "shall",
    "will",
    "would",
    "should",
    "shall",
    "may",
    "might",
    "must",
    "can",
    "could",
    "need",
    "dare",
]
SPACE_AFTER = [
    "}",
    ")",
    "]",
    ">",
    ".",
    ",",
    ";",
    ":",
    "'s",
]
SPACE_BEFORE = [
    "{",
    "(",
    "[",
    "<",
]
NO_SPACE = ["-", "–"]
# Determiner or Personal pronoun or Preposition or subordinating conjunction
DEPS = ["DT", "IN", "PRP", "PRP$"]
LOWER = [
    "DT",
    "IN",
    "PRP",
    "PRP$",
    "JJR",
    "JJS",
]
LEADING_VERBS = {
    "VBP": "do",
    "VBZ": "does",
    "VBD": "did",
}


class YesNoQuestion:
    def __init__(self, source, n):
        self.source = source
        self.n = n * 2
        self.questions = []

    def ask(self):
        self.dep()

    # get string made from leaf recursively
    # https://stackoverflow.com/questions/21004181/how-to-get-leaf-nodes-of-a-tree-using-python
    def get_leaf_string(self, root, skip=None):
        leafs = []
        self._collect_leaf_nodes(root, leafs)
        text = ""
        no_space = ""
        for leaf in leafs:
            if leaf == skip:
                continue
            if leaf in NO_SPACE:
                no_space = leaf
            elif leaf[-1] in NO_SPACE or leaf in SPACE_BEFORE:
                no_space = " " + leaf
            elif leaf in SPACE_AFTER or leaf[:1] in NO_SPACE or leaf[-1] == "'":
                text += leaf
            else:
                if no_space != "":
                    text += no_space + leaf
                    no_space = ""
                else:
                    text += " " + leaf
        return text.strip(), leafs

    def _collect_leaf_nodes(self, node, leafs, lower=False):
        if node is not None:
            if not hasattr(node, "children") or len(node.children) == 0:
                text = str(node)
                if lower:
                    text = text.lower()
                leafs.append(text)
            else:
                for n in node.children:
                    if node.label in LOWER:
                        self._collect_leaf_nodes(n, leafs, lower=True)
                    else:
                        self._collect_leaf_nodes(n, leafs, lower=False)

    def dep(self):
        for i,sentences in enumerate(self.source):   
            try: 
                sent = sentences.sentences[0]
                if len(self.questions) >= 2 * self.n:
                    return
                question = ""
                np = ""
                aux = ""
                for child in sent.constituency.children[0].children:
                    # noun phrase
                    if child.label == "NP":
                        for grandchild in child.children:
                            con = grandchild.label
                            text, _ = self.get_leaf_string(grandchild)
                            if con in DEPS:
                                np += text.lower()
                                if np == "i":
                                    np = "I"
                            else:
                                np += " " + text
                        np += " "
                    # verb phrase
                    elif child.label == "VP":
                        for i in range(len(child.children)):
                            grandchild = child.children[i]
                            con = grandchild.label
                            leading = ""
                            leading_arr = []
                            need_lemma = False
                            aux, arr = self.get_leaf_string(grandchild)
                            if con == "MD" or arr[0] in AUX_VERBS:
                                leading = aux
                                leading_arr = arr
                            elif con in LEADING_VERBS.keys():
                                leading = LEADING_VERBS[con]
                                need_lemma = True
                            else:
                                continue
                            if len(leading) != 0 and len(np.strip()) != 0:
                                if len(leading_arr) > 1:
                                    leading_arr[0] = leading_arr[0] + " " + np.strip()
                                    question = " ".join(leading_arr)
                                else:
                                    question = leading + " " + np.strip()
                                if need_lemma:
                                    for j in range(i, len(child.children)):
                                        replace = child.children[j]
                                        if replace.label == con:
                                            word = replace.children[0]
                                            lemma = WordNetLemmatizer().lemmatize(
                                                str(word), wordnet.VERB
                                            )
                                            child.children[j] = lemma

                                break
                        if len(question) != 0:
                            if len(leading_arr) <= 1:
                                text, _ = self.get_leaf_string(child, skip=aux)
                                question += " " + text
                            question += "?"
                            question = question.replace(".", "").strip()
                            question = question[:1].upper() + question[1:]  # cap first char
                            self.questions.append(question)
            except:
                continue
