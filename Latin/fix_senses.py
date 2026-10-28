import json, re, time, requests
import xwb

with open('data/entries_with_sense.json', 'r') as f:
    entries = json.load(f)

count = 0
for entry in entries:
    count +=1
    lexeme_id = entry['wikibase_lexeme'].replace('https://monumenta.wikibase.cloud/entity/', '')
    # r = requests.get(f"https://monumenta.wikibase.cloud/wiki/Special:EntityData/{lexeme_id}.json",
    #                  headers={"User-Agent": "User:DavidL python requests"})
    # lexeme = r.json()['entities'][lexeme_id]
    existing_senses = list(range(int(entry['senses'])+1))[1:]
    all_senses = list(range(len(entry['proposed_senses'])+1))[1:]
    print(f"\n{count}: existing {existing_senses} -> {all_senses} - {entry['wikibase_lexeme']}")
    for sense_num in all_senses:
        sense_id = f"{lexeme_id}-S{sense_num}"
        gloss_text = entry['proposed_senses'][sense_num-1]
        gloss_dict = {"glosses": {"eu": {"language": "eu", "value": gloss_text.strip()}}}
        if sense_num in existing_senses:
            xwb.editsense(sense_id, gloss_dict)
            time.sleep(.51)
        else:
            xwb.addsense(lexeme_id, gloss_dict)
            time.sleep(.51)

        grammar_note = None
        text_to_split = gloss_text
        while re.search(r'[\[\(][^\)\]]+, ?[^\)\]]+[\)\]]', text_to_split):
            text_to_split = re.sub(r'([\[\(][^\)\]]+), ?([^\)\]]+[\)\]])', r'\1 @ \2', text_to_split)
        equiv_blocks = text_to_split.split(",")
        equivs = []
        for equiv_block in equiv_blocks:
            equiv_note = None

            equiv_block = equiv_block.replace(" @ ", ", ")
            equiv_note_re = re.search(r" ?[\(\[]([^\)\]][^\)\]]+)[\]\)] ?", equiv_block)
            if equiv_note_re:
                equiv_note = equiv_note_re.group(1).strip()
                equiv_block = equiv_block.replace(equiv_note_re.group(0), "").strip()
                print(f"Oharra: {equiv_note} FOR {equiv_block}")
            grammar_note_re = re.search(r"^ ?([a-z]+)\.?: ?", equiv_block)
            if grammar_note_re:
                grammar_note = grammar_note_re.group(1).strip()
                equiv_block = equiv_block.replace(grammar_note_re.group(0), "").strip()
                print(f"grammar_noteion: {grammar_note} FOR {equiv_block}")
            equivs.append({'P199': equiv_note, 'P200': grammar_note, 'equiv': equiv_block.strip()})

        for equiv in equivs:
            claimset = xwb.updateclaim(sense_id, "P201", {"text": equiv['equiv'], "language": "eu"}, "monolingualtext")
            if claimset:
                claimid = claimset
            time.sleep(.34)
            if equiv['P199']:
                # xwb.setqualifier(lexeme_id, "P201", claimid, "P199", equiv['P199'], "string")
                claimset = xwb.updateclaim(sense_id, "P199", equiv['P199'], "string")
                time.sleep(.34)
            if equiv['P200']:
                # xwb.setqualifier(lexeme_id, "P201", claimid, "P200", equiv['P200'], "string")
                claimset = xwb.updateclaim(sense_id, "P200", equiv['P200'], "string")
                time.sleep(.34)





