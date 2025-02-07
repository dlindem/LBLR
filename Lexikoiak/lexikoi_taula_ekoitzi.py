import json

json_lexicon = "data/etxepare_lexicon.json"

with open(json_lexicon) as file:
    lexicon = json.load(file)
    lang = "eu"
    taula = "testu_hitza\tlemma\thitz_egokitua\tmlv_lexeme\taingura\ttestuingurua\n"
    for word in lexicon[lang]:
        for entry in lexicon[lang][word]:
            print(entry)
            taula += f"{word}\t{entry['lemma']['lemma']}\t{entry['lemma']['hitz_egok']}\t{entry['lemma']['lexeme']}\t{entry['aingura']}\t{entry['context']}\n"

    with open(json_lexicon.replace(".json", ".csv"), 'w') as file:
        file.write(taula)