from unidecode import unidecode
import csv
import re

with open ('larbasque.txt', 'r', encoding='utf-8') as infile:
    larlemlist = infile.read().replace(' ','\n').split('\n') # splits basque multiwords into lines, and reads words into list

with open ('D:/Lab_LAR/Sarasola/sarasola.txt', 'r', encoding='utf-8') as infile:
    sarlemlist = infile.read().split('\n') # reads list entries
#    print(sarlemlist)

with open ('D:/Lab_LAR/Sarasola/sarasola1745.txt', 'r', encoding='utf-8') as infile:
    sarlarlemlist = infile.read().split('\n') # reads list entries
#    print(sarlarlemlist)

with open ('wikidata_basque_lexemes.txt', 'r', encoding='utf-8') as infile:
    wdlemlist = infile.read().split('\n') # reads list entries
#    print(wdlemlist)

with open('rules.csv', encoding="utf-8") as csvfile:
    mapping = csv.reader(csvfile, delimiter=",") # reads replace rules

    mapdict = {}
    for row in mapping:
        print(row)
        mapdict[row[0]]=row[1]

    sarmatches = ""
    sarlemmatch = []
    sarlarmatches = ""
    sarlarlemmatch = []
    wdmatches = ""
    wdlemmatch = []
    nomatches = ""

    print('\nStarted processing...')

    with open('egokitor_result_table.csv', 'w', encoding='utf-8') as outfile:
        outfile.write('LAR_LEMMA\tUNIDECODE\tEGOKITUA\tSARASOLA\tSARASOLA1745\tWIKIDATA\n') # csv header row
        for oldlem in larlemlist:
            oldnorlem = unidecode(oldlem.rstrip())
            newlem = oldnorlem
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
            elif len(newlem) > 3 and newlem[-2] == "a" and newlem[-1] == "k" and newlem[:-2] in sarlemlist: # asks for match if letter "-ak" is stripped off from LAR_LEMMA
                sarlem = newlem[:-2]
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
            elif len(newlem) > 3 and newlem[-2] == "a" and newlem[-1] == "k" and newlem[:-2] in sarlemlist: # asks for match if letter "-ak" is stripped off from LAR_LEMMA
                sarlarlem = newlem[:-2]
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
            elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-1] in wdlemlist: # asks for match if letter "-k" is stripped off from EGOKITUA finishing with "-ak"
                wdlem = newlem[:-2]
            elif len(newlem) > 3 and newlem[-2]+newlem[-1] == "ak" and newlem[:-2] in wdlemlist: # asks for match if letter "-ak" is stripped off from EGOKITUA
                wdlem = newlem[:-2]
            else:
                wdlem = ""
            if wdlem != "":
                wdlemmatch.append(wdlem)
                wdmatches += wdlem+','+oldlem+'\n'
            # no match >>> nomatchlist
            if sarlem == "" and wdlem == "":
                nomatches += oldlem+','+newlem+'\n'

            outfile.write(oldlem.rstrip()+'\t'+oldnorlem+'\t'+newlem+'\t'+sarlem+'\t'+sarlarlem+'\t'+wdlem+'\n')
    # writes Sarasola matches unique
    sarmatchset = set(sarlemmatch)
    with open('egokitor_sarasolamatches_unique.txt', 'w', encoding='utf-8') as outfile:
        for match in sarmatchset:
            outfile.write(match+','+'\n')
    sarlarmatchset = set(sarlarlemmatch)
    # writes Sarasola matching pairs
    with open('egokitor_sarasolamatches.csv', 'w', encoding='utf-8') as outfile:
        outfile.write(sarmatches)
    # writes Sarasola1745 matches unique
    sarlarmatchset = set(sarlarlemmatch)
    with open('egokitor_sarasola1745matches_unique.txt', 'w', encoding='utf-8') as outfile:
        for match in sarlarmatchset:
            outfile.write(match+','+'\n')
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
    # writes nomatchlist
    with open('egokitor_nomatches.csv', 'w', encoding='utf-8') as outfile:
        outfile.write(nomatches)

print('Finished.')
