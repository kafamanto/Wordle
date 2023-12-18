import re

def select_regexes(words, regexes, debug=False):
    '''
    Return words in list that match regex list
    '''
    if len(regexes) == 0:
        return words
    filtered_words = []
    for word in words:
        if all(re.match(regex, word) for regex in regexes):
            filtered_words.append(word)
    return filtered_words

def reject_regexes(words, regexes, debug=False):
    '''
    Return strings in string list that don't match regex list
    '''
    if len(regexes) == 0:
        return words
    filtered_words = []
    for word in words:
        if not any(re.match(regex, word) for regex in regexes):
            filtered_words.append(word)
    return filtered_words

def select_letters(words, letters, debug=False):
    if len(letters) == 0:
        return words
    if debug: print('select_letters: ', letters)
    filtered_words = [word for word in words if all(letter in word for letter in letters)]
    return filtered_words

def reject_letters(words, letters, debug=False):
    if len(letters) == 0:
        return words  
    if debug: print('select_letters: ', letters)  
    filtered_words = [word for word in words if not any(letter in word for letter in letters)]
    return filtered_words
