# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import requests

def http_get (url):
  r = requests.get(url)
  if int(r.status_code) > 400:
    msg = "Erreur d'appel GET {} ({})".format(api_endpoint, r.status_code)
    raise Exception(msg)
  return r.text

