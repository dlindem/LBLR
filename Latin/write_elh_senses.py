import csv, time, re, sys, json

import config_private
from wikibaseintegrator import WikibaseIntegrator, wbi_login, datatypes
from wikibaseintegrator.wbi_config import config
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.models import Qualifiers, References, Reference, Sense

config['MEDIAWIKI_API_URL'] = "https://monumenta.wikibase.cloud/w/api.php"
config['USER_AGENT'] = "User DavidL wrtie_lilalem_metadata.pz"
print("Getting logged into monumenta wikibase...")
monumenta = WikibaseIntegrator(login=wbi_login.Login(user=config_private.wb_bot_user, password=config_private.wb_bot_pwd))
print("Login successful.")

with open('sense_entities.txt', 'r') as logfile:
    done_entities = logfile.read().split("\n")

with open('senses_dict.json') as file:
    senses_dict = json.load(file)
    count = 0
    for entry in senses_dict:
        count += 1
        lexeme_lid = senses_dict[entry]['qid']
        if lexeme_lid in done_entities:
            continue
        print(f"\n[{count}] Now processing entry {entry} {lexeme_lid}: {senses_dict[entry]}")
        lexeme_entity = monumenta.lexeme.get(entity_id=lexeme_lid)
        for sense in senses_dict[entry]['senses']:
            new_sense = Sense()
            new_sense.glosses.set(language="eu", value=sense['glosstext'])
            for equiv in sense['equivs']:
                qualifiers = Qualifiers()
                if equiv['ohar']:
                    qualifiers.add(datatypes.String(prop_nr="P199", value=equiv['ohar']))
                if equiv['restrict']:
                    qualifiers.add(datatypes.String(prop_nr="P200", value=equiv['restrict']))
                references = References()
                reference1 = Reference()
                reference1.add(datatypes.String(prop_nr='P186', value=entry))
                references.add(reference1)
                claim = datatypes.MonolingualText(prop_nr="P201", language="eu", text=equiv['equiv'], qualifiers=qualifiers, references=references)
                new_sense.claims.add(claim, action_if_exists=ActionIfExists.APPEND_OR_REPLACE)
            lexeme_entity.senses.add(new_sense)
        lexeme_entity.write()
        with open('sense_entities.txt', 'a') as logfile:
            logfile.write(lexeme_entity.id + "\n")
        print(f"[{count}] Successfully written to http://monumenta.wikibase.cloud/entity/{lexeme_entity.id}")
        time.sleep(0.5)

