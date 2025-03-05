from xml.etree import ElementTree
import json, csv, re

tree = ElementTree.parse('content_structured.xml')
result = {'noun': {}, 'verb': {}, 'prep': {}, 'xref': {}, 'adj':{}}
resultcount = {'found_pos':{'noun': 0, 'verb': 0, 'prep': 0, 'xref': 0, 'adj':0}, 'not_found':0}
for entry in tree.findall('entry'):
    entry_id = entry.attrib['entry_id']
    for lemma in entry.findall('lemma'):
        lemma = re.sub(r'[^\w]+$', '', lemma.text)
    for xref in entry.findall('xref_lemma'):
        pos = {'lemma': lemma, 'pos': 'xref', 'xref_lemma': xref.text}
        break
    for basque in entry.findall('basque'):
        pos = None
        noun_re = re.search(r'^([mfn])\.:', basque.text.strip())
        if noun_re:
            pos = {'lemma': lemma, 'pos': 'noun', 'gender': noun_re.group(1)}
            break
        verb_re = re.search(r'^(\d):', basque.text.strip())
        if verb_re:
            pos = {'lemma': lemma, 'pos': 'verb', 'conj': str(verb_re.group(1))}
            break
        prep_re = re.search(r'^prep\. *(\w+)\.:', basque.text.strip())
        if prep_re:
            pos = {'lemma': lemma, 'pos': 'prep', 'casus': prep_re.group(1)}
            break
        adj_re1 = re.search('-a, -um', lemma)
        if adj_re1:
            pos = {'lemma': lemma, 'pos': 'adj', 'dek': adj_re1.group(0)}
            break
        adj_re2 = re.search('is, -e', lemma)
        if adj_re2:
            pos = {'lemma': lemma, 'pos': 'adj', 'dek': adj_re2.group(0)}
            break
    if pos:
        result[pos['pos']][entry_id] = pos
        resultcount['found_pos'][pos['pos']] += 1
    else:
        resultcount['not_found'] += 1



with open('content_pos.json', 'w') as file:
    json.dump(result, file, indent=2)

print(resultcount)