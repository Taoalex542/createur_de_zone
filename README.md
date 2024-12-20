<a name="top"></a>
![language](https://img.shields.io/badge/langage-python-blue)
![OS](https://img.shields.io/badge/OS-linux%2C%20windows%2C%20macOS-0078D4)


## Table of Contents
- [À propos](#-À-propos)
- [Comment installer](#-Comment-installer)

## 🚀 À propos

CETACE (Créateur d'Espaces de Travail À Caractère Éphémère) est un plugin permettant de créer des polygones facilement dans QGIS.

Ce plugin créé des zones dans une couche donnée au préalable en paramètre dans le plugin, il est possible d'utiliser le nom par défaut qui est "zone_plugin_CETACE"

**Maintenabilité Facile**: l'architecture simple du plugin permet une meilleure gestion de la base de code.


[SHREC](https://github.com/Taoalex542/portage-OGRE-QGIS) communique aussi avec le plugin CETACE et  utilise ses zones pour contrôler les géométries, comme avec les zones de réconciliations, permettant de facilement contrôler une zone.


## 📝 Comment installer le plugin sur QGIS

Il existe plusieurs façons d'installer le plugin :

### Installer depuis un fichier zip
- Créez un fichier zip et mettez le dossier CETACE dans ce fichier zip
- Vous devriez avoir un chemin de dossier tel que \CETACE.zip\CETACE
- Allez ensuite dans QGIS, dans le menu extensions, puis installez des extensions depuis un zip et sélectionnez le fichier zip.
- CETACE sera installé

### Installer le plugin manuellement
- Mettez le dossier CETACE dans l'installation des plugins QGIS
- Le chemin est C:\Users\\[nom_utilisateur]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins
- Il suffit ensuite d'activer le plugin dans la fenêtre des extensions de QGIS

[Back to top](#top)
