#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import argparse
import requests
from itertools import product
import re
import sys
import dns.resolver

class ParameterException (Exception):
  pass

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
    if len (elements) != 2:
      raise ParameterException ("Merci de n'indiquer que le domaine; sans les sous-domaines.")
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

class NsLookup (object):
  def __init__ (self, adapter = 'web'):
    self._adapter = adapter.lower ()
    if self._adapter not in [ 'web', 'dns', 'none' ]:
      raise ParameterException ("L'adapteur demandé ({}) n'est pas disponible.".format (adapter))
    self._nslookup_provider_url = 'http://dnslookup.fr/__DOMAIN__'
    self._nslookup_provider_result_line = '<td>IN</td><td>A</td>'
    self._ns_regular_expression_to_get_ip = re.compile ('^.*>(?P<ip>[0-9][^<]+)</.*$')

  def _http_get (self, url):
    r = requests.get(url)
    if int(r.status_code) > 400:
      msg = "Erreur d'appel GET {} ({})".format(api_endpoint, r.status_code)
      raise Exception(msg)
    return r.text

  def _web_fetch (self, domain):
    for l in self._http_get (self._nslookup_provider_url.replace ('__DOMAIN__', domain)).split ('\n'):
      if self._nslookup_provider_result_line in l:
        m = re.match (self._ns_regular_expression_to_get_ip, l)
        if m:
          return m.group ('ip')
    return None

  def _none_fetch (self, domain):
    return 'N/A'

  def _dns_fetch (self, domain):
    for query_type in [ 'A', 'AAAA']:
      try:
        temp = dns.resolver.query (domain, query_type)
        if len (temp):
          return str (temp[0])
      except (dns.resolver.NoNameservers, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        pass
    return None

  def fetch (self, domain):
    try:
      return getattr (self, "_{}_fetch".format (self._adapter))(domain)
    except AttributeError:
      raise Exception ("Impossible d'appeler l'adaptateur {}.".format (self._adapter))

def header ():
  return [ 'Domaine', 'Encodage PunnyCode', 'Encodage UTF-8', 'Réservé?' ]

def run (**kwargs):
  if 'domain' not in kwargs or 'adapter' not in kwargs:
    raise Exception ("La fonction n'est pas appellée correctement.")
  try:
    ns = NsLookup (kwargs['adapter'])
    punny = PunnyGenerator (kwargs['domain'])
    for punny_domain in punny.generate_domains ():
      punny_status = ns.fetch ("{}".format (punny_domain[1]))
      if not punny_status:
        punny_status = 'dispo à l\'achat'
      yield [ kwargs['domain'], punny_domain[1], punny_domain[0], punny_status ]
  except ParameterException as e:
    print (e)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Génération de tout plein de noms de domaines potentiels pour surveiller le phishing.')
  parser.add_argument('-d', '--domains', nargs = '*', type = str, required = True, \
    help = 'Adresse du domaine ou des domaines à surveiller (séparés par des virgules).',\
    dest = 'domains')
  parser.add_argument('-a', '--adapter', type = str, required = False, \
    help = 'Adapteur à utiliser pour réaliser la résolution DNS.', default = 'WEB', \
    dest = 'adapter')
  parser.add_argument ('-o', '--output', nargs = '?', type = argparse.FileType ('w'), \
    default = sys.stdout, help = "Emplacement du rapport.", dest = 'output' )
  args = parser.parse_args ()

  args.output.write ("""+-{:-<32}-+-{:->40}-+-{:->32}-+-{:->15}-+\n""".format ("", "", "", ""))
  args.output.write ("""| {:<32} | {:>40} | {:>32} | {:>15} |\n""".format (*header ()))
  args.output.write ("""+-{:-<32}-+-{:->40}-+-{:->32}-+-{:->15}-+\n""".format ("", "", "", ""))

  for current_domain in args.domains[0].split (','):
    for l in run (domain = current_domain, adapter = args.adapter):
      args.output.write ("""| {:<32} | {:>40} | {:>32} | {:>15} |\n""".format (*l))
    args.output.write ("""+-{:-<32}-+-{:->40}-+-{:->32}-+-{:->15}-+\n""".format ("", "", "", ""))
