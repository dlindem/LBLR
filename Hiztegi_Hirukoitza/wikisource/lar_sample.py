from wspageload import *

pagenums = range(988, 1035)
wikitext = get_wikisource(pagenums)

with open('wikisource_text.txt', 'w') as f:
    f.write(wikitext)