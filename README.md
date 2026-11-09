# LycéeConnect — Une curiosité mal placée (V8)

Challenge Web Mars@Hack — **niveau lycéen / débutant+**.

## Concept

Lucas Martin, élève de Terminale, explore **de sa propre initiative** le portail LycéeConnect de son lycée. Après avoir aperçu une annonce faisant état d'un incident de consultation de documents, il soupçonne un problème de contrôle d'accès.

Aucun professeur ne lui donne de mission. Le site reste un ENT scolaire ordinaire : notes, emploi du temps, documents, actualités, profil.

L'énoncé destiné aux participants est disponible dans `ENONCE-JOUEUR.md`.

## Lancement

Le vrai flag est défini **uniquement par l'organisateur** dans le fichier `.env` (et non dans `app.py`, les templates ou `docker-compose.yml`).

1. Ouvrir `.env`.
2. Renseigner une valeur personnelle :

```dotenv
FLAG=MARS{ton_flag_personnel}
```

3. Démarrer :

```bash
docker compose up --build -d
```

4. Ouvrir `http://localhost:8080`.

Si `.env` n'existe pas, copier `.env.example` vers `.env`, puis renseigner `FLAG` et une valeur aléatoire pour `SECRET_KEY`.

### Vérification après démarrage

```bash
python3 scripts/test_http.py --verbose
```

Ce script contrôle les routes, la connexion, le chemin IDOR, les leurres et l'accès au rapport final **sans afficher le flag réel**.


### Identifiants du joueur

- Utilisateur : `eleve`
- Mot de passe : `rentree2026`

## Mécanique conservée

- Une vulnérabilité IDOR / Broken Access Control sur `/document`.
- Identifiants numériques non séquentiels.
- Références documentaires accessibles avec `?ref=`.
- Une actualité technique évoquant `SEC-7314`.
- Un rapport préliminaire avec trois références, dont deux impasses.
- Un ancien rapport contenant un **faux flag expiré**.
- Des fausses pistes dans `robots.txt`.

## Validation avec d'autres IA

Distribuer uniquement l'énoncé, l'URL et les identifiants. **Ne pas fournir le dépôt**, le `.env` ou `WRITEUP-ORGANISATEUR.md` pour une validation en black-box.

## Sécurité

Application intentionnellement vulnérable et fictive. La déployer dans un environnement de CTF isolé uniquement.
