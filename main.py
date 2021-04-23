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

# input_text = "Apple's Steve Jobs died in 2011 in Palo Alto, California."

# docEx = nlp(input_text)

result = []

for sent in docList:

    chunkType = list(sent.noun_chunks)

    entities = []

    for ents in chunkType:
        variousChunks = []
        for nc in ents.ents:
            variousChunks.append(nc)
        entities.append(variousChunks)

    separatedChunks = []

    for element in entities:
        l = []
        for counts in element:
            count = (counts.lemma_, counts.label_)
            l.append(count)
        separatedChunks.append(l)

    entityType = [(ent.text, ent.label_) for ent in sent.ents]

    output = []
    separatedChunks = [x for x in separatedChunks if (len(x) > 0)]

    i = 0
    k = 0
    while(i < len(entityType)):
        if(k < len(separatedChunks) and entityType[i] == separatedChunks[k][0]):
            l = []
            for chunk in separatedChunks[k]:
                l.append(chunk)
                i += 1
            output.append(l)
            k += 1
        else:
            output.append([entityType[i]])
            i += 1

    result.append(output)

############################################################################

frequencyAnalysis = [x for x in result if (len(x) > 0)]

dictionary = {}

def get_key(matching, my_dict):
    for key, value in my_dict.items():
         if key == matching:
             return True
 
    return False

for sents in frequencyAnalysis:
    for elems in sents:
        e = []
        for i in range(len(elems)):
            e.append(str(elems[i][1]))
        if(get_key(str(e), dictionary)):
            # add the key's matching number in the dictionary
            dictionary[str(e)] += 1
        else:
            # create a new entry in the dictionary
            dictionary[str(e)] = 1

print(dictionary)

print("End of frequency analysis...")

############################################################################
