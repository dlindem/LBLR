#extracts headwords and translation equivalents from TEI
import xml.etree.ElementTree as ET
from unidecode import unidecode
import re

tree = ET.parse('D:/Lab_LAR/TEI/LAR.tei.xml')
root = tree.getroot()

with open ('D:/Lab_LAR/TEI/LAR_eu_es.csv', 'w', encoding='utf-8') as euesfile, open ('D:/Lab_LAR/TEI/LAR_es_eu.csv', 'w', encoding='utf-8') as eseufile:
    for entry in root:
        sarrera = ''
        if len(entry.findall('form')) > 0:
            #print ("\nNew entry:")
            for orth in entry.iter('orth'):
                if re.match(r"[A-ZÁÀÉÈÍÓÒÚÙÑñ]", orth.text[0]):
                    #sarrera = unidecode(orth.text.replace('ñ', '_')).lower().replace('ss', 's').replace('_', 'ñ')+'\t'+orth.text
                    sarrera = orth.text
            equivlist = []
            for equiv in entry.iter('quote'):
                equivlist.append(equiv.text)

        if len(sarrera) > 0 and len(equivlist) > 0:
            #line.encode('cp1252')
            for equiv in equivlist:
                euesfile.write(equiv+'\t'+sarrera+'\n')
            eseufile.write(sarrera)
            for equiv in equivlist:
                eseufile.write('\t'+equiv)
            eseufile.write('\n')
