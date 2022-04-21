class WhoWhenWhereAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""
    
    def who(self):
        answers = []
        for ent in self.sentence.ents:
            if ent.type == "PERSON":
                answers.append(ent.text) # could be used for ranking
                return ent.text
        return "Who: can't find answer"
    
    def when(self):
        answers = []
        for ent in self.sentence.ents:
            if ent.type == "DATE":
                answers.append(ent.text) # could be used for ranking
                return ent.text
        return "when can't find answer"

    def where(self):
        answers = []
        for ent in self.sentence.ents:
            if ent.type == "GPE":
                answers.append(ent.text) # could be used for ranking
                return ent.text
        return "where can't find answer"
    


