class HowWhatWhyAnswer:
    def __init__(self, sentence, question):
        self.sentence = sentence
        self.question = question
        self.answer = ""
    
    def what(self):
        return
    
    def how(self):
        return
    
    def why(self):
        return
    
    def rank(self):
        """
            TODO: there could be multiple potential answers
            we should rank them and select the best.
            Note that # of answers must equal to # of questions.
        """