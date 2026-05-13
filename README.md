# LITRevu

Réseau social de critiques de livres et d'articles.  
Projet 9 — Formation Python RNCP, OpenClassrooms.

## Fonctionnalités

- Inscription et connexion
- Créer des billets (demandes de critique) et des critiques
- Suivre d'autres utilisateurs
- Flux personnalisé : billets et critiques des utilisateurs suivis + les siens
- Un utilisateur ne peut poster qu'une seule critique par billet

## Prérequis

- Python 3.10+

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/hschbonus/pyOCP9.git
cd pyOCP9

# Créer et activer l'environnement virtuel
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/ dans un navigateur.

## Données de test

La base de données `db.sqlite3` est incluse avec des comptes et contenus de démonstration.

## Vérification PEP8

```bash
flake8 .
```
