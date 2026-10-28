import xwb, re, csv, time

with open('data/sense_glosses.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        sense_id = row['sense'].replace('https://monumenta.wikibase.cloud/entity/', '')
        glossdict = {"glosses": {"eu": {"language": "eu", "value": row['gloss']}}}
        xwb.editsense(sense_id=sense_id, glossdict=glossdict)
        time.sleep(.6)