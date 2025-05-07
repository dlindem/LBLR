import csv

with open('ekc-authors-wd.csv') as file1:
    ekc = csv.DictReader(file1, delimiter=",")

    result = "authorname\tWikidata_Qid\tMLV_Qid\n"
    seen_names = []
    for row in ekc:
        print(row)
        if row['authorname'] in seen_names:
            continue
        seen_names.append(row['authorname'])
        wd = row['Wikidata_Qid']
        wb = ""
        with open('egileak_mlv.csv') as file2:
            mlv = csv.DictReader(file2, delimiter="\t")
            for mlv_row in mlv:
                if mlv_row['wd'] == wd:
                    wb = mlv_row['qid']
        result += f"{row['authorname']}\t{wd}\t{wb}\n"

with open('ekc-authors-wd-wb.csv', 'w') as file3:
    file3.write(result)
