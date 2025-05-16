import json
import wikipedia

# Generate missing language names
# code_lang_list = list(wikipedia.languages().keys())
# with open('data/lang-code.txt', 'w') as write:
#     for item in code_lang_list:
#         write.write(f'{item}\n')

# wiki_lang_list = None
# with open('data/lang-wiki.txt', 'r') as read:
#     wiki_lang_list = read.readlines()
# for i in range(len(wiki_lang_list)):
#     wiki_lang_list[i] = wiki_lang_list[i][:-1]

# diff = sorted(set(code_lang_list).difference(set(wiki_lang_list)))
# print(code_lang_list)
# print(wiki_lang_list)
# print(diff)

# with open('data/lang-missing.txt', 'w') as write:
#     for item in diff:
#         write.write(f'{item}\n')


# Write to code to native names dict to JSON
lang_native = wikipedia.languages()
with open('data/lang-en.json', 'w') as write:
    json.dump(lang_native, write, indent=4)

# Import text
# Format:
# <code>\t<English name>
lang_en_text = None
with open('data/lang-en.txt', 'r', encoding='utf-8') as read:
    lang_en_text = read.readlines()
# Remove \n at end
for i in range(len(lang_en_text)):
    lang_en_text[i] = lang_en_text[i][:-1]

# Create 'lang code: English name' dict
lang_en = lang_native
item = None
for i in range(len(lang_en_text)):
    item = lang_en_text[i].split('\t')
    lang_en.update({item[0]: item[1]})

# Write to JSON
with open('data/lang-en.json', 'w') as write:
    json.dump(lang_en, write, indent=4)
