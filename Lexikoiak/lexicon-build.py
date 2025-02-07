import re, json, csv
from unidecode import unidecode
from nltk.tokenize import word_tokenize

with open('data/mlv_lexemes.csv') as csvfile:
    csvrows = csv.DictReader(csvfile, delimiter=",")
    mlv_lexicon = {}
    for row in csvrows:
        mlv_lexicon[(row['lemma'])] = row['lexeme']

with open('data/grafia_arauak/Manuel Larramendi.csv', encoding="utf-8") as csvfile:
    mapping = csv.reader(csvfile, delimiter=",") # reads replace rules

    mapdict = {}
    for row in mapping:
        mapdict[row[0]]=row[1]

def search_oeh(word):
    global mlv_lexicon
    global mapdict
    lexns = "https://monumenta.wikibase.cloud/wiki/Lexeme:"
    oldnorlem = unidecode(word.replace('ñ', '_')).replace('_', 'ñ').rstrip()
    newlem = oldnorlem
    for rule in mapdict:
        interlem = re.sub(rule, mapdict[rule], newlem)
        if len(interlem) > 0:
            newlem = interlem
    print(f"egokituzapena: {word} >> {newlem}")

    candidates = []
    for lemma in mlv_lexicon:
        if lemma == newlem: # exact match
            return {'lemma': newlem, 'hitz_egok': newlem, 'lexeme': lexns+mlv_lexicon[newlem]}
        searchlem = re.sub(r'a$', '', lemma) # cut off final -a ("hikuntza" > "hizkuntz")
        if re.search(fr'^{searchlem}', newlem) or re.search(fr'^{searchlem}', f'h{newlem}'): # if word begins with lemma candidate (maybe with 'h')
            candidates.append(lemma) # candidate matches word begin (evtl. 'h')
    print(f"Lemma candidates for {newlem}: {candidates}")
    if len(candidates) == 0:
        return {'lemma': "", 'hitz_egok': newlem, 'lexeme': ""}
    longestlen = len(max(candidates, key=len))  # length of longest match
    longest = []
    for candidate in candidates:
        if len(candidate) == longestlen:
            longest.append(candidate)
    if len(longest) > 1:
        for item in longest:
            if re.search(r'[^a]$', item):
                return {'lemma': item, 'hitz_egok': newlem, 'lexeme': lexns + mlv_lexicon[item]}
    return {'lemma': longest[0], 'hitz_egok': newlem, 'lexeme': lexns + mlv_lexicon[longest[0]]}

def lexicon_build(textname=None, doclink=None):
    with open(f'data/{textname}.wikitext') as file:
        wikitext = file.read()
        wikitext = wikitext.replace("\n","")

    spans = wikitext.split('<span lang="')
    print("Wikitestua kargatuta. Goiburua hau da:\n"+spans.pop(0))
    lexicon = {"eu": {}, "es": {}, "la": {}}
    actual_aingura = ""
    for span in spans:
        lang = span[0:2].lower()
        print(f"Atal honen hizkuntza: {lang}")

        span_content = re.search(rf'{lang}">(.*)</span>', re.sub(r'</ ?br>', ' ', span)).group(1)
        print(span_content)
        # find aingurak
        aingurak_re = re.compile(r'\{\{aingura\|([^\}]+)\}\}')
        aingurak = aingurak_re.findall(span_content)
        print(aingurak)
        if len(aingurak) == 0: # hartu aurreko aingura
            span_content = "{{aingura|" + actual_aingura + "}}" + span_content
        for paragraph in span_content.split('{{aingura|'):
            if len(paragraph.strip()) == 0:
                continue # aingura is right at the begin
            try:
                actual_aingura = re.search(r'^([^\}]+)\}\}', paragraph).group(1)
            except:
                pass # actual_aingura stays the same
            paragraph = re.sub('  +', ' ',paragraph.replace('\n',' '))
            paragraph = re.sub(r'<ins>[^<]+</ins>', '', paragraph)
            paragraph = re.sub(r'<ref>[^<]+</ref>', '', paragraph)
            paragraph = re.sub(r'<br ?/>', ' @', paragraph)
            paragraph = re.sub(r'<[^>]+>', '', paragraph)
            tokens = word_tokenize(paragraph)
            for token in tokens:
                if re.search(r"[^\w]", token) or re.search(r"\d", token):
                    print(f"\nSkipping token: {token}")
                    continue
                print(f"\nNow processing token: {token}")
                if lang == "eu" and token.lower() not in lexicon["eu"]:
                    lemma_candidate = search_oeh(token.lower())
                    print(f"lemma candidate: {lemma_candidate}")
                elif lang == "eu" and token.lower() in lexicon["eu"]:
                    lemma_candidate = lexicon["eu"][token.lower()][0]['lemma']
                    print(f"Got seen lemma candidate: {lemma_candidate}")
                else:
                    lemma_candidate = {'lemma': "", 'hitz_egok': "", 'lexeme': ""}
                    print(f"Got no lemma candidate for token: {token}")
                aingura_link = doclink + "#" + actual_aingura
                print(f"Getting context for token: {token}")
                contexts = re.findall(rf' ?[^\.@]*{token}[ ,\.;:\?][^ \.@]*\.?', paragraph)
                if len(contexts) == 0:
                    contexts = [" *** ERROR: Testuingurua ez dut topatu *** "]
                for context in contexts:
                    print_context = context.replace("'","").strip()
                    print_context = re.sub(r'\d+\}+', '', print_context)
                    print(f"context in aingura paragraph #{actual_aingura}: '{print_context}'")
                    if token.lower() not in lexicon[lang]:
                        lexicon[lang][token.lower()] = [{'lemma': lemma_candidate, 'aingura': aingura_link, 'context': print_context}]
                    else:
                        lexicon[lang][token.lower()].append({'lemma': lemma_candidate, 'aingura': aingura_link, 'context': print_context})
    return lexicon

lexicon = {"eu": {}, "es": {}, "la": {}}
# documents = [("HHHT", "https://eu.wikisource.org/wiki/Hiztegi_Hirukoitzeko_hitzaurreko_testuak#"),
#             ("LAZK", "https://eu.wikisource.org/wiki/Azkoitiko_Sermoia#")]
documents = [("etxepare", "https://eu.wikisource.org/wiki/Linguae_vasconum_primitiae")]
for document, baselink in documents:
    doc_lexicon = lexicon_build(textname=document, doclink=baselink)
    with open(f'data/{document}_lexicon.json', 'w') as file:
        json.dump(doc_lexicon, file, indent=2)
    for lang in ["eu", "es", "la"]:
        for word in doc_lexicon[lang]:
            if word not in lexicon[lang]:
                lexicon[lang][word] = doc_lexicon[lang][word]
            else:
                lexicon[lang][word] += doc_lexicon[lang][word]

sorted_lexicon = {"eu": dict(sorted(lexicon['eu'].items())),
                  "es": dict(sorted(lexicon['es'].items())),
                  "la": dict(sorted(lexicon['la'].items()))}


with open('data/sorted_lexicon.json', 'w') as file:
    json.dump(sorted_lexicon, file, indent=2)


