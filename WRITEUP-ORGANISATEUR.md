# Write-up organisateur — LycéeConnect V8

## Intention narrative

Le participant incarne **Lucas Martin**, un élève qui décide de chercher seul une faille sur le portail de son lycée.

Il n'est sollicité ni par un enseignant, ni par le club informatique. Le défi n'est **pas affiché dans l'ENT** : il est fourni séparément dans `ENONCE-JOUEUR.md`.

L'interface doit ressembler à un espace scolaire ordinaire. Le joueur doit choisir lui-même de consulter les actualités, d'observer les liens et de recouper les références.

## Solution

1. Se connecter avec `eleve` / `rentree2026`.
2. Consulter **Documents** puis ouvrir le certificat de Lucas : `/document?id=4821`.
3. Remarquer le lien permanent en bas de la page : `/document?ref=SCOL-4821`.
4. Examiner les **Actualités** et relever la référence d'incident `SEC-7314`.
5. Tester `/document?ref=SEC-7314` : le compte élève accède à un rapport interne.
6. Le rapport préliminaire présente trois références :
   - `CFG-8820` : annexe technique sans secret ;
   - `AUDIT-LC-2025-113` : ancien rapport contenant un **faux code expiré** ;
   - `DIR-2026-42` : bordereau de transmission utile.
7. Consulter `/document?ref=DIR-2026-42` et découvrir `AUDIT-LC-9287`.
8. Ouvrir `/document?ref=AUDIT-LC-9287` pour lire le rapport confidentiel de la direction, dont le code de validation provient du `.env`.

## Fausses pistes

- `/robots.txt` renvoie vers `/admin-console` et `/backup-2025` ;
- la console d'administration affiche un `403` réel, sans contournement nécessaire ;
- l'archive 2025 contient un faux flag obsolète ;
- les annonces mentionnent des références de maintenance et de scolarité sans lien avec l'audit final.

## Vulnérabilité

**IDOR / Broken Access Control**. L'application vérifie la connexion de Lucas, mais pas ses droits sur chaque document.

Le flag réel n'est pas dans le dépôt. Il est injecté par la variable `FLAG` via `.env` au démarrage du conteneur.

## Indices pour les lycéens

1. Dans une enquête, une actualité administrative peut contenir une information utile.
2. Un document comporte un numéro, mais également une référence. Observe les liens du portail.
3. Le dossier `SEC-7314` est-il consultable de la même manière qu'un document ?
4. Une annexe technique, un ancien audit et un bordereau de transmission n'ont pas la même utilité.

## Débrief

Le changement d'identifiants ou l'usage de références difficiles à deviner ne remplacent pas une vérification d'autorisation côté serveur.

> Réservé à un environnement de challenge fictif ; ne pas tester un véritable ENT sans autorisation.
