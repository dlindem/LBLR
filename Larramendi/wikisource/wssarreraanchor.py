import requests
import time
import json
import csv
import re
from unidecode import unidecode

alfdict = {}
with open('laralfabetoatalak.csv', encoding="utf-8") as csvfile: # source file
    alfatalak = csv.reader(csvfile, delimiter="\t")
    for row in alfatalak:
        alfdict[int(row[0])] = row[1] # first row: page number, second row: letter(s)
    print(str(alfdict))

with open('D:/Lab_LAR/pagedict.json', 'r', encoding="utf-8") as json_file:
	pagedict = json.load(json_file)

newpagedict = {}
homonym = ""
for num in range(len(pagedict)):
    pagenum = num+1
    wikitext = pagedict[str(pagenum)]['parse']['wikitext']['*']
    wspage = pagedict[str(pagenum)]['parse']['title']

    wikitext = re.sub(r'\{\{sarrera[^\}]+\}\}', '', wikitext) # remove old 'sarrera' anchor
    letters = alfdict[pagenum]
    for letter in range(len(letters)):
        alf = letters[letter]
        burukop = len(re.findall(r'\n:'+alf, wikitext))
        for buru in range(burukop):
            burua = re.findall(r'\n:('+alf+'[^,\.:; \']*)', wikitext)[0]
            normburua = unidecode(burua.replace('ñ', '_')).lower().replace('ss', 's').replace('_', 'ñ').rstrip()
            if normburua == homonym:
                homcount += 1
                sarburua = normburua+str(homcount)
            else:
                homcount = 1
                sarburua = normburua
            print(burua)
            search = '\n:'+burua
            replace = '\n:{{sarrera|'+sarburua+'}}'+burua
            wikitext = wikitext.replace(search, replace, 1)
            homonym = normburua

        newpagedict[wspage] = wikitext
    print(wikitext)

with open('D:/Lab_LAR/anchoreddict.json', 'w', encoding="utf-8") as json_file:
	json.dump(newpagedict, json_file, ensure_ascii=False, indent=2)
print('Finished and saved to JSON file.')
