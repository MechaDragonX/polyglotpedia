import json
from mediawiki import MediaWiki
import random
import wikipedia

mediawiki = MediaWiki()

# List all languages and number of them for given article
article = mediawiki.page(input())
print(article.title)
langlist = list(article.langlinks.keys())
print(f'Languages: {langlist}')
print(f'Language Count: {len(langlist)}')


# List all articles for given language...?
# random_lang = langlist[random.randint(0, len(langlist) - 1)]
# print(f'{random_lang} chosen')
# wikipedia.set_lang(random_lang)
