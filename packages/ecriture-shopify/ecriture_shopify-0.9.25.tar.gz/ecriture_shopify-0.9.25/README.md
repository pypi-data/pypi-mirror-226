# Ecriture-Shopify
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/:packageName)
![PyPI - License](https://img.shields.io/pypi/l/:ecriture-shopify)
<!-- test passed ? tests cov -->
<!-- licence -->

Génère une écriture comptable à partir d'un extrait mensuel de Shopify.<br>Avec notamment le calcul de la TVA en fonction des ventes dans les différents pays en UE.<br><br>
Le coeur du traitement est en Pandas/XlsxWriter avec l'aide de Loguru pour la partie log.

## Fonctionnement
La fonction principale du package est _"main_shopify"_. Cette fonction encapsule le pipeline complet pour créer une écriture comptable à partir du fichier xlsx mensuel de Shopify. Le pipeline est composé de 3 étapes majeures:
* chargement et nettoyage du fichier d'entrée
* si ok, application de la TVA et génération de l'écriture comptable
* création du fichier de sortie xlsx avec une mise en forme propre

<u>Explication de la fonction</u><br>
_"main_shopify"_ prend en argument le path du fichier d'entrée, et le path du (futur) fichier de sortie. La fonction génère et enregistre le fichier d'écriture comptable dans ce dernier et émet un booléen pour indiquer si la génération à fonctionner.

<u>Code:</u><br>
```python
from ecriture_shopify.main import main_shopify
status = main_shopify(input_file_path, output_file_path)
```

<u>Définition des arguments </u>:
* `input_file_path`: str, path du fichier d'entrée
* `output_file_path`: str, path du fichier de sortie
* `status`: bool, _True_ si génération ok, _False_ sinon



## A propos
Le projet est mené avec Poetry, Black, isort, Pytest et pre-commit. Voir "pyproject.toml" pour la liste comptète.

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)<br>


## Auteur:
michel padovani

## Licence
License "GNU General Public License v3.0 or later".
Voir [LICENSE](https://github.com/michelpado/ecriture-shopify/blob/master/LICENSE)
