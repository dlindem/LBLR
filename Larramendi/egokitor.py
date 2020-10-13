from unidecode import unidecode
import csv
import re

with open ('larbasque.txt', 'r', encoding='utf-8') as infile:
    larlemlist = infile.read().replace(' ','\n').split('\n') # splits basque multiwords into lines, and reads words into list

with open ('D:/Lab_LAR/Sarasola/sarasola.txt', 'r', encoding='utf-8') as infile:
    sarlemlist = infile.read().split('\n') # reads list entries
#    print(sarlemlist)

with open ('wikidata_basque_lexemes.txt', 'r', encoding='utf-8') as infile:
    wdlemlist = infile.read().split('\n') # reads list entries
#    print(wdlemlist)

with open('mapping.csv', encoding="utf-8") as csvfile:
    mapping = csv.reader(csvfile, delimiter="\t") # reads replace rules

    mapdict = {}
    for row in mapping:
        print(row)
        mapdict[row[0]]=row[1]

    with open('result.csv', 'w', encoding='utf-8') as outfile:
        outfile.write('LAR_LEMMA\tUNIDECODE\tEGOKITUA\tSARASOLA\tWIKIDATA\n')
        for oldlem in larlemlist:
            oldnorlem = unidecode(oldlem.rstrip())
            newlem = oldnorlem
            for rule in mapdict:
                interlem = re.sub(rule, mapdict[rule], newlem)
                newlem = interlem
#                print(rule+' '+mapdict[rule]+' '+interlem)
            if newlem in sarlemlist: # if EGOKITUA is found in SARASOLA
                sarlem = newlem
            elif newlem[-1] == "a" and newlem[:-1] in sarlemlist: # asks for match if letter "-a" is stripped off from LAR_LEMMA
                sarlem = newlem[:-1]
            else:
                sarlem = ""
            if newlem in wdlemlist: # if EGOKITUA is found in WIKIDATA
                wdlem = newlem
            elif newlem[-1] == "a" and newlem[:-1] in wdlemlist: # asks for match if letter "-a" is stripped off from LAR_LEMMA
                wdlem = newlem[:-1]
            else:
                wdlem = ""

            outfile.write(oldlem.rstrip()+'\t'+oldnorlem+'\t'+newlem+'\t'+sarlem+'\t'+wdlem+'\n')
