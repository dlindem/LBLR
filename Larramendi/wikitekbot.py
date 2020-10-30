import os
import re
import shlex, subprocess
import time

wtxt_dir = "D:/Lab_Lar/WTXT"
for path, dirs, files in os.walk(wtxt_dir):
    for file in files:
        pnum = int(re.search(r'^([0-9]+)_', file).group(1))
        print ('Now processing page number '+str(pnum)+'...')
        txtfile = os.path.join(path, wtxt_dir+"/", file)
        #print (file)
        botcommandline = "python D:/Lab_LAR/pywikibot/pwb.py pagefromfile.py -textonly -notitle -force -file:"+txtfile+" -title:Orrialde:Larramendi_1745_dictionary_body.pdf/"+str(pnum)
        args = shlex.split(botcommandline)
        print(args)
        p = subprocess.Popen(args)
        time.sleep(5)
