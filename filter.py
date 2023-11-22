import re

def select_regexes(words, regexes):
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

def reject_regexes(words, regexes):
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

def select_letters(words, letters):
    if len(letters) == 0:
        return words
    filtered_words = [word for word in words if any(letter in word for letter in letters)]
    return filtered_words

def reject_letters(words, letters):
    if len(letters) == 0:
        return words    
    filtered_words = [word for word in words if not any(letter in word for letter in letters)]
    return filtered_words

if __name__ == '__main__':
    words = ['STERN', 'AUDIO', 'SMITH', 'SIGHT', 'TRADE', 'TARDY']
    print('word list: ', words, '\n')

    # select words by regex list
    regexes = ['T....']
    print('regex: ', regexes)
    print('selected: ', select_regexes(words, regexes), '\n')

    # reject words by regex list
    regexes = ['.T...']
    print('regex: ', regexes)
    print('rejected: ', reject_regexes(words, regexes), '\n')

    # select words by letter list
    letters = ['T']
    print('letters: ', letters)
    print('selected: ', select_letters(words, letters), '\n')

    # reject words by letter list
    letters = ['T']
    print('letters: ', letters)
    print('rejected: ', reject_letters(words, letters), '\n')
