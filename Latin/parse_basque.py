import json, re
from xml.etree import ElementTree

with open('content_pos.json') as file:
    content = json.load(file)

result = {}

#nouns
result['noun'] = {}
found_count = 0
not_found_count = 0
for id in content['noun']:
    entry = ElementTree.fromstring(content['noun'][id]['full_entry'])
    gender = content['noun'][id]['gender']
    senses = []
    for basque in entry.findall('basque'):
        straightforward_re = re.search(fr'{gender}\.: (.*)\.', basque.text)
        if straightforward_re:
            found_count += 1
            sense_blocks = straightforward_re.group(1).split(";")
            for sense_block in sense_blocks:
                block_senses = sense_block.split(",")
                stripped_senses = []
                for sense in block_senses:
                    stripped_senses.append(sense.strip())
                senses.append(stripped_senses)

    if len(senses) == 0:
        not_found_count += 1
        senses = None
    else:
        result['noun'][id] = content['noun'][id]
        result['noun'][id]['senses'] = senses

with open('content_pos_translations.json', 'w') as file:
    json.dump(result, file, indent=2)





print(f"Found {found_count} noun translation blocks, did not find {not_found_count} translation blocks")