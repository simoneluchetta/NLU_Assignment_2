# Simone Luchetta

import conll
import spacy
import nltk
import pandas as pd

from remapping import remapping
from spacy.tokens import Doc

nlp = spacy.load("en_core_web_sm")
doc = conll.read_corpus_conll("data/train.txt", " ")[:100]

refs = [[(text, iob) for text, pos, syntactic_chunk, iob in sent]
        for sent in doc]

sentenceList = []

for sent in refs:
    sentence = []
    for i in range(len(sent)):
        sentence.append(sent[i][0])
    sentenceList.append(sentence)

docTextList = []
docNLP = []
docList = []

for sent in sentenceList:
    inputText = ' '.join(sent)
    docTextList.append(inputText)
    doc = Doc(nlp.vocab, words=sent)
    for name, proc in nlp.pipeline:
        doc = proc(doc)
    docList.append(doc)
    entityType = [(t.text, t.ent_iob_, t.ent_type_) for t in doc]
    docNLP.append(entityType)

docNLPRemappedList = remapping(docNLP)

results = conll.evaluate(refs, docNLPRemappedList)

pd_tbl = pd.DataFrame().from_dict(results, orient='index')
pd_tbl.round(decimals=3)
print(pd_tbl)

############################################################################

plusCounts = 0
total = 0

for i in range(len(refs)):
    for j in range(len(refs[i])):
        total += 1
        if (refs[i][j] == docNLPRemappedList[i][j]):
            plusCounts += 1
    
accuracy = plusCounts/total
print("Accuracy: " + str(accuracy))

############################################################################

docNER = []

for sent in docList:
    entityType = sent.ents
    docNER.append(entityType)

############################################################################


