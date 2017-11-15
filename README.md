Plusieurs outils disponibles dans ce dépôt; principalement destinés à l'identification de noms de domaines pouvant entrer en concurrence avec une marque donnée que vous souhaitez protéger.

# Installation
```
python -m venv <NOM_ENVIRONNEMENT_VIRTUEL>
source <NOM_ENVIRONNEMENT_VIRTUEL>/bin/activate
git clone https://github.com/yapoc/phishing_finder.git
cd phishing_finder
pip install -r requirements
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
usage: predict_punny_code_dns_names.py [-h] -d [DOMAINS [DOMAINS ...]]
                                       [-a ADAPTER] [-o [OUTPUT]]
Génération de tout plein de noms de domaines potentiels pour surveiller le
phishing.
optional arguments:
  -h, --help            show this help message and exit
  -d [DOMAINS [DOMAINS ...]], --domains [DOMAINS [DOMAINS ...]]
                        Adresse du domaine ou des domaines à surveiller
                        (séparés par des virgules).
  -a ADAPTER, --adapter ADAPTER
                        Adapteur à utiliser pour réaliser la résolution DNS.
  -o [OUTPUT], --output [OUTPUT]
                        Emplacement du rapport.
```

  * `--domains` correspond à la liste des domaines à interroger, séparés par une virgule. Exemple d'utilisation : 
```
./predict_punny_code_dns_names.py --domains domaine1.tld,domaine2.tld
./predict_punny_code_dns_names.py -d domaine1.tld,domaine2.tld
```

  * `--adapter` correspond à l'adapteur utilisé pour obtenir les informations de déclaration DNS. Trois valeurs sont possibles à ce jour; seules deux sont développées : 
    * `web` interroge le résultat du site `http://dnslookup.fr`. C'est l'adapteur par défaut.
    * `none` ne retourne aucune information de déclaration DNS.
    * `dns`, réalise les requêtes DNS par le biais de la lib `dnspython`.
```
./predict_punny_code_dns_names.py --domains domaine1.tld,domaine2.tld --adapter none
./predict_punny_code_dns_names.py --domains domaine1.tld,domaine2.tld -a none
./predict_punny_code_dns_names.py -d domaine1.tld,domaine2.tld -a none
./predict_punny_code_dns_names.py -d domaine1.tld,domaine2.tld --adapter none
```

  * `--output` permet d'indiquer l'emplacement du fichier contenant les résultats. `/dev/stdout` par défaut.
```
./predict_punny_code_dns_names.py --domains domaine1.tld,domaine2.tld --adapter none --output /tmp/fichier_de_resultat
./predict_punny_code_dns_names.py --domains domaine1.tld,domaine2.tld --adapter none -o /tmp/fichier_de_resultat
./predict_punny_code_dns_names.py --domains domaine1.tld,domaine2.tld -a none --output /tmp/fichier_de_resultat
./predict_punny_code_dns_names.py --domains domaine1.tld,domaine2.tld -a none -o /tmp/fichier_de_resultat
./predict_punny_code_dns_names.py -d domaine1.tld,domaine2.tld --adapter none --output /tmp/fichier_de_resultat
./predict_punny_code_dns_names.py -d domaine1.tld,domaine2.tld --adapter none -o /tmp/fichier_de_resultat
./predict_punny_code_dns_names.py -d domaine1.tld,domaine2.tld -a none --output /tmp/fichier_de_resultat
./predict_punny_code_dns_names.py -d domaine1.tld,domaine2.tld -a none -o /tmp/fichier_de_resultat
```

### Exemple de résultat
```
(NOM_ENVIRONNEMENT_VIRTUEL) [user@host phishing_finder]$ ./predict_punny_code_dns_names.py --domains example.com --adapter web
+----------------------------------+------------------------------------------+----------------------------------+-----------------+
| Domaine                          |                       Encodage PunnyCode |                   Encodage UTF-8 |        Réservé? |
+----------------------------------+------------------------------------------+----------------------------------+-----------------+
| example.com                      |                              example.com |                      example.com |   93.184.216.34 |
| example.com                      |                       xn--exampl-uva.com |                      examplë.com | dispo à l'achat |
| example.com                      |                       xn--exampl-8ua.com |                      examplè.com | dispo à l'achat |
8<...>8
+----------------------------------+------------------------------------------+----------------------------------+-----------------+
```
