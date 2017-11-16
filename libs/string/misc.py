# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
from itertools import product
import logging
from libs.exceptions import WrongDomainException
logger = logging.getLogger (__name__)

_WORDS_SEPARATORS = [ '-', '_' ]

def extract_domain_tld (element):
  temp = element.split ('.')
  if len (temp) < 2:
    raise WrongDomainException ("{} ne ressemble vraiment pas à un domaine!!!.".format (element))
  return ("".join (temp[:-1]), temp[-1])

def shuffle_words_from_lists (domain, words_list, combine = False, combine_times = 3):
  possibilities = []
  if combine:
    logger.info ("Activation de la combinaison ({} itérations).".format (combine_times))
    for i in range (0, combine_times):
      possibilities.append ([domain] + words_list)
      possibilities.append (_WORDS_SEPARATORS)
    """Ça, c'est pour enlever le séparateur final."""
    possibilities = possibilities[:-1]
  else:
    logger.info ("Pas de combinaison.")
    possibilities = [
      [ domain ],
      _WORDS_SEPARATORS,
      words_list
    ]
  for temp in product (*possibilities):
    if domain in (temp):
      yield "".join (temp)
