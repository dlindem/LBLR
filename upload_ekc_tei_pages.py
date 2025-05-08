import os, sys, re, csv, time
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import xwb

with open('EKC/ekc-texts-wb.csv') as file:
    ekc = csv.DictReader(file, delimiter="\t")
    for row in ekc:
        ekc_code = row['kodea']
        filename = ekc_code + ".xml"
        page_name = f"Testua:{ekc_code}/TEI"

        print(f"Now processing: {filename}")

        with open(f"EKC/TEI-UTF8/{filename}", 'r', encoding="utf-8") as tei_file:
            rawfile = tei_file.read()

        content = f"= {row['egile_izena']}: {row['izenburua']} =\n"
        content += '* TEI-XML bertsioa, Josu Landak ekoitzia.\n'
        content += f'* Testua deskribatzen duen entitatea: [[Item:{row['item']}|{row['item']}]].\n'
        content += f'* Bertsio hau deskribatzen duen entitatea: [[Item:{row['item']}|{row['bertsioa']}]].\n'
        body = '<syntaxhighlight lang="XML" line>\n'
        body += rawfile
        body += "</syntaxhighlight>"

        try:
            pagecreation = xwb.site.post('edit', token=xwb.token, contentformat='text/x-wiki', contentmodel='wikitext',
                                         bot=True, recreate=True, summary=f"recreate wiki page using upload_ekc_tei_pages.py",
									     title=page_name, text=content+body)
        except:
            pagecreation = xwb.site.post('edit', token=xwb.token, contentformat='text/x-wiki', contentmodel='wikitext',
                                         bot=True, recreate=True,
                                         summary=f"recreate wiki page using upload_ekc_tei_pages.py",
                                         title=page_name, text=content)
            print("*** Failed uploading body of: "+ filename)
        time.sleep(1)