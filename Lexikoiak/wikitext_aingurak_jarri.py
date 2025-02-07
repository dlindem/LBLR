

with open('data/etxepare.wikitext') as file:
    wikitext = file.read()

spans = wikitext.split('<span lang="')
goiburua = spans.pop(0)
print(f"Dokumentua kargatuta. Goiburua hau da:\n{goiburua}")

result = [goiburua]
paragraph_number = 1
for span in spans:
    paragraphs = f'<span lang="{span}'.split("\n\n")
    for paragraph in paragraphs:
        print(paragraph)
        if not paragraph.startswith("<ins>"):
            paragraph = "{{aingura|" + str(paragraph_number) + "}}" + paragraph
            paragraph_number += 1
        result.append(paragraph)
result_text = ("\n\n").join(result)

with open('data/etxepare_ainguratuta.wikitext', 'w') as file:
    file.write(result_text)

