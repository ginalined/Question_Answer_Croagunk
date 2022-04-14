from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from stanza.server import CoreNLPClient
from processor.stanza_process import StanzaProcessor


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
NO_SPACE = [
    "-",
]
# Determiner or Personal pronoun or Preposition or subordinating conjunction
DEPS = ["DT", "IN", "PRP", "PRP$"]
LOWER = [
    "DT",
    "IN",
    "PRP",
    "PRP$",
    "JJ",
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
            if leaf == "–" or leaf == "-":
                no_space = leaf
            elif leaf[-1] == "-" or leaf[-1] == "–":
                no_space = " " + leaf
            elif (
                leaf in SPACE_AFTER
                or leaf[:1] == "–"
                or leaf[:1] == "-"
                or leaf[-1] == "'"
            ):
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
        # with CoreNLPClient(
        #     properties="english",
        #     annotators=["coref"],
        #     be_quiet=True,
        # ) as client:
            for paragraph in self.source:
                if len(self.questions) >= self.n:
                    return self.questions
                processed_paragraph = StanzaProcessor(sentence=paragraph).process()
                # ann = client.annotate(paragraph)
                # print(ann.corefChain)
                for sent in processed_paragraph.sentences:
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
                                need_lemma = False
                                aux, arr = self.get_leaf_string(grandchild)
                                if con == "MD" or arr[0] in AUX_VERBS:
                                    leading = aux
                                elif con in LEADING_VERBS.keys():
                                    leading = LEADING_VERBS[con]
                                    need_lemma = True
                                else:
                                    continue
                                if len(leading) != 0 and len(np) != 0:
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
                                text, _ = self.get_leaf_string(child, skip=aux)
                                question += " " + text + "?"
                                question = question.replace(".", "").strip()
                                question = question[:1].upper() + question[1:]
                                self.questions.append(question)
