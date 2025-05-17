import json
from mediawiki import MediaWiki
from mediawiki.exceptions import DisambiguationError
import wikipedia
from wikipedia.exceptions import PageError

class Game():
    def __init__(self, language='en'):
        self.mediawiki = MediaWiki()
        # Lookup table for response letter to number for use in code
        self.response_letter2number = {
            'a': 0,
            'b': 1,
            'c': 2
        }
        self.response_number2letter = { v: k for k, v in self.response_letter2number.items() }

        if language == 'en':
            self.lang_en = {}
            # Import 'lang code: English name' dict
            self.import_lang_en('data/lang-en.json')


    # Data functions
    # Take JSON for 'lang code: English name' and import as dict
    def import_lang_en(self, path):
        with open(path) as file:
            self.lang_en = json.load(file)

    # Take list of lang codes and turn it into list of English names
    # Used with list(MediaWiki.Page.langlinks.keys())
    def gen_langlist_en(self, codelist):
        langlist = []
        for code in codelist:
            langlist.append(self.lang_en[code])
        # return sorted by English name
        return sorted(langlist)


    # Gameplay functions
    # Single compare two question
    def compare_two(self):
        same = 'They\'re the same'

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
        article_counts = [
            len(list(articles[0].langlinks.keys())),
            len(list(articles[1].langlinks.keys()))
        ]
        # Make list of language names in English
        article0_langlist = self.gen_langlist_en(list(articles[0].langlinks.keys()))
        article1_langlist = self.gen_langlist_en(list(articles[1].langlinks.keys()))

        # Figure out the correct answer
        answer = 0
        if article_counts[0] > article_counts[1]:
            answer = 0
        elif article_counts[1] > article_counts[0]:
            answer = 1
        else:
            answer = 2
        # Set value to answer_title for use when telling user what correct answer was
        if answer != 2:
            answer_title = articles[answer].title
        else:
            answer_title = same

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
        print('Which of the following has more foreign language versions?\n')
        print(f'A: {article_titles[0]}\n{summaries[0]}\n\nB: {article_titles[1]}\n{summaries[1]}\n\nC: {same}\n')

        # Prompt user for choice and loop until accepted input is given
        response = ''
        while True:
            response = input(f'Please type "A", "B", "C", or "1", "2", "3": ').lower()
            if response == 'a' or response == '1':
                break
            elif response == 'b' or response == '2':
                break
            elif response == 'c' or response == '3':
                break
        if response.isdigit():
            if response == '1':
                response = 'a'
            elif response == '2':
                response = 'b'
            elif response == '3':
                response = 'c'
        print()

        # Check if user is correct
        correct = False
        if self.response_letter2number[response] == answer:
            correct = True

        # Tell user if they were correct or not
        # What they answered
        if self.response_letter2number[response] != 2:
            print(f'You answered "{articles[self.response_letter2number[response]].title}", ', end='')
        else:
            print(f'You answered "{same}", ', end='')
        # Response if correct vs not
        if correct:
            print('and that was correct!')
        else:
            print('and that was incorrect!')
            print(f'The correct answer was, {self.response_number2letter[answer].upper()}: {answer_title}')
        print()
        print()

        return correct

    def compare_two_10(self):
        score = 0

        i = 0
        for i in range(10):
            print(f'Question {i + 1}:')
            if self.compare_two():
                score += 1

        print(f'Score: {score}/10')

        # End program
        print('\nThanks for playing!')
