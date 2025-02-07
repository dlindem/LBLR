#extracts headwords and translation equivalents from TEI
import xml.etree.ElementTree as ET
from unidecode import unidecode
import re

tree = ET.parse('D:/Lab_LAR/TEI/LAR.tei.xml')
root = tree.getroot()

with open ('LAR_eu_es.csv', 'w', encoding='utf-8') as euesfile, open ('LAR_es_eu.csv', 'w', encoding='utf-8') as eseufile:
    hom = ""
    for entry in root:
        sarrera = ''
        if len(entry.findall('form')) > 0:
            #print ("\nNew entry:")
            for orth in entry.iter('orth'):
                if re.match(r"[A-ZÁÀÉÈÍÓÒÚÙÑñ]", orth.text[0]):
                    #sarrera = unidecode(orth.text.replace('ñ', '_')).lower().replace('ss', 's').replace('_', 'ñ')+'\t'+orth.text.replace('ſ','s').lower()
                    #sarrera = orth.text
                    if orth.text == hom:
                        homnr += 1
                    else:
                        homnr = 1
                    saregok = unidecode(orth.text.replace('ñ', '_')).lower().replace('ss', 's').replace('_', 'ñ')
                    if homnr > 1:
                        sarrera = saregok+'\t'+saregok+str(homnr)+'\t'+orth.text.replace('ſ','s').lower()
                    else:
                        sarrera = saregok+'\t'+saregok+'\t'+orth.text.replace('ſ','s').lower()
                    hom = orth.text
            equivlist = []
            for equiv in entry.iter('quote'):
                equivlist.append(equiv.text)

        if len(sarrera) > 0 and len(equivlist) > 0:
            #line.encode('cp1252')
            for equiv in equivlist:
                euesfile.write(equiv+'\t'+sarrera+'\n')
            eseufile.write(sarrera+'\t'+equivlist[0].replace('ſ','s'))
            equivlist.pop(0)
            for equiv in equivlist:
                eseufile.write(', '+equiv.replace('ſ','s'))
            eseufile.write('\n')
        elif len(sarrera) > 0 and len(equivlist) == 0:
            eseufile.write(sarrera+'\n')
