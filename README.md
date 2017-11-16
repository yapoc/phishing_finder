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

## Script `000_create_cache.py`
### Lancement
Ce script est destiné à générer le fichier de cache contenant les associations entre un `tld` et le serveur de `whois` associé. Plusieurs paramètres peuvent être utilisés conjointement pour réaliser les opérations souhaitées : 
  * `--help` est le paramètre principal correspondant à la documentation du script : 
```
usage: 000_create_cache.py [-h] [--cache-tld-whois CACHE_TLD_WHOIS]

Génération des différents fichiers de cache utilisés par les scripts.

optional arguments:
  -h, --help            show this help message and exit
  --cache-tld-whois CACHE_TLD_WHOIS
                        Emplacement du fichier de cache
```
  * `--cache-tld-whois` : ce paramètre indique l'emplacement du fichier de cache à utiliser. La valeur par défaut est `cache/tld_whois.py`.

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

## Script `120_check_for_name_completed_by_list.py`
Ce script part d'un mot ("example", par exemple) et d'un fichier contenant une liste de mots clefs. Ensuite, il mélange tout et teste la réservation du domaine sur tous les TLDs qu'il connait. 

Par exemple, si : 
  * le mot est `example`, 
  * la liste des mots clefs vaut `[ 'test1', 'test2' ]`

Alors, le script va tester tous les TLDs pour les domaines `['example-test1', 'example-test2', 'example_test1', 'example_test2']`. Si la combinaison est activée, le script va tenter de mélanger tout ça un `combine_times` nombre de fois et va tester les domaines `[ 'example-example-example', 'example-example-test1', 'example-example-test2', 'example-example_example', 'example-example_test1', 'example-example_test2', 8<...>8, 'test2_test1-example', 'test2_test1_example', 'test2_test2-example', 'test2_test2_example' ]`. Compris quelque chose?

### Lancement
  * `--help` est le paramètre principal correspondant à la documentation du script : 
```
usage: 120_check_for_name_completed_by_list.py [-h] -d DOMAIN -wl WORDS_LIST
                                               [-a ADAPTER] [-o OUTPUT] [-c]
                                               [-ct COMBINE_TIMES]
                                               [--no-cache]
                                               [--cache-file CACHE_FILE]
Génération de noms de domaines potentiels sur la base d' mot initial et d'une
liste de mots à ajouter avant, après, pendant, ...
optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domaine d'origine à partir duquel construire la liste
                        des possibles.
  -wl WORDS_LIST, --words-list WORDS_LIST
                        Emplacement du fichier contenant la liste des mots à
                        utiliser pour générer les domaines.
  -a ADAPTER, --adapter ADAPTER
                        Adapteur à utiliser pour réaliser la résolution DNS.
  -o OUTPUT, --output OUTPUT
                        Emplacement du rapport.
  -c, --combine         Activer la combinatoire de tous les mots clefs
                        présents dans le fichier?
  -ct COMBINE_TIMES, --combine-times COMBINE_TIMES
                        Nombre de combinaisons autorisées.
  --no-cache            Activer ce booléen pour ne pas utiliser le dossier de
                        cache.
  --cache-file CACHE_FILE
                        Fichier de cache.
```
  * `--domain` ou `-d` correspond au domaine à interroger. Exemple d'utilisation : 
```
./120_check_for_name_completed_by_list.py --domain example1.com -d example2.com -wl /tmp/file
```
  * `--words-list` ou `-wl` correspond au fichier contenant l'ensemble des mots clefs à utiliser. Le format du fichier doit être de un mot par ligne.
  * `--adapter` ou `-a` correspond à l'adapteur utilisé pour obtenir les informations de déclaration DNS. Trois valeurs sont possibles à ce jour; seules deux sont développées : 
    * `dns`, réalise les requêtes DNS par le biais de la lib `dnspython`. **C'est l'adapteur par défaut**.
    * `none` ne retourne aucune information de déclaration DNS.
    * `web` interroge le résultat du site `http://dnslookup.fr`.

  * `--output` ou `-o` permet d'indiquer l'emplacement du fichier contenant les résultats. `/dev/stdout` par défaut.
  * `-c` ou `--combine` permet d'activer la combinatoire entre les mots. On passe de `[ 'a-b', 'a_b' ]` à `[ 'a-a-a', 'a-a_a', 'a_a-a', ... ]`; bref à plein de mots.
  * `-ct` ou `--combine-times` permet de définir le nombre de combinatoires qu'on veut faire. Attention ça grimpe vite; **3 par défaut**.
  * `--no-cache` est un drapeau permettant d'indiquer au programme de ne pas utiliser son cache mais de récupérer toutes les informations depuis la page web IANA. Positionné à `True` par défaut => **Par défaut on requête plein de fois IANA!!!**
  * `--cache-file` correspond au fichier contenant le cache. Généré par le script `000_create_cache.py`.
