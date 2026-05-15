# Cahier des charges - Farm2Door

## Page de garde

**Projet :** Farm2Door  
**Type :** Projet de Fin d'Annee  
**Domaine :** Marketplace agricole locale  
**Technologies :** Django, Python, SQLite, HTML, CSS  
**Version :** 1.0  

---

## 1. Introduction

Farm2Door est une application web qui met en relation les agriculteurs locaux et les clients. L'objectif principal est de faciliter la vente directe des produits agricoles frais, sans intermediaire complique, avec une experience simple pour le client et un espace de gestion pratique pour l'agriculteur.

Le projet permet aux clients de consulter les produits disponibles, ajouter des articles au panier, choisir un mode de paiement, finaliser une commande et telecharger un bon d'achat PDF. Les agriculteurs peuvent publier leurs produits, gerer les prix, les stocks, les images, consulter les commandes recues et suivre leurs ventes. L'administrateur dispose d'un espace de suivi global.

---

## 2. Contexte du projet

Les petits producteurs agricoles rencontrent souvent des difficultes pour vendre leurs produits directement aux consommateurs. De leur cote, les clients cherchent une solution simple pour acceder a des produits frais, connaitre les prix, verifier la disponibilite et passer commande rapidement.

Farm2Door repond a ce besoin en proposant une plateforme locale de vente directe. Le projet simule un fonctionnement professionnel avec catalogue, panier, paiement, bon d'achat, dashboard farmer et dashboard admin.

---

## 3. Problematique

Comment creer une application web simple et efficace permettant :

- aux agriculteurs de publier et gerer leurs produits ;
- aux clients de commander des produits frais facilement ;
- a l'administrateur de suivre l'activite de la plateforme ;
- de generer une preuve d'achat claire apres chaque commande.

---

## 4. Objectifs du projet

### Objectif general

Developper une application web nommee Farm2Door permettant la vente directe de produits agricoles entre agriculteurs et clients.

### Objectifs specifiques

- Creer une page d'accueil claire et professionnelle.
- Afficher un catalogue de produits agricoles.
- Permettre l'inscription et la connexion des utilisateurs.
- Gerer deux roles principaux : client et agriculteur.
- Permettre aux agriculteurs d'ajouter, modifier et supprimer des produits.
- Permettre aux clients de gerer un panier.
- Ajouter une etape de paiement simule.
- Generer un bon d'achat PDF apres finalisation.
- Mettre a jour le stock apres chaque commande.
- Fournir un historique des commandes au client.
- Fournir un suivi des commandes recues a l'agriculteur.
- Fournir un tableau de bord admin.

---

## 5. Perimetre du projet

### Inclus dans le projet

- Application web Django.
- Gestion des utilisateurs.
- Gestion des produits.
- Gestion des images produits.
- Gestion du panier.
- Validation des commandes.
- Paiement simule.
- Generation de bon d'achat PDF.
- Dashboard client.
- Dashboard agriculteur.
- Dashboard administrateur.
- Interface admin Django pour gerer les donnees.

### Non inclus dans cette version

- Paiement bancaire reel.
- Livraison avec suivi GPS.
- Notifications SMS ou email.
- Application mobile native.
- Systeme d'avis clients.
- Gestion avancee des categories.

---

## 6. Acteurs du systeme

### Client

Le client est un utilisateur qui consulte les produits disponibles, ajoute des produits au panier, choisit un mode de paiement et finalise une commande. Il peut aussi consulter l'historique de ses commandes et telecharger ses bons d'achat.

### Agriculteur

L'agriculteur est un utilisateur qui publie ses produits sur la plateforme. Il peut ajouter un produit avec nom, prix, stock et image. Il peut modifier ou supprimer ses produits, consulter les commandes recues et suivre ses revenus.

### Administrateur

L'administrateur gere la plateforme depuis l'espace admin. Il peut consulter les utilisateurs, produits, commandes, revenus et profils. Il peut aussi ajouter ou modifier des produits directement depuis l'administration Django.

---

## 7. Besoins fonctionnels

### 7.1 Authentification

L'application doit permettre :

- la creation d'un compte ;
- le choix du role client ou agriculteur ;
- la connexion ;
- la deconnexion ;
- la protection des pages reservees aux utilisateurs connectes.

### 7.2 Gestion des produits

L'application doit permettre :

- l'affichage des produits sur la page d'accueil ;
- l'affichage de tous les produits dans le catalogue ;
- l'ajout d'un produit par un agriculteur ;
- la modification d'un produit par son agriculteur ;
- la suppression d'un produit par son agriculteur ;
- l'ajout d'une image produit ;
- la gestion du stock.

### 7.3 Panier

L'application doit permettre :

- l'ajout d'un produit au panier ;
- l'augmentation de la quantite ;
- la diminution de la quantite ;
- la suppression d'un produit du panier ;
- le calcul du total ;
- la verification du stock disponible.

### 7.4 Paiement

L'application doit permettre deux modes de paiement :

- paiement a la livraison ;
- paiement par carte bancaire simule.

Si l'utilisateur choisit le paiement par carte, il doit remplir :

- le nom sur la carte ;
- le numero de carte ;
- la date d'expiration ;
- le code CVC.

Le paiement par carte est simule pour les besoins du PFA. Aucun vrai paiement bancaire n'est effectue.

### 7.5 Commandes

L'application doit permettre :

- la creation d'une commande apres paiement ;
- l'enregistrement des produits commandes ;
- la mise a jour automatique du stock ;
- l'affichage d'une page de confirmation ;
- l'historique des commandes du client ;
- l'affichage des commandes recues pour l'agriculteur.

### 7.6 Bon d'achat PDF

Apres finalisation de la commande, l'application doit generer un bon d'achat PDF contenant :

- le nom de la plateforme ;
- le numero de commande ;
- le nom du client ;
- la date de commande ;
- le mode de paiement ;
- le statut du paiement ;
- la liste des produits ;
- la quantite ;
- le prix unitaire ;
- le total par produit ;
- le total general.

Le bon d'achat doit etre telechargeable depuis :

- la page de confirmation ;
- l'historique des commandes client ;
- l'espace admin ;
- l'espace commandes recues de l'agriculteur.

### 7.7 Dashboard client

Le client doit disposer d'un espace affichant :

- ses commandes ;
- le total depense ;
- le nombre de commandes payees ;
- le nombre de paiements en attente ;
- le lien de telechargement du bon PDF.

### 7.8 Dashboard agriculteur

L'agriculteur doit disposer d'un espace affichant :

- le nombre de produits ;
- le nombre de commandes ;
- les revenus ;
- le produit le plus vendu ;
- les alertes de stock faible ;
- la liste de ses produits ;
- les actions modifier et supprimer ;
- les commandes recues.

### 7.9 Dashboard administrateur

L'administrateur doit disposer d'un tableau de bord affichant :

- le nombre total d'utilisateurs ;
- le nombre d'agriculteurs ;
- le nombre de clients ;
- le nombre de produits ;
- le nombre de commandes ;
- le revenu total ;
- les dernieres commandes ;
- les bons d'achat PDF.

---

## 8. Besoins non fonctionnels

### Simplicite

L'interface doit etre claire, lisible et facile a utiliser pour un client ou un agriculteur.

### Ergonomie

Les pages principales doivent etre accessibles depuis la barre de navigation. Les boutons doivent etre visibles et les actions importantes doivent etre simples.

### Securite

Les pages reservees doivent etre protegees :

- seul un utilisateur connecte peut finaliser une commande ;
- seul un agriculteur peut acceder a son dashboard ;
- seul l'agriculteur proprietaire peut modifier ses produits ;
- seul l'administrateur peut acceder au dashboard admin ;
- un bon d'achat PDF ne doit etre accessible qu'au client concerne, a l'agriculteur concerne ou a l'admin.

### Performance

L'application doit charger rapidement avec SQLite pour un contexte de PFA et de demonstration locale.

### Maintenabilite

Le code doit etre organise selon la structure Django :

- models ;
- views ;
- urls ;
- templates ;
- static ;
- migrations ;
- management commands.

---

## 9. Technologies utilisees

### Backend

- Python
- Django
- SQLite

### Frontend

- HTML
- CSS
- Templates Django

### Fichiers statiques et media

- CSS dans le dossier static ;
- images produits dans le dossier media ;
- configuration MEDIA_URL et MEDIA_ROOT pour afficher les photos.

### Administration

- Django Admin pour gerer les utilisateurs, produits, commandes, profils et lignes de commande.

---

## 10. Structure principale de l'application

### Pages principales

- Accueil : presentation et produits recents.
- Catalogue : liste des produits.
- Comment ca marche : explication du parcours.
- Inscription : creation du compte.
- Connexion : authentification.
- Panier : gestion des produits choisis.
- Paiement : choix du mode de paiement.
- Confirmation : commande validee et bon PDF.
- Mes commandes : historique client.
- Espace farmer : gestion produits et statistiques.
- Commandes recues : suivi des ventes farmer.
- Admin dashboard : suivi global.
- Admin Django : gestion directe des donnees.

### Modeles principaux

- Profile : role de l'utilisateur.
- Product : produit agricole.
- Order : commande.
- OrderItem : produit commande avec quantite.

---

## 11. Regles de gestion

- Un produit appartient a un agriculteur.
- Un client peut passer plusieurs commandes.
- Une commande contient plusieurs lignes de commande.
- Le stock diminue apres validation de la commande.
- Le paiement par carte marque la commande comme payee.
- Le paiement a la livraison marque la commande comme en attente.
- Le bon d'achat est genere apres finalisation de la commande.
- Un agriculteur ne peut gerer que ses propres produits.
- Un utilisateur non connecte ne peut pas finaliser une commande.

---

## 12. Donnees de demonstration

Une commande Django `seed_demo` permet de creer rapidement des donnees de test :

- Admin : `admin` / `admin123`
- Agriculteur : `farmer` / `farmer123`
- Client : `client` / `client123`

Elle cree aussi quelques produits de demonstration afin de tester rapidement l'application.

---

## 13. Contraintes

- Le projet doit fonctionner localement.
- La base utilise SQLite.
- Le paiement est uniquement simule.
- Le bon PDF est genere sans dependance externe.
- Le projet doit rester simple a presenter et a expliquer.

---

## 14. Planning previsionnel

### Phase 1 : Analyse

- Definition du sujet.
- Identification des acteurs.
- Identification des besoins.

### Phase 2 : Conception

- Choix de Django.
- Creation des modeles.
- Organisation des pages.
- Preparation du parcours client et farmer.

### Phase 3 : Developpement

- Authentification.
- Catalogue produits.
- Gestion panier.
- Gestion commandes.
- Paiement simule.
- Bon d'achat PDF.
- Dashboards.
- Admin Django.

### Phase 4 : Tests

- Test inscription et connexion.
- Test ajout produit.
- Test panier.
- Test paiement.
- Test generation PDF.
- Test dashboards.

### Phase 5 : Finalisation

- Amelioration de l'interface.
- Redaction du rapport.
- Preparation de la demonstration.

---

## 15. Tests a effectuer

- Creer un compte client.
- Creer un compte agriculteur.
- Ajouter un produit avec image.
- Modifier un produit.
- Supprimer un produit.
- Ajouter un produit au panier.
- Modifier les quantites du panier.
- Finaliser une commande avec paiement a la livraison.
- Finaliser une commande avec paiement par carte simule.
- Telecharger le bon d'achat PDF.
- Verifier la baisse du stock.
- Verifier l'historique client.
- Verifier les commandes recues farmer.
- Verifier le dashboard admin.

---

## 16. Conclusion

Farm2Door est une application web complete pour un PFA de marketplace agricole locale. Elle propose un parcours coherent depuis la publication des produits jusqu'a la commande et la generation du bon d'achat PDF.

Le projet met en valeur plusieurs competences : developpement web avec Django, gestion de base de donnees, authentification, gestion des roles, panier, paiement simule, generation de PDF, interface admin et tableaux de bord.

Des ameliorations futures peuvent etre ajoutees, comme le paiement reel, les notifications, les categories, les avis clients, le suivi de livraison et une application mobile.
