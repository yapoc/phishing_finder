# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
from itertools import product

class PunnyGenerator (object):
  def __init__ (self, domain):
    self._replacements = {
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
    self._domain, self._tld = self._safety_checks (domain)

  def _safety_checks (self, domain):
    elements = domain.split ('.')
    if len (elements) > 2:
      raise ParameterException ("Merci de n'indiquer que le domaine; sans les sous-domaines.")
    elif len (elements) < 2:
      raise ParameterException ("On dirait que c'est pas vraiment un domaine que t'as indiqué!")
    return elements[0], elements[1]

  def _build_letters_tree (self, word):
    result = []
    for letter in word:
      if letter in self._replacements:
        result.append ([letter]+self._replacements [letter])
      else:
        result.append ([letter])
    return result

  def _utf8_to_punny (self, word):
    return word.encode ('idna').decode ('ascii')

  def generate_domains (self):
    possibilities = self._build_letters_tree (self._domain)
    for temp in product (*possibilities):
      current = "".join (temp)
      yield ("{}.{}".format (current, self._tld), "{}.{}".format (self._utf8_to_punny (current), self._tld))
