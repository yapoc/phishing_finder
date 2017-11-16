Plusieurs outils disponibles dans ce dépôt; principalement destinés à l'identification de noms de domaines pouvant entrer en concurrence avec une marque donnée que vous souhaitez protéger.

# Installation
```
python -m venv <NOM_ENVIRONNEMENT_VIRTUEL>
source <NOM_ENVIRONNEMENT_VIRTUEL>/bin/activate
git clone https://github.com/yapoc/phishing_finder.git
cd phishing_finder
pip install -r requirements
cd /tmp
git clone https://github.com/yapoc/python-whois.git
cd python-whois
python setup.py build
python setup.py install
rm -rf /tmp/python-whois
```

# Utilisation des scripts

## Prérequis standards
Sourcer l'environnement correctement et se positionner dans le bon dossier : 
```
source <NOM_ENVIRONNEMENT_VIRTUEL>/bin/activate
cd phishing_finder
```

## Script `predict_punny_code_dns_names.py`
### Lancement
Plusieurs paramètres peuvent être utilisés conjointement pour réaliser les opérations souhaitées : 
  * `--help` est le paramètre principal correspondant à la documentation du script : 
```
usage: predict_punny_code_dns_names.py [-h] -d DOMAIN [-a ADAPTER] [-o OUTPUT]
Génération de tout plein de noms de domaines potentiels pour surveiller le
phishing.
optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Adresse du domaine à surveiller (Option duplicable 1
                        fois par domaine).
  -a ADAPTER, --adapter ADAPTER
                        Adapteur à utiliser pour réaliser la résolution DNS.
  -o OUTPUT, --output OUTPUT
                        Emplacement du rapport.
```

  * `--domain` ou `-d` correspond au domaine à interroger. Exemple d'utilisation : 
```
./predict_punny_code_dns_names.py --domain example1.com -d example2.com
./predict_punny_code_dns_names.py -d example1.com -d example2.com
```

  * `--adapter` ou `-a` correspond à l'adapteur utilisé pour obtenir les informations de déclaration DNS. Trois valeurs sont possibles à ce jour; seules deux sont développées : 
    * `dns`, réalise les requêtes DNS par le biais de la lib `dnspython`. **C'est l'adapteur par défaut**.
    * `none` ne retourne aucune information de déclaration DNS.
    * `web` interroge le résultat du site `http://dnslookup.fr`.
```
./predict_punny_code_dns_names.py -d example.com -a none
./predict_punny_code_dns_names.py -d example.com --adapter none
```

  * `--output` ou `-o` permet d'indiquer l'emplacement du fichier contenant les résultats. `/dev/stdout` par défaut.
```
./predict_punny_code_dns_names.py -d example.com -a none --output /tmp/fichier_de_resultat
./predict_punny_code_dns_names.py -d example.com -a none -o /tmp/fichier_de_resultat
```

### Exemple de résultat
```
(NOM_ENVIRONNEMENT_VIRTUEL) [user@host phishing_finder]$ ./predict_punny_code_dns_names.py -d example.com
+---------------------------+------------------------------------------+---------------------------+----------+-----------------+
| Domaine                   |                       Encodage PunnyCode |            Encodage UTF-8 | Réservé? |          @IPv4? |
+---------------------------+------------------------------------------+---------------------------+----------+-----------------+
| example.com               |                              example.com |               example.com |      Oui |   93.184.216.34 |
| example.com               |                       xn--exampl-uva.com |               examplë.com |      Non |             N/A |
| example.com               |                       xn--exampl-8ua.com |               examplè.com |      Non |             N/A |
| example.com               |                       xn--exampl-gva.com |               examplé.com |      Non |             N/A |
| example.com               |                             exarnple.com |              exarnple.com |      Oui |             N/A |
| example.com               |                      xn--exarnpl-xya.com |              exarnplë.com |      Non |             N/A |
| example.com               |                      xn--exarnpl-8xa.com |              exarnplè.com |      Non |             N/A |
| example.com               |                      xn--exarnpl-hya.com |              exarnplé.com |      Non |             N/A |
| example.com               |                       xn--exmple-cua.com |               exämple.com |      Oui |   85.13.149.201 |
| example.com               |                      xn--exmpl-hra6c.com |               exämplë.com |      Non |             N/A |
| example.com               |                      xn--exmpl-hra5a.com |               exämplè.com |      Non |             N/A |
|                                                              8<...>8                                                          |
+---------------------------+------------------------------------------+---------------------------+----------+-----------------+
```

## Script `create_tld_whois_server_cache_file.py`
### Lancement
Ce script est destiné à générer le fichier de cache contenant les associations entre un `tld` et le serveur de `whois` associé. Plusieurs paramètres peuvent être utilisés conjointement pour réaliser les opérations souhaitées : 
  * `--help` est le paramètre principal correspondant à la documentation du script : 
```
usage: create_tld_whois_server_cache_file.py [-h] [-c CACHE]

Génération du fichier de cache contenant les associations entre les tld et les
serveurs de whois.

optional arguments:
  -h, --help            show this help message and exit
  -c CACHE, --cache CACHE
                        Emplacement du fichier de cache
```
  * `--cache` ou `-c` : ce paramètre indique l'emplacement du fichier de cache à utiliser. La valeur par défaut est `cache/tld_whois.py`.

### Exemple de résultat
Un fichier `cache` a été créé dans un format proche de celui-ci : 
```
{
  "whois.afilias-srs.net": [
    "abarth", 
    "abbott", 
    "abbvie", 
    "aco", 
    "active"
  ], 
  "whois.donuts.co": [
    "academy", 
    "accountants"
  ], 
  8<...>8,
  "whois.unitedtld.com": [
    "actor"
  ], 
}
```
