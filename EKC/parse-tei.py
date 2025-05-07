from bs4 import BeautifulSoup
from xml.etree import cElementTree as ET
import html
import os, sys, re

def get_deep_text( element ):
    text = element.text or ''
    for subelement in element:
        text += get_deep_text( subelement )
    text += element.tail or ''
    return text


for filename in os.listdir('TEI-UTF8'):
    print(f"Now processing: {filename}")
    result = ""

   # with open(f"TEI-UTF8/{filename}", 'r', encoding="iso-8859-15") as tei_file:
        # soup = BeautifulSoup(tei_file, 'lxml')


    tree = ET.ElementTree(file=f"TEI-UTF8/{filename}")
    TEI = tree.getroot()
    firstlevel_text = TEI.findall('text')[0]
        # print(firstlevel_text.getText())
    docTitle = firstlevel_text.find('front').find('docTitle').text
    # result += f"= {firstlevel_text.find('front').getText(strip=True)} =\n\n"
    result += f"= {docTitle} =\n\n"
    for group in firstlevel_text.findall('group'):
        for text in group.findall('text'):
            textsoup = BeautifulSoup(ET.tostring(text), 'html.parser')
            if textsoup.front:
                title = textsoup.front.getText(separator=' ', strip=True)
                result += f"== {title} ==\n\n"
            for paragraph in textsoup.find_all('p'):
                # par_text = get_deep_text(paragraph)
                par_text = re.search(r'<p>(.*)</p>', str(paragraph)).group(1)
                result += f"{par_text}\n\n"
        # textgroup = firstlevel_text.find('group')
        # for text in textgroup.find_all('text'):
        #     for element in text.children:
        #         if element != "None":
        #             print(element.name, element.string)
        #     front = text.find('front')
        #     # print(front)
        #     title = front.find('p').getText()
        #     # result += f"== {title} ==\n\n"
        #     # print(text)
        #     # for elem in text:
        #     #     print(elem)
        #     # for p in body.find_all('p'):
        #     #     result += f"{p.getText()}\n\n"

        print(result)


