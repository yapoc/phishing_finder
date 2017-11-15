#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
from whois import query, WhoisException
import time

def whois (domain, nb_done = 0, nb_max_try = 5, sleep_time = 1):
  while nb_done < nb_max_try:
    nb_done += 1
    try:
      d = query (domain, force=1)
      return d
    except WhoisException:
      sleep_delay = sleep_time * nb_done
      time.sleep (sleep_delay)
      return whois (domain, nb_done, nb_max_try, sleep_time)
  return None
