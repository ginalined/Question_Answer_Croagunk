from stanfordcorenlp import StanfordCoreNLP
from nltk import sent_tokenize


def per_count(sentence):
    ner_sentence = nlp.ner(sentence)
    count = 0
    names = []
    for i, token in enumerate(ner_sentence):
        if token[1] != 'O' and (i == 0 or token[1] != ner_sentence[i-1][1]):
            count += 1
            names.append(token[0])
        elif token[1] != 'O':
            names[-1] += ' ' + token[0]
    return names, count


if __name__ == '__main__':
    nlp = StanfordCoreNLP('http://localhost', 9000)
    sentence = '''Harry Potter and the Prisoner of Azkaban is a 2004 fantasy film directed by Alfonso Cuarón and distributed by Warner Bros. Pictures. It is based on the novel of the same name by J. K. Rowling. The film, which is the third instalment in the Harry Potter film series, was written by Steve Kloves and produced by Chris Columbus (director of the first two instalments), David Heyman, and Mark Radcliffe. 
    '''
    print(sentence + '\n')
    sent_parsed = sent_tokenize(sentence)
    print("Sentence Segmentation:", sent_parsed)
    print("Number of sentence is: ", len(sent_parsed), '\n')
    print('Tokenize: ', nlp.word_tokenize(sentence))
    print("Number of token is: {0}".format(len(nlp.word_tokenize(sentence))))
    print("")
    print('Part of Speech:', nlp.pos_tag(sentence), '\n')

    print('Named Entities:', nlp.ner(sentence))
    names, count = per_count(sentence)
    print("Name Count is:", count)
    print("Names are:", names)
    print("")
    print('Constituency Parsing: ', nlp.parse(sentence))
    print("")
    print('Dependency Parsing:', nlp.dependency_parse(sentence))
    print("")
    nlp.close()
