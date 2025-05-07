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


for filename in os.listdir('TEI'):
    print(f"Now processing: {filename}")
    result = ""

    with open(f"TEI/{filename}", 'r', encoding="iso-8859-15") as tei_file:
        # soup = BeautifulSoup(tei_file, 'lxml')
        filestring = html.unescape(tei_file.read().replace("-->","").replace("<--",""))
        filestring = filestring.replace("&", "&amp;")
        # filestring = re.sub(r"<hi rend='Bold'>([^<]*)</hi>", r"<b>\1</b>", filestring)
        # filestring = re.sub(r"<hi rend='Italic'>([^<]*)</hi>", r"<i>\1</i>", filestring)
        with open(f'TEI-UTF8/{filename.replace(".sgml",".xml")}', 'w', encoding="utf-8") as xml_file:
            xml_file.write(filestring)

    # tree = ET.ElementTree(ET.fromstring(filestring))
    # TEI = tree.getroot()
    # firstlevel_text = TEI.findall('text')[0]
    #     # print(firstlevel_text.getText())
    # docTitle = firstlevel_text.find('front').find('docTitle').text
    # # result += f"= {firstlevel_text.find('front').getText(strip=True)} =\n\n"
    # result += f"= {docTitle} =\n\n"
    # for group in firstlevel_text.findall('group'):
    #     for text in group.findall('text'):
    #         textsoup = BeautifulSoup(ET.tostring(text), 'html.parser')
    #         if textsoup.front:
    #             title = textsoup.front.getText(separator=' ', strip=True)
    #             result += f"== {title} ==\n\n"
    #         for paragraph in textsoup.findall('p'):
    #             # par_text = get_deep_text(paragraph)
    #             par_text = re.search(r'<p>(.*)</p>', ET.tostring(paragraph, encoding="unicode")).group(1)
    #             result += f"{par_text}\n\n"
    #     # textgroup = firstlevel_text.find('group')
    #     # for text in textgroup.find_all('text'):
    #     #     for element in text.children:
    #     #         if element != "None":
    #     #             print(element.name, element.string)
    #     #     front = text.find('front')
    #     #     # print(front)
    #     #     title = front.find('p').getText()
    #     #     # result += f"== {title} ==\n\n"
    #     #     # print(text)
    #     #     # for elem in text:
    #     #     #     print(elem)
    #     #     # for p in body.find_all('p'):
    #     #     #     result += f"{p.getText()}\n\n"
    #
    # print(result)


