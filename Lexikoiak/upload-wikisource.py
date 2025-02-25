import mwclient, config_private, os, re, time


site = mwclient.Site("eu.wikisource.org")
def get_token():
	global site

	# lwb login via mwclient
	while True:
		try:
			login = site.login(username=config_private.wikisource_user, password=config_private.wikisource_pwd)
			break
		except Exception as ex:
			print('lwb login via mwclient raised error: '+str(ex))
			time.sleep(60)
	# get token
	csrfquery = site.api('query', meta='tokens')
	token = csrfquery['query']['tokens']['csrftoken']
	print("Got fresh CSRF token for eu.wikisource")
	return token
token = get_token()

wikitext_folder = "data/wikitext"
wikitext_filename_base = "Azkoitiko_Sermoia"
wikisource_pagename_base = "Orrialde:Larramendi_1737_Azkoitiko_Sermoia.pdf/"

for filename in os.listdir(wikitext_folder):
	if wikitext_filename_base in filename:
		pagenum = re.search(rf'{wikitext_filename_base}[^\d]*(\d+)', filename).group(1)
		pagename = wikisource_pagename_base + pagenum
		print(f"\nWill now upload '{filename}' to '{pagename}'...")
		with open(f"{wikitext_folder}/{filename}") as file:
			wikitext = file.read()
		site.post('edit',
			  bot=True,
			  contentformat="text/x-wiki",
			  recreate=True,
			  summary=f"Orrialdea birsortua LBLR/upload-wikisource.py, {config_private.wikisource_user}",
			  text=wikitext,
			  title=pagename,
			  token=token)
		time.sleep(1)


print("Finished.")


