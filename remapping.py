# Function to remap items from spaCy to conll format, in order to compare them

def remapping(processedNLP):
    docNLPRemappedList = []
    for docs in processedNLP:
        docNLPRemapped = []
        for item in docs:
            # Compare items and convert them to a more suitable format
            # For example: spaCy "NORP" --> via remapping process becomes --> conll "MISC"
            # See the spaCy to conll reference for completeness.

            # There is 1 spaCy to "PER" conversion to do:

            if (str(item[2]) == "PERSON"):
                docNLPRemapped.append((item[0], item[1] + "-PER"))

            # There is 1 spaCy to "LOC" conversion to do:

            elif (str(item[2]) == "LOC"):  # 1
                docNLPRemapped.append((item[0], item[1] + "-LOC"))

            # There are 3 spaCy to "ORG" conversions to carry:

            elif (str(item[2]) == "ORG"):
                # MISC, LOC
                docNLPRemapped.append((item[0], item[1] + "-ORG"))
            elif (str(item[2]) == "FACILITY"):
                docNLPRemapped.append((item[0], item[1] + "-ORG"))
            elif (str(item[2]) == "FAC"):
                docNLPRemapped.append((item[0], item[1] + "-ORG"))

            # There are 19 spaCy to "MISC" conversions to carry:

            elif (str(item[2]) == "NORP"):  # 1
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "GPE"):  # 2
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "PRODUCT"):  # 3
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "EVENT"):  # 4
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "WORK_OF_ART"):  # 5
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "LAW"):  # 6
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "LANGUAGE"):  # 7
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "DATE"):  # 8
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "TIME"):  # 9
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "PERCENT"):  # 10
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "MONEY"):  # 11
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "QUANTITY"):  # 12
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "ORDINAL"):  # 13
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "CARDINAL"):  # 14
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "PER"):  # 15
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "MISC"):  # 16
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "EVT"):  # 17
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "PROD"):  # 18
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            elif (str(item[2]) == "DRV"):  # 19
                docNLPRemapped.append((item[0], item[1] + "-MISC"))
            
            # Other transforms:

            elif (str(item[2]) == "GPE_LOC"):  # 20
                docNLPRemapped.append((item[0], item[1] + "-LOC")) ## These could have been MISC, but since the term "LOC" is present in the text, I decided to leave it as it is
            elif (str(item[2]) == "GPE_ORG"):  # 21
                docNLPRemapped.append((item[0], item[1] + "-GPE")) ## Same reason of above, but with "GPE"

            # And for those I may have missed... Just ignore the third Item and keep the IOB tag
            # I could have put the "MISC" conversions in the final else, but I wasn't extremely sure I included all the item-tags I needed.

            else:
                docNLPRemapped.append((item[0], item[1]))
        docNLPRemappedList.append(docNLPRemapped)
    
    return docNLPRemappedList

# If we want to see the chunks types, we have:

# chunks = []
# chunks.append(conll.get_chunks("data/train.txt", fs=" ", otag="O"))
