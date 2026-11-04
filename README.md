# LycéeConnect — Incident de sécurité (V7)

Challenge Web d'initiation « débutant+ » pour Mars@Hack.

## Lancement

Le vrai flag n'est plus stocké dans le code source ni dans `docker-compose.yml`.
Il est injecté au lancement depuis `.env`.

1. Ouvre le fichier `.env`.
2. Renseigne ton flag :

```dotenv
FLAG=MARS{ton_flag_ici}
```

3. Lance le challenge :

```bash
docker compose up --build -d
```

4. Ouvre :

`http://localhost:8080`

### Compte joueur

- Identifiant : `eleve`
- Mot de passe : `rentree2026`

## Important

- Ne distribue pas `.env` aux joueurs ou aux IA chargées de valider le challenge en black-box.
- `.env` est ignoré par Git grâce à `.gitignore`.
- L'application utilise désormais `os.environ["FLAG"]` : il n'existe aucun flag de secours dans `app.py`.
- Docker Compose refuse de démarrer si `FLAG` ou `SECRET_KEY` sont absents ou vides.

## Validation recommandée

Pour tester réellement la difficulté, donne uniquement :

- l'URL du challenge ;
- `eleve` / `rentree2026` ;
- l'énoncé joueur.

Ne fournis ni le code source, ni `.env`, ni le write-up organisateur.

## Vulnérabilité pédagogique

Broken Access Control / IDOR. Le portail est volontairement vulnérable et doit être déployé dans un environnement isolé.
