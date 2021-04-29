# Simone Luchetta, Student ID: 223716
# Second assignment

import conll
import spacy
import nltk
import pandas as pd
# import pprint

from remapping import remapping
from getKey import get_key
from spacy.tokens import Doc

nlp = spacy.load("en_core_web_sm")

refs = [[(text, iob) for text, pos, syntactic_chunk, iob in sent]
        for sent in doc]

def getSentences(reference):
    sentenceList = []

    for sent in reference:
        sentence = []
        for i in range(len(sent)):
            sentence.append(sent[i][0])
        sentenceList.append(sentence)
    return sentenceList

def task_1_2(reference):

    sentenceList = getSentences(reference)

    docTextList = []
    docNLP = []
    docList = []

    for sent in sentenceList:
        inputText = ' '.join(sent)
        docTextList.append(inputText) # Optionally one could decide to store here the sentences, maybe for future use
        doc = Doc(nlp.vocab, words=sent)
        for name, proc in nlp.pipeline: # Here we obtain spaCy doc objects, with a different flavour with respect to the usual modality
            doc = proc(doc)
        docList.append(doc)
        entityType = [(t.text, t.ent_iob_, t.ent_type_) for t in doc]
        docNLP.append(entityType)

    docNLPRemappedList = remapping(docNLP) # Everything is remapped from spaCy format to CoNLL IOB format

    results = conll.evaluate(reference, docNLPRemappedList)

    pd_tbl = pd.DataFrame().from_dict(results, orient='index')
    pd_tbl.round(decimals=3)
    print(pd_tbl)

    return docList, docNLPRemappedList # Choose what to return

print("Task 1.2:")
docList, docNLPRemappedList = task_1_2(refs)
print("")

############################################################################

def task_1_1(reference, docR):

    plusCounts = 0
    total = 0

    accuracyDict = {}
    referenceDict = {}

    for i in range(len(refs)):
        for j in range(len(refs[i])):
            total += 1
            if (refs[i][j][1] == docNLPRemappedList[i][j][1]):
                if(get_key(docNLPRemappedList[i][j][1], accuracyDict)):
                # add the key's matching number in the dictionary
                    accuracyDict[docNLPRemappedList[i][j][1]] += 1
                else:
                # create a new entry in the dictionary
                    accuracyDict[docNLPRemappedList[i][j][1]] = 1
                plusCounts += 1
            if(get_key(refs[i][j][1], referenceDict)):
                # add the key's matching number in the dictionary
                    referenceDict[refs[i][j][1]] += 1
            else:
                # create a new entry in the dictionary
                referenceDict[refs[i][j][1]] = 1
            
    print("Accuracies for each IOB type:")
    for keys in referenceDict:
        try:
            print("{}: {:.2f}".format(keys, accuracyDict[keys]/referenceDict[keys]))
        except:
            print("No matches for {}".format(keys))
            pass

    accuracy = plusCounts/total
    print("Total accuracy: " + str(accuracy))

print("Task 1.1:")
task_1_1(refs, docNLPRemappedList)
print("")

############################################################################

# input_text = "Apple's Steve Jobs died in 2011 in Palo Alto, California."

# docEx = nlp(input_text)

def task_2_1(docL):

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

        # Control logic

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
    return result

# It is possible to insert [docEx] instead of docList, if one wants
print("Task 2.1:")
result = task_2_1(docList)
print("All items are now stored in 'result' data structure...\n")

############################################################################

def task_2_2(previousResult):

    frequencyAnalysis = [x for x in result if (len(x) > 0)]

    dictionary = {}

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

    # If one wants to sort the dictionary and then use the pretty print:
    # resultDict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    # pprint.pprint(resultDict)

    # If one wants to print the dictionary as it is:
    for keys in dictionary:
        print("{}:{}".format(keys, dictionary[keys]))

print("Task 2.2:")
task_2_2(result)
print("End of frequency analysis...")

############################################################################

def trail(token):

    if(token.head.dep_ == "compound"):
        return trail(token.head)
    else:
        return token

def task_3_option_1(texts):
    expansion = []
    for sent in texts: # Since this function is designed to work with other lists of sentences, I decided to process the sentences here.
        plainString = ""
        for ele in sent: 
            plainString += str(ele + " ")
        doc = nlp(plainString)

        toModify = [[token.text, token.ent_iob_, token.ent_type_] for token in doc]

        for token in doc:
            if(token.dep_ == "compound" and token.head.ent_type_ != ""):
                toModify[token.i][2] = token.head.ent_type_
                if(token.head.i < token.i): # In which side of the sentence am I? Take a look and then...
                    toModify[token.i][1] = "B"
                elif(toModify[token.head.i][1] == "B"):
                    toModify[token.head.i][1] = "I"
                    toModify[token.i][1] = "B"
                elif(toModify[token.i-1][2] == toModify[token.i][2]): # Corrects for B-B-I or stuffs like that
                    toModify[token.i][1] = "I"
                else:
                    toModify[token.i][1] = "B"

        expansion.append(toModify)
    return expansion

def task_3_option_2(texts):
    expansion = []
    doc = nlp(texts)

    toModify = [[token.text, token.ent_iob_, token.ent_type_] for token in doc]

    for token in doc:
        if(token.dep_ == "compound" and token.head.ent_type_ != ""):
            toModify[token.i][2] = token.head.ent_type_
            if(token.head.i < token.i): # In which side of the sentence am I? Take a look and then...
                toModify[token.i][1] = "B"
            elif(toModify[token.head.i][1] == "B"):
                toModify[token.head.i][1] = "I"
                toModify[token.i][1] = "B"
            elif(toModify[token.i-1][2] == toModify[token.i][2]): # Corrects for B-B-I or stuffs like that
                toModify[token.i][1] = "I"
            else:
                toModify[token.i][1] = "B"

    expansion.append(toModify)
    return expansion

def task3_option_3(texts):
    expansion = []
    for sent in texts: 
        plainString = ""
        for ele in sent: 
            plainString += str(ele + " ")
        doc = nlp(plainString)
    
        toModify = [[token.text, token.ent_iob_, token.ent_type_] for token in doc]

        childList = []

        for token in doc:
            for childrens in list(token.children):
                childList.append([childrens, token])
            childList = sorted(childList)

            idx = 0
            try:
                while(childList[idx][0].dep_ == "compound"):
                    elem = trail(childList[idx][0])
                    toModify [elem.i][1] = "I"
                    toModify [childList[idx][0].i][1] = "B"
                    toModify [childList[idx][0].i][2] = toModify [item.i+1][2]
                    idx += 1
            except:
                pass
            
            if(token.dep_ == "compound" and token.head.ent_type_ != ""):
                toModify[token.i][2] = token.head.ent_type_
                if(token.head.i < token.i): # In which side of the sentence am I? Take a look and then...
                    toModify[token.i][1] = "B"
                elif(toModify[token.head.i][1] == "B"):
                    toModify[token.head.i][1] = "I"
                    toModify[token.i][1] = "B"
                elif(toModify[token.i-1][2] == toModify[token.i][2]): # Corrects for B-B-I or stuffs like that
                    toModify[token.i][1] = "I"
                else:
                    toModify[token.i][1] = "B"

        expansion.append(toModify)
    return expansion

# On train.txt files:
print("Task 3:")
sentenceList = getSentences(refs)
# segmentationCorrection = task_3_option_1(sentenceList)

# On the sentence about Steve Jobs:
# string = "Apple 's Steve Jobs died in 2011 in Palo Alto , California ."
# segmentationCorrection = task_3_option_2(string)

# Other option using token.children and compounds
segmentationCorrection = task3_option_3(sentenceList)
print("All sentences are processed and stored in segmentationCorrection data structure...")
print("End of program")

############################################################################
