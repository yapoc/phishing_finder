#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import argparse
import sys
import logging
logging.basicConfig (
  format = "[%(asctime)s] - %(levelname)-8s - %(name)-15s - %(message)s",
  level = logging.INFO,
)

from libs.exceptions import ParameterException
from libs.string.tld import compute_all_domains_tld
from libs.network.nslookup import lookup
from libs.network.whois import estimate_domain_is_registered
from libs.misc import get_file_full_path

SEP_LINE = """+-{:-<45}-+-{:->8}-+-{:->15}-+\n""".format ("", "", "", "", "")
HEADERS = [ 'Domaine', 'Réservé?' , '@IPv4?' ]

logger = logging.getLogger (__name__)

def run (**kwargs):
  for i in [ 'name', 'adapter', 'no_cache', 'cache_file']:
    if i not in kwargs:
      raise Exception ("La fonction n'est pas appellée correctement.")
  try:
    logger.info ("Dans la fonction principale.")
    for d in compute_all_domains_tld (element = kwargs['name'], no_cache = kwargs['no_cache'], cache_file = kwargs['cache_file']):
      logger.info ("Analyse du domaine {} ({}).".format (*d))
      is_reserved = "Non"
      has_ip = 'N/A'
      try:
        if estimate_domain_is_registered (domain = d[0], whois_server = d[1]):
          is_reserved = "Oui"
          has_ip = lookup (d[0], kwargs['adapter']) or 'N/A'
      except Exception as e:
        logger.warn ("Une erreur s'est produite.")
        logger.warn (e)
      yield [ d[0], is_reserved, has_ip ]
  except ParameterException as e:
    logger.critical (e)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Génération de tout plein de noms de domaines potentiels pour surveiller le phishing.')
  parser.add_argument('-n', '--name', type = str, required = True, \
    help = 'Nom à surveiller (Option duplicable 1 fois par nom).',\
    dest = 'name', action = 'append')
  parser.add_argument('-a', '--adapter', type = str, required = False, \
    help = 'Adapteur à utiliser pour réaliser la résolution DNS.', default = 'dns', \
    dest = 'adapter')
  parser.add_argument ('-o', '--output', type = argparse.FileType ('w'), \
    default = sys.stdout, help = "Emplacement du rapport.", dest = 'output' )
  parser.add_argument ('--no-cache', required = False, default = True, \
    help = "Activer ce booléen pour ne pas utiliser le dossier de cache.", \
    action = 'store_false' )
  parser.add_argument ('--cache-file', required = False, default = "cache/tld_whois.py", \
    help = "Fichier de cache.")
  args = parser.parse_args ()
  logger.debug ("Arguments utilisés par le script : {}.".format (args))

  args.output.write (SEP_LINE)
  args.output.write ("""| {:<45} | {:>8} | {:>15} |\n""".format (*HEADERS))
  args.output.write (SEP_LINE)

  try:
    for current_name in args.name:
      logger.info ("Analyse du nom {}.".format (current_name))
      for l in run (name = current_name, adapter = args.adapter, no_cache = args.no_cache, \
          cache_file = get_file_full_path (args.cache_file, __file__)):
        args.output.write ("""| {:<45} | {:>8} | {:>15} |\n""".format (*l))
      args.output.write (SEP_LINE)
  except Exception as e:
    logger.critical ("Erreur catastrophique : {}".format (e))
