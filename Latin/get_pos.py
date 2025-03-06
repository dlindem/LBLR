from xml.etree import ElementTree
import json, csv, re

tree = ElementTree.parse('content_structured.xml')
result = {'no_pos':{}, 'noun': {}, 'verb': {}, 'prep': {}, 'xref': {}, 'adj':{}, 'adb':{}, 'conj':{}}
resultcount = {'found_pos':{'noun': 0, 'verb': 0, 'prep': 0, 'xref': 0, 'adj':0, 'adb':0, 'conj':0}, 'not_found':0}
for entry in tree.findall('entry'):
    entry_id = entry.attrib['entry_id']
    for lemma in entry.findall('lemma'):
        lemma = re.sub(r'[^\w]+$', '', lemma.text.lstrip())
    altlem = None
    pos = None
    for altlemma in entry.findall('altlemma'):
        altlem = re.sub(r'[^\w]+$', '', altlemma.text)
    for xref in entry.findall('xref_lemma'):
        pos = {'pos': 'xref', 'xref_lemma': xref.text.strip()}
        break
    for basque in entry.findall('basque'):

        #nouns
        noun_re = re.search(r'^[\], ]*([mfn])\.:', basque.text.strip())
        if noun_re:
            pos = {'pos': 'noun', 'gender': noun_re.group(1)}
            break

        #verbs
        verb_re = re.search(r'^[\], ]*(\d):', basque.text.strip())
        if verb_re:
            pos = {'pos': 'verb', 'conj': str(verb_re.group(1))}
            break
        prep_re1 = re.search(r'^[\], ]*prep\.[: ]*(\w+)\.:', basque.text.strip())
        prep_re2 = re.search(r'^[\], ]*prep\.', basque.text.strip())
        if prep_re1:
            pos = {'pos': 'prep', 'casus': prep_re1.group(1)}
            break
        elif prep_re2:
            pos = {'pos': 'prep', 'casus': None}
            break

        # adverbs
        adb_re = re.search(r'^[\], ]*adb\.', basque.text.strip())
        if adb_re:
            pos = {'pos': 'adb'}
            break

        # conjugations
        conj_re = re.search(r'^[\], ]*konj\.', basque.text.strip())
        if conj_re:
            pos = {'pos': 'conj'}
            break

        # adjectives
        adj_re1 = re.search('-a, -um', lemma)
        adj_re2 = re.search('is, -e', lemma)
        if adj_re1:
            pos = {'pos': 'adj', 'dek': adj_re1.group(0)}
            break
        elif adj_re2:
            pos = {'pos': 'adj', 'dek': adj_re2.group(0)}
            break
        else:
            for latin in entry.findall('latin'):
                adj_re1 = re.search('-a, -um', latin.text)
                adj_re2 = re.search('is, -e', latin.text)
                if adj_re1:
                    pos = {'pos': 'adj', 'dek': adj_re1.group(0)}
                    break
                elif adj_re2:
                    pos = {'pos': 'adj', 'dek': adj_re2.group(0)}
                    break

    if pos:
        pos['lemma'] = lemma
        pos['altlemma'] = altlem
        pos['full_entry'] = ElementTree.tostring(entry, encoding="utf8").decode("utf-8")
        result[pos['pos']][entry_id] = pos
        resultcount['found_pos'][pos['pos']] += 1
    else:
        resultcount['not_found'] += 1
        result['no_pos'][entry_id] = ElementTree.tostring(entry, encoding="utf8").decode("utf-8")



with open('content_pos.json', 'w') as file:
    json.dump(result, file, indent=2)

print(resultcount)