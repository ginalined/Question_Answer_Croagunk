import collections
from html import entities
import sys
import stanza
import nltk
from nltk.tree import *
import logging
stanza_logger = logging.getLogger('stanza')
stanza_logger.disabled = True


conjunctions = ["because"]
class WhQuestion:
    def __init__(self, processed):
        self.stanza = stanza.Pipeline(
            lang='en', processors='tokenize,ner,pos,lemma,depparse,constituency')
        self.article = open("../tests/wh_test2.txt").read()
        self.nlp = processed
        self.questions = []
    
        #self.parsed_article = self.sp.sentence_segmentation()

        # print(parsed_article)
        #
        # doc = aa.ners
        # for ent in doc.ents:
        #     print(ent.text, ent.start_char, ent.end_char, ent.label_)
        


    def ask(self):
        self.questions = self.generate_question()
    

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
    
    def retrive_text(self,node)->str:
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

                #sentences.append(temp_article.sentences[0])
                sentence_count += 1
        if sentence_count <= 1:
            return [sentence]
        return sentences
    
    def clean_output(self, output_text,main_verb):
        output_text[main_verb - 1] = self.word_map[main_verb].lemma
        output_text = list(filter(lambda x: x!="", output_text))
        output_text = " ".join(output_text[:-1]).strip()
        output_text = output_text.replace(" ,", ",")
        return output_text.strip()
    

            
    def format_question(self,starter, question_text, aux):
        return "{0} {1} {2}?".format(starter, aux,question_text)
    
    def generate_why_question(self, sentence, verb, aux):
        all_result = []
        for conj in conjunctions:
            output_text = [w.text for w in sentence.words]
            if conj not in output_text:continue
            conj_index = output_text.index(conj)
            if conj_index == 0: 
                if "," not in output_text:continue
                comma_index = output_text.index(",")
                output_text = output_text[comma_index+1:]
            else: 
                output_text = output_text[:conj_index]
            output_text = self.clean_output(output_text, verb)
            all_result.append(self.format_question("Why", output_text, aux))
        return all_result
       

        
        """_summary_
        return who when where
        """
    def get_question_type(self, entity)->str:
        if entity.type == "DATE":
            return "When"
        elif entity.type =="TIME":
            return "How long"
        elif entity.type == "GPE":
            return "Where"
        elif entity.type == "PERSON":
            return "Who"
        else:
            return "What"
        
        
    
        
                

    def generate_question(self):

        questions = []

        #self.print_dep_parse()
        for complex_sentence in self.nlp.sentences:
            
            constituency = complex_sentence.constituency
        
            simple_sentences = self.split_sentence(complex_sentence, constituency)
       
            for sentence in simple_sentences:
                try:
                
                    sentence_text = sentence.text

                    self.word_map = collections.defaultdict()
                    dependency = sentence.dependencies
                    for w in sentence.words:
                        self.word_map[w.id] = w
                        #print(w.id, w.text, w.head,  w.pos, w.xpos, w.upos)
                        #[w.id, w.text, w.lemma, w.pos, w.start_char, w.end_char, w.head]

                    entities_list = sentence.entities
        
        
                        
                    main_verb, main_aux = self.find_verb(sentence)
                    if main_verb == -1:
                        continue
                    
                    questions += self.generate_why_question(sentence, main_verb, main_aux)

                    # generate question based on entities
            
                    if sentence.words[0].pos == "VERB":
                        question_text = ""
                        question_starter = "What"
                        for i, w in enumerate(sentence.words):
                            
                            if w.text != ',':
                                if i == 0:question_text +=  w.text.lower()
                                else: question_text += " "+ w.text
                            else:
                                next_word = sentence.words[i+1]
                                for entity in entities_list:
                                    if next_word.start_char == entity.start_char:
                                        question_starter = self.get_question_type(entity)
                                break
                                                           
                        question_text = self.format_question(question_starter, question_text, "was")
                        
                        questions.append(question_text)
                    

                        
    
                                        
                    for entity in entities_list:
                        output_text = [w.text for w in sentence.words]
                        question_starter = self.get_question_type(entity)
                        # ask a question about person
                        if entity.type == "PERSON":

                            if sentence_text.startswith(entity.text):
                                questions.append(
                                question_starter + sentence_text[len(entity.text):-1] + "?")
                            

                        elif entity.type == "DATE" or entity.type == "GPE":

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
                                    
                            output_text = self.clean_output(output_text, main_verb)

                            question = self.format_question(question_starter, output_text, main_aux)
                            questions.append(question)
                            
                except Exception as e:
                    continue
                    
        return questions
                        
                        

                
                


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



