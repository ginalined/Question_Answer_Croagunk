class WhoWhenWhereAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""
    
    def who(self):
        num = 0
        answer = ""
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                num = num + 1
                answer = ent.text
        if num > 1:
            return self.sentence.text
        if num == 1:
            return answer
        return "Who: can't find answer"
    
    def when(self):
        num = 0
        answer = ""
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                num = num + 1
                answer = ent.text
        if num > 1:
            return self.sentence.text
        if num == 1:
            return answer
        return "when can't find answer"

    def where(self):
        num = 0
        answer = ""
        for ent in self.sentence.ents:
            if ent.text not in self.question.text:
                num = num + 1
                answer = ent.text
        if num > 1:
            return self.sentence.text
        if num == 1:
            return answer
        return "where can't find answer"






