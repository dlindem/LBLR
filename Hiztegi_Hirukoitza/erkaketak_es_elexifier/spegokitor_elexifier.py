from unidecode import unidecode
import csv
import re
from os.path import expanduser
home = expanduser("~")


with open (home+'/Lab_LAR/SpanishLem/LAR_spanish_lem_uniq.txt', 'r', encoding='utf-8') as infile:
    larlemlist = infile.read().split('\n') # reads LAR Spanish item lstst
with open (home+'/Lab_LAR/SpanishLem/Diccionario_Autoridades_lemario.txt', 'r', encoding='utf-8') as infile:
    dalemlist = unidecode(infile.read().replace('ñ', '_')).lower().replace('ss', 's').replace('_', 'ñ').split('\n') # reads DA lemma list entries
    #print(dalemlist)

matches = []
nomatches = ""

print('\nStarted processing...')

with open('spegokitor_result_table.csv', 'w', encoding='utf-8') as outfile:
    outfile.write('LAR_LEMMA\tEGOKITUA\tDA_MATCH\n') # csv header row
    for oldlem in larlemlist:
        oldnorlem = unidecode(oldlem.replace('ñ', '_')).lower().replace('ss', 's').replace('_', 'ñ')
        print(oldnorlem)
        try:
            oldnorlemfirst = re.search(r'^([^ \n]+)', oldnorlem).group(1)
            # look at DA
            if oldnorlemfirst in dalemlist:
                outfile.write(oldlem.rstrip()+'\t'+oldnorlem+'\t'+oldnorlemfirst.rstrip()+'\n')
                matches.append(oldnorlemfirst)

            else: # no match >>> nomatchlist
                nomatches += oldlem+'\t'+oldnorlem+'\t'+oldnorlemfirst+'\n'
            print(oldnorlemfirst)
        except:
            pass



# writes matchlist: items that appear in both lists
matchset = sorted(set(matches))
with open('spegokitor_LAR_and_DA.txt', 'w', encoding='utf-8') as outfile:
    for match in matchset:
        outfile.write(match+'\n')
# writes list of LAR items not in DA
with open('spegokitor_LAR_not_DA.csv', 'w', encoding='utf-8') as outfile:
    outfile.write('LAR_LEMMA\tEGOKITUA\tFAILED_MATCH\n'+nomatches)
# writes list of DA items not in LAR
with open('spegokitor_DA_not_LAR.txt', 'w', encoding='utf-8') as outfile:
    for dalem in dalemlist:
        if dalem not in matchset:
            outfile.write(dalem+'\n')


print('Finished.')
