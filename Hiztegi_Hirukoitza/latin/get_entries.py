import json
import time

with open('D:/Lab_LAR/anchoreddict_without_noinclude.json', 'r', encoding="utf-8") as json_file:
	anchoreddict = json.load(json_file)

text = ""
for page in anchoreddict:
	text += anchoreddict[page].replace("\n","")

entries = text.split('{{sarrera|')
latin_dict = {}
for entry in entries:
	entry = entry.split("}}")
	print(str(entry))
	headword = entry[0]
	if len(entry) > 1:
		content = entry[1].replace("-::","").replace("- ::","").replace(":","").split("Lat.") # remove wikitext indent, hyphen at EOL
		pre_lat = content[0]
		if len(content) > 1:
			post_lat = content[1].strip().split(".")[0] # until the first dot
			if len(post_lat) > 1:
				print(post_lat)
				latin_dict[headword] = post_lat
		else:
			print('No Latin.')
	else:
		print('ERROR')
	#time.sleep(0.2)

with open('D:/Lab_LAR/latin_dict.json', 'w', encoding="utf-8") as json_file:
	json.dump(latin_dict, json_file)
