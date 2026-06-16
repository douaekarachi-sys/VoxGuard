# Charte d'Usage — Projet Clonage Vocal & Détection de Deepfakes

Cette charte définit les règles d'utilisation de cet outil. Elle s'adresse à toute personne utilisant le générateur de voix (`src/generator.py`) et/ou le détecteur (`src/detector.py`), via le code ou l'interface Streamlit (`app.py`).

## 1. Principes

1. **Consentement avant tout** : aucune voix ne peut être clonée sans l'accord explicite et éclairé de la personne concernée.
2. **Transparence** : tout audio généré par ce système doit être identifié comme tel auprès de toute personne susceptible de l'entendre.
3. **Finalité pédagogique** : cet outil est conçu pour comprendre et démontrer les mécanismes de génération et de détection de voix synthétiques, pas pour produire des contenus destinés à un usage réel.
4. **Traçabilité** : conserver une trace (qui, quoi, pourquoi) de chaque audio généré dans le cadre du projet.
5. **Responsabilité individuelle** : la personne qui utilise l'outil est responsable de l'usage qu'elle en fait.

## 2. Usages autorisés

- Cloner **sa propre voix** pour tester et démontrer le fonctionnement du générateur.
- Cloner la voix d'un tiers **uniquement** avec son consentement explicite, documenté, et pour une démonstration encadrée (ex. présentation de projet).
- Utiliser le détecteur pour analyser des audios générés dans le cadre de ce projet, ou des jeux de données publics destinés à la recherche (ex. ASVspoof).
- Présenter, expliquer et faire écouter des exemples générés dans un cadre éducatif, en précisant systématiquement leur origine artificielle.

## 3. Usages strictement interdits

- ❌ Cloner la voix d'une personne **sans son consentement**, qu'elle soit publique ou privée.
- ❌ Utiliser un audio généré pour **usurper l'identité** d'une personne (appels, messages vocaux, réseaux sociaux, etc.).
- ❌ Diffuser un audio généré **sans indiquer** qu'il s'agit d'un contenu produit par IA.
- ❌ Utiliser l'outil pour produire des contenus **diffamatoires, trompeurs, harcelants ou frauduleux**.
- ❌ Utiliser l'outil pour contourner des systèmes d'**authentification vocale** ou tromper un tiers (banque, support technique, proche, etc.).
- ❌ Partager publiquement des audios clonés de personnalités, journalistes, responsables politiques ou toute personne tierce, même « pour rire ».

## 4. Bonnes pratiques recommandées

- Toujours nommer les fichiers générés de façon explicite (ex. préfixe `ia_` ou `clone_`) pour éviter toute confusion avec un enregistrement réel.
- Ajouter une mention audio ou visuelle (« Ceci est une voix générée par IA ») lors de toute présentation.
- Supprimer les échantillons de référence et les audios générés après usage si la personne concernée le demande.
- Garder à l'esprit que le détecteur fourni est un **outil pédagogique**, pas une preuve juridique d'authenticité.

## 5. Avertissement

Cet outil est fourni dans un cadre **strictement éducatif**. Les auteurs du projet déclinent toute responsabilité pour un usage contraire à cette charte. En utilisant ce projet, vous acceptez de respecter les principes énoncés ci-dessus.
