from unidecode import unidecode
import csv
import re
#from os.path import expanduser
#home = expanduser("~")
home = "D:"

with open ('LAR_eu_es.csv', 'r', encoding='utf-8') as infile:
    #larlemlist = infile.read().replace(' ','\n').split('\n') # splits basque multiwords into lines, and reads words into list
    larlemlist = infile.read().split('\n') # reads words into list

with open (home+'/Lab_LAR/Sarasola/sarasola.txt', 'r', encoding='utf-8') as infile:
    sarlemlist = infile.read().split('\n') # reads list entries
#    print(sarlemlist)

with open (home+'/Lab_LAR/Sarasola/sarasola1745.txt', 'r', encoding='utf-8') as infile:
    sarlarlemlist = infile.read().split('\n') # reads list entries
#    print(sarlarlemlist)

with open ('wikidata_basque_lexemes.txt', 'r', encoding='utf-8') as infile:
    wdlemlist = infile.read().split('\n') # reads list entries
#    print(wdlemlist)
with open (home+'/Lab_LAR/OEH/oeh_lemak_egok.txt', 'r', encoding='utf-8') as infile:
    oehlemlist = infile.read().replace('_', ' ').split('\n') # reads list entries, converts "_" hyphen-or-space normalization into space
#    print(oehlemlist)

with open('rules.csv', encoding="utf-8") as csvfile:
    mapping = csv.reader(csvfile, delimiter=",") # reads replace rules

    mapdict = {}
    for row in mapping:
#        print(row)
        mapdict[row[0]]=row[1]

    sarmatches = ""
    sarlemmatch = []
    sarlarmatches = ""
    sarlarlemmatch = []
    wdmatches = ""
    wdlemmatch = []
    oehmatches = ""
    oehlemmatch = []
    nomatches = ""
    nlsarrerakcsv = ""

    print('\nWorking...')

    with open('egokitor_result_table.csv', 'w', encoding='utf-8') as outfile:
        outfile.write('EGOKITUA\tUNIDECODE\tJATORRIZKOA\tSARASOLA\tSARASOLA1745\tWIKIDATA\tOEH\tOEHLINK\n') # csv header row
        for line in larlemlist:
            if re.match(r"[^\t]+\t", line): # if sarrera has a translation
                splitline = line.split('\t')
#                print(splitline)
                oldlem = splitline[0]
                sarrera = splitline[1]
                oldnorlem = unidecode(oldlem.replace('ñ', '_')).replace('_', 'ñ').rstrip()
                newlem = oldnorlem
                nlsarrerakcsv += newlem+'\t'+sarrera+'\n'
                for rule in mapdict:
                    interlem = re.sub(rule, mapdict[rule], newlem)
                    if len(interlem) > 0:
                        newlem = interlem
    #                print(rule+' '+mapdict[rule]+' '+interlem)
                # look at Sarasola
                if newlem in sarlemlist: # if EGOKITUA is found in SARASOLA
                    sarlem = newlem
                elif newlem[-1] == "a" and newlem[:-1] in sarlemlist: # asks for match if letter "-a" is stripped off from LAR_LEMMA
                    sarlem = newlem[:-1]
                elif len(newlem) > 3 and newlem[-3]+newlem[-2]+newlem[-1] == "rra" and newlem[:-2] in sarlemlist: # asks for match if r"-ra" is stripped off from EGOKITUA finishing with "-ak"
                    sarlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-1] in sarlemlist: # asks for match if "-k" is stripped off from EGOKITUA
                    sarlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-2] in sarlemlist: # asks for match if "-ak" is stripped off from EGOKITUA
                    sarlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-4]+newlem[-3]+newlem[-2]+newlem[-1] == "rrak" and newlem[:-3] in sarlemlist: # asks for match if "-rak" is stripped off from EGOKITUA
                    oehlem = newlem[:-3]
                else:
                    sarlem = ""
                if sarlem != "":
                    sarlemmatch.append(sarlem)
                    sarmatches += sarlem+','+oldlem+'\n'
                # look at Sarasola lemmata marked with date "1745"
                if newlem in sarlarlemlist: # if EGOKITUA is found in SARASOLA1745
                    sarlarlem = newlem
                elif newlem[-1] == "a" and newlem[:-1] in sarlarlemlist: # asks for match if letter "-a" is stripped off from LAR_LEMMA
                    sarlarlem = newlem[:-1]
                elif len(newlem) > 3 and newlem[-3]+newlem[-2]+newlem[-1] == "rra" and newlem[:-2] in sarlarlemlist: # asks for match if r"-ra" is stripped off from EGOKITUA finishing with "-ak"
                    sarlarlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-1] in sarlarlemlist: # asks for match if "-k" is stripped off from EGOKITUA
                    sarlarlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-2] in sarlarlemlist: # asks for match if "-ak" is stripped off from EGOKITUA
                    sarlarlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-4]+newlem[-3]+newlem[-2]+newlem[-1] == "rrak" and newlem[:-3] in sarlarlemlist: # asks for match if r"-rak" is stripped off from EGOKITUA
                    oehlem = newlem[:-3]
                else:
                    sarlarlem = ""
                if sarlarlem != "":
                    sarlarlemmatch.append(sarlarlem)
                    sarlarmatches += sarlarlem+','+oldlem+'\n'
                # look at Wikidata
                if newlem in wdlemlist: # if EGOKITUA is found in WIKIDATA
                    wdlem = newlem
                elif newlem[-1] == "a" and newlem[:-1] in wdlemlist: # asks for match if letter "-a" is stripped off from EGOKITUA
                    wdlem = newlem[:-1]
                elif len(newlem) > 3 and newlem[-3]+newlem[-2]+newlem[-1] == "rra" and newlem[:-2] in wdlemlist: # asks for match if r"-ra" is stripped off from EGOKITUA finishing with "-ak"
                    wdlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-1] in wdlemlist: # asks for match if letter "-k" is stripped off from EGOKITUA finishing with "-ak"
                    wdlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-2] in wdlemlist: # asks for match if letter "-ak" is stripped off from EGOKITUA
                    wdlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-4]+newlem[-3]+newlem[-2]+newlem[-1] == "rrak" and newlem[:-3] in wdlemlist: # asks for match if r"-rak" is stripped off from EGOKITUA
                    oehlem = newlem[:-3]
                else:
                    wdlem = ""
                if wdlem != "":
                    wdlemmatch.append(wdlem)
                    wdmatches += wdlem+','+oldlem+'\n'
                # look at OEH
                if newlem in wdlemlist: # if EGOKITUA is found in OEH
                    oehlem = newlem
                elif newlem[-1] == "a" and newlem[:-1] in oehlemlist: # asks for match if letter "-a" is stripped off from EGOKITUA
                    oehlem = newlem[:-1]
                elif len(newlem) > 3 and newlem[-3]+newlem[-2]+newlem[-1] == "rra" and newlem[:-2] in oehlemlist: # asks for match if r"-ra" is stripped off from EGOKITUA finishing with "-ak"
                    oehlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-1] in oehlemlist: # asks for match if "-k" is stripped off from EGOKITUA finishing with "-ak"
                    oehlem = newlem[:-1]
                elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-2] in oehlemlist: # asks for match if "-ak" is stripped off from EGOKITUA
                    oehlem = newlem[:-2]
                elif len(newlem) > 3 and newlem[-4]+newlem[-3]+newlem[-2]+newlem[-1] == "rrak" and newlem[:-3] in oehlemlist: # asks for match if r"-rak" is stripped off from EGOKITUA
                    oehlem = newlem[:-3]
                else:
                    oehlem = ""
                    oehlink = ""
                if oehlem != "":
                    oehlemmatch.append(oehlem)
                    oehmatches += oehlem+','+oldlem+'\n'
                    oehlink = 'https://www.euskaltzaindia.eus/index.php?option=com_oehberria&task=bilaketa&Itemid=413&lang=eu&query='+oehlem
                # no match >>> nomatchlist
                if sarlem == "" and wdlem == "" and oehlem =="":
                    nomatches += oldlem+','+newlem+'\n'

                outfile.write(newlem+'\t'+oldnorlem+'\t'+oldlem.rstrip()+'\t'+sarlem+'\t'+sarlarlem+'\t'+wdlem+'\t'+oehlem+'\t'+oehlink+'\n')
    # writes Sarasola matches unique
    sarlemmatchset = set(sarlemmatch)
    with open('egokitor_sarasolamatches_unique.txt', 'w', encoding='utf-8') as outfile:
        for match in sarlemmatchset:
            outfile.write(match+'\n')
    sarlarmatchset = set(sarlarlemmatch)
    # writes Sarasola matching pairs
    with open('egokitor_sarasolamatches.csv', 'w', encoding='utf-8') as outfile:
        outfile.write(sarmatches)
    # writes Sarasola1745 matches unique
    sarlarlemmatchset = set(sarlarlemmatch)
    with open('egokitor_sarasola1745matches_unique.txt', 'w', encoding='utf-8') as outfile:
        for match in sarlarlemmatchset:
            outfile.write(match+'\n')
    # writes Sarasola1745 matching pairs
    with open('egokitor_sarasola1745matches.csv', 'w', encoding='utf-8') as outfile:
        outfile.write(sarlarmatches)
    # writes wikidata matches unique
    wdlemmatchset = set(wdlemmatch)
    with open('egokitor_wikidatamatches_unique.txt', 'w', encoding='utf-8') as outfile:
        for match in wdlemmatchset:
            outfile.write(match+'\n')
    # writes Wikidata matching pairs
    with open('egokitor_wikidatamatches.csv', 'w', encoding='utf-8') as outfile:
        outfile.write(wdmatches)
    # writes OEH matches unique
    oehlemmatchset = set(oehlemmatch)
    with open('egokitor_oehmatches_unique.txt', 'w', encoding='utf-8') as outfile:
        for match in oehlemmatchset:
            outfile.write(match+'\n')
    # writes OEH matching pairs
    with open('egokitor_oehmatches.csv', 'w', encoding='utf-8') as outfile:
        outfile.write(oehmatches)
    # writes nomatchlist
    with open('egokitor_nomatches.csv', 'w', encoding='utf-8') as outfile:
        outfile.write(nomatches)
    # writes EGOKITUA - SARRERA matching pairs
    with open('egokitor_sarrerak.csv', 'w', encoding='utf-8') as outfile:
        outfile.write(nlsarrerakcsv)

print('Finished.')
