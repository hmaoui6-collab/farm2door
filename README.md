# Farm2Door

Farm2Door est une application web Django pour la vente de produits agricoles entre agriculteurs et clients.

## Fonctionnalites

- Inscription et connexion des utilisateurs
- Espace client avec catalogue, panier et commandes
- Espace agriculteur pour gerer les produits et les commandes
- Tableau de bord administrateur
- Images de produits de demonstration

## Installation

1. Creer et activer un environnement virtuel Python.
2. Installer les dependances :

```bash
pip install -r requirements.txt
```

3. Preparer la base de donnees et les donnees de demonstration :

```bash
python manage.py migrate
python manage.py setup_abdellah_admin
python manage.py fix_product_images
```

Sur Windows, le fichier `preparer_farm2door.bat` lance ces commandes automatiquement.

## Lancement

```bash
python manage.py runserver
```

Puis ouvrir :

```text
http://127.0.0.1:8000/
```

## Comptes de demonstration

- Administrateur : `abdellah` / `Anomaly123`
- Agriculteur : `farmer` / `farmer123`

## Technologies

- Python
- Django
- SQLite
- HTML / CSS
