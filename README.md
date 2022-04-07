# Question_Answer_Croagunk

## Environment Setup
```
pip3 install nltk
pip3 install stanfordcorenlp   
pip3 install spacy
python3 -m spacy download en_core_web_md
./runserver.sh
```
Citation: https://github.com/Lynten/stanford-corenlp

### Stanfordcorenlp usage example
`python3 corenlp.py`

## Article Analysis
- Using stanfordcorenlp:
```
python3 article_analysis-corenlp.py <article>
```
- Using stanza: 
```
pip3 install stanza
python3 article_analysis-stanza.py <article>
```
- Using nltk:
```
python3 nltk_process.py <article>
```
