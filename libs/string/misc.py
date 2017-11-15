# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
from libs.exceptions import WrongDomainException

def extract_domain_tld (element):
  temp = element.split ('.')
  if len (temp) < 2:
    raise WrongDomainException ("{} ne ressemble vraiment pas à un domaine!!!.".format (element))
  return ("".join (temp[:-1]), temp[-1])
