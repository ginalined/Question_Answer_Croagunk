import collections
import sys
import stanza
import nltk
from nltk.tree import *
import logging
stanza_logger = logging.getLogger('stanza')
stanza_logger.disabled = True
AUX_VERBS = [
    'am', 'is', 'are',
    'was', 'were',
    'being', 'been', 'be',
    'has', 'have', 'had',
    'did', 'do', 'does',
    'shall',
    'will', 'would',
    'should', 'shall',
    'may', 'might',
    'must',
    'can', 'could',
    'need',
    'dare',
]


class WhQuestion:
    def __init__(self):
        self.stanza = stanza.Pipeline(
            lang='en', processors='tokenize,ner,pos,lemma,depparse,constituency')
        self.article = open("tests/wh_test2.txt").read()
        self.nlp = self.stanza(self.article)
    
        #self.parsed_article = self.sp.sentence_segmentation()

        # print(parsed_article)
        #
        # doc = aa.ners
        # for ent in doc.ents:
        #     print(ent.text, ent.start_char, ent.end_char, ent.label_)
        


    def generate_n_question(self, article):
        pass
    


    def generate_who_question(self, sentence):
        pass

    def print_dep_parse(self):
        msg = ""
        for sent in self.nlp.sentences:
            for word in sent.words:
                msg += 'id: ' + str(word.id) + '\tword: ' + \
                    word.text + '\thead id: ' + str(word.head)
                if word.head > 0:
                    msg += '\thead: ' + sent.words[word.head-1].text
                else:
                    msg += '\thead: root'
                msg += '\tdeprel: ' + word.deprel
                msg += '\n'
            msg += '\n'
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
    def find_verb(self, sentence) -> int:
        
        replaced_aux = "do"
 
        min_dist_verb = [0, float("inf"), None]
        for word in sentence.words:
            if word.pos == "VERB" or word.pos == "AUX":
                dist = self.find_distance_to_root(word.id)
                if dist < min_dist_verb[1]:
                    min_dist_verb = [word.id, dist, word]
                    
        
        if min_dist_verb[2].pos == "AUX":
            return -1, ""
        elif min_dist_verb[0] >1 and self.word_map[min_dist_verb[0]-1].pos == "AUX":
            replaced_aux = self.word_map[min_dist_verb[0]-1].text
        elif min_dist_verb[2].xpos == "VBD":
            replaced_aux = "did"
        elif min_dist_verb[2].xpos == "VBZ":
            replaced_aux = "does"
        
    
        return min_dist_verb[0], replaced_aux
                

    def generate_question(self):

        questions = []

        #self.print_dep_parse()
        for sentence in self.nlp.sentences:
            sentence_text = sentence.text
            self.word_map = collections.defaultdict()
            dependency = sentence.dependencies

            for w in sentence.words:
                self.word_map[w.id] = w
                print(w.id, w.text, w.head,  w.pos, w.xpos, w.upos)
                #[w.id, w.text, w.lemma, w.pos, w.start_char, w.end_char, w.head]


            entities_list = sentence.entities

            constituency = sentence.constituency
            #print(constituency.get_compound_constituents())
            print(constituency.get_root_labels())
            print(constituency.get_unique_tags())
            print(constituency.get_rare_words())
            
            child = constituency.children[0].children
            print(constituency.children[0])
            #Tree.fromstring(str(sentence.constituency)).pretty_print()
            
            main_verb, main_aux = self.find_verb(sentence)
            if main_verb == -1:
                continue


            # generate question based on entities
            #print(entities_list)
            for entity in entities_list:
                output_text = [w.text for w in sentence.words]
            # ask a question about person
                if entity.type == "PERSON":

                    if sentence_text.startswith(entity.text):
                        questions.append(
                            "Who" + sentence_text[len(entity.text):-1] + "?")
                        
                elif entity.type == "":
                    pass

                elif entity.type == "DATE":

                    date_range = [x.id[0] for x in entity.tokens]
                    

                    for entity_id in date_range:
                        output_text[entity_id-1] = ""

                    prev_index, post_index = date_range[0]-1, date_range[-1]+1
                    if prev_index in self.word_map:
                        prev_word = self.word_map[prev_index]
           

                    if prev_word.upos == "ADP":
                        output_text[prev_index-1] = ""
                
                    if post_index in self.word_map:
                        post_word = self.word_map[post_index]
                        if post_word.xpos == ",":
                            output_text[post_index-1] = ""
    
                                   
                    output_text[main_verb - 1] = self.word_map[main_verb].lemma

                    questions.append("When " + main_aux + " " +
                                     " ".join(output_text[:-1]).strip() + "?")

        print(questions)

        # for word in sentence.words:
        #     print(word.text, word.lemma, word.pos)
        # questions = []
        # entities = self.nlp.get_entities(sentence)
        # print(entities)

        # if entities
        # constitution = self.sp.get_con_parse(sentence)
        # print(constitution)
        # self.sp.print_dep_parse(sentence)
        # for entity in entities:
        #     #ask a question about person
        #     if entity.type == "PERSON":
        #         if entity.start_char == 0:
        #             questions.append("Who" + sentence[entity.end_char:-1] + "?" )

        # if entity.type == "DATE":
        #     pass
        # if entity.type == "TIME":

        # print(questions)


newQuestion = WhQuestion()
newQuestion.generate_question()
