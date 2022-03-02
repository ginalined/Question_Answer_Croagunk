from stanfordcorenlp import StanfordCoreNLP

if __name__ == '__main__':
    nlp = StanfordCoreNLP('http://localhost', 9000)
    sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
    print('Tokenize: ', nlp.word_tokenize(sentence))
    print("")
    print('Part of Speech:', nlp.pos_tag(sentence))
    print("")
    print('Named Entities:', nlp.ner(sentence))
    print("")
    print('Constituency Parsing: ', nlp.parse(sentence))
    print("")
    print('Dependency Parsing:', nlp.dependency_parse(sentence))
    print("")
    nlp.close()