import json, re, csv
from xml.etree import ElementTree

with open('data/entries_for_sense_extraction.csv') as file:
    content = csv.DictReader(file, delimiter="\t")
    count = 0
    result = {}
    for entry in content:
        count += 1
        entry_id = entry['wikibase_lexeme'].replace("https://monumenta.wikibase.cloud/entity/","")

        senses = []
        entrycontent = re.sub(r'^[^\:]+: ?',"",entry['sarrera_testu']) # cut off headword block until colon
        print(f"{count} {entrycontent}")
        sense_blocks = entrycontent.split(";")
        for sense_block in sense_blocks:
            sense_block = re.sub(r"\.$", "", sense_block.strip())
            ohar = None
            restrict = None
            equiv_blocks = sense_block.split(",")
            equivs = []
            for equiv_block in equiv_blocks:
                ohar_re = re.search(r" ?[\(\[]([^\)\]][^\)\]]+)[\]\)] ?", equiv_block)
                if ohar_re:
                    ohar = ohar_re.group(1)
                    equiv_block = equiv_block.replace(ohar_re.group(0), "")
                    print(f"Oharra: {ohar} FOR {equiv_block}")
                restrict_re = re.search(r"^ ?([a-z]+): ?", equiv_block)
                if restrict_re:
                    restrict = restrict_re.group(1)
                    equiv_block = equiv_block.replace(restrict_re.group(0), "")
                    print(f"Restriction: {restrict} FOR {equiv_block}")
                equivs.append({'P199': ohar, 'P200': restrict, 'equiv': equiv_block.strip()})
            senses.append({'glosstext': sense_block, 'equivs': equivs})
        result[entry_id] = {"id": entry['source_id'], "senses": senses}
with open('data/senses_dict_v2.json', 'w') as file:
    json.dump(result, file, indent=2)



# #nouns
# result['noun'] = {}
# found_count = 0
# not_found_count = 0
# for id in content['noun']:
#     entry = ElementTree.fromstring(content['noun'][id]['full_entry'])
#     gender = content['noun'][id]['gender']
#     senses = []
#     for basque in entry.findall('basque'):
#         straightforward_re = re.search(fr'{gender}\.: (.*)\.', basque.text)
#         if straightforward_re:
#             found_count += 1
#             sense_blocks = straightforward_re.group(1).split(";")
#             for sense_block in sense_blocks:
#                 block_senses = sense_block.split(",")
#                 stripped_senses = []
#                 for sense in block_senses:
#                     stripped_senses.append(sense.strip())
#                 senses.append(stripped_senses)
#
#     if len(senses) == 0:
#         not_found_count += 1
#         senses = None
#     else:
#         result['noun'][id] = content['noun'][id]
#         result['noun'][id]['senses'] = senses
#
# with open('data/content_pos_translations.json', 'w') as file:
#     json.dump(result, file, indent=2)
#
#
#
#
#
# print(f"Found {found_count} noun translation blocks, did not find {not_found_count} translation blocks")