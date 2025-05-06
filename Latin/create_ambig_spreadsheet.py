import re, csv, time
from xml.etree import ElementTree

tree = ElementTree.parse('content_structured.xml')
dict_text = {}
for entry in tree.findall('entry'):
    entry_id = entry.attrib['entry_id']
    entry_text_bits = []
    for element in entry:
        if element.tag == "lemma":
            lemma = re.sub(r'[^\w]+$', '', element.text.lstrip())
        else:
            entry_text_bits.append(element.text)
    entry_text = lemma + " " + " ".join(entry_text_bits).replace("  ", " ")
    dict_text[entry_id] = entry_text
# print(dict_text)

spreadsheet_json = {}
spreadsheet = "source_id\tsarrera_buru\twikibase_lexeme\tlila_form\tlila_uri\tlila_lemma\tlila_pos\tlila_gender\tlila_inflectionType\tsense_translations\tsarrera_osoa\n"
seen_once = []
seen_twice = []
lexeme_count = {}
with open('lila_ambig_matches.csv') as file:
    lila_content = csv.reader(file, delimiter=",")

    for row in lila_content:
        source_id = row[0]
        lila_id = row[4]

        if not re.search(r'^[0-9]+$', source_id):
            continue

        wb_lexeme = row[2]
        spreadsheet_json[lila_id] = {'lexeme': wb_lexeme, 'line': "\t".join(row) + "\t" + dict_text[source_id]}

        if wb_lexeme not in lexeme_count:
            lexeme_count[wb_lexeme] = 1
        else:
            lexeme_count[wb_lexeme] += 1




    for lila_id in spreadsheet_json:
        print(spreadsheet_json[lila_id])
        if lexeme_count[spreadsheet_json[lila_id]['lexeme']] > 1:
            spreadsheet += spreadsheet_json[lila_id]['line']+"\n"


with open('lila_ambig_spreadsheet.csv', 'w') as file:
    file.write(spreadsheet)






