import yaml
import re
from filter import select_regexes, reject_regexes, select_letters, reject_letters

class Wordle:
    def __init__(self, debug=False, config_file='Wordle/config.yml'):
        print(f"config_file: {config_file}") #@
        # read config file
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # read list of acceptible quesses
        guess_file = config['file']['guesses']
        with open(guess_file) as f:
            all_words = [line.strip() for line in f.readlines()]
        
        # set members
        self.debug              = debug
        self._is_running        = True
        self.config             = config
        self.possible_words     = all_words
        self.full_word_count    = len(all_words)
        self.wrong_letters      = []
        self.wrong_regexes      = []
        self.correct_regexes    = []
        self.needed_letters     = []

        # show instructions
        self.show_instructions()

    def is_running(self):
        return self._is_running
    
    def show_instructions(self):
        result_codes = self.config['result'].keys()
        print('This helps solve Wordle.  Input is case-insensitive.  Feedback chars:')
        for desc in result_codes:
            code = self.config['result'][desc]
            print(f'- {desc}: {code}')
        print()

    def show_status(self):
        max_show = self.config['display']['max_possible']
        poss_ct  = len(self.possible_words)
        block_ct = self.full_word_count - poss_ct
        if poss_ct == 1:
           self._is_running = False
        print(f'Blocked count: {block_ct:,}, remaining count: {poss_ct:,}', end='')
        if poss_ct <= max_show:
            print(f', remaining words: {self.possible_words}', end='')
        print('\n')
        if(self.debug):
            print('wrong_letters:', self.wrong_letters)
            print('wrong_regexes', self.wrong_regexes)  
            print('misplaced_letters:', self.needed_letters)
            print('correct_regexes:', self.correct_regexes)
            print('\n')

    def get_input(self, input_type): 
        prompt = f'{input_type}? '
        regex = self.config['validate'][input_type]['regex']
        in_str = ''
        while in_str == '':
            in_str = input(prompt).upper()
            match = re.match(regex, in_str)
            if not match:
                in_str = ''
                desc = self.config['validate'][input_type]['description']
                print(desc)
        return in_str

    def get_guess(self):
        input_type = 'guess'
        guess = self.get_input(input_type)
        return guess
    
    def get_result(self):
        input_type = 'result'
        result = self.get_input(input_type)
        return result

    def success_result(self):
        return 'Y' * self.config['word']['length']

    def check_guess(self, guess, result):
        correct_letter = self.config['result']['correct_letter'].upper()
        wrong_letter   = self.config['result']['wrong_letter'].upper()
        wrong_pos      = self.config['result']['wrong_pos'].upper()
        word_length    = self.config['word']['length']

        # make list comprehension to get list of characters
        guess_chars = [char for char in guess.upper()]
        result_chars = [char for char in result.upper()]

        # analyze guess and result one position at a time
        for i in range(word_length):
            guess_char = guess_chars[i]
            result_char = result_chars[i]

            # wrong letter, block letter
            if result_char == wrong_letter:
                # add letter to wrong_letters if not in already in needed_letters
                if not select_letters(self.needed_letters, guess_char):
                    self.store_wrong_letter(guess_char)

            # right letter right place, save letter/pos
            if result_char == correct_letter: 
                self.store_correct_regex(guess_char, i)
                self.needed_letters.append(guess_char)

            # right letter wrong place, block pos, save letter
            if result_char == wrong_pos: 
                self.store_misplaced_letter(guess_char, i)

        # apply filters
        self.possible_words = select_regexes(self.possible_words, self.correct_regexes)
        self.possible_words = select_letters(self.possible_words, self.needed_letters)
        self.possible_words = reject_letters(self.possible_words, self.wrong_letters)
        self.possible_words = reject_regexes(self.possible_words, self.wrong_regexes)

    def store_wrong_letter(self, char):
        if char not in self.wrong_letters:
            self.wrong_letters.append(char)
        # if self.debug: 
            # print( f'char: {char}, wrong_letters: {self.wrong_letters}' )

    def store_correct_regex(self, char, i):
        word_len = self.config['word']['length']
        regex = '.'*i + char + '.'*(word_len-1 - i)
        if regex not in self.correct_regexes:
            self.correct_regexes.append(regex)
        # if self.debug: 
            # print( f'char: {char}, i: {i}, regex: {regex}, correct_regexes: {self.correct_regexes}' )

    def store_misplaced_letter(self, char, i):
        if char not in self.needed_letters:
            self.needed_letters.append(char)
        word_len = self.config['word']['length']
        regex = '.'*i + char + '.'*(word_len-1 - i)
        if regex not in self.wrong_regexes:
            self.wrong_regexes.append(regex)
        # if self.debug: 
            # print( f'char: {char}, i: {i}, regex: {regex}, wrong_regexes: {self.wrong_regexes}' )
