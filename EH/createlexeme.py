import json
import re
import mwclient
import time


# LexBib wikibase OAuth
site = mwclient.Site('euskalhitza.wiki.opencura.com')
with open('D:/EH/pwd.txt', 'r', encoding='utf-8') as pwdfile:
    pwd = pwdfile.read()
def get_token():
    print('Getting fresh login token...')
    login = site.login(username='DavidL', password=pwd)
    csrfquery = site.api('query', meta='tokens')
    token=csrfquery['query']['tokens']['csrftoken']
    print("Got CRSF Token: "+token)
    return token
token = get_token() # get first new token

with open ('D:/EH/wd_lar.csv', 'r', encoding='utf-8') as file:
    input = file.read().split('\n')

#print(str(tlex))
errorlog = []
edits = 0
rowcount = 1
del input[0]
for row in input:

    rowcount += 1
    lemma = row.split('\t')[0]
    wdItem = row.split('\t')[1]
    posItem = row.split('\t')[2]
    print('Row ['+str(rowcount)+']: '+lemma+' '+wdItem+' '+posItem)
    # create lexeme
    labels = {}
    labels["en"] = {"language":"en","value":lemma}

    print(str(labels))
    claimdic = json.dumps([{"mainsnak":{"snaktype":"value", "property":"P1", "datavalue":{"value":wdItem,"type":"url"}}}])
    lexdata = json.dumps({"type":"lexeme","forms":[],"lemmas":labels,"lexicalCategory":posItem, "language":"Q5"}) #, "claims":claims

    # lexdata = """{
    # "claims": [
    # {"mainsnak":{"snaktype":"value", "property":"P1", "datavalue":{"value":"""+wdItem+""","type":"url"}}}
    # ],
    # "language": "Q5",
    # "lemmas":  { "language": "eu", "value": """+lemma+"""}  ,
    # "lexicalCategory": """+posItem+""" ,
    # "type": "lexeme"
    # }"""
    print(claimdic)
    print(lexdata)

    results = site.post('wbeditentity', token=token, new="lexeme", data=lexdata)
    print(str(results))
