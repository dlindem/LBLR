import requests
import time
import json, re

def get_wikisource(pagenums=[]):
    pagedict = {}
    wikitext = ""
    print('Fetching Wikisource pages...')
    for pagenum in pagenums: # Larramendi_1745_dictionary_body.pdf has 1656 pages, numbered from 1 to 1656
        pagejson = requests.get('https://eu.wikisource.org/w/api.php?action=parse&page=Orrialde:Larramendi_1745_dictionary_body.pdf/'+str(pagenum)+'&prop=wikitext&format=json', headers={"User-Agent":"User:DL2204 python requests"})
        # print(pagejson.text)
        pagedict[str(pagenum)] = pagejson.json()
        print('Got JSON version of page number '+str(pagenum))
        pagewikitext = pagejson.json()['parse']['wikitext']['*']
        cleantext = re.sub(r'<BR/>', '', pagewikitext)
        cleantext = re.sub(r'<pagequality[^>]*>', '', cleantext)
        cleantext = re.sub(r'<noinclude>[^<]*</noinclude>', '', cleantext)
        wikitext += cleantext+"\n"
        time.sleep(1)
    print(str(pagedict))

    with open('pagedict.json', 'w', encoding="utf-8") as json_file:
        json.dump(pagedict, json_file, ensure_ascii=False, indent=2)
    print('Saved to JSON file "pagedict.json".')

    return wikitext
