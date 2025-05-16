import json
from mediawiki import MediaWiki
import random
import wikipedia

lang_en = {}

def import_lang_en(path):
    global lang_en
    with open(path) as file:
        lang_en = json.load(file)

def gen_langlist_en(codelist):
    langlist = []
    for code in codelist:
        langlist.append(lang_en[code])
    return langlist



# Import 'lang code: English name' dict
import_lang_en('data/lang-en.json')

mediawiki = MediaWiki()
# List all languages and number of them for given article
article = mediawiki.page(input())
print(article.title)
langlist = gen_langlist_en(list(article.langlinks.keys()))
print(f'Languages: {langlist}')
print(f'Language Count: {len(langlist)}')
