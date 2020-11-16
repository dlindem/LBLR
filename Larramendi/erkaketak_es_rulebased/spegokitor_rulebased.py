from unidecode import unidecode
import csv
import re
from os.path import expanduser
import json
#home = expanduser("~")
home = "D:/"

with open('D:/Lab_LAR/basquedict.json', 'r', encoding="utf-8") as json_file:
	pagedict = json.load(json_file)

dalemcsv = "EGOKITUA\tJATORRIZKOA\n"
dalemdict = {}
with open (home+'/Lab_LAR/SpanishLem/Diccionario_Autoridades_lemario.txt', 'r', encoding='utf-8') as infile:
    dalemlist = infile.read().split('\n')
    for dalem in dalemlist:
        dalemegok = unidecode(dalem.replace('ñ', '_')).lower().replace('ss', 's').replace('_', 'ñ').rstrip()
        dalemdict[dalemegok] = dalem.rstrip()
        dalemcsv += dalemegok+'\t'+dalem.rstrip()+'\n'

    print(dalemdict)

matches = []
nomatches = []


print('\nStarted processing...')

with open('spegokitor_result_table.csv', 'w', encoding='utf-8') as outfile:
    outfile.write('LAR_LEMMA_EGOKITUA\tANCHORTEXT\tANCHORLINK\tEUS_CANDIDATES\n') # csv header row
    for sarrera in pagedict:
        larlem = re.sub(r'\d', '', sarrera).lower()
        homnr = re.search(r'\d', sarrera)
        if homnr == None:
            homnr = 1
        else:
            homnr = homnr.group(0)
        anchor = 'https://eu.wikisource.org/wiki/Hiztegi_Hirukoitza/'+sarrera[0]+'#'+sarrera
        # get Basque equiv. candidates
        candidates = pagedict[sarrera].get('candidates')

        if candidates != None:
            candidateslist = ""
            for candidate in candidates:
                #eseucsv += larlem+'\t'+sarrera+'\thttps://eu.wikisource.org/wiki/Hiztegi_Hirukoitza/'+sarrera[0]+'#'+sarrera+'\t'+candidate+'\n'
                candidateslist += candidate.replace('ſ','s')+', '
            candidateslist = candidateslist[:-2]
        else:
            candidateslist = ""

        # look at DA
        if larlem in dalemdict:
            print ('match: '+larlem)
            matches.append(larlem) # match >>> matchlist
        else:
            nomatches.append(larlem) # no match >>> nomatchlist
        outfile.write(larlem+'\t'+sarrera+'\t'+anchor+'\t'+candidateslist+'\n')

print('\nWriting results to files...')

# writes matchlist: items that appear in both lists
matchset = sorted(set(matches))
with open('spegokitor_LAR_and_DA_uniq.txt', 'w', encoding='utf-8') as outfile:
    for match in matchset:
        outfile.write(match+'\n')
# writes list of LAR items not in DA
nomatchset = sorted(set(nomatches))
with open('spegokitor_LAR_not_DA.txt', 'w', encoding='utf-8') as outfile:
    for nomatch in nomatchset:
        outfile.write(nomatch+'\n')
# writes list of DA items not in LAR
with open('spegokitor_DA_not_LAR.txt', 'w', encoding='utf-8') as outfile:
    for dalem in dalemdict:
        if dalem not in matchset:
            outfile.write(dalem+'\n')
# writes DA csv for TshwaneLex
with open('D:/Lab_LAR/TLex/DA_lemma_egok.csv', 'w', encoding='utf-8') as outfile:
	outfile.write(dalemcsv)


print('Finished.')
