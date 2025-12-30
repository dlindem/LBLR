from xml.etree import ElementTree
from xml.dom import minidom
import json, csv

with open('ELH_wikibase_entries.csv') as file:
    elh_entries = {}
    rows = csv.DictReader(file, delimiter=",")
    for row in rows:
        elh_entries[row['source_id']] = row['wikibase_lexeme']

tree = ElementTree.parse('content_structured.xml')
newroot = ElementTree.Element('root')
element_types = {}
mapped_types = {}
csvtext = ""
for entry in tree.findall("entry"):
    entry_id = entry.attrib['entry_id']
    if entry_id not in elh_entries:
        print(f"Entry {entry_id} not in Wikibase")
        continue
    entry_qid = elh_entries[entry_id]
    prettytext = ""
    for element in entry:
        prettytext += element.text.replace("\n","")
    csvtext += f"{entry_id}\t{entry_qid}\t{prettytext}\n"




with open('pretty_entries.csv', "w", encoding="utf-8") as file:
    file.write(csvtext)
print('Finished.')








        # elif element_type not in element_types:
        #     element_types[element_type] = [element.text]
        # else:
        #     element_types[element_type].append(element.text)


# with open('element_types.json', 'w') as file:
#     json.dump(element_types, file, indent=2)