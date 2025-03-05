from xml.etree import ElementTree
from xml.dom import minidom
import json, csv

with open('mapping.csv') as file:
    mappingfile = csv.reader(file, delimiter="\t")
    mapping = {}
    for row in mappingfile:
        mapping[row[0]] = row[1]




tree = ElementTree.parse('content.xml')
newroot = ElementTree.Element('root')
element_types = {}
mapped_types = {}

for entry in tree.findall("entry"):
    # entry_type = entry.attrib['type']
    # if entry_type not in entrytypes:
    #     entrytypes[entry_type] = 1
    # else:
    #     entrytypes[entry_type] += 1
    newentry = ElementTree.Element('entry')
    actual_lang = None
    for element in entry.findall("element"):
        element_type = element.attrib['type']
        if element_type in mapping:
            element_name = mapping[element_type]
        else:
            element_name = "basque"
        if element_name == "lemma":
            new_element = ElementTree.Element(element_name)
            actual_lang = "latin"
        else:
            if element_name != actual_lang:
                newentry.append(new_element)
                new_element = ElementTree.Element(element_name)
                actual_lang = element_name

        if 'type' not in new_element.attrib:
            new_element.set('type', element_type)
        else:
            new_element.set('type', new_element.attrib['type'] + " " + element_type)
        if new_element.text:
            new_element.text = new_element.text + element.text
        else:
            new_element.text = element.text
    newentry.append(new_element)
    newroot.append(newentry)

reparsed = minidom.parseString(ElementTree.tostring(newroot, 'utf-8')).toprettyxml(indent="\t")
print(str(reparsed))
outfile = 'content_structured.xml'
with open(outfile, "w", encoding="utf-8") as file:
    file.write(reparsed)
print('Wrote to ' + outfile)








        # elif element_type not in element_types:
        #     element_types[element_type] = [element.text]
        # else:
        #     element_types[element_type].append(element.text)


# with open('element_types.json', 'w') as file:
#     json.dump(element_types, file, indent=2)