# https://nudin.github.io/LexData/

import logging

import LexData
from LexData.language import en

logging.basicConfig(level=logging.INFO)

repo = LexData.WikidataSession("DL2204", "Humboldt1817")

# Open a Lexeme
#L2 = LexData.Lexeme(repo, "L72517")
#LexData.get_or_create_lexeme(repo, "zuri", eu, "Q1084")

# Access the claims
print(L2.claims.keys())
# and Forms
print(len(L2.forms))
F1 = L2.forms[0]
print(F1.claims.keys())
# and senses
print(len(L2.senses))
S1 = L2.senses[0]
print(S1.claims.keys())
