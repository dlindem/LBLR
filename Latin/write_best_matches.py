import csv, xwbi, time

with open('lila_best_matches_wikidata.csv') as file:
    content = csv.DictReader(file, delimiter="\t")
    count = 0
    for row in content:
        count += 1
        if count < 2440:
            continue
        lexeme = xwbi.wbi.lexeme.get(entity_id=row['wikibase_lexeme'])
        claim = xwbi.ExternalID(prop_nr="P1", value=row['wikidata_lexeme'],
                                qualifiers=[xwbi.String(prop_nr="P66", value="batch #1 best matches")])
        lexeme.claims.add(claim)
        lexeme.write()
        print(f"[{count}] Successfully written to http://monumenta.wikibase.cloud/entity/{lexeme.id}")
        time.sleep(0.5)
