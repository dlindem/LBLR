#!/usr/bin/env python
# Usage: python alto_ocr_text.py <altofile>

import codecs
import os
import sys
import xml.etree.ElementTree as ET
import re

alto_dir = "D:/Lab_LAR/ALTO"
wtxt_dir = "D:/Lab_LAR/WTXT"


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
                        minhpos = hpos
                print('minhpos in '+xmlfile+' is '+str(minhpos))
                for lines in tree.iterfind('.//{%s}TextLine' % xmlns):
                    hpos= int(lines.attrib.get('HPOS'))

                    wikitxtline = ''

                    for altostring in lines.findall('{%s}String' % xmlns):
                        content = altostring.attrib.get('CONTENT') + ' '
                        wikitxtword = re.sub(r"@([^ \n<]+)", r"''\1''", content)
                        wikitxtline += wikitxtword



                    if hpos < minhpos+115 and re.search('^[A-Z]', wikitxtline) != None and hpos < lasthpos + 20:
                        indentchar = ':'
                    elif hpos < 1000:
                        indentchar = '::'
                    else:
                        indentchar = ':::::'

                    outfile.write('</br>\n'+str(hpos)+' '+indentchar+' '+wikitxtline)
                    lasthpos = hpos


            else:
                print('ERROR: Not a valid ALTO file (namespace declaration missing)')
