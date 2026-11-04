# Write-up organisateur — LycéeConnect V7

## Configuration du flag

Le flag réel est exclusivement défini par l'organisateur dans `.env` :

```dotenv
FLAG=MARS{valeur_choisie_par_l_organisateur}
```

Il n'est pas présent dans le dépôt applicatif. Dans le rapport final, l'application affiche dynamiquement la valeur de la variable d'environnement `FLAG`.

## Parcours attendu

1. Connexion avec `eleve` / `rentree2026`.
2. Observer le fonctionnement des documents et le lien permanent utilisant `?ref=`.
3. Lire les actualités et relever `SEC-7314`.
4. Accéder à `/document?ref=SEC-7314`.
5. Examiner les trois références :
   - `CFG-8820` : cul-de-sac ;
   - `AUDIT-LC-2025-113` : ancien rapport avec un code expiré ;
   - `DIR-2026-42` : bonne piste.
6. `DIR-2026-42` révèle `AUDIT-LC-9287`.
7. `/document?ref=AUDIT-LC-9287` affiche le flag configuré dans `.env`.

## Fausses pistes

- `/robots.txt` ;
- `/admin-console` → 403 ;
- `/backup-2025` ;
- ancien audit 2025 ;
- références techniques parasites.

## Vulnérabilité

La route `/document` vérifie l'authentification mais pas l'autorisation sur l'objet demandé.

## Débrief

L'identifiant ou la référence d'une ressource, même difficile à deviner, ne constitue pas un mécanisme d'autorisation.
