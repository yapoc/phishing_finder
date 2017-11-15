#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import argparse
import sys

from libs.exceptions import ParameterException
from libs.string.punny import PunnyGenerator
from libs.network.nslookup import NsLookup

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
  parser.add_argument('-d', '--domain', type = str, required = True, \
    help = 'Adresse du domaine à surveiller (Option duplicable 1 fois par domaine).',\
    dest = 'domain', action = 'append')
  parser.add_argument('-a', '--adapter', type = str, required = False, \
    help = 'Adapteur à utiliser pour réaliser la résolution DNS.', default = 'dns', \
    dest = 'adapter')
  parser.add_argument ('-o', '--output', type = argparse.FileType ('w'), \
    default = sys.stdout, help = "Emplacement du rapport.", dest = 'output' )
  args = parser.parse_args ()

  args.output.write ("""+-{:-<32}-+-{:->40}-+-{:->32}-+-{:->15}-+\n""".format ("", "", "", ""))
  args.output.write ("""| {:<32} | {:>40} | {:>32} | {:>15} |\n""".format (*header ()))
  args.output.write ("""+-{:-<32}-+-{:->40}-+-{:->32}-+-{:->15}-+\n""".format ("", "", "", ""))

  for current_domain in args.domain:
    for l in run (domain = current_domain, adapter = args.adapter):
      args.output.write ("""| {:<32} | {:>40} | {:>32} | {:>15} |\n""".format (*l))
    args.output.write ("""+-{:-<32}-+-{:->40}-+-{:->32}-+-{:->15}-+\n""".format ("", "", "", ""))
