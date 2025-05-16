import json
from mediawiki import MediaWiki

class Game():
    def __init__(self, language='en'):
        self.mediawiki = MediaWiki()
        # Lookup table for response letter to number for use in code
        self.response_letter2number = {
            'a': 0,
            'b': 1,
            'c': 2
        }

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
    def compare_two(self):
        # Pick to random articles
        article_titles = self.mediawiki.random(pages=2)
        # Make list of Page classes of those articles
        articles = [
            self.mediawiki.page(article_titles[0]),
            self.mediawiki.page(article_titles[1])
        ]
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

        # Actually game portion
        print('Which of the following has more foreign language versions?')
        print(f'A: {articles[0].title}\nB: {articles[1].title}\nC: They\'re the same\n')

        # Prompt user for choice and loop until accepted input is given
        response = ''
        while True:
            response = input(f'Please type "A", "B", "C": ').lower()
            if response == 'a':
                break
            elif response == 'b':
                break
            elif response == 'c':
                break
        print()

        # Check if user is correct
        correct = False
        if self.response_letter2number[response] == answer:
            correct = True

        # Tell user if they were correct or not
        print(f'You answered {response.upper()}, ', end='')
        if correct:
            print('and that was correct!')
        else:
            print('and that was incorrect!')
        # End program
        print('\nThanks for playing!')
