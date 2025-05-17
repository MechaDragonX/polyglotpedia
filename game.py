from ui import UI
import json
from mediawiki import MediaWiki
from mediawiki.exceptions import DisambiguationError
import wikipedia
from wikipedia.exceptions import PageError

class Game():
    def __init__(self, ui, language='en'):
        self.ui = ui
        self.mediawiki = MediaWiki()
        # Lookup table for response letter to number for use in code
        self.RESPONSE_LETTER2NUMBER = {
            'a': 0,
            'b': 1,
            'c': 2
        }
        # This apparently reverses a dict
        self.RESPONSE_NUMBER2LETTER = { v: k for k, v in self.RESPONSE_LETTER2NUMBER.items() }
        self.VALID_RESPONSES = [
            'a',
            'b',
            'c',
            '1',
            '2',
            '3',
            'q',
            'quit'
        ]
        # Option for if lang counts are the same
        self.same = 'They\'re the same'

        if language == 'en':
            self.LANG_EN = {}
            # Import 'lang code: English name' dict
            self.import_lang_en('data/lang-en.json')


    # Data functions
    # Take JSON for 'lang code: English name' and import as dict
    def import_lang_en(self, path):
        with open(path) as file:
            self.LANG_EN = json.load(file)

    # Take list of lang codes and turn it into list of English names
    # Used with list(MediaWiki.Page.langlinks.keys())
    def gen_langlist_en(self, codelist):
        langlist = []
        for code in codelist:
            langlist.append(self.LANG_EN[code])
        # return sorted by English name
        return sorted(langlist)


    # Gameplay functions
    # Figure out the correct answer
    def gen_correct_answer(self, lang_counts):
        answer = 0

        if lang_counts[0] > lang_counts[1]:
            answer = 0
        elif lang_counts[1] > lang_counts[0]:
            answer = 1
        else:
            answer = 2

        return answer


    # Prompt user for choice and loop until accepted input is given
    # Then validate response
    def get_response(self):
        response = ''
        while response not in self.VALID_RESPONSES:
            response = input(f'Please type "A", "B", "C", or "1", "2", "3": ').lower()
            if response == 'q' or response == 'quit':
                return 'q'

        if response.isdigit():
            response = self.RESPONSE_NUMBER2LETTER[int(response)]
        self.ui.output()

        return response


    # Tell user if they were correct or not
    def print_results(self, article_titles, response, correct, answer, answer_title):
        # What they answered
        if self.RESPONSE_LETTER2NUMBER[response] != 2:
            self.ui.output(f'You answered "{article_titles[self.RESPONSE_LETTER2NUMBER[response]]}", ', '')
        else:
            self.ui.output(f'You answered "{self.same}", ', '')
        # Response if correct vs not
        if correct:
            self.ui.output('and that was correct!')
        else:
            self.ui.output('and that was incorrect!')
            self.ui.output(f'The correct answer was, {self.RESPONSE_NUMBER2LETTER[answer].upper()}: {answer_title}')
        self.ui.output('\n')


    # Single compare two question
    def compare_two(self):
        article_titles = []
        articles = []
        summaries = []
        # Generate until disambugation error does not occur
        generated = False
        while not generated:
            # Pick to random articles
            article_titles = self.mediawiki.random(pages=2)
            # Make list of Page classes of those articles
            try:
                # Make list of Page classes of those articles
                articles = [
                    self.mediawiki.page(article_titles[0]),
                    self.mediawiki.page(article_titles[1])
                ]
                summaries.append(articles[0].content.split('\n')[0])
                summaries.append(articles[1].content.split('\n')[0])
                generated = True
            except DisambiguationError:
                pass

        # Make list of language counts
        lang_counts = [
            len(list(articles[0].langlinks.keys())),
            len(list(articles[1].langlinks.keys()))
        ]

        # Make list of language names in English
        # article0_langlist = self.gen_langlist_en(list(articles[0].langlinks.keys()))
        # article1_langlist = self.gen_langlist_en(list(articles[1].langlinks.keys()))

        # Figure out the correct answer
        answer = self.gen_correct_answer(lang_counts)
        # Set value to answer_title for use when telling user what correct answer was
        if answer != 2:
            answer_title = article_titles[answer]
        else:
            answer_title = self.same

        # Actually game portion
        # Format:
        # Which of the following has more foreign language versions?
        #
        # A: <title>
        # <1 sentence summary>
        #
        # B:  <title>
        # <1 sentence summary>
        #
        # C: They're the same
        self.ui.output('Which of the following has more foreign language versions?\n')
        self.ui.output(f'A: {article_titles[0]}\n{summaries[0]}\n\nB: {article_titles[1]}\n{summaries[1]}\n\nC: {self.same}\n')

        # Prompt user for choice and loop until accepted input is given
        # Then validate response
        response = self.get_response()
        if response == 'q':
            # return val is bool of correctness, so -1 represents quit
            return -1

        # Check if user is correct
        correct = False
        if self.RESPONSE_LETTER2NUMBER[response] == answer:
            correct = True

        # Tell user if they were correct or not
        self.print_results(article_titles, response, correct, answer, answer_title)

        return correct


    def compare_two_10(self):
        score = 0

        i = 0
        answer = -1
        for i in range(10):
            self.ui.output(f'Question {i + 1}:')
            answer = self.compare_two()
            if answer == True:
                score += 1
            # Recieved quit signal
            elif answer == -1:
                return 1

        self.ui.output(f'Score: {score}/10')

        # End program
        self.ui.output('\nThanks for playing!')

        # Used for handling quit
        return 0


    def print_lives(self, lives):
        # not the emoj
        char = '♥'
        result = ''

        i = 0
        for i in range(lives):
            if i != lives - 1:
                result += f'{char} '
            else:
                result += char

        self.ui.output(f'Lives: {result}')


    def compare_two_inf(self):
        # 3 strikes and out lol
        lives = 3
        score = 0

        i = 0
        while lives > 0:
            self.ui.output(f'Question {i + 1}:')
            self.print_lives(lives)
            answer = self.compare_two()
            if answer == False:
                lives -= 1
            elif answer == True:
                score += 1
            # Recieved quit signal
            else:
                return 1

            i += 1

        self.ui.output(f'Score: {score}')

        # End program
        self.ui.output('\nThanks for playing!')

        # Used for handling quit
        return 0
