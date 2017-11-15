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
    * `web` interroge le résultat du site `http://dnslookup.fr`. C'est l'adapteur par défaut.
    * `none` ne retourne aucune information de déclaration DNS.
    * `dns`, réalise les requêtes DNS par le biais de la lib `dnspython`.
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
(NOM_ENVIRONNEMENT_VIRTUEL) [user@host phishing_finder]$ ./predict_punny_code_dns_names.py -d example.com -a dns

+----------------------------------+------------------------------------------+----------------------------------+-----------------+
| Domaine                          |                       Encodage PunnyCode |                   Encodage UTF-8 |        Réservé? |
+----------------------------------+------------------------------------------+----------------------------------+-----------------+
| example.com                      |                              example.com |                      example.com |   93.184.216.34 |
| example.com                      |                       xn--exampl-uva.com |                      examplë.com | dispo à l'achat |
| example.com                      |                       xn--exampl-8ua.com |                      examplè.com | dispo à l'achat |
|                                                           8<...>8                                                                |
| example.com                      |                      xn--exarnpl-hya.com |                     exarnplé.com | dispo à l'achat |
| example.com                      |                       xn--exmple-cua.com |                      exämple.com |   85.13.149.201 |
| example.com                      |                      xn--exmpl-hra6c.com |                      exämplë.com | dispo à l'achat |
| example.com                      |                      xn--exmpl-hra5a.com |                      exämplè.com | dispo à l'achat |
|                                                           8<...>8                                                                |
+----------------------------------+------------------------------------------+----------------------------------+-----------------+
```
