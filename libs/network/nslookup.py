# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import dns.resolver
import re

from libs.exceptions import ParameterException
from libs.network.http import http_get

import logging
logger = logging.getLogger (__name__)

_NSLOOKUP_PROVIDER_URL = 'http://dnslookup.fr/__DOMAIN__'
_NSLOOKUP_PROVIDER_RESULT_LINE = '<td>IN</td><td>A</td>'
_NS_REGULAR_EXPRESSION_TO_GET_IP = re.compile ('^.*>(?P<ip>[0-9][^<]+)</.*$')

def _web_fetch (domain):
  logger.debug ("Réalisation d'une requête web pour connaitre l'adresse IPv4 du domaine {}.".format (domain))
  for l in http_get (_NSLOOKUP_PROVIDER_URL.replace ('__DOMAIN__', domain)).split ('\n'):
    if _NSLOOKUP_PROVIDER_RESULT_LINE in l:
      m = re.match (_NS_REGULAR_EXPRESSION_TO_GET_IP, l)
      if m:
        logger.info ("Un enregistrement DNS a été trouvé pour {}!".format (domain))
        return m.group ('ip')
  return None

def _none_fetch (domain):
  return 'N/A'

def _dns_fetch (domain):
  for query_type in [ 'A', 'AAAA']:
    logger.debug ("Réalisation d'une requête de type {} vers {}.".format (query_type, domain))
    try:
      temp = dns.resolver.query (domain, query_type)
      if len (temp):
        logger.info ("Un enregistrement DNS a été trouvé pour {}!".format (domain))
        return str (temp[0])
    except (dns.resolver.NoNameservers, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as e:
      logger.error ("Problème lors de la résolution DNS du domaine {}.".format (domain))
      logger.error (e)
      pass
  return None

def lookup (domain, adapter = 'dns'):
  adapter = adapter.lower ()
  if adapter not in [ 'web', 'dns', 'none' ]:
    raise ParameterException ("L'adapteur demandé ({}) n'est pas disponible.".format (adapter))
  try:
    return globals () ["_{}_fetch".format (adapter)](domain)
  except AttributeError:
    raise Exception ("Impossible d'appeler l'adaptateur {}.".format (adapter))

