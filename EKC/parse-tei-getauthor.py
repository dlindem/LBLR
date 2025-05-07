from bs4 import BeautifulSoup
import os, sys, re



result = "authorname\n"
for filename in os.listdir('TEI-UTF8'):
    print(f"Now processing: {filename}")


    with open(f"TEI-UTF8/{filename}", 'r', encoding="utf-8") as tei_file:
        soup = BeautifulSoup(tei_file, 'lxml')
    author = soup.author.getText()
    result += f"{author}\n"

with open('ekc_authors.csv', 'w') as file:
    file.write(result)