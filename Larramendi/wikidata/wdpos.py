from SPARQLWrapper import SPARQLWrapper, JSON
import time
import json

wdquerycount = 0

with open ('LAR_sar1745_wd_matches.csv', 'r') as file:
    matchlist = file.read().split('\n')

print(matchlist)
matchdict = {}


for line in matchlist:
    try:
        larlemma = line.split(',')[0]
        wdlemma = line.split(',')[1]
        querylemma = '\"'+wdlemma+'\"'
        print('['+str(wdquerycount)+' of '+str(len(matchlist))+': '+querylemma+']')

        #query wikidata
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Basque Lexemes project (lexbib.org/larramendi)')
        sparql.setQuery(
        """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        #Lexemes in Basque: lemma and POSLabel and Sense and Definition
        #Example Query for demonstration (Lindemann/Alonso 2021)
        select ?lemma ?lexemeId ?categoryLabel   WHERE {
            ?lexemeId <http://purl.org/dc/terms/language> wd:Q8752;
                    wikibase:lemma ?lemma;
        			wikibase:lexicalCategory ?category.
          FILTER (str(?lemma) = """+querylemma+""")


         SERVICE wikibase:label { bd:serviceParam wikibase:language "eu". }
         }

        """
        )

        sparql.setReturnFormat(JSON)
        wdquerycount = wdquerycount + 1

        datalist = sparql.query().convert()['results']['bindings']
        print(str(datalist))
        matchdict[larlemma] = []
        for result in datalist:
            matchdict[larlemma].append(result)
        time.sleep(0.5)
    except Exception as ex:
        print('Error: '+str(ex))
        pass

with open ('D:/Lab_LAR/Wikidata/wdpos_result.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(matchdict, jsonfile, indent=2)
