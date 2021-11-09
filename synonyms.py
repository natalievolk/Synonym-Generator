'''Semantic Similarity

Author: Natalie Volk Last modified: Dec 7, 2020. Starter code by Professor Guerzhoy
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''
    computes cosine similarity of two vectors of words
    '''
    numerator = 0
    norm1 = 0
    norm2 = norm(vec2)
    
    for key, value in vec1.items():
        if key in vec2:
            numerator += vec1[key] * vec2[key]
            
        norm1 += vec1[key] * vec1[key]
        
    norm1 = math.sqrt(norm1)
        
    similarity = numerator / (norm1 * norm2)
    return similarity


def build_semantic_descriptors(sentences):
    '''
    given list of sentences, goes through and creates semantic descriptors dictionary
    '''
    # main dictionary that will be returned
    d = {}
    # iterates through the sentences
    for sentence in sentences:
        # creates and fill a dictionary with all the words in the sentence
        #(it ignores repeated words)
        count = {}
        for word in sentence:
            count[word] = 1
        
        # goes through each word again
        for word in sentence:
            # creates an 'inner' dictionary and removes the word from it
            r = dict(count)
            del r[word]
            # check if that word is already in the dictionary and if not, adds
            #the corresponding 'inner' dictionary
            if d.get(word) == None:
                d[word] = r
            # if the word is already the dicionary d, it adds any new words
            #that appeared in the same sentence as that word
            else:
                for key, value in r.items():
                    if key in d[word]:
                        d[word][key] += r[key]
                    else:
                        d[word][key] = r[key]
    return d

def build_semantic_descriptors_from_files(filenames):
    '''
    given a list of files, builds semantic descriptors dictionary
    '''
    sentences = []
    # goes through each file and formats it into a list based on sentences
    for file in filenames:
        file = open(file, "r", encoding="latin1")
        file = file.read()
        sentences.extend(file.lower().replace(',', '').replace('--', ' ').replace('-', ' ').replace(':', '').replace(';', '')\
            .replace('? ', '.').replace('!', '.').replace('\n', ' ').split('.'))
    # goes through the sentences and splits into words
    for i, word in enumerate(sentences):
        sentences[i] = word.split(" ")
        # remove duplicate keys
        sentences[i] = list(dict.fromkeys(sentences[i]))
        # remove empty elements
        sentences[i] = [x for x in sentences[i] if x != '']
    sentences = [x for x in sentences if x != [] and x != ['']]
        
    return build_semantic_descriptors(sentences)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''
    uses cosine similarity function to determine the synonym of a word, given
    a list of choices
    '''
    # if the word to find synonyms for isn't in sem_descr, then just return the
    #first choice given
    if not word in semantic_descriptors:
        return choices[0]
    # calcultate the similarity of each option and return the one with the max similarity
    similarity= [0]*len(choices)
    for i, choice in enumerate(choices):
        if not choice in semantic_descriptors:
            similarity[i] = -1
            continue
        similarity[i] = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
    return choices[similarity.index(max(similarity))]   


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''
    given a file of test cases, will determine which is the correct synonym
    and return the percentage of correct test cases
    '''
    count = 0
    correct = 0
    file = open(filename, 'r', encoding='latin1')
    # goes through each line in file
    for line in file.readlines():
        count += 1
        line = line.replace('\n', '').split(' ')
        # word we're trying to find synonyms for is the first word on the line
        word = line[0]
        #  choices are the rest of the words
        choices = line[1:]
        # the answer is the 'choice' that is repeated in a line
        for synonym in choices:
            if choices.count(synonym) > 1:
                answer = synonym
                break
        # check if the computed most similar word equals the answer
        if most_similar_word(word, choices, semantic_descriptors, similarity_fn) == answer:
            correct += 1
    # return percentage correct
    return (correct / count) * 100

if __name__ == "__main__": 

    d = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    
    res = run_similarity_test("test.txt", d, cosine_similarity)
    print(res, "of the guesses were correct")

    