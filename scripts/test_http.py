#!/usr/bin/env python3
"""Test fonctionnel HTTP de LycéeConnect après `docker compose up -d`."""
import argparse
import http.cookiejar
import re
import urllib.error
import urllib.parse
import urllib.request

def main():
    parser = argparse.ArgumentParser(description="Vérification HTTP du challenge LycéeConnect")
    parser.add_argument("--base-url", default="http://localhost:8080", help="Adresse du portail")
    parser.add_argument("--verbose", action="store_true", help="Afficher chaque contrôle")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    client = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    )
    completed = 0

    def request(path, data=None):
        req = urllib.request.Request(
            base + path,
            data=(urllib.parse.urlencode(data).encode("utf-8") if data else None),
        )
        try:
            with client.open(req, timeout=8) as response:
                return response.status, response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as err:
            return err.code, err.read().decode("utf-8", errors="replace")

    def check(label, path, expected=200, must_contain=(), data=None):
        nonlocal completed
        status, html = request(path, data=data)
        missing = [value for value in must_contain if value not in html]
        if status != expected or missing:
            raise AssertionError(
                f"{label}: HTTP={status}, attendu={expected}, texte absent={missing}"
            )
        completed += 1
        if args.verbose:
            print(f"[OK] {label} — HTTP {status}")
        return html

    check("Connexion : formulaire", "/", must_contain=("Se connecter",))
    check(
        "Connexion : compte Lucas",
        "/",
        data={"username": "eleve", "password": "rentree2026"},
        must_contain=("Bonjour Lucas",),
    )
    check("Tableau de bord normal", "/dashboard", must_contain=("Dernières informations",))
    check("Actualités et incident", "/actualites", must_contain=("SEC-7314",))
    check("Liste des documents", "/documents", must_contain=("Certificat de scolarité",))
    check("Document de Lucas", "/document?id=4821", must_contain=("SCOL-4821",))
    check("Lien permanent", "/document?ref=SCOL-4821", must_contain=("Certificat de scolarité",))
    check("Rapport de l'incident", "/document?ref=SEC-7314", must_contain=("DIR-2026-42",))
    check("Annexe leurre", "/document?ref=CFG-8820", must_contain=("Aucune donnée confidentielle",))
    check("Ancien audit", "/document?ref=AUDIT-LC-2025-113", must_contain=("archive_2025_not_valid",))
    check("Bordereau de direction", "/document?ref=DIR-2026-42", must_contain=("AUDIT-LC-9287",))
    final_report = check(
        "Rapport final",
        "/document?ref=AUDIT-LC-9287",
        must_contain=("Code de validation",),
    )
    if re.search(r"MARS\{[^}]+\}", final_report) is None:
        raise AssertionError("Aucun flag au format MARS{...} dans le rapport final")
    if "MARS{archive_2025_not_valid}" in final_report:
        raise AssertionError("Le flag réel est identique au leurre")
    if args.verbose:
        print("[OK] Le rapport final contient un flag différent du leurre (valeur masquée)")

    check("Admin protégé", "/admin-console", expected=403)
    check("ID inexistant", "/document?id=3", expected=404)
    check("Fichier robots.txt", "/robots.txt", must_contain=("/admin-console", "/backup-2025"))
    print(f"Succès : {completed} contrôles HTTP validés.")

if __name__ == "__main__":
    try:
        main()
    except (AssertionError, urllib.error.URLError, TimeoutError) as exc:
        raise SystemExit(f"ÉCHEC : {exc}") from exc
