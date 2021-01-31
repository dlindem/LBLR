import csv
import re
import json


with open ('D:/Lab_LAR/Wikidata/wdpos_result.json', 'r', encoding='utf-8') as infile:
    dict = json.load(infile)

result = "lar_lemma\twdlexeme\twdpos\twdurl\n"
for lemma in dict:
    for lempos in dict[lemma]:
        print(dict[lemma])
        print(str(lempos))
        result += lemma+'\t'+lempos['lemma']['value']+'\t'+lempos['categoryLabel']['value']+'\t'+lempos['lexemeId']['value']+'\n'

print(result)

with open('D:/Lab_LAR/Wikidata/wd4tlex.csv', 'w', encoding='utf-8') as outfile:
    outfile.write(result)
