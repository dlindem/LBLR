import re, xwbi, time, requests

with open('data/statements_to_deprecate.txt') as f:
    statements = f.readlines()
    for guid in statements:
        guidfix = re.compile(r'^([LQ]\d+\-?S?\d*)\-')
        guid = re.sub(guidfix, r'\1$', guid).strip()
        lexeme_id = re.search(r'L\d+', guid).group(0)
        r = requests.get(f"https://monumenta.wikibase.cloud/wiki/Special:EntityData/{lexeme_id}.json", headers={"User-Agent":"User:DL2204 python requests"})
        lexeme = r.json()['entities'][lexeme_id]
        claims_json = lexeme['claims']
        for prop in claims_json:
            claimscount = 0
            for claim in claims_json[prop]:
                if claim['id'] == guid:
                    print(f"Found matching claim: {prop} - #{claimscount}: {claim}")
                    claims_json[prop][claimscount]['rank'] = 'deprecated'
                    break
                claimscount += 1
        lexeme['claims'] = claims_json
        wb_lexeme = xwbi.wbi.lexeme.from_json(json_data=lexeme)
        wb_lexeme.write()
        print(f"Successfully written to http://monumenta.wikibase.cloud/entity/{wb_lexeme.id}")
        time.sleep(.51)


