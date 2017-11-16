#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import argparse
import sys
import logging
import json
logging.basicConfig (
  format = "[%(asctime)s] - %(levelname)-8s - %(name)-15s - %(message)s",
  level = logging.DEBUG,
)
from libs.string.tld import fetch_n_parse_tlds
logger = logging.getLogger (__name__)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Génération du fichier de cache contenant les associations entre les tld et les serveurs de whois.')
  parser.add_argument('-c', '--cache', type = argparse.FileType ('w'), \
    help = 'Emplacement du fichier de cache',\
    dest = 'cache', default = 'cache/tld_whois.py')
  args = parser.parse_args ()
  logger.debug ("Arguments utilisés par le script : {}.".format (args))

  result = {}
  for asso in fetch_n_parse_tlds ():
    if asso[1] not in result:
      result[asso[1]] = []
    result[asso[1]].append (asso[0])
  args.cache.write (json.dumps (result))

