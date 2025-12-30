import csv, time, re, sys
import config_private
import mwclient # mediawiki api client (will be used for itemdata > 1MB
monumenta_api = mwclient.Site('monumenta.wikibase.cloud')
login = monumenta_api.login(username=config_private.wb_bot_user, password=config_private.wb_bot_pwd)
csrfquery = monumenta_api.api('query', meta='tokens')
monumenta_api_token = csrfquery['query']['tokens']['csrftoken']
print("Got fresh CSRF token for monumenta.wikibase.cloud.")

with open('ELH_wikibase_entries.csv') as file:
    elh_entries = {}
    rows = csv.DictReader(file, delimiter=",")
    for row in rows:
        elh_entries[row['source_id']] = row['p6st']

with open('pretty_entries.csv') as file:
    content = csv.DictReader(file, delimiter="\t")
    count = 0
    for row in content:
        count += 1
        # if count < 7900:
        #     continue
        print(f"\n[{count}] Now processing row {row}")
        # lexeme = monumenta.lexeme.get(entity_id=row['qid'])
        # claim = datatypes.String(prop_nr="P198", value=row['text'][:999].strip())
        # lexeme.claims.add(claim)
        # lexeme.write()
        claim_id = elh_entries[row['id']]
        guidfix_re = re.search(r'^([QLP]\d+)\-(.*)', claim_id)
        if guidfix_re:
            claim_id = guidfix_re.group(1) + '$' + guidfix_re.group(2)
        try:
            claimcreation = monumenta_api.post('wbsetqualifier', token=monumenta_api_token, claim=claim_id, property="P198", snaktype="value", value=f'"{row['text'][:999].strip()}"', bot=1)
            if claimcreation['success'] == 1:
                print(f"[{count}] Successfully written to http://monumenta.wikibase.cloud/entity/{row['qid']}")
                time.sleep(.3)
            else:
                print(f"Failed to write claim to http://monumenta.wikibase.cloud/entity/{row['qid']}")
                sys.exit()
        except Exception as ex:
            if "The statement has already a qualifier" in str(ex):
                print(f"[{count}] Skipped (processed before)")
                continue

        time.sleep(0.34)
