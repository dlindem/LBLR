#!/usr/bin/env python
# converts Larramendi dictionary Kraken ALTO-XML export to Wikitext, looks at indentation (TextLine HPOS), and applies Wikitext indent markers (":")

import codecs
import os
import sys
import xml.etree.ElementTree as ET
import re

alto_dir = "D:/Lab_LAR/ALTO"
wtxt_dir = "D:/Lab_LAR/WTXT"

spanishlem = ''
spanishlemdir = 'D:/Lab_LAR/SpanishLem'

for path, dirs, files in os.walk(alto_dir):
    for file in files:
        xmlfile = os.path.join(path, alto_dir, file)
        #print(xmlfile)
        with open(wtxt_dir+'/'+file.replace('.xml','.wtxt'), 'w', encoding='utf-8') as outfile:
            namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
                 'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#'}
            tree = ET.parse(xmlfile)
            xmlns = tree.getroot().tag.split('}')[0].strip('{')
            if xmlns in namespace.values():
                minhpos = 1000
                for lines in tree.iterfind('.//{%s}TextLine' % xmlns):
                    hpos= int(lines.attrib.get('HPOS'))
                    if hpos < minhpos:
                        minhpos = hpos # finds line with least indent
                print('minhpos in '+xmlfile+' is '+str(minhpos))
                for lines in tree.iterfind('.//{%s}TextLine' % xmlns):
                    hpos= int(lines.attrib.get('HPOS'))

                    wikitxtline = ''

                    for altostring in lines.findall('{%s}String' % xmlns):
                        content = altostring.attrib.get('CONTENT') + ' '
                        wikitxtword = re.sub(r"@([^ \n\.,;\?:<]+)", r"''\1''", content) # @words to ''words''. Words end with space, EOL, "<", or interpunction
                        wikitxtline += wikitxtword



                    if hpos < minhpos+115 and re.search('^[A-Z]', wikitxtline) != None and hpos < lasthpos + 20:
                        indentchar = ':' # simple indent for lines that start between minhpos and minhpos +115, and start with a capital letter
                        spanishlem += re.sub(" +$", "", re.sub(r"(^[^,\.']+).*", r"\1", wikitxtline))+"\n"
                    elif hpos < 1000:
                        indentchar = '::' # double indent for lines that start after minhpos+115 or do not start with a capital letter
                    else:
                        indentchar = ':::::' # five indent markers for lines that start after hpos 1000

                    outfile.write('</br>\n'+indentchar+wikitxtline)
                    lasthpos = hpos


            else:
                print('ERROR: Not a valid ALTO file (namespace declaration missing)')


with open(spanishlemdir+'/'+'LAR_spanish_lem.txt', 'w', encoding='utf-8') as outfile:
    outfile.write(spanishlem)
