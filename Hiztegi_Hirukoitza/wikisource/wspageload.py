import requests
import time
import json

pagedict = {}
for pagenum in range(1656): # Larramendi_1745_dictionary_body.pdf has 1656 pages, numbered from 1 to 1656
    pagejson = requests.get('https://eu.wikisource.org/w/api.php?action=parse&page=Orrialde:Larramendi_1745_dictionary_body.pdf/'+str(pagenum+1)+'&prop=wikitext&format=json')
    print(pagejson.json())
    pagedict[str(pagenum+1)] = pagejson.json()

    print('\n...that was JSON version of page number '+str(pagenum+1)+'\n')
    time.sleep(1)
print(str(pagedict))

with open('D:/Lab_LAR/pagedict.json', 'w', encoding="utf-8") as json_file:
	json.dump(pagedict, json_file, ensure_ascii=False, indent=2)
print('Finished and saved to JSON file.')
