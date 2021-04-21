import conll
import spacy
import nltk
import pandas as pd

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

for sent in sentenceList:
    inputText = ' '.join(sent)
    docTextList.append(inputText)
    dummyDoc = nlp(inputText)
    entityType = [(t.text, t.ent_iob_, t.ent_type_) for t in dummyDoc]
    docNLP.append(entityType)

# for sent in sentenceList:
#     inputText = ' '.join(sent)
#     docTextList.append(inputText)
#     dummyDoc = nlp(inputText)
#     entityType = [(t.text, t.ent_iob_ + ("-" if len(t.ent_type_) > 0 else "") + t.ent_type_) for t in dummyDoc]
#     docNLP.append(entityType)

docNLPRemappedList = []

def remapping(processedNLP):
    for docs in processedNLP:
        docNLPRemapped = []
        for item in docs:
            # compare items
            if (str(item[2]) == "PERSON"):
                docNLPRemapped.append((item[0], item[1] + "-PER"))
            elif (str(item[2]) == "ORG"):
                # MISC, LOC
                docNLPRemapped.append((item[0], item[1] + "-ORG"))
            else: 
                docNLPRemapped.append((item[0], item[1]))
        docNLPRemappedList.append(docNLPRemapped)

remapping(docNLP)
