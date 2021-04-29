# NLU_Assignment_2
Second assignment of the NLU course.

Make sure all the packages are installed by running the following commands:

```
pip install -U pip setuptools wheel
pip install -U spacy
```

Also make sure to download the english pre-trained model for spaCy:

```
python -m spacy download en_core_web_sm
```

Another thing to mention is that, for the sake of simplicity, ```pandas``` library was used in order to better represent the data output. The command to install the package using ```pip``` is the following:

```
pip install pandas
```

## Other functions in the document:
For these tasks I decided to program other useful functions, them being ```remapping.py``` and ```getKey.py``` in their respective Python file.
The first one comes in handy because since spaCy applies pos tags in another format which is different from the one of CoNLL, one might think to map the spaCy tags to the other format, so that the simple evaluation procedure that we saw in the laboratory could be applied.
The second one is useful to check whether or not a specific dictionary has a given key.

```remapping(processedNLP)``` takes as argument some ```[.text, .ent_iob_, .ent_type_]``` that have been gotten from a spaCy DOC object. It returns another list processed sentences, but with the iob_ and type_ parameters merged and slightly changed.

```getKey(key, dictionary)``` takes as argument a key that has to be searched in a specific dictionary, and returns ```True``` if the key is already present in the dictionary, and ```False``` otherwise.

I also included a function in order to get the various sentences from the ```refs``` structure, and store them in some other format.
```
def getSentences(reference):
    sentenceList = []

    for sent in reference:
        sentence = []
        for i in range(len(sent)):
            sentence.append(sent[i][0])
        sentenceList.append(sentence)
    return sentenceList
```

Another function which could be useful is the ```trail``` function. It can return the end of a sequence of compounds relations, so that one can know which is the starting token and the ending one in the trail.

```
def trail(token):

    if(token.head.dep_ == "compound"):
        return trail(token.head)
    else:
        return token
```

## Evaluation of spaCy NER on CoNLL 2003 Data:
This task is divided in two main parts and involves an analysis on the CoNLL dataset.
The first part is about reporting the token-level performance of spaCy NER, while the second one aims at calculating the chunk-level performance.
The input data is firstly collected from the ```Data``` folder by using the following command:

```
doc = conll.read_corpus_conll("data/train.txt", " ")[:100]
```

Where the ```[:100]``` specifies how many sentences we want to upload (which is convenient for debug purposes, so that the execution time of the whole program gets reduced by a lot)
Then, the text and the iob are stored in a data structure named ```refs```; the aim here is mainly to store the iob tags so that then they could be compared later in similar fashion as we saw in the lab lesson.

```
refs = [[(text, iob) for text, pos, syntactic_chunk, iob in sent]
        for sent in doc]
```

Basically, ```refs``` stores the text and the IOB tag of each sentence of the CoNLL 2003 corpus. The textual part will form a sentence that will then be passed into the ```task_1_2``` function, which will process the sentences using spaCy. Since spaCy and CoNLL have some different IOB tag annotation, another function called ```remapping``` will be used so that it will be possible to do further comparisons about the data. So, in the end, the function ```task_1_2``` returns both a list of documents objects processed by spaCy and a list of remapped documents.

On top of that, this way is possible to use the ```conll.py``` evaluation function:

```
results = conll.evaluate(refs, docNLPRemappedList)

pd_tbl = pd.DataFrame().from_dict(results, orient='index')
pd_tbl.round(decimals=3)
print(pd_tbl)
```

Which will give us the following measures (if the algorithm is ran over all the data in the train.txt file):

```
Task 1.2:
              p         r         f      s
LOC    0.626794  0.018347  0.035651   7140
ORG    0.407710  0.284449  0.335104   6321
PER    0.770980  0.631970  0.694588   6600
MISC   0.088448  0.551193  0.152435   3438
total  0.254181  0.340227  0.290976  23499
```

For what concerns about the accuracy measure, it is possible to calculate by just counting the number of spaCy's correct guesses over the total number of elements in CoNLL. For simplicity, data can be stored in ```accuracyDict = {}``` and ```referenceDict = {}```, using a combination of IOB-tags + Entity type as key and increasing their count value as long as new matching elements are encountered.

Overall, the output of the ```task_1_1``` function will be the following:

```
Task 1.1:
Accuracies for each IOB type:
O: 0.87
B-ORG: 0.32
B-MISC: 0.59
B-PER: 0.65
I-PER: 0.80
B-LOC: 0.02
I-ORG: 0.56
I-MISC: 0.25
I-LOC: 0.05
Total accuracy: 0.7999970669756119
```

## Grouping of entities:
The grouping of entities has been done by carefully merging together the structures composed by:
```
chunkType = list(sent.noun_chunks)
```

and 

```
entityType = [(ent.text, ent.label_) for ent in sent.ents
```

To get useful informations out of ```chunkType```, one has to carry out four for-loops. Thanks to this, it is possible to recover how recognized named entities are grouped together. For example, for the input text: "Apple's Steve Jobs died in 2011 in Palo Alto, California.", the result, that is stored in the variable ```separatedChunks``` in my code, is going to be the following:

```
[[('Apple', 'ORG'), ('Steve Jobs', 'PERSON')], [('Palo Alto', 'GPE')], [('California', 'GPE')]]
```

For what concerns about the ```entityType```, they are used to simply store all the recognized entities. In the example above, one clearly see that there's a ```'Date'``` entity missing, so there's got to be a fancy way to put it in there. The task is simply accomplished by the control logic.

It assumes that there must be at least a number of total entities per-sentence equal to ```len(entityType)```; two indices, namely ```k``` and ```i``` are used to navigate into the above data structures, and appending a proper result into ```output``` list, which then goes straight into ```result``` which will store all of our desired data.

Using ```task_2_1``` function, one could extract the groupings of each sentence in the CoNLL train.txt file. Results are going to be store in the ```result``` data structure. Here, I am reporting just one random entry:

```
[('Thursday', 'DATE'), ('afternoon', 'TIME')]
[('daily', 'DATE')]
[('Le Monde', 'FAC')]
[('23', 'CARDINAL')]
```

Using ```task_2_2``` function, we just run a pure frequency analysis; items are firstly filtered to exclude fancy -DOCSTART- stuff and then stored in a ```dictionary```, where the key is the grouped entity type, and the value is the count. The whole combinations that occur in the train.txt file are the following:

```
['ORG']:3825
['NORP']:1814
['PERSON']:4745
['DATE']:4020
['GPE']:5603
['ORG', 'PERSON']:72
['LOC']:185
['CARDINAL']:5602
['QUANTITY']:346
['PERCENT']:322
['MONEY']:572
['GPE', 'PERSON']:107
['LANGUAGE']:40
['TIME']:379
['ORDINAL']:750
['CARDINAL', 'CARDINAL', 'ORG', 'ORG']:1
['GPE', 'PRODUCT']:17
['MONEY', 'DATE']:1
['ORG', 'CARDINAL', 'ORG']:4
['GPE', 'NORP']:14
['GPE', 'ORG']:52
['CARDINAL', 'NORP', 'NORP']:3
['EVENT']:120
['FAC']:130
['PRODUCT']:89
['CARDINAL', 'ORG']:99
['CARDINAL', 'NORP']:40
['LAW']:21
['DATE', 'TIME']:34
['ORG', 'NORP']:6
['DATE', 'DATE']:5
['ORG', 'DATE']:3
['CARDINAL', 'PERSON']:298
['ORDINAL', 'CARDINAL']:11
['DATE', 'NORP']:10
['CARDINAL', 'CARDINAL', 'PERSON']:1
['MONEY', 'ORG', 'PRODUCT']:5
['GPE', 'ORDINAL']:23
['PERSON', 'GPE']:7
['CARDINAL', 'GPE']:48
['PERSON', 'PERSON']:26
['EVENT', 'PERSON']:3
['WORK_OF_ART']:45
['TIME', 'GPE']:2
['GPE', 'GPE']:38
['ORG', 'ORG']:35
['CARDINAL', 'CARDINAL']:22
['DATE', 'GPE']:13
['CARDINAL', 'EVENT']:4
['DATE', 'ORG']:22
['ORDINAL', 'ORG']:2
['PERSON', 'CARDINAL']:9
['NORP', 'PERSON']:42
['ORDINAL', 'PRODUCT']:1
['CARDINAL', 'NORP', 'PERSON']:3
['MONEY', 'NORP']:1
['ORDINAL', 'NORP']:7
['PERCENT', 'DATE']:1
['PERSON', 'ORG']:6
['GPE', 'DATE']:11
['PERSON', 'MONEY']:2
['ORG', 'MONEY']:1
['DATE', 'WORK_OF_ART']:2
['LANGUAGE', 'ORDINAL']:2
['NORP', 'ORG', 'GPE']:1
['ORDINAL', 'ORDINAL']:2
['LOC', 'PERSON']:2
['GPE', 'CARDINAL']:25
['CARDINAL', 'EVENT', 'PERSON']:1
['ORG', 'NORP', 'PERSON']:1
['ORDINAL', 'PERSON']:6
['GPE', 'LOC']:4
['LAW', 'QUANTITY']:1
['DATE', 'PERSON']:14
['NORP', 'DATE', 'DATE', 'PERSON']:1
['CARDINAL', 'PERSON', 'GPE']:1
['ORG', 'ORDINAL']:9
['ORG', 'CARDINAL']:9
['LOC', 'GPE', 'ORG']:2
['CARDINAL', 'LOC', 'GPE', 'ORG']:1
['MONEY', 'GPE']:1
['MONEY', 'ORG']:6
['ORG', 'GPE', 'ORG']:1
['CARDINAL', 'NORP', 'LOC', 'GPE', 'ORG']:1
['PERCENT', 'LOC']:1
['CARDINAL', 'MONEY', 'GPE', 'ORG']:1
['CARDINAL', 'ORG', 'MONEY', 'ORG']:1
['DATE', 'CARDINAL']:5
['NORP', 'NORP']:1
['GPE', 'CARDINAL', 'NORP']:1
['NORP', 'ORG']:3
['ORG', 'GPE']:11
['DATE', 'MONEY']:1
['MONEY', 'MONEY']:1
['GPE', 'DATE', 'CARDINAL']:1
['PERSON', 'CARDINAL', 'GPE']:2
['DATE', 'GPE', 'GPE']:1
['ORG', 'ORG', 'PERSON']:1
['DATE', 'EVENT']:11
['CARDINAL', 'PRODUCT']:5
['MONEY', 'ORDINAL']:1
['ORG', 'PRODUCT']:16
['DATE', 'PERSON', 'QUANTITY']:1
['GPE', 'GPE', 'ORDINAL']:1
['NORP', 'GPE', 'PERSON']:1
['FAC', 'GPE']:1
['CARDINAL', 'CARDINAL', 'GPE']:2
['CARDINAL', 'PERSON', 'PERSON']:1
['GPE', 'NORP', 'PERSON']:1
['ORDINAL', 'EVENT']:3
['PERSON', 'PRODUCT']:1
['NORP', 'GPE']:3
['DATE', 'QUANTITY']:1
['ORG', 'PERCENT']:1
['CARDINAL', 'FAC']:3
['PRODUCT', 'PERSON']:3
['DATE', 'LANGUAGE']:1
['PERSON', 'ORDINAL']:5
['CARDINAL', 'CARDINAL', 'CARDINAL']:1
['GPE', 'ORG', 'PERSON']:2
['GPE', 'ORDINAL', 'PERSON']:1
['GPE', 'NORP', 'ORG']:1
['CARDINAL', 'DATE']:6
['LOC', 'LOC']:2
['CARDINAL', 'MONEY']:2
['CARDINAL', 'CARDINAL', 'ORG']:1
['LOC', 'CARDINAL']:1
['GPE', 'EVENT']:3
['MONEY', 'CARDINAL']:1
['ORDINAL', 'GPE']:2
['TIME', 'PERSON']:1
['LANGUAGE', 'PERSON']:1
['QUANTITY', 'ORDINAL']:4
['WORK_OF_ART', 'PERSON']:3
['LOC', 'GPE']:2
['DATE', 'PERCENT']:2
['PRODUCT', 'CARDINAL']:2
['ORG', 'CARDINAL', 'CARDINAL', 'ORG']:1
['ORG', 'ORG', 'ORG', 'NORP', 'ORG']:3
['DATE', 'ORG', 'ORG', 'ORG', 'NORP', 'ORG']:2
['DATE', 'LOC']:3
['CARDINAL', 'GPE', 'PERSON']:1
['CARDINAL', 'PERSON', 'GPE', 'CARDINAL']:1
['ORDINAL', 'CARDINAL', 'CARDINAL']:1
['GPE', 'DATE', 'PERSON']:1
['GPE', 'PERCENT']:1
['PERSON', 'TIME']:1
['GPE', 'QUANTITY']:1
['DATE', 'DATE', 'PERSON']:1
['PERSON', 'DATE']:1
['ORDINAL', 'DATE']:2
['DATE', 'NORP', 'PERSON']:1
['DATE', 'GPE', 'PERSON']:1
['DATE', 'GPE', 'NORP']:1
['GPE', 'NORP', 'NORP']:1
['FAC', 'ORG']:1
['CARDINAL', 'GPE', 'DATE']:1
['GPE', 'LOC', 'PERSON']:1
['ORG', 'ORDINAL', 'CARDINAL']:1
['GPE', 'CARDINAL', 'EVENT']:1
['PERSON', 'LOC']:1
['CARDINAL', 'GPE', 'GPE']:1
['LANGUAGE', 'ORDINAL', 'ORG']:1
['PERCENT', 'GPE']:1
['NORP', 'ORDINAL']:1
['TIME', 'ORG']:1
['DATE', 'PERSON', 'DATE']:1
['QUANTITY', 'QUANTITY']:1
['PERSON', 'NORP']:1
['GPE', 'FAC']:1
['ORG', 'ORG', 'CARDINAL']:1
['ORG', 'LOC']:1
```

It is possible to first sort the dictionary and then take advantage of the pretty print options; i left commented those lines in my code, but if one ever changes his mind, just uncomment (at the top of the main.py):

```
import pprint
```

And (in task_2_2):

```
resultDict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
pprint.pprint(resultDict)
```

## Post processing:
The last task was about fixing segmentation errors. I proposed three functions:
1. ```task_3_option_1```: This function aims at correcting spaCy's segmentation errors by looking at compound relations between tokens. It mainly assumes that if a token has a compound relation between its head, then one has to check its ```token.i``` id to see whether the token itself stands at the right or at the left of the head. Once this is known, ```"B"``` and ```"I"``` tags can be placed accordingly.
On top of that, if some tokens have a compound relation and share the same ```token.ent_type_``` parameter, then the token that follows will be an ```"I"``` for sure.
2. ```task_3_option_2```: This function is really the same as the first one, but its input argument is a text.
3. ```task_3_option_3```: This function aims at improving the first one, so that even the relationships between the children of a token and its parent are taken into consideration. Children of a token are stored in a list that contains both the children and the father, and then sorted. If an child has a compound relation, it suggests that the following token could be ```"I"```, while the child itself could be a "```"B"```.

For example, this is the result that we get if we feed the text: ```"Apple 's Steve Jobs died in 2011 in Palo Alto , California ."``` to ```task_3_option_2```:

```
[['Apple', 'B', 'ORG'], ["'s", 'O', ''], ['Steve', 'B', 'PERSON'], ['Jobs', 'I', 'PERSON'], ['died', 'O', ''], ['in', 'O', ''], ['2011', 'B', 'DATE'], ['in', 'O', ''], ['Palo', 'B', 'GPE'], ['Alto', 'I', 'GPE'], [',', 'O', ''], ['California', 'B', 'GPE'], ['.', 'O', '']]
```

The same reasoning is applied to all the sentences in the CoNLL ```train.txt``` file.
