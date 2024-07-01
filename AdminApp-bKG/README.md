# AdminApp-bKG - README

## Übersicht

MeineAdminApp ist eine leistungsstarke Admin-Anwendung, die auf Deta Space läuft und Ihnen die Verwaltung Ihres Projekts erleichtert. Sie bietet folgende Funktionen:

* **Admin-Dashboard:** Führen Sie Deta Space-Befehle aus, überwachen Sie Logs, verwalten Sie API-Schlüssel und Benutzer.
* **Benutzerverwaltung:** Erstellen und verwalten Sie Benutzerkonten, weisen Sie Berechtigungen zu.
* **REST-API:** Bieten Sie eine sichere Schnittstelle für den Zugriff auf Ihre Daten und Funktionen.

## Voraussetzungen

* **Deta Space-Konto:** Erstellen Sie ein kostenloses Konto auf [https://deta.space](https://deta.space).
* **Deta CLI:** Installieren Sie die Deta CLI, indem Sie den Anweisungen auf [https://docs.deta.sh/docs/cli/install](https://docs.deta.sh/docs/cli/install) folgen.
* **Python 3.11:** Stellen Sie sicher, dass Python 3.11 auf Ihrem System installiert ist.

## Installation

1. **Projekt klonen:**
   ```bash
   git clone [https://github.com/](https://github.com/)<Ihr-GitHub-Benutzername>/MeineAdminApp.git
   cd MeineAdminApp
   ```

2. **Virtuelle Umgebung erstellen (optional, aber empfohlen):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Auf Windows: venv\Scripts\activate
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Umgebungsvariablen konfigurieren:**
   - Erstellen Sie eine Datei namens `.env` im Ordner `backend`.
   - Fügen Sie folgende Zeilen hinzu und ersetzen Sie die Platzhalter durch Ihre tatsächlichen Werte:
     ```
     DETA_PROJECT_KEY=Ihr_Deta_Projekt_Schlüssel
     FLASK_SECRET_KEY=Ein_zufälliger_und_sicherer_String
     ADMIN_USERNAME=Ihr_Admin_Benutzername
     ADMIN_PASSWORD=Ihr_Admin_Passwort
     MAIL_SERVER=smtp.example.com
     MAIL_PORT=587
     MAIL_USE_TLS=1
     MAIL_USERNAME=Ihr_Email_Benutzername
     MAIL_PASSWORD=Ihr_Email_Passwort
     ```

5. **Deta Space bereitstellen:**
   ```bash
   deta deploy