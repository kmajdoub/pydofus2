# Changelog Mise à Jour (Update Log)

## 16.01.2024

Répositories Mise à Jour: Post-mise à jour, actualisation des dépôts.
Nouveau Outil d'Extraction de Données: Intégration d'ankalauncher hackerino pour l'extraction de données des comptes via le launcher.

## 18.01.2024

Ajout d'une Application Flask: Déploiement d'une application Flask basique sous le répertoire app. Appel aux contributeurs frontend pour enrichir l'application avec des fonctionnalités telles que la gestion de formulaires de lancement, la création de chemins, et un bouton d'import de comptes depuis le launcher. L'application est actuellement à un stade rudimentaire.
Traduction des Modules de Statistiques: Début de la traduction des modules pour la collecte de statistiques de jeu, visant à contourner la détection de bots par Ankama.

## 21.01.2024

Import de Comptes via Launcher: Implémentation d'un bouton pour l'import de comptes depuis le launcher dans l'application.
Progression sur les Modules de Statistiques: Avancement significatif dans l'implémentation des modules de collecte de statistiques.
Diverses Corrections: Apport de multiples corrections à travers le projet.
Amélioration Anti-Ban pour Bots: Nécessité d'intégrer l'envoi de statistiques et la signature des appels API avec cookies pour réduire les bannissements.

## 22.01.2024

Mise à Jour de l'Interface de Sniffing: Introduction d'un bouton toggle start/stop et d'une option de suppression des messages. Le premier onglet est désormais sélectionné automatiquement.

## 17.03.2024

Système de Mimic d'Envoi de Stats: Travail continu sur l'amélioration du système d'imitation de l'envoi de statistiques.
Mise à Jour de l'Interface de Sniffing: Légers ajustements de forme.
Expansion de l'API Haapi: Ajout d'endpoints et gestion des cookies dans Haapi.
Tests de Détection de Bots: Les tests indiquent une réduction des détections de bots, grâce à l'intégration des envois d'événements.

## 19.03.2024

Introduction de Latences: Ajout de délais entre certains envois de messages pour mimiquer le comportement humain.
Module Simulant le Launcher: Développement de ZaapDecoy.
Améliorations sur AccountManager: Optimisation de la fonctionnalité de récupération de personnages.
Envoi d'Événements lors de l'Usage de Raccourcis: Les bots émettent désormais des événements lors de l'utilisation de raccourcis en combat ou en déplacement.
Réduction des Détections de Bots: Les ajustements actuels semblent réduire significativement la détection des bots par les systèmes automatisés.
Serveur Discord pour le Projet: Création d'un serveur pour rassembler la communauté intéressée.

## 20.03.2024

Amélioration de l'Interface WebUI: Refonte de l'interface du bot manager avec ajout d'une fonctionnalité de lancement de combats et affichage du niveau des bots.
Polling des Logs via SocketIO: Intégration d'un handler custom pour le logger, permettant l'envoi de logs formatés en HTML via SocketIO.
Correction de Bugs: Résolution de problèmes dans les modules autotripUseZaap, Haapi, et dans le cadre de gestion des combats du bot, améliorant la stabilité générale.

## 24.03.2024

- isBasicAccount() is not working correctly
- Farm form added to webui and is stable
- UseSkill works now correctly when the resource is picked by another player
- Treasure hunt haven bag usage was improved and some bugs fixed (still need some work)
- A ban protection that closes launcher before launching the bot was added
- Everything related to thrift server and its types was cleaned from the repo and python dataclasses where used instead for modeling pyd2bot data
- It is now possible to run the bot with custom random paths that parkour a zone defined by a set of mapIds
- Now the bot sends the messages that asks for freindlist, ignored, spouce etc
- CRA config and FECA configs added
- Status route missing from sniffer backend fixed
- usage of pymarshal to validate forms using python schemas was intergrated to the app
- pydofus2 now handles AchievmentList message and store infos about the player achievement
- Readme was updated and install process was simplified, now user defines paths to dofus and its dev directory/logs in env variables
- And much more little bug fixes and enhacements

## 27.03.2024

Mise à jour majeure du dépôt : Des modifications importantes ont été apportées aux modules liés à l'utilisation des sorts pour assurer la compatibilité du client pydofus2 avec la nouvelle version de Dofus.

Interface utilisateur : Le bouton permettant de lancer les différentes activités affiche désormais une erreur si un bot est déjà actif sur le compte concerné.

Améliorations et corrections de bugs :

De nombreuses corrections ont été apportées à la fonctionnalité permettant l'utilisation automatique des zaaps et des havres-sacs pour les déplacements.
Pour lutter contre le système anti-bot, l'utilisation des sorts en combat a été ralentie, et des délais ont été introduits entre les combats.
Une pause obligatoire de 5 minutes entre les chasses aux trésors a été implémentée pour contrecarrer le système anti-bot.
Gestion des montures : Une gestion spécifique pour l'utilisation des montures a été ajoutée, prenant en compte les cas où la monture manque d'énergie.

Fonctionnalité Autotrip : Lorsqu'une destination est spécifiée uniquement par son MapId, Autotrip désormais cherche automatiquement un vertex accessible sur la carte de destination, au lieu de tenter directement le vertex avec zoneId 1.

## 31.03.2024

Auto trip use zaap, maintenant traite les cas particulier et gère le déplacement de Ankarnam vers Astrub correctement, gère aussi maintenant les déplacements de/vers albuera.
Average prices frame maintenant ne demande les données des prix moyens qu'une fois par jour comme le client.
Multiple paths farmer maintenant estime le temps à passer par chemin à partir d'un multiple du cover time et donc s'adapte automatiquement à la taille de votre trajet.
Le bot maintenant prend des pauses de 30 mins après chaque 2h de farme pour s'assimiler plus à un humain et se faire encore moins détecter.
Un paramètre à été ajouté pour contrôler le nombre de fights pat minute que le bot a le droit de faire et ainsi l'adapter plus pour avoir un comportement humain.
La fonctionnalité de combat en group fonctionne de nouveau et s'intégrera prochainement à l'interface graphique.
