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

## Script `110_check_for_name_on_punnycode_replacement.py`
### Lancement
Plusieurs paramètres peuvent être utilisés conjointement pour réaliser les opérations souhaitées : 
  * `--help` est le paramètre principal correspondant à la documentation du script : 
```
usage: 110_check_for_name_on_punnycode_replacement.py [-h] -d DOMAIN [-a ADAPTER] [-o OUTPUT]
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
./110_check_for_name_on_punnycode_replacement.py --domain example1.com -d example2.com
./110_check_for_name_on_punnycode_replacement.py -d example1.com -d example2.com
```

  * `--adapter` ou `-a` correspond à l'adapteur utilisé pour obtenir les informations de déclaration DNS. Trois valeurs sont possibles à ce jour; seules deux sont développées : 
    * `dns`, réalise les requêtes DNS par le biais de la lib `dnspython`. **C'est l'adapteur par défaut**.
    * `none` ne retourne aucune information de déclaration DNS.
    * `web` interroge le résultat du site `http://dnslookup.fr`.
```
./110_check_for_name_on_punnycode_replacement.py -d example.com -a none
./110_check_for_name_on_punnycode_replacement.py -d example.com --adapter none
```

  * `--output` ou `-o` permet d'indiquer l'emplacement du fichier contenant les résultats. `/dev/stdout` par défaut.
```
./110_check_for_name_on_punnycode_replacement.py -d example.com -a none --output /tmp/fichier_de_resultat
./110_check_for_name_on_punnycode_replacement.py -d example.com -a none -o /tmp/fichier_de_resultat
```

### Exemple de résultat
```
(NOM_ENVIRONNEMENT_VIRTUEL) [user@host phishing_finder]$ ./110_check_for_name_on_punnycode_replacement.py -d example.com
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

## Script `000_create_cache.py`
### Lancement
Ce script est destiné à générer le fichier de cache contenant les associations entre un `tld` et le serveur de `whois` associé. Plusieurs paramètres peuvent être utilisés conjointement pour réaliser les opérations souhaitées : 
  * `--help` est le paramètre principal correspondant à la documentation du script : 
```
usage: 000_create_cache.py [-h] [-c CACHE]

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

## Script `100_check_for_name_on_each_tld.py`
### Lancement
Plusieurs paramètres peuvent être utilisés conjointement pour réaliser les opérations souhaitées : 
  * `--help` est le paramètre principal correspondant à la documentation du script : 
```
usage: 100_check_for_name_on_each_tld.py [-h] -n NAME [-a ADAPTER] [-o OUTPUT]
                                 [--no-cache] [--cache-file CACHE_FILE]

Génération de tout plein de noms de domaines potentiels pour surveiller le
phishing.

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Nom à surveiller (Option duplicable 1 fois par nom).
  -a ADAPTER, --adapter ADAPTER
                        Adapteur à utiliser pour réaliser la résolution DNS.
  -o OUTPUT, --output OUTPUT
                        Emplacement du rapport.
  --no-cache            Activer ce booléen pour ne pas utiliser le dossier de
                        cache.
  --cache-file CACHE_FILE
                        Fichier de cache.
```
  * `--name` ou `-n` permet d'indiquer la marque pour laquelle on veut tester tous les TLDs obtenus dans la liste IANA. L'option peut se répéter pour surveiller plusieurs marques.
  * `--adapter` ou `-a` correspond à l'adapteur utilisé pour obtenir les informations de déclaration DNS. Trois valeurs sont possibles à ce jour; seules deux sont développées : 
    * `dns`, réalise les requêtes DNS par le biais de la lib `dnspython`. **C'est l'adapteur par défaut**.
    * `none` ne retourne aucune information de déclaration DNS.
    * `web` interroge le résultat du site `http://dnslookup.fr`.
  * `--output` ou `-o` permet d'indiquer l'emplacement du fichier contenant les résultats. `/dev/stdout` par défaut.
  * `--no-cache` est un drapeau permettant d'indiquer au programme de ne pas utiliser son cache mais de récupérer toutes les informations depuis la page web IANA. Positionné à `True` par défaut => **Par défaut on requête plein de fois IANA!!!**
  * `--cache-file` correspond au fichier contenant le cache. Généré par le script `000_create_cache.py`.

