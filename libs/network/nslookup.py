# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import dns.resolver
import requests
import re

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

