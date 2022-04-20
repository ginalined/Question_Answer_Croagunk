from cProfile import label
import collections
from html import entities
import sys
import stanza
import nltk
from nltk.tree import *
from torch import true_divide
from processor.stanza_process import StanzaProcessor
import logging

stanza_logger = logging.getLogger("stanza")
stanza_logger.disabled = True


conjunctions = ["because"]


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
NO_SPACE = ["-", "-"]
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


class Process:
    @staticmethod
    def find_top_level_cons(const):
        res = []
        for x in const.children[0].children:
            if len(x.label) == 0 or not x.label[0].isalpha():
                continue
            if x.label in ['ADVP','ADJP']:
                continue
            res.append([x.label, Process.get_leaf_string(x)[0], x])

        return res


    @staticmethod
    def collect_leaf_nodes(node, leafs, lower=False):
        if node is not None:
            if not hasattr(node, "children") or len(node.children) == 0:
                text = str(node)
                if lower:
                    text = text.lower()
                leafs.append(text)
            else:
                for n in node.children:
                    if node.label in LOWER:
                        Process.collect_leaf_nodes(n, leafs, lower=True)
                    else:
                        Process.collect_leaf_nodes(n, leafs, lower=False)

    @staticmethod
    def get_leaf_string(root, skip=None):
        leafs = []
        Process.collect_leaf_nodes(root, leafs)
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


class WhQuestion:
    def __init__(self, source, n):

        self.source = source
        self.n = n
        self.questions = []

    def ask(self):
        self.questions = self.generate_question()


    def print_dep_parse(self):
        msg = ""
        for sent in self.source.sentences:
            for word in sent.words:
                msg += (
                    "id: "
                    + str(word.id)
                    + "\tword: "
                    + word.text
                    + "\thead id: "
                    + str(word.head)
                )
                if word.head > 0:
                    msg += "\thead: " + sent.words[word.head - 1].text
                else:
                    msg += "\thead: root"
                msg += "\tdeprel: " + word.deprel
                msg += "\n"
            msg += "\n"
        print(msg)

        """_summary_
        """

    def find_distance_to_root(self, item_id):
        count = 0
        while item_id != 0:
            item_id = self.word_map[item_id].head
            count += 1
        return count

        """_summary_
        find the main very of the sentence, 
        return the id of the verb word
        """

    def find_aux(self, w):
    
        replaced_aux = "do"

        if w.pos == "AUX":
            return ""
        elif w.xpos == "VBD":
            replaced_aux = "did"
        elif w.xpos == "VBZ":
            replaced_aux = "does"

        return  replaced_aux

    def retrive_text(self, node):
        if len(node.children) == 0:
            return node.label
        else:
            text = ""
            for child in node.children:
                text += " " + self.retrive_text(child)

        return text.strip()

    def split_sentence(self, sentence, constituency):

        sentences = []
        child = constituency.children[0].children
        sentence_count = 0
        for c in child:
            if c.label == "S":
                text = self.retrive_text(c)
                temp_article = self.stanza(text).sentences[0]
                sentences += self.split_sentence(temp_article, c)

                # sentences.append(temp_article.sentences[0])
                sentence_count += 1

        if sentence_count <= 1:
            return [sentence]
        return sentences

    def clean_output(self, output_text):
        # output_text[main_verb - 1] = self.word_map[main_verb].lemma
        # output_text[0] = self.word_map[1].lemma
        output_text = list(filter(lambda x: x != "", output_text))
        output_text = " ".join(output_text[:-1]).strip()
        output_text = output_text.replace(" ,", ",")
        return output_text.strip()

    def format_question(self, starter, question_text, aux):
        return "{0} {1} {2}?".format(starter, aux, question_text)

    def generate_why_question(self, sentence, verb, aux):
        all_result = []
        for conj in conjunctions:
            output_text = [w.text for w in sentence.words]
            if conj not in output_text:
                continue
            conj_index = output_text.index(conj)
            if conj_index == 0:
                if "," not in output_text:
                    continue
                comma_index = output_text.index(",")
                output_text = output_text[comma_index + 1:]
            else:
                output_text = output_text[:conj_index]
            output_text = self.clean_output(output_text, verb)
            all_result.append(self.format_question("Why", output_text, aux))
        return all_result

        """_summary_
        return who when where
        """

    def get_question_type(self, entity):
        if entity.type == "DATE":
            return "When"
        elif entity.type == "TIME":
            return "How long"
        elif entity.type == "GPE":
            return "Where"
        elif entity.type == "PERSON":
            return "Who"
        elif entity.type == "ORG":
            return "Where"
        else:
            return "What"
        
    
        
    def ask_by_pp(self, sentence, labels):
        questions = []
        np_text, vp_text, pp_text = "", "", ""
        
        for tag, text, _ in labels:
            if tag == "PP":
                pp_text = text
            elif tag == "NP":
                np_text = text
            elif tag == "VP":
                vp_text = text
                break
        entities = sentence.entities
        entities = list(filter(lambda x: x.text in pp_text and x.type in ["DATE", "TIME","GEO", "ORG"], entities))
        if not entities:
            return questions
    
        question_starter = self.get_question_type(entities[0])
        
        aux, vp_text = self.find_verb_index(sentence, vp_text)
        if not aux:
            return questions

        question_word_text = np_text + " " + vp_text
        questions.append(self.format_question(question_starter,question_word_text, aux))
        return questions


    def ask_by_np_vp(self, sentence, labels):
        questions = []
        np_text, vp_text, pp_text = "", "", ""
        bg_text = False
        for tag, text, _ in labels:
            if tag == "SBAR":
                bg_text = True
            if tag == "NP":
                np_text = text
            elif tag == "VP":
                vp_text = text
                break
        
                
        entities = sentence.entities
        entities = list(filter(lambda x: x.text in np_text, entities))
        
        question_starter = "What"
        if entities:
            question_starter = self.get_question_type(entities[0])
        
        if question_starter == "Who":
            splited_vp = vp_text.split(" ")
            first_verb = splited_vp[0]

            if not first_verb.endswith("s") and not first_verb.endswith("d"): 
                for w in sentence.words:
                    if w.text == first_verb:
                        break

                if w.xpos == "VBP":
                    vp_text = first_verb +"s " + " ".join(splited_vp[1:])
        
        question_text = question_starter + " " + vp_text + "?"
        
        if question_text.count(" ")>=5:
            questions.append(question_text)
        
        
        
        if bg_text:
            aux, vp_text = self.find_verb_index(sentence, vp_text)
            if not aux:
                return questions
            question_word_text = np_text + " " + vp_text
            if question_word_text.count(" ")>=5:
                questions.append(self.format_question("When",question_word_text, aux))
            return questions
         
    
        return questions

    def find_verb_index(self, sentence, vp_text):
        orig_verb = vp_text.split(" ")[0]
        lemma_verb = ""
        verb_index = 0
        aux = ""
        
        sentence_after_ver = []
        
        in_scope = False
   
        for i,s in enumerate(sentence.words):
            
            #start vp text
            if s.text == orig_verb:
                
                sentence_after_ver = [w.text for w in sentence.words[i:]]
               
                if s.pos == "AUX":
                    aux = sentence_after_ver[0]
                    sentence_after_ver[0] = ""
                    #this sentence is not usable
                    if i+1 == len(sentence.words) or sentence.words[i+1].pos != "VERB":
                        return "", ""
                else:
                    aux = self.find_aux(s)
                    sentence_after_ver[0] = s.lemma
                break
              
        new_vp_text = self.clean_output(sentence_after_ver)  
        return aux, new_vp_text

    def generate_question(self):
        all_questions = []
        import collections
        c = collections.Counter()
        
        for i,sentences in enumerate(self.source):    
            if len(all_questions) >= 3 * self.n:
                return all_questions
            sentence = sentences.sentences[0]
 
            labels = Process.find_top_level_cons(sentence.constituency)
            label_text = tuple([x[0] for x in labels])
            c[label_text] += 1

            if label_text in [('NP', 'VP'), ('NP', 'ADVP', 'VP'), ('NP', 'ADJP', 'VP'), ('SBAR', 'NP', 'VP')]:
                all_questions += self.ask_by_np_vp(sentence, labels)
                
            
                
            if label_text and label_text == ('PP', 'NP', 'VP'):
                all_questions += self.ask_by_pp(sentence, labels)
        
        for i, question in enumerate(all_questions):
            all_questions[i] = question.replace(" n't ", "n't ")
        
        return all_questions


