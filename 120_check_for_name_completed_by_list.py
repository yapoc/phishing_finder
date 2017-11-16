#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import argparse
import sys
import logging
logging.basicConfig (
  format = "[%(asctime)s] - %(levelname)-8s - %(name)-15s - %(message)s",
  level = logging.DEBUG,
)

from libs.exceptions import ParameterException
from libs.string.misc import extract_domain_tld
from libs.string.misc import shuffle_words_from_lists
from libs.string.tld import compute_all_domains_tld
from libs.network.whois import estimate_domain_is_registered

SEP_LINE = """+-{:-<75}-+-{:->10}-+\n""".format ("", "", "", "", "")
HEADERS = [ 'Domaine', 'Réservé?' ]

logger = logging.getLogger (__name__)

def run (**kwargs):
  for i in [ 'domain', 'adapter', 'words_list', 'combine', 'combine_times', 'no_cache', 'cache_file' ]:
    if i not in kwargs:
      raise Exception ("La fonction n'est pas appellée correctement.")
  try:
    (domain, tld) = extract_domain_tld (kwargs['domain'])
    for a in shuffle_words_from_lists (domain, kwargs['words_list'], kwargs['combine'], kwargs['combine_times']):
      for d in compute_all_domains_tld (element = a, no_cache = kwargs['no_cache'], cache_file = kwargs['cache_file']):
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
  parser = argparse.ArgumentParser(description='Génération de noms de domaines potentiels sur la base d\' mot initial et d\'une liste de mots à ajouter avant, après, pendant, ...')
  parser.add_argument ('-d', '--domain', type = str, required = True, \
    help = "Domaine d'origine à partir duquel construire la liste des possibles.", \
    dest = 'domain', action = 'append')
  parser.add_argument ('-wl', '--words-list', type = argparse.FileType ('r'), required = True, \
    help = "Emplacement du fichier contenant la liste des mots à utiliser pour générer les domaines.", \
    dest = 'words_list')
  parser.add_argument('-a', '--adapter', type = str, required = False, \
    help = 'Adapteur à utiliser pour réaliser la résolution DNS.', default = 'dns', \
    dest = 'adapter')
  parser.add_argument ('-o', '--output', type = argparse.FileType ('w'), \
    default = sys.stdout, help = "Emplacement du rapport.", dest = 'output' )
  parser.add_argument ('-c', '--combine', action = 'store_true', dest = 'combine', \
    help = 'Activer la combinatoire de tous les mots clefs présents dans le fichier?',
    default = False )
  parser.add_argument ( '-ct', '--combine-times', type = int, dest = 'combine_times', \
    help = 'Nombre de combinaisons autorisées.', default = 3 )
  parser.add_argument ('--no-cache', required = False, default = True, \
    help = "Activer ce booléen pour ne pas utiliser le dossier de cache.", \
    action = 'store_false' )
  parser.add_argument ('--cache-file', required = False, default = "cache/tld_whois.py", \
    help = "Fichier de cache.")
  args = parser.parse_args ()

  logger.debug ("Arguments utilisés par le script : {}.".format (args))

  words_list = [ x.lower ().strip () for x in args.words_list.readlines () ]

  args.output.write (SEP_LINE)
  args.output.write ("| {:<75} | {:>10} |\n".format (*HEADERS))
  args.output.write (SEP_LINE)

  try:
    for current_domain in args.domain:
      for l in run (domain = current_domain, adapter = args.adapter, \
        words_list = words_list, combine = args.combine, combine_times = args.combine_times, \
        no_cache = args.no_cache, cache_file = args.cache_file):
        args.output.write ("| {:<75} | {:>10} |\n".format (*l))
      args.output.write (SEP_LINE)
  except Exception as e:
    logger.critical ("Erreur catastrophique : {}".format (e))
