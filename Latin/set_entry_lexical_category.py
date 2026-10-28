import xwbi, time, csv

with open("data/entries_for_pos.csv", "r") as f:
    rows = csv.DictReader(f, delimiter="\t")
    count = 0
    for row in rows:
        entry = row["wikibase_lexeme"]
        pos = row["leh_pos"]
        count += 1
        lexeme = xwbi.wbi.lexeme.get(entity_id=entry)
        lexeme.lexical_category = pos
        lexeme.write()
        print(f"{count}: https://monumenta.wikibase.cloud/entity/{entry}: success.")
        time.sleep(.51)
