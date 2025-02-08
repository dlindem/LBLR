import re

with open('data/SanAgustin.wikitext') as file:
    wikitext = file.read()

paragraph_number = 0
result = []
paragraphs = wikitext.split("\n\n")
for paragraph in paragraphs:
    paragraph = re.sub(r'\n', '<br/>', paragraph)
    print(paragraph)
    if not paragraph.startswith("<span"):
        paragraph = "{{aingura|" + str(paragraph_number) + "}}" + paragraph
    else:
        span_split = re.search("^(<span[^>]+>)(.*)", paragraph)
        paragraph = span_split.group(1) + "{{aingura|" + str(paragraph_number) + "}}" + span_split.group(2)
    paragraph_number += 1
    result.append(paragraph)
result_text = ("\n\n").join(result)

with open('data/SanAgustin_ainguratuta.wikitext', 'w') as file:
    file.write(result_text)

