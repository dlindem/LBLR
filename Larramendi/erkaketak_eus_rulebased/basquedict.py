import requests
import time
import json
import csv
import re
from unidecode import unidecode

with open('D:/Lab_LAR/basquedict.json', 'r', encoding="utf-8") as json_file:
	pagedict = json.load(json_file)
basqueitems = {}
for sarrera in pagedict:
	candidates = pagedict[sarrera].get('candidates')
	if candidates != None:
		
		for n in range(len(candidates)):
			if candidates[n] not in basqueitems:
				basqueitems[candidates[n]] = {'sarrerak':[sarrera]}
			else:
				if sarrera not in basqueitems[candidates[n]]['sarrerak']:
					basqueitems[candidates[n]]['sarrerak'].append(sarrera)




with open('reversedict.json', 'w', encoding="utf-8") as json_file:
	json.dump(basqueitems, json_file, ensure_ascii=False, indent=2)
print('Finished and saved to JSON file.')
