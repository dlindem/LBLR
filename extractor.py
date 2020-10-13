#extracts headwords and translation equivalents from TEI
import xml.etree.ElementTree as ET
from unidecode import unidecode

tree = ET.parse('D:/Lab_LAR/TEI/LAR.tei.xml')
root = tree.getroot()

with open ('D:/Lab_LAR/TEI/LARlat.csv', 'w', encoding='utf-8') as outfile:
    for entry in root:
        line = ''
        if len(entry.findall('form')) > 0:
            print ("\nNew entry:")
            for orth in entry.iter('orth'):
                print (orth.text)
                line = unidecode(orth.text.replace('ñ', '_')).lower().replace('ss', 's').replace('_', 'ñ')+'\t'+orth.text
            for sense in entry.iter('sense'):
                print (sense.text)
                line = line + '\t' + sense.text
        if len(line) > 0:
            #line.encode('cp1252')
            outfile.write(line+'\n')
