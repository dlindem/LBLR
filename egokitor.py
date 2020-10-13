from unidecode import unidecode
import csv
import re

with open ('larbasque.txt', 'r', encoding='utf-8') as infile:
    larlemlist = infile.readlines()

with open ('sarasola.txt', 'r', encoding='utf-8') as infile:
    sarlemlist = infile.read().split('\n')
    print(sarlemlist)

with open('mapping.csv', encoding="utf-8") as csvfile:
    mapping = csv.reader(csvfile, delimiter="\t")

    mapdict = {}
    for row in mapping:
        print(row)
        mapdict[row[0]]=row[1]

    with open('result.csv', 'w', encoding='utf-8') as outfile:
        outfile.write('LAR_LEMMA\tEGOKITUA\tSARASOLA\n')
        for oldlem in larlemlist:
            newlem = oldlem.rstrip()
            for rule in mapdict:
                interlem = re.sub(rule, mapdict[rule], newlem)
                newlem = interlem
#                print(rule+' '+mapdict[rule]+' '+interlem)
            if newlem in sarlemlist:
                sarlem = newlem
            elif newlem[-1] == "a" and newlem[:-1] in sarlemlist:
                sarlem = newlem[:-1]
            else:
                sarlem = "0"
            outfile.write(oldlem.rstrip()+'\t'+newlem+'\t'+sarlem+'\n')
