import csv, xwbi, time, requests, re

upos_mapping = {
    "NOUN": "Q65",
    "ADJ": "Q55",
    "VERB": "Q52",
    "ADV": "Q59",
    "PROPN": "Q66",
    "INTJ": "Q56",
    "ADP": "Q67",
    "NUM": "Q60",
    "PRON": "Q64",
    "CCONJ": "Q57",
    "PART": "Q68",
    "DET": "Q69"
}
# PREFIX mwb: <https://monumenta.wikibase.cloud/entity/>
# PREFIX mdp: <https://monumenta.wikibase.cloud/prop/direct/>
# PREFIX mp: <https://monumenta.wikibase.cloud/prop/>
# PREFIX mps: <https://monumenta.wikibase.cloud/prop/statement/>
# PREFIX mpq: <https://monumenta.wikibase.cloud/prop/qualifier/>
# PREFIX mpr: <https://monumenta.wikibase.cloud/prop/reference/>
# PREFIX mno: <https://monumenta.wikibase.cloud/prop/novalue/>
#
# SELECT ?source_id (strafter(str(?entry),str(mwb:)) as ?wikibase) WHERE {
# ?entry mp:P6 [mps:P6 mwb:Q1284; mpq:P186 ?source_id].
#
# }

r = requests.get("https://monumenta.wikibase.cloud/query/sparql?format=json&query=PREFIX%20mwb%3A%20%3Chttps%3A%2F%2Fmonumenta.wikibase.cloud%2Fentity%2F%3E%0APREFIX%20mdp%3A%20%3Chttps%3A%2F%2Fmonumenta.wikibase.cloud%2Fprop%2Fdirect%2F%3E%0APREFIX%20mp%3A%20%3Chttps%3A%2F%2Fmonumenta.wikibase.cloud%2Fprop%2F%3E%0APREFIX%20mps%3A%20%3Chttps%3A%2F%2Fmonumenta.wikibase.cloud%2Fprop%2Fstatement%2F%3E%0APREFIX%20mpq%3A%20%3Chttps%3A%2F%2Fmonumenta.wikibase.cloud%2Fprop%2Fqualifier%2F%3E%0APREFIX%20mpr%3A%20%3Chttps%3A%2F%2Fmonumenta.wikibase.cloud%2Fprop%2Freference%2F%3E%0APREFIX%20mno%3A%20%3Chttps%3A%2F%2Fmonumenta.wikibase.cloud%2Fprop%2Fnovalue%2F%3E%0A%0ASELECT%20%3Fsource_id%20(strafter(str(%3Fentry)%2Cstr(mwb%3A))%20as%20%3Fwikibase)%20WHERE%20%7B%0A%3Fentry%20mp%3AP6%20%5Bmps%3AP6%20mwb%3AQ1284%3B%20mpq%3AP186%20%3Fsource_id%5D.%0A%0A%7D%20")
results = r.json()['results']['bindings']
mapping = {}
for result in results:
    mapping[result['source_id']['value']] = result['wikibase']['value']
input(f"Got {len(mapping)} existing entry mappings. ENTER to proceed.")

with open('lila_matches.csv') as file:
    lilacsv = csv.DictReader(file, delimiter="\t")

    for row in lilacsv:
        entry_id = row['id']
        if int(entry_id) < 16507:
            continue
        lemma = row['wr']
        print(f"[{entry_id}] Now processing ID {entry_id}, '{lemma}' ...")

        lilarefs = row['lilaRef'].split(",")
        if entry_id in mapping:
            lexeme = xwbi.wbi.lexeme.get(entity_id=mapping[entry_id])
            print(f"Got existing lexeme {mapping[entry_id]}")
        else:
            lexeme = xwbi.wbi.lexeme.new(language="Q225", lexical_category="Q70")
            print(f"Will create new lexeme for this ID.")
        lexeme.lemmas.set(language="la", value=lemma)

        id_quali = xwbi.String(prop_nr="P186", value=entry_id)

        headword = re.sub(r'[^\w]*$', '', row['lemmaRaw'])
        print(f"Will write source headword '{headword}'")
        headword_quali = xwbi.MonolingualText(prop_nr= "P187", language="la", text=headword)

        claim = xwbi.Item(prop_nr="P6", value="Q1284", qualifiers=[id_quali, headword_quali])
        lexeme.claims.add(claim)



        for lilaref in lilarefs:
            if lilaref.startswith("lemma") or lilaref.startswith("hypolemma"):
                claim = xwbi.ExternalID(prop_nr="P185", value=lilaref)
                lexeme.claims.add(claim,action_if_exists=xwbi.ActionIfExists.APPEND_OR_REPLACE)
        lexeme.write()
        print(f"Successfully created https://monumenta.wikibase.cloud/entity/{lexeme.id}")
        time.sleep(0.5)





