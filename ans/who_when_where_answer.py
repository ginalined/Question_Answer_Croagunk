class WhoWhenWhereAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""
    
    def who(self):
        return
    
    def when(self):
        return

    def where(self):
        return
    
    def rank(self):
        """
            TODO: there could be multiple potential answers
            we should rank them and select the best.
            Note that # of answers must equal to # of questions.
        """