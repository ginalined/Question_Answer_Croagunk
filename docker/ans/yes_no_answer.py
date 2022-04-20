import random

class YesNoAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""
    
    def yesno(self):
        # for testing
        # return str(bool(random.getrandbits(1)))
        answer = "Yes"
        # if NERS unmatching
        for ner in self.sentence.ents:
            if ner.text not in self.question.words:
                answer = "No"
        # if parts match with not
        for token in self.question.words:
            if token.text not in str(self.question.text) :
                if token.text.endswith("n't") or token.tect.endswith('not') or token.text.endswith('no'):
                    answer = "No"
        return answer

    
    def rank(self):
        """
            TODO: there could be multiple potential answers
            we should rank them and select the best.
            Note that # of answers must equal to # of questions.
        """
        best_id = 0
        best_similarity = -1
        # 1. calculate the frequency of words
        lemmas = []
        for token in self.sentence.ents:
            lemmas.append(token.lemma_)
        term_f = {}
        for word in lemmas:
            term_f[word] = term_f.get(word, 0) + 1
        # 2. vectorize sentence
        vector_question = {}
        word_f = {}
        for word in term_f:
            vector_question[word] = term_f[word] * word_f.get(word, 0)

        # 3. calculate similarity
        sentences = []
        for sentence_id in range(len(sentences)):
            similarity = 0
            qvalue = 0
            svalue = 0
            for vq in vector_question:
                if vq in sentences[sentence_id]: # should be fixed later
                    similarity += vector_question * sentences[sentence_id]
                    qvalue += vector_question ** 2
                    svalue += sentences[sentence_id] ** 2
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_idx = sentence_id
        return sentences[best_idx]