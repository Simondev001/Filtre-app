# 🖼️ Mini-App de Traitement d'Images

Une application de bureau interactive conçue en **Python** avec **Tkinter** et **Pillow**. Elle propose une interface simple pour appliquer des filtres d'images (linéaires et non linéaires) et des algorithmes de détection de contours, avec un affichage comparatif en temps réel.

---

## 📋 Table des Matières
* [🚀 Installation et Lancement](#-installation-et-lancement)
* [📁 Structure du Projet](#-structure-du-projet)
* [👥 Répartition des Tâches](#-répartition-des-tâches)
* [💻 Guide d'Intégration (Développeurs)](#-guide-dintégration-développeurs)

---

## 🚀 Installation et Lancement

### Prérequis
* **Python 3.8+** installé sur votre système.

### Étapes de démarrage

1. **Cloner ou télécharger le projet** :
   ```bash
   git clone <url-du-depot>
   cd <nom-du-dossier>


1- Créer l'environnement virtuel :
     ```bash
     
      python -m venv env

2-Activer l'environnement virtuel :
       ```bash
     
      Windows (CMD) : env\Scripts\activate 


3-Installer la bibliothèque Pillow :
     ```bash
     
      Windows (CMD) : env\Scripts\activate 

4-Exécuter l'application :
python app.py


##📁 Structure du Projet
** L'application repose sur une architecture centralisée dans app.py facilitant l'intégration modulaire :
  bash

      ├── app.py                     # Code principal (GUI & Logique)
      ├── env/                       # Environnement virtuel (exclu du commit)
      └── README.md                  # Documentation du proj



Méthodes clés de la classe MiniImageApp :

create_menu() : Configure la barre supérieure (File, Filtres, Contour).

create_layout() : Gère l'affichage double (Image originale à gauche, Résultats à droite).

upload_image() : Gère le chargement et la mise à l'échelle des images importées.

display_single_result() : Gère le rafraîchissement de la zone de droite pour afficher le rendu final.


Guide d'Intégration (Développeurs)
[!IMPORTANT]
Pour garantir la stabilité de la branche principale, veuillez créer vos propres branches de travail (feature-filtres ou feature-contours) et ne travailler que sur vos méthodes dédiées.
Comment ajouter votre filtre pas-à-pas :
1. Déclarer l'option dans le menu (create_menu)
Ajoutez votre bouton de menu dans la fonction create_menu() en le reliant à votre future méthode.


   ```bash
   Exemple pour l'Étudiant A (Filtres)
   filters_menu.add_command(label="Filtre de Nagao", command=self.apply_filter_nagao)

   # Exemple pour l'Étudiant B (Contours)
   contour_menu.add_command(label="Filtre de Sobel", command=self.apply_sobel)
   

2. Créer la méthode de traitement correspondante
   
Ajoutez votre méthode à la fin de la classe MiniImageApp dans app.py. Respectez la structure suivante :

  ```bash
    def apply_sobel(self):
    # 1. Vérification de la présence d'une image chargée
    if self.original_pil_image is None:
        messagebox.showwarning("Attention", "Veuillez d'abord charger une image.")
        return
    
    # 2. Logique de traitement (ex: conversion et filtrage)
    image_en_gris = self.original_pil_image.convert("L")
    image_traitee = image_en_gris.filter(ImageFilter.FIND_EDGES) # Remplacez par votre algorithme
    
    # 3. Envoi du résultat à la zone d'affichage
    self.display_single_result(image_traitee, title="Contours - Sobel")
