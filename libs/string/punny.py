# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
from itertools import product
from libs.string.misc import extract_domain_tld
from libs.exceptions import WrongDomainException
import logging
logger = logging.getLogger (__name__)

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
  try:
    return extract_domain_tld (element)[0]
  except WrongDomainException: 
    return element

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
  logger.info ("Tentative d'identification des domaines dérivés de {}".format (domain))
  possibilities = _build_letters_tree (domain)
  logger.debug ("Produits cartésiens qu'il va falloir se fader.".format (possibilities))
  for temp in product (*possibilities):
    current = "".join (temp)
    yield ("{}".format (current), "{}".format (_utf8_to_punny (current)))
