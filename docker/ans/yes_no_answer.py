import random
import spacy

from stanza.pipeline.external import spacy


class YesNoAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""

    def load_sentence(self,sentence):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(sentence)
        ner_lst = set()
        for ent in doc.ents:
            ner_lst.add(ent.lemma_)

        return ner_lst, doc

    def compare_NER(sentence_ner, question_ner):
        # TODO: check is question has NER
        result = False
        if not question_ner:
            return True, None

        only_question_ner = question_ner - sentence_ner

        result = (len(only_question_ner) == 0)

        return result, only_question_ner

    def find_negation(question, sentence):
        found_negative = False
        # find root of question:
        q_root_token = None
        for token in question:
            if token.dep_ == 'ROOT':
                q_root_token = token

        if q_root_token:
            for token in sentence:
                if token.dep_ == 'neg':
                    # print(token.head.lemma_, q_root_token.lemma_)
                    # print(token.similarity(q_root_token))
                    if token.head.lemma_ == q_root_token.lemma_ or token.similarity(q_root_token) >= 0.6:
                        found_negative = True

        return found_negative

    def yesno(self):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.sentence)
        ner_lst = set()
        for ent in doc.ents:
            ner_lst.add(ent.lemma_)
        question_ner = ner_lst
        q_doc = doc

        doc = nlp(self.question)
        ner_lst = set()
        for ent in doc.ents:
            ner_lst.add(ent.lemma_)
        sentence_ner = ner_lst
        s_doc = doc

        compare_ner_result, only_question_ner = self.sentence.compare_NER(sentence_ner, question_ner)
        if not compare_ner_result:
            if only_question_ner and random.randint(1, 10) > 4:
                answer = ('No, it should not be {}.'.format(str(only_question_ner.pop())))
            else:
                answer = "No"
        elif self.sentence.find_negation(q_doc, s_doc):
            answer = "No"
        else:
            answer = "Yes"
        return answer

