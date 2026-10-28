import csv, time, re, json

result = []
with open('data/entries_with_sense.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t')
    for row in csv_reader:
        sense_count = int(row['senses'])
        testua = row['sarrera_testua']

        while re.search(r'[\[\(][^\)\]]+; ?[^\)\]]+[\)\]]', testua):
            testua = re.sub(r'([\[\(][^\)\]]+); ?([^\)\]]+[\)\]])', r'\1 @ \2', testua)
        while re.search(r'\([^\)]+: ?[^\)]+\)', testua):
            testua = re.sub(r'(\([^\)]+): ?([^\)]+\))', r'\1 € \2', testua)

        semicolon_count = len(re.findall(';', testua))
        row['real_sensecount'] = semicolon_count + 1
        if sense_count != semicolon_count + 1:
            proposal = testua
            while re.search(r'^[^\:;—\(\[]+\: ?', proposal):
                proposal = re.sub(r'^[^\:;—]+\: ?', '', proposal)
            if "—" in proposal:
                continue
            proposal = re.sub(r'; ?', ' * ', proposal)
            row['proposal'] = proposal
            row['proposed_senses'] = [re.sub(r'\.$','', x.strip()) for x in proposal.split("*")]
            row['proposed_senses'] = [x.replace(" @ ", "; ") for x in row['proposed_senses'] if x.strip()]
            row['proposed_senses'] = [x.replace(" € ", ": ") for x in row['proposed_senses']]
            result.append(row)


with open('data/entries_with_sense.json', 'w') as file:
    json.dump(result, file, indent=2)
