from mediawiki import MediaWiki

mediawiki = MediaWiki()

article = mediawiki.page(input())
print(article.title)
langlist = list(article.langlinks.keys())
print(f'Languages: {langlist}')
print(f'Language Count: {len(langlist)}')
