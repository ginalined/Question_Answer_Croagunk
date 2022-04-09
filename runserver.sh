# if [ ! -d "stanford-corenlp-4.4.0" ]
# then
#     curl -O -L http://nlp.stanford.edu/software/stanford-corenlp-4.4.0.zip
#     unzip stanford-corenlp-4.4.0.zip
#     rm stanford-corenlp-4.4.0.zip
# fi

# cd stanford-corenlp-4.4.0
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

if [ ! -d "stanford-parser-full-2020-11-17" ]
then
    curl -O -L https://nlp.stanford.edu/software/stanford-parser-4.2.0.zip
    unzip stanford-parser-4.2.0.zip
    rm stanford-parser-4.2.0.zip
fi
