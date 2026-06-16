# Mémoire Éthique — Clonage Vocal et Détection de Deepfakes Audio

## 1. Introduction

Ce projet explore deux faces complémentaires d'une même technologie : la **génération** de voix synthétiques par clonage (avec XTTS-v2) et la **détection** de voix synthétiques (avec des embeddings WavLM).

L'objectif n'est pas de produire un outil de clonage vocal « prêt à l'emploi », mais de comprendre **comment** ces technologies fonctionnent, **quels risques** elles posent, et **quelles contre-mesures** peuvent être mises en place — à la fois techniques (détection automatique) et organisationnelles (charte d'usage, consentement, transparence).

Ce document présente :
- le contexte technique du projet,
- les risques identifiés liés aux deepfakes vocaux,
- les solutions et limites des approches de détection,
- notre approche éthique pour ce projet, et les usages que nous excluons explicitement.

## 2. Contexte technique

### 2.1 Génération : clonage vocal avec XTTS-v2

XTTS-v2 (Coqui) est un modèle de synthèse vocale multilingue capable de cloner une voix à partir de quelques secondes d'enregistrement audio de référence (*speaker embedding*), puis de générer n'importe quel texte avec le timbre de cette voix.

Concrètement, dans `src/generator.py`, la classe `VoiceGenerator` :
1. charge un échantillon audio de référence (`data/voice_ref/`),
2. extrait les caractéristiques vocales du locuteur,
3. synthétise un nouveau texte avec ces caractéristiques,
4. enregistre le résultat dans `data/generated/`.

### 2.2 Détection : embeddings WavLM

WavLM (`microsoft/wavlm-base-plus-sd`) est un modèle pré-entraîné qui transforme un signal audio en un vecteur numérique (*embedding*) représentant ses caractéristiques acoustiques et vocales.

Dans `src/detector.py`, la classe `DeepfakeDetector` :
1. extrait un embedding pour l'audio de référence et pour l'audio à tester,
2. calcule la **similarité cosinus** entre les deux vecteurs,
3. compare cette similarité à un seuil (`threshold`),
4. retourne un verdict (`REAL` / `DEEPFAKE`) et un niveau de confiance.

Cette approche est volontairement simple et pédagogique : elle illustre le principe général de la détection par embeddings, mais **n'est pas un détecteur de niveau industriel** (voir section 4.3).

## 3. Risques liés aux deepfakes vocaux

### 3.1 Fraude et ingénierie sociale
Un clone vocal peut être utilisé pour se faire passer pour une personne réelle auprès de sa famille, de ses collègues ou de sa banque (« arnaque au président », faux appels d'urgence, contournement de l'authentification vocale).

### 3.2 Désinformation et manipulation de l'opinion
Des extraits audio truqués de personnalités publiques (responsables politiques, journalistes, dirigeants) peuvent être diffusés pour propager de fausses déclarations, avec un impact sur l'opinion publique ou les marchés financiers.

### 3.3 Atteinte au consentement et à l'image de la personne
Cloner la voix d'une personne sans son accord constitue une atteinte à son droit à l'image et à sa vie privée, indépendamment de l'usage qui en est fait ensuite.

### 3.4 Érosion générale de la confiance
À mesure que les deepfakes audio se banalisent, le doute s'installe sur **tous** les enregistrements audio — y compris les authentiques —, ce qui peut être exploité pour décrédibiliser des preuves réelles (« effet de dilution de la vérité »).

### 3.5 Limites juridiques et techniques actuelles
- Le cadre légal autour de la voix synthétique reste flou dans de nombreux pays.
- Les détecteurs actuels (y compris le nôtre) ne sont pas infaillibles et peuvent être contournés par des modèles de génération plus récents.

## 4. Solutions et bonnes pratiques

### 4.1 Solutions techniques
- **Détection automatique** par embeddings/classification (notre approche), idéalement combinée avec plusieurs modèles complémentaires.
- **Watermarking audio** : intégrer une signature inaudible dans les audios générés par IA, pour permettre leur identification ultérieure.
- **Traçabilité** : conserver des métadonnées sur l'origine d'un audio généré (modèle utilisé, date, consentement).

### 4.2 Solutions organisationnelles
- **Consentement explicite** de la personne dont la voix est clonée, avant toute génération.
- **Marquage clair** de tout contenu généré par IA (« Cet audio a été généré artificiellement »).
- **Charte d'usage** définissant les usages autorisés et interdits (voir `Charte_Usage.md`).
- **Sensibilisation** du public aux risques et aux signes d'un deepfake audio.

### 4.3 Limites de notre détecteur
Notre `DeepfakeDetector` repose sur une comparaison de similarité d'embeddings WavLM avec un seuil fixe. Cette approche a des limites importantes :
- Elle compare une voix de **référence** à une voix de **test** — elle ne peut pas détecter un deepfake sans disposer d'un échantillon authentique de la personne ciblée.
- Le seuil de décision est arbitraire et devrait être calibré sur un grand jeu de données (ex. ASVspoof) plutôt que choisi empiriquement.
- Les modèles de génération les plus récents (dont XTTS-v2 lui-même) produisent des voix de plus en plus proches de l'original, ce qui réduit la marge de détection.
- Le détecteur ne « comprend » pas le contenu audio : il ne détecte que des différences de signature acoustique, pas de cohérence sémantique.

## 5. Notre approche pour ce projet

Dans le cadre de ce projet pédagogique, nous nous engageons à :

1. **N'utiliser que nos propres voix** (ou des voix avec consentement explicite et documenté) comme échantillons de référence.
2. **Marquer systématiquement** les audios générés (nom de fichier, mention dans l'interface) comme étant produits par IA.
3. **Présenter le détecteur comme un outil pédagogique**, avec ses limites clairement énoncées dans l'interface Streamlit (section « Info & Éthique »).
4. **Ne jamais diffuser publiquement** d'audio cloné sans accord de la personne concernée, ni l'utiliser pour usurper une identité, même à titre de démonstration.
5. **Documenter les risques** (cette page) et les règles d'usage (`Charte_Usage.md`) de façon visible pour tout utilisateur du projet.

## 6. Conclusion

Le clonage vocal et sa détection sont deux faces d'une même course technologique : plus les modèles génératifs progressent, plus les détecteurs doivent évoluer pour suivre. Ce projet ne prétend pas résoudre ce problème, mais vise à le **rendre concret et compréhensible** : voir comment une voix peut être clonée, comment on peut tenter de la détecter, et pourquoi un cadre d'usage responsable (consentement, transparence, traçabilité) reste indispensable, quelle que soit la performance technique des outils.
