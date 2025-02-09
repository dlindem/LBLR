import os
import re
import shlex, subprocess
import time
import json

with open('D:/Lab_LAR/anchoreddict.json', 'r', encoding="utf-8") as json_file:
	anchoreddict = json.load(json_file)

for page in anchoreddict:
    pagetitle = page.replace(' ', '_')
    pagenum = int(re.search(r'pdf/([0-9]+)', pagetitle).group(1))
    if pagenum > 0: # page number range to upload
        print ('Now processing page '+str(pagenum)+'...')
        wtxtfile = 'D:/Lab_LAR/WTXT_anchored/'+pagetitle.replace('.', '_').replace('/', '_').replace(':','_')
        with open(wtxtfile, 'w', encoding='utf-8') as singlefile:
            singlefile.write(anchoreddict[page])
        botcommandline = 'python D:/Lab_LAR/pywikibot/pwb.py pagefromfile.py -textonly -notitle -force -pt:2 -file:'+wtxtfile+' -bot:True -title:'+pagetitle+' -summary:"Bot: Sarrera-aingurak jarri. "'
        args = shlex.split(botcommandline)
        print(args)
        p = subprocess.Popen(args)
        time.sleep(5) # seems to be important
