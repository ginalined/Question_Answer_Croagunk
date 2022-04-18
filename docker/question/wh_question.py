import collections
from html import entities
import sys
import stanza
import nltk
from nltk.tree import *
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


class Process:
    @staticmethod
    def find_top_level_cons(const):
        res = []
        for x in const.children[0].children:
            if len(x.label) == 0 or not x.label[0].isalpha():
                continue
            res.append([x.label, Process.get_leaf_string(x)[0]])
        # if res == ['NP', 'ADVP', 'VP']:
        #res = [[x.label, ] for x in const.children[0].children]

            # print(Process.get_leaf_string(const.children[0].children)[1])
        return res
        #print(x.label, Process.get_leaf_string(x)[0])
        #print([[x.label, Process.get_leaf_string(x)[0]] for x in const.children[0].children])

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
        self.stanza = stanza.Pipeline(
            lang="en", processors="tokenize,ner,pos,lemma,depparse,constituency"
        )
        self.source = source
        self.n = n * 2
        self.questions = []

        # self.parsed_article = self.sp.sentence_segmentation()

        # print(parsed_article)
        #
        # doc = aa.ners
        # for ent in doc.ents:
        #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

    def ask(self):
        self.questions = self.generate_question()

    def preprocess_sentence(self, sentence):
        pass

    def generate_who_question(self, sentence):
        pass

    def generate_when_question(self, sentence):
        pass

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

    def find_verb(self, sentence):

        replaced_aux = "do"

        min_dist_verb = [0, float("inf"), None]
        for word in sentence.words:
            if word.pos == "VERB" or word.pos == "AUX":
                dist = self.find_distance_to_root(word.id)
                if dist < min_dist_verb[1]:
                    min_dist_verb = [word.id, dist, word]

        if min_dist_verb[2].pos == "AUX":
            return -1, ""
        elif min_dist_verb[0] > 1 and self.word_map[min_dist_verb[0] - 1].pos == "AUX":
            replaced_aux = self.word_map[min_dist_verb[0] - 1].text
        elif min_dist_verb[2].xpos == "VBD":
            replaced_aux = "did"
        elif min_dist_verb[2].xpos == "VBZ":
            replaced_aux = "does"

        return min_dist_verb[0], replaced_aux

    def find_aux(self, w):
    
        replaced_aux = "do"

        if w.pos == "AUX":
            return ""
        elif w.xpos == "VBD":
            replaced_aux = "did"
        elif w.xpos == "VBZ":
            replaced_aux = "does"

        return  replaced_aux

    def retrive_text(self, node) -> str:
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
            return "What organization"
        else:
            return "What"

    def ask_by_np_vp(self, sentence, labels):
        questions = []
        np_text, vp_text = "", ""
        bg_text = False
        for tag, text in labels:
            if tag == "SBAR":
                bg_text = True
            if tag == "NP":
                np_text = text
            elif tag == "VP":
                vp_text = text
                break
        
                
        entities = sentence.entities
        
        orig_verb = vp_text.split(" ")[0]
        lemma_verb = ""
        verb_index = 0
        for i,s in enumerate(sentence.words):
            if s.text == orig_verb:
               lemma_verb = s.lemma
               verb_index = i
               
        
        entities = list(filter(lambda x: x.text in np_text, entities))
        question_starter = "What"
        if entities:
            question_starter = self.get_question_type(entities[0])
        
        if lemma_verb in ["say", "think", "consider", "suggest", "ask"]:
            question_text = "Who"
        
        question_text = question_starter + " " + vp_text + "?"
        questions.append(question_text)
        
        
        if bg_text:
            question_word_text = [w.text for w in sentence.words]
            aux = ""
            aux = self.find_aux(sentence.words[verb_index])
            if not aux:
                aux = orig_verb
                question_word_text[i] = ""
            else:
                question_word_text[i] = lemma_verb
                    
            questions.append(self.format_question("When",self.clean_output(question_word_text), aux))
         
        return questions

    def generate_question(self):
        import collections
        all_questions = []

        all_struct = collections.Counter()
        for complex_sentence in self.source.sentences:
            constituency = complex_sentence.constituency
            
            simple_sentences = self.split_sentence(
                complex_sentence, constituency)

            for sentence in simple_sentences:
                struct = sentence.constituency
                labels = Process.find_top_level_cons(struct)
                label_text = tuple([x[0] for x in labels])
                
            
                if label_text in [('NP', 'VP'), ('NP', 'ADVP', 'VP'), ('NP', 'ADJP', 'VP'), ('SBAR', 'NP', 'VP')]:
                    all_questions += self.ask_by_np_vp(sentence, labels)

                # print(labels)
                #all_struct[tuple(labels)] += 1
        # print(all_struct)
                # print(sentence.dependencies)
                # print(sentence)

        return all_questions

    def generate_question1(self):

        questions = []

        # self.print_dep_parse()
        for complex_sentence in self.source.sentences:

            constituency = complex_sentence.constituency
            print("-----sentence info---------")
            Process.find_top_level_cons(constituency)

            # print(complex_sentence.text)

            print("-----end ---------\n")
            simple_sentences = self.split_sentence(
                complex_sentence, constituency)
            for sentence in simple_sentences:

                try:
                    sentence_text = sentence.text

                    self.word_map = collections.defaultdict()
                    dependency = sentence.dependencies
                    for w in sentence.words:
                        self.word_map[w.id] = w
                        # print(w.id, w.text, w.head,  w.pos, w.xpos, w.upos)
                        # [w.id, w.text, w.lemma, w.pos, w.start_char, w.end_char, w.head]

                    entities_list = sentence.entities

                    main_verb, main_aux = self.find_verb(sentence)
                    if main_verb == -1:
                        continue

                    questions += self.generate_why_question(
                        sentence, main_verb, main_aux
                    )

                    # generate question based on entities

                    if sentence.words[0].pos == "VERB":
                        question_text = ""
                        question_starter = "What"
                        for i, w in enumerate(sentence.words):

                            if w.text != ",":
                                if i == 0:
                                    question_text += w.text.lower()
                                else:
                                    question_text += " " + w.text
                            else:
                                next_word = sentence.words[i + 1]
                                for entity in entities_list:
                                    if next_word.start_char == entity.start_char:
                                        question_starter = self.get_question_type(
                                            entity
                                        )
                                break

                        question_text = self.format_question(
                            question_starter, question_text, "was"
                        )

                        questions.append(question_text)

                    for entity in entities_list:
                        output_text = [w.text for w in sentence.words]
                        question_starter = self.get_question_type(entity)
                        # ask a question about person
                        if entity.type == "PERSON":

                            if sentence_text.startswith(entity.text):
                                questions.append(
                                    question_starter
                                    + sentence_text[len(entity.text): -1]
                                    + "?"
                                )

                        elif entity.type == "DATE" or entity.type == "GPE":

                            date_range = [x.id[0] for x in entity.tokens]

                            for entity_id in date_range:
                                output_text[entity_id - 1] = ""

                            prev_index, post_index = (
                                date_range[0] - 1,
                                date_range[-1] + 1,
                            )
                            if prev_index in self.word_map:
                                prev_word = self.word_map[prev_index]

                            if prev_word.upos == "ADP":
                                output_text[prev_index - 1] = ""

                            if post_index in self.word_map:
                                post_word = self.word_map[post_index]
                                if post_word.xpos == ",":
                                    output_text[post_index - 1] = ""

                            output_text = self.clean_output(
                                output_text, main_verb)

                            question = self.format_question(
                                question_starter, output_text, main_aux
                            )
                            questions.append(question)

                except Exception as e:
                    continue

        return questions
