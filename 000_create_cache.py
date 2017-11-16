#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import argparse
import sys
import logging
import json
logging.basicConfig (
  format = "[%(asctime)s] - %(levelname)-8s - %(name)-15s - %(message)s",
  level = logging.INFO,
)
from libs.string.tld import create_cache_data as tld_whois_cache_data
logger = logging.getLogger (__name__)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Génération des différents fichiers de cache utilisés par les scripts.')
  parser.add_argument('--cache-tld-whois', type = argparse.FileType ('w'), \
    help = 'Emplacement du fichier de cache',\
    dest = 'cache_tld_whois', required = False)
  args = parser.parse_args ()
  logger.debug ("Arguments utilisés par le script : {}.".format (args))

  if args.cache_tld_whois:
      logging.info ("Rafraîchissement du cache pour les associations tld <=> serveur de whois.")
      result = tld_whois_cache_data ()
      args.cache_tld_whois.write (json.dumps (result, sort_keys = True, indent = 2))
