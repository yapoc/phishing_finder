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
usage: predict_punny_code_dns_names.py [-h] --domain [DOMAIN [DOMAIN ...]]
                                       [--adapter ADAPTER] [--output [OUTPUT]]
Génération de tout plein de noms de domaines potentiels pour surveiller le
phishing.
optional arguments:
  -h, --help            show this help message and exit
  --domain [DOMAIN [DOMAIN ...]]
                        Adresse du domaine à surveiller.
  --adapter ADAPTER     Adapteur à utiliser pour réaliser la résolution DNS.
  --output [OUTPUT]     Emplacement du rapport.
```

  * `--domain` correspond à la liste des domaines à interroger, séparés par un espace. Exemple d'utilisation : 
```
./predict_punny_code_dns_names.py --domain domaine1.tld domaine2.tld
```

  * `--adapter` correspond à l'adapteur utilisé pour obtenir les informations de déclaration DNS. Trois valeurs sont possibles à ce jour; seules deux sont développées : 
    * `web` interroge le résultat du site `http://dnslookup.fr`. C'est l'adapteur par défaut.
    * `none` ne retourne aucune information de déclaration DNS.
    * `dns`, à développer, réalisera les requêtes DNS (`UDP:53`).
```
./predict_punny_code_dns_names.py --domain domaine1.tld domaine2.tld --adapter none
```

  * `--output` permet d'indiquer l'emplacement du fichier contenant les résultats. `/dev/stdout` par défaut.
```
./predict_punny_code_dns_names.py --domain domaine1.tld domaine2.tld --adapter none --output /tmp/fichier_de_resultat
```

### Exemple de résultat
```
(NOM_ENVIRONNEMENT_VIRTUEL) [user@host phishing_finder]$ ./predict_punny_code_dns_names.py --domain example.com --adapter web
+----------------------------------+------------------------------------------+----------------------------------+-----------------+
| Domaine                          |                       Encodage PunnyCode |                   Encodage UTF-8 |        Réservé? |
+----------------------------------+------------------------------------------+----------------------------------+-----------------+
| example.com                      |                              example.com |                      example.com |   93.184.216.34 |
| example.com                      |                       xn--exampl-uva.com |                      examplë.com | dispo à l'achat |
| example.com                      |                       xn--exampl-8ua.com |                      examplè.com | dispo à l'achat |
8<...>8
+----------------------------------+------------------------------------------+----------------------------------+-----------------+
```
