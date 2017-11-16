# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import requests
import logging
logger = logging.getLogger (__name__)

def http_get (url):
  logger.debug ("Appel HTTP de l'URL {}".format (url))
  r = requests.get(url)
  logger.debug ("Code retour : {}".format (r.status_code))
  if int(r.status_code) > 400:
    msg = "Erreur d'appel GET {} ({})".format(url, r.status_code)
    logger.critical (msg)
    raise Exception(msg)
  return r.text

