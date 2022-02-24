if [ ! -d "stanford-corenlp-4.4.0" ]
then
    curl -O -L http://nlp.stanford.edu/software/stanford-corenlp-latest.zip
    unzip stanford-corenlp-latest.zip
    rm stanford-corenlp-latest.zip
fi

cd stanford-corenlp-4.4.0
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000