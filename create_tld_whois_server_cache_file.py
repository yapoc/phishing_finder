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
from libs.string.tld import create_cache_data
logger = logging.getLogger (__name__)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Génération du fichier de cache contenant les associations entre les tld et les serveurs de whois.')
  parser.add_argument('-c', '--cache', type = argparse.FileType ('w'), \
    help = 'Emplacement du fichier de cache',\
    dest = 'cache', default = 'cache/tld_whois.py')
  args = parser.parse_args ()
  logger.debug ("Arguments utilisés par le script : {}.".format (args))

  result = create_cache_data ()
  args.cache.write (json.dumps (result))
