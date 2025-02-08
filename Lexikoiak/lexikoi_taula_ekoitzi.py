import json

# converts a json lexicon produced by 'lexicon-build.py' to a csv table

json_lexicon = "data/etxepare_sorted_lexicon.json"

with open(json_lexicon) as file:
    lexicon = json.load(file)
    lang = "eu"
    taula = "testu_hitza\thitz_egokitua\tlemma\tmlv_lexeme\taingura\ttoken_zbk\ttestuingurua-ezker\ttestu-hitza\teskuin-testuingurua\n"
    for word in lexicon[lang]:
        for entry in lexicon[lang][word]:
            print(entry)
            taula += f"{word}\t{entry['lemma']['hitz_egok']}\t{entry['lemma']['lemma']}\t{entry['lemma']['lexeme']}\t{entry['aingura']}\t{entry['doc_token_count']}\t{entry['context']}\n"

    with open(json_lexicon.replace(".json", ".csv"), 'w') as file:
        file.write(taula)