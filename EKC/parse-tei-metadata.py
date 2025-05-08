from bs4 import BeautifulSoup
import os, sys, re, csv, time
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import xwbi

vocab = {"G-0": "Q1436",
"G-ANT": "Q1437",
"G-BER": "Q1438",
"G-ERL": "Q1439",
"G-NAR": "Q1440",
"G-POE": "Q1441",
"G-SAI": "Q1442",
"M-0": "Q1443",
"M-16": "Q1444",
"M-17-1": "Q1445",
"M-17-2": "Q1446",
"M-18-1": "Q1447",
"M-18-2": "Q1448",
"M-19-1": "Q1449",
"M-19-2": "Q1450",
"M-20-1": "Q1451",
"M-20-2": "Q1452",
"E-0": "Q1453",
"E-BAT": "Q1454",
"E-BIZ": "Q1455",
"E-BNA": "Q1456",
"E-ERR": "Q1457",
"E-GIP": "Q1458",
"E-GNA": "Q1459",
"E-LAP": "Q1460",
"E-NAF": "Q1461",
"E-ZAR": "Q1462",
"E-ZUB": "Q1463"}

with open('ekc-authors-wd-wb.csv') as file1:
    authors_csv = csv.DictReader(file1, delimiter="\t")
    authors = {}
    for row in authors_csv:
        authors[row['authorname']] = row['MLV_Qid']

result = "qid\tP13\tP11\tLeu\tP86\n"
for filename in os.listdir('TEI-UTF8'):
    print(f"Now processing: {filename}")


    with open(f"TEI-UTF8/{filename}", 'r', encoding="utf-8") as tei_file:
        soup = BeautifulSoup(tei_file, 'lxml')
    with open(f"TEI-UTF8/{filename}", 'r', encoding="utf-8") as tei_file:
        rawfile = tei_file.read()

    # child item (version level)

    statements = [{'prop_nr': 'P5', 'value': 'Q19', 'type': 'item'},
                  {'prop_nr': 'P192', 'value': 'Q22', 'type': 'item'}]

    author_qid = authors[soup.author.getText()]
    statements.append({'prop_nr': 'P13', 'value': author_qid, 'type': 'item'})

    title = soup.title.getText()
    statements.append({'prop_nr': 'P11', 'value': title, 'type': 'string'})
    labels = [{'lang': 'eu', 'value': f'{title} (TEI)'}]

    idno = soup.idno.getText()
    statements.append({'prop_nr': 'P191', 'value': idno, 'type': 'string'})
    textpage = f'Testua:{idno}/TEI'
    statements.append({'prop_nr': 'P124', 'value': textpage, 'type': 'string'})

    aliases = [{'lang': 'eu', 'value': idno}]
    descriptions = [{'lang': 'eu', 'value': 'testu klasikoaren TEI bertsioa (armiarma / EKC)'}]

    availability_statement = soup.availability.getText()
    url = re.search(r'http.*', availability_statement).group(0)
    statements.append({'prop_nr': 'P86', 'value': url, 'type': 'url'})

    textqid = xwbi.itemwrite({'qid': False, 'statements': statements, 'labels': labels, 'descriptions': descriptions, 'aliases': aliases})

    # parent item (work level)

    labels = [{'lang': 'eu', 'value': title}]
    statements = [{'prop_nr': 'P5', 'value': 'Q23', 'type': 'item'},
                  {'prop_nr': 'P50', 'value': textqid, 'type': 'item'}]

    statements.append({'prop_nr': 'P13', 'value': author_qid, 'type': 'item'})
    statements.append({'prop_nr': 'P11', 'value': title, 'type': 'string'})
    descriptions = [{'lang': 'eu', 'value': 'testu klasikoa'}]
    aliases = [{'lang': 'eu', 'value': idno}]


    keyws = []
    for keyw in re.findall(r'<list><item>([^<]+)</item></list>', rawfile):
        print(keyw, end=" > ")
        keyw_qid = vocab[keyw]
        print(keyw_qid)
        statements.append({'prop_nr': 'P189', 'value': keyw_qid, 'type': 'item'})

    parentqid = xwbi.itemwrite(
        {'qid': False, 'statements': statements, 'labels': labels, 'descriptions': descriptions, 'aliases': aliases})





    break

# with open('ekc_authors.csv', 'w') as file:
#     file.write(result)

print(result)