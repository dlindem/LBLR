import requests
import time
import json

pagedict = {}
for pagenum in [1, 4, 5]: # Larramendi_1745_dictionary_body.pdf has 1656 pages, numbered from 1 to 1656
    pagejson = requests.get('https://eu.wikisource.org/w/api.php?action=parse&page=Orrialde:Larramendi_1745_dictionary_body.pdf/'+str(pagenum)+'&prop=wikitext&format=json', headers={"User-Agent":"User:DL2204 python requests"})
    print(pagejson.text)
    pagedict[str(pagenum+1)] = pagejson.json()

    print('\n...that was JSON version of page number '+str(pagenum+1)+'\n')
    time.sleep(1)
print(str(pagedict))

with open('pagedict.json', 'w', encoding="utf-8") as json_file:
    json.dump(pagedict, json_file, ensure_ascii=False, indent=2)
print('Finished and saved to JSON file.')
