


AUX_VERBS = [
        'am',
        'is',
        'are',
        'was',
        'were',
        'being',
        'been',
        'be',
        'has',
        'have',
        'had',
        'did',
        'shall',
        'will',
        'should',
        'would',
        'may',
        'might',
        'must',
        'can',
        'could',
        'does',
        'do'
        'need',
        'ought to',
        'dare',
        'going to',
        'be able to',
        'have to',
        'had better',
]

class YesNoQuestion:

    def __init__(self, source):
        self.source = source

    def ask(self):
        self.questions = []
        for sent in self.source.sentences:
            question = ''
            the_rest = ''
            for i in range(0, len(sent.words)):
                word = sent.words[i]
                # first word is not proper noun (single/plural)
                if i == 0 and word.xpos != 'NNP' and word.xpos != 'NNPS':
                    word.text = word.text.lower()
                # word is an aux verb or a model
                if (word.text.lower() in AUX_VERBS or word.xpos == 'MD') and len(question) == 0:
                    question += word.text
                # verb past tense
                elif word.xpos == 'VBD' and len(question) == 0:
                    question += 'did'
                    the_rest += ' ' + word.lemma
                elif word.xpos == 'VBP' and len(question) == 0:
                    question += 'do'
                    the_rest += ' ' + word.lemma
                elif word.xpos == 'VBZ' and len(question) == 0:
                    question += 'does'
                    the_rest += ' ' + word.lemma
                elif word.text != '.':
                    the_rest += ' ' + word.text

            if len(question) != 0:
                question += the_rest + '?'
                question = question[:1].upper() + question[1:]
                self.questions.append(question)


