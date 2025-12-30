import csv, time, re, sys
import config_private
from wikibaseintegrator import WikibaseIntegrator, wbi_login, datatypes
from wikibaseintegrator.wbi_config import config
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.models import Qualifiers, References, Reference
config['MEDIAWIKI_API_URL'] = "https://monumenta.wikibase.cloud/w/api.php"
config['USER_AGENT'] = "User DavidL wrtie_lilalem_metadata.pz"
print("Getting logged into monumenta wikibase...")
monumenta = WikibaseIntegrator(login=wbi_login.Login(user=config_private.wb_bot_user, password=config_private.wb_bot_pwd))
print("Login successful.")

with open('cleared_entities.txt', 'r') as logfile:
    cleared_entities = logfile.read().split("\n")

with open('lila_uri_wikibase.csv') as file:
    lila_uris = {}
    rows = csv.DictReader(file, delimiter=",")
    for row in rows:
        lila_uris[row['lila_uri']] = row['qid']

with open('lila_matches_liladata.csv') as file:
    content = csv.DictReader(file, delimiter=",")
    count = 0

    for row in content:
        count += 1
        lexeme_id = re.search(r'statement/(L\d+)', row['lila_id_st']).group(1)
        statement_id = re.sub('https://monumenta.wikibase.cloud/entity/statement/(L\d+)\-(.*)', r"\1$\2", row['lila_id_st'])
        lila_lemma_uri = row['lila_uri'].replace("http://lila-erc.eu/data/id/", "")
        print(f"\n[{count}] Now processing lexeme {lexeme_id} {lila_lemma_uri} {row['lila_lemma']}: {row['sense_translations']}")
        lexeme_entity = monumenta.lexeme.get(entity_id=lexeme_id)
        # lexeme_json = lexeme_entity.get_json()
        # for claim in lexeme_json['claims']['P185']:
        #     if claim['id'] == statement_id:
        #         print(f"Found match: {claim}")
        #         sys.exit()

        references = References()
        reference1 = Reference()
        reference1.add(datatypes.ExternalID(prop_nr='P196', value='2cc6muar'))
        reference1.add(datatypes.Time(prop_nr="P188", time="now"))
        references.add(reference1)

        qualifiers = Qualifiers()
        qualifiers.add(datatypes.MonolingualText(prop_nr="P187", language="la", text=row['lila_lemma']))
        if row['lila_POS'] != "":
            for pos_uri in row['lila_POS'].split("|"):
                qualifiers.add(datatypes.Item(prop_nr="P153", value=lila_uris[pos_uri]))
        if row['lila_GENDER'] != "":
            for gender_uri in row['lila_GENDER'].split("|"):
                qualifiers.add(datatypes.Item(prop_nr="P194", value=lila_uris[gender_uri]))
        if row['lila_inflectionType'] != "":
                qualifiers.add(datatypes.Item(prop_nr="P195", value=lila_uris[row['lila_inflectionType']]))
        if row['sense_translations'] != "":
                qualifiers.add(datatypes.String(prop_nr="P197", value=row['sense_translations'][:999].strip()))
        if lexeme_id not in cleared_entities:
            action = ActionIfExists.REPLACE_ALL
            cleared_entities.append(lexeme_id)
            with open('cleared_entities.txt', 'a') as logfile:
                logfile.write(lexeme_id+"\n")
        else:
            action = ActionIfExists.FORCE_APPEND
        lexeme_entity.claims.add(datatypes.ExternalID(prop_nr="P185", value=lila_lemma_uri, qualifiers=qualifiers, references=references), action_if_exists=action)

        lexeme_entity.write()
        print(f"[{count}] Successfully written to http://monumenta.wikibase.cloud/entity/{lexeme_entity.id}")
        time.sleep(0.5)
