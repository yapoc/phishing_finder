# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
from itertools import product
_REPLACEMENTS = {
  'a': ['ä', 'à', 'á'],
  'e': ['ë', 'è', 'é'],
  'i': ['ï', 'ì', 'í'],
  'o': ['ö', 'ò', 'ó', '0'],
  'u': ['ü', 'ù', 'ú'],
  'm': ['rn'],
  's': ['5'],
  'b': ['6'],
  'g': ['q', '9'],
  'd': ['cl'],
  'w': ['vv'],
}

def _domain_from_element (element):
  temp = element.split ('.')
  if len (temp) > 2:
    raise ParameterException ("Merci de n'indiquer que le domaine; sans les sous-domaines.")
  return temp [0]

def _build_letters_tree (word):
  result = []
  for letter in word:
    temp = [ letter ]
    if letter in _REPLACEMENTS:
      temp += _REPLACEMENTS [letter]
    result.append (temp)
  return result

def _utf8_to_punny (word):
  return word.encode ('idna').decode ('ascii')

def derivate_domains (domain):
  domain = _domain_from_element (domain)
  possibilities = _build_letters_tree (domain)
  for temp in product (*possibilities):
    current = "".join (temp)
    yield ("{}".format (current), "{}".format (_utf8_to_punny (current)))
