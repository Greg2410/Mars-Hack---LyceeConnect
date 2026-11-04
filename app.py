import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, abort, g

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lycee.db"

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
FLAG = os.environ["FLAG"]

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(_=None):
    conn = g.pop("db", None)
    if conn:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS documents;
    DROP TABLE IF EXISTS grades;
    DROP TABLE IF EXISTS timetable;

    CREATE TABLE users(
      id INTEGER PRIMARY KEY,
      username TEXT UNIQUE,
      password TEXT,
      firstname TEXT,
      lastname TEXT,
      role TEXT,
      class_name TEXT,
      email TEXT
    );

    CREATE TABLE documents(
      id INTEGER PRIMARY KEY,
      ref TEXT UNIQUE,
      title TEXT,
      owner TEXT,
      category TEXT,
      body TEXT
    );

    CREATE TABLE grades(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      subject TEXT,
      grade TEXT,
      coefficient INTEGER,
      comment TEXT
    );

    CREATE TABLE timetable(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      day TEXT,
      start_time TEXT,
      end_time TEXT,
      subject TEXT,
      room TEXT,
      teacher TEXT
    );

    CREATE TABLE news(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      published_at TEXT,
      title TEXT,
      category TEXT,
      body TEXT
    );
    """)

    cur.executemany("INSERT INTO users VALUES(?,?,?,?,?,?,?,?)", [
      (1,"proviseur","not-used","Alain","Bernard","Proviseur",None,"a.bernard@jean-moulin.local"),
      (2,"cdurand","not-used","Claire","Durand","Professeure",None,"c.durand@jean-moulin.local"),
      (3,"eleve","rentree2026","Lucas","Martin","Élève","Terminale 2","lucas.martin@eleves.jean-moulin.local"),
      (4,"cdupont","not-used","Camille","Dupont","Élève","Première 3","camille.dupont@eleves.jean-moulin.local"),
    ])

    docs = [
      (9287,"AUDIT-LC-9287","Audit final de sécurité — LycéeConnect","Alain Bernard — Proviseur","Confidentiel","__FLAG__"),

      (8042,"DIR-2026-42","Bordereau de transmission — Direction","Secrétariat de direction","Interne",
       "BORDEREAU DE TRANSMISSION\nRéférence : DIR-2026-42\n\nObjet : transmission du rapport final de l'audit LycéeConnect au proviseur.\n\nPièce transmise : AUDIT-LC-9287\nStatut : CONFIDENTIEL — DIRECTION"),

      (8820,"CFG-8820","Annexe technique — journalisation","DSI","Technique",
       "ANNEXE TECHNIQUE\nRéférence : CFG-8820\n\nLa journalisation applicative a été renforcée après l'incident.\nAucune donnée confidentielle n'est contenue dans cette annexe.\nStatut : clôturé."),

      (6113,"AUDIT-LC-2025-113","Ancien audit LycéeConnect — 2025","DSI","Archive",
       "ARCHIVE — RAPPORT 2025\nRéférence : AUDIT-LC-2025-113\n\nCe document concerne l'ancienne version du portail.\n\nCode de test expiré : MARS{archive_2025_not_valid}\n\nCe code n'est plus valable."),

      (7314,"SEC-7314","Rapport préliminaire — incident LycéeConnect","DSI / Direction","Interne",
       "RAPPORT PRÉLIMINAIRE\nRéférence : SEC-7314\n\nL'anomalie de permissions a été reproduite. Trois éléments sont associés au dossier :\n\n- Annexe de configuration : CFG-8820\n- Ancien rapport utilisé pour comparaison : AUDIT-LC-2025-113\n- Bordereau de transmission à la direction : DIR-2026-42\n\nLe rapport final n'est pas joint à ce dossier."),

      (6502,"NOTE-6502","Note de service — sécurité numérique","Secrétariat","Administration",
       "À la suite d'un incident sur LycéeConnect, le proviseur a demandé un audit. Le suivi technique porte la référence SEC-7314."),

      (5840,"MAINT-5840","Compte-rendu maintenance B204","Intendance","Maintenance",
       "Intervention terminée en salle B204. Une anomalie de permissions sur LycéeConnect a été signalée à la direction.\n\nDossier de suivi : SEC-7314"),

      (5193,"CLUB-5193","Club informatique — qualification Mars@Hack","Claire Durand","Activités",
       "Réunion exceptionnelle du club informatique mercredi à 13 h en salle B204. Mme Durand présentera le défi de qualification Mars@Hack."),

      (4472,"CDI-4472","Inventaire annuel du CDI","CDI","Vie scolaire",
       "Le CDI sera fermé vendredi matin pour inventaire."),

      (3906,"RI-3906","Règlement intérieur 2026-2027","Administration","Officiel",
       "Le règlement intérieur est applicable à l'ensemble des élèves et personnels."),

      (3521,"CANTINE-3521","Menu de la cantine — semaine 43","Intendance","Restauration",
       "Lundi : pâtes bolognaises\nMardi : couscous\nJeudi : gratin dauphinois\nVendredi : poisson et riz"),

      (3148,"EXAM-3148","Planning des examens blancs","Vie scolaire","Scolarité",
       "Les épreuves blanches auront lieu du 7 au 11 décembre 2026."),

      (2675,"SORTIE-2675","Autorisation de sortie scolaire","Camille Dupont","Personnel",
       "Sortie pédagogique au musée des sciences — autorisation enregistrée."),

      (4821,"SCOL-4821","Certificat de scolarité","Lucas Martin","Personnel",
       "Je soussigné, le proviseur du lycée Jean-Moulin, certifie que Lucas Martin est inscrit en Terminale 2 pour l'année scolaire 2026-2027."),
    ]
    cur.executemany("INSERT INTO documents VALUES(?,?,?,?,?,?)", docs)

    cur.executemany("INSERT INTO grades(user_id,subject,grade,coefficient,comment) VALUES(?,?,?,?,?)", [
      (3,"Mathématiques","14,5 / 20",3,"Ensemble satisfaisant."),
      (3,"NSI","17 / 20",2,"Très bon travail."),
      (3,"Anglais","13 / 20",2,"Participation régulière."),
      (3,"Philosophie","11,5 / 20",2,"Argumentation à approfondir."),
      (3,"Histoire-Géographie","15 / 20",2,"Bon devoir."),
    ])

    cur.executemany("INSERT INTO timetable(day,start_time,end_time,subject,room,teacher) VALUES(?,?,?,?,?,?)", [
      ("Lundi","08:00","09:00","Mathématiques","B112","Mme Leroy"),
      ("Lundi","09:00","10:00","Anglais","A203","M. Smith"),
      ("Lundi","10:15","12:15","NSI","B204","Mme Durand"),
      ("Mardi","08:00","10:00","Histoire-Géographie","A105","M. Petit"),
      ("Mardi","10:15","12:15","Philosophie","A107","Mme Robert"),
      ("Mercredi","09:00","11:00","Mathématiques","B112","Mme Leroy"),
      ("Jeudi","08:00","10:00","NSI","B204","Mme Durand"),
      ("Jeudi","10:15","11:15","Anglais","A203","M. Smith"),
      ("Vendredi","08:00","10:00","Philosophie","A107","Mme Robert"),
      ("Vendredi","10:15","12:15","Histoire-Géographie","A105","M. Petit"),
    ])

    cur.executemany("INSERT INTO news(published_at,title,category,body) VALUES(?,?,?,?)", [
      ("19/10/2026 16:40","Maintenance terminée en salle B204","Maintenance",
       "L'intervention sur les postes de la salle B204 est terminée. Ticket matériel MAINT-8842 clôturé. Les cours de NSI reprendront normalement dès demain."),
      ("18/10/2026 11:15","Incident sur LycéeConnect : suivi en cours","Informatique",
       "Une anomalie de permissions a été observée sur le portail LycéeConnect. L'équipe technique a ouvert le dossier SEC-7314 et transmis les éléments à la direction. Aucun changement de mot de passe n'est demandé aux élèves."),
      ("16/10/2026 09:20","Qualification Mars@Hack — club informatique","Vie du lycée",
       "Le club informatique se réunira mercredi à 13 h en B204 pour une séance spéciale de préparation à Mars@Hack."),
      ("14/10/2026 14:00","Examens blancs de décembre","Scolarité",
       "Le calendrier prévisionnel des examens blancs est disponible dans la rubrique Documents. Référence administrative EXAM-3148."),
      ("12/10/2026 08:30","Réunion parents-professeurs","Vie scolaire",
       "La réunion parents-professeurs des classes de Terminale aura lieu vendredi 6 novembre à partir de 18 h."),
      ("09/10/2026 12:05","Menu de la semaine","Restauration",
       "Le menu de la semaine prochaine est disponible dans la rubrique Documents.")
    ])
    conn.commit()
    conn.close()

if not DB_PATH.exists():
    init_db()

def require_login():
    if "user_id" not in session:
        return redirect(url_for("login"))

def current_user():
    if "user_id" not in session:
        return None
    return db().execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        user = db().execute("SELECT * FROM users WHERE username=? AND password=?", (username,password)).fetchone()
        if user:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Identifiant ou mot de passe incorrect.")
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    guard = require_login()
    if guard: return guard
    user = current_user()
    recent_docs = db().execute("SELECT * FROM documents WHERE id IN (4821,3148,3906) ORDER BY title").fetchall()
    grades = db().execute("SELECT * FROM grades WHERE user_id=? LIMIT 3", (user["id"],)).fetchall()
    news = db().execute("SELECT * FROM news ORDER BY id ASC LIMIT 4").fetchall()
    return render_template("dashboard.html", user=user, recent_docs=recent_docs, grades=grades, news=news)

@app.route("/notes")
def grades():
    guard = require_login()
    if guard: return guard
    user = current_user()
    rows = db().execute("SELECT * FROM grades WHERE user_id=?", (user["id"],)).fetchall()
    return render_template("grades.html", user=user, grades=rows)

@app.route("/emploi-du-temps")
def timetable():
    guard = require_login()
    if guard: return guard
    rows = db().execute("SELECT * FROM timetable ORDER BY CASE day WHEN 'Lundi' THEN 1 WHEN 'Mardi' THEN 2 WHEN 'Mercredi' THEN 3 WHEN 'Jeudi' THEN 4 ELSE 5 END, start_time").fetchall()
    return render_template("timetable.html", user=current_user(), lessons=rows)

@app.route("/documents")
def documents():
    guard = require_login()
    if guard: return guard
    # Vue normale de Lucas : seulement ses documents et quelques documents publics.
    rows = db().execute("SELECT * FROM documents WHERE id IN (4821,3148,3521,3906) ORDER BY title").fetchall()
    return render_template("documents.html", user=current_user(), documents=rows)

@app.route("/document")
def document():
    guard = require_login()
    if guard: return guard

    # Deux mécanismes de consultation existent dans le portail :
    # - id : ancien identifiant numérique
    # - ref : référence documentaire utilisée par l'administration
    #
    # VULNÉRABILITÉ INTENTIONNELLE :
    # dans les deux cas, le serveur vérifie seulement l'authentification,
    # jamais l'autorisation sur l'objet demandé.
    doc = None
    requested_by = None

    if request.args.get("ref"):
        ref = request.args.get("ref", "").strip().upper()
        doc = db().execute("SELECT * FROM documents WHERE ref=?", (ref,)).fetchone()
        requested_by = f"ref={ref}"
    elif request.args.get("id"):
        try:
            document_id = int(request.args.get("id", ""))
        except ValueError:
            abort(404)
        doc = db().execute("SELECT * FROM documents WHERE id=?", (document_id,)).fetchone()
        requested_by = f"id={document_id}"
    else:
        abort(404)

    if not doc:
        abort(404)

    body = doc["body"]
    if doc["ref"] == "AUDIT-LC-9287":
        body = (
          "⚠ DOCUMENT CONFIDENTIEL — DIRECTION ⚠\n\n"
          "Destinataire : Alain Bernard, Proviseur\n"
          "Référence : AUDIT-LC-9287\n\n"
          "L'audit confirme une défaillance de contrôle d'accès sur le portail.\n"
          "Un utilisateur authentifié peut demander des ressources qui ne lui appartiennent pas.\n\n"
          f"Code de validation : {FLAG}"
        )
    return render_template("document.html", user=current_user(), doc=doc, body=body, requested_by=requested_by)

@app.route("/robots.txt")
def robots():
    return (
        "User-agent: *\\n"
        "Disallow: /admin-console\\n"
        "Disallow: /backup-2025\\n",
        200,
        {"Content-Type": "text/plain; charset=utf-8"}
    )

@app.route("/admin-console")
def admin_console():
    guard = require_login()
    if guard: return guard
    return render_template("admin_console.html", user=current_user()), 403

@app.route("/backup-2025")
def backup_2025():
    guard = require_login()
    if guard: return guard
    return render_template("backup_2025.html", user=current_user())

@app.route("/actualites")
def news():
    guard = require_login()
    if guard: return guard
    rows = db().execute("SELECT * FROM news ORDER BY id ASC").fetchall()
    return render_template("news.html", user=current_user(), news=rows)

@app.route("/profil")
def profile():
    guard = require_login()
    if guard: return guard
    return render_template("profile.html", user=current_user())

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.errorhandler(404)
def not_found(_):
    return render_template("404.html", user=current_user()), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
