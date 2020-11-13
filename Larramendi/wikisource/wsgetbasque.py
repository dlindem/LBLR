import requests
import time
import json
import csv
import re
from unidecode import unidecode

with open('D:/Lab_LAR/anchoreddict.json', 'r', encoding="utf-8") as json_file:
	pagedict = json.load(json_file)

basquedict = {}
wikitext = ""

for num in range(len(pagedict)):
    page = 'Orrialde:Larramendi 1745 dictionary body.pdf/'+str(num+1)
    pagetext = re.sub(r'<[^>]+>', '', pagedict[page])
    wikitext += '\n['+str(num+1)+']\n'+pagetext # join pages to single text

sarrerak = wikitext.split('{{sarrera|')

for sarrera in sarrerak:
    esburu = re.search(r'([^\}]+)\}\}', sarrera)
    if esburu != None:
        esburu = esburu.group(1)

        basquedict[esburu] = {}
        sarrera = re.sub(r'\- *\'\' *\n:*\'\'', '', sarrera) # join end-of-line-hyphened italics words
        sarrera = re.sub(r'\n:+' ,' ', sarrera) # join lines, eliminate indent markers
        basques = re.findall(r'\'\'[^\']+\'\'', sarrera)
        for n in range(len(basques)):
            basques[n] = basques[n].replace("'", "")
            basquedict[esburu]['candidates'] = basques


#print(sarrerak)

with open('D:/Lab_LAR/basquedict.json', 'w', encoding="utf-8") as json_file:
	json.dump(basquedict, json_file, ensure_ascii=False, indent=2)
print('Finished and saved to JSON file.')
