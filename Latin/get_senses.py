from xml.etree import ElementTree
from xml.dom import minidom
import json, csv, time, re

with open('ELH_wikibase_entries.csv') as file:
    elh_entries = {}
    rows = csv.DictReader(file, delimiter=",")
    for row in rows:
        elh_entries[row['source_id']] = row['wikibase_lexeme']

tree = ElementTree.parse('content_structured_equivs.xml')
newroot = ElementTree.Element('root')
element_types = {}
mapped_types = {}
sense_dict = {}
for entry in tree.findall("entry"):
    entry_id = entry.attrib['entry_id']
    if entry_id not in elh_entries:
        print(f"Entry {entry_id} not in Wikibase")
        continue
    entry_qid = elh_entries[entry_id]
    senses = []

    for element in entry.findall("basque"):
        if element.attrib['type'] == "equivs" and element.text:
            # print(element.text)

            raw_senses = element.text.split(";")
            for sense in raw_senses:
                glosstext = re.sub(r"\.$", "", sense).strip()
                equivs = []
                raw_equivs = sense.split(",")
                for equiv in raw_equivs:
                    ohar = None
                    restrict = None
                    clean_equiv = equiv.replace(".","").strip()
                    clean_equiv = re.sub(r" \($", "", clean_equiv)
                    clean_equiv = re.sub(r" \[[^\]]+$", "", clean_equiv)
                    clean_equiv = re.sub(r" ?— ?", "", clean_equiv)
                    clean_equiv = re.sub(r"@", ",", clean_equiv)
                    ohar_re = re.search(r" [\(\[]([^\)\]]+)[\]\)] ?", clean_equiv)
                    if ohar_re:
                        ohar = ohar_re.group(1)
                        clean_equiv = clean_equiv.replace(ohar_re.group(0), "")
                        print(f"{entry_id} Oharra: {ohar} FOR {clean_equiv}")
                    restrict_re = re.search(r"^ ?([a-z]+): ?", clean_equiv)
                    if restrict_re:
                        restrict = restrict_re.group(1)
                        clean_equiv = clean_equiv.replace(restrict_re.group(0), "")
                        print(f"{entry_id} restriction: {restrict} FOR {clean_equiv}")
                    if not clean_equiv.startswith("[") and len(clean_equiv) > 1:
                        equivs.append({'ohar':ohar, 'restrict':restrict, 'equiv': clean_equiv.strip()})
                if len(equivs) > 0:
                    senses.append({'glosstext': glosstext, 'equivs': equivs})
    if len(senses) > 0:
        sense_dict[entry_id] = {'qid': entry_qid, 'senses': senses}
with open('senses_dict.json', 'w') as file:
    json.dump(sense_dict, file, indent=2)






# with open('pretty_entries.csv', "w", encoding="utf-8") as file:
#     file.write(csvtext)
# print('Finished.')








        # elif element_type not in element_types:
        #     element_types[element_type] = [element.text]
        # else:
        #     element_types[element_type].append(element.text)


# with open('element_types.json', 'w') as file:
#     json.dump(element_types, file, indent=2)