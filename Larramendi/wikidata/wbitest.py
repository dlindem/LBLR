from wikibaseintegrator import wbi_login, wbi_core
import logging
logging.basicConfig(level=logging.INFO)

login_instance = wbi_login.Login(user='DavidL', pwd='VP4ptJbLhNM9vB4')

my_first_wikidata_item = wbi_core.ItemEngine(item_id='Q1')

# to check successful installation and retrieval of the data, you can print the json representation of the item
print(my_first_wikidata_item.get_json_representation())

result = wbi_core.ItemEngine(item_id='Q1', data={'P3':'http://www.wikidata.org/entity/Q65216433'})
