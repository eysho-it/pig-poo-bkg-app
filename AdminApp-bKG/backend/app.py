import os
import secrets
import bcrypt
from deta import Deta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_mail import Mail, Message
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
csrf = URLSafeTimedSerializer(app.secret_key)

mail_settings = {
    "MAIL_SERVER": os.getenv("MAIL_SERVER"),
    "MAIL_PORT": int(os.getenv("MAIL_PORT")),
    "MAIL_USE_TLS": bool(int(os.getenv("MAIL_USE_TLS"))),
    "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD")
}

app.config.update(mail_settings)
mail = Mail(app)

deta = Deta(os.getenv("DETA_PROJECT_KEY"))
deta_base = deta.Base("admin_logs")
deta_keys = deta.Base("api_keys")
deta_users = deta.Base("users")
deta_tokens = deta.Base("tokens")

# --- Admin-Panel ---

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        command = request.form['command']
        result = execute_command(command)
        deta_base.put({"command": command, "result": result, "user": session['user']})

    logs = deta_base.fetch().items
    return render_template('admin_panel.html', logs=logs)

# --- Befehlsausführung ---

def execute_command(command):
    if command.startswith("deta new"):
        project_name = command.split("deta new ")[1]
        if not project_name.isalnum():
            return "Ungültiger Projektname"
        os.system(f"deta new {project_name}")
        return f"Projekt '{project_name}' erstellt"
    elif command == "deta dev":
        os.system("deta dev")
        return "Entwicklungsumgebung gestartet"
    elif command == "deta logs":
        os.system("deta logs")
        return "Logs abgerufen"
    else:
        return "Ungültiger Befehl"

# --- API-Schlüsselverwaltung ---

@app.route('/api_keys', methods=['GET', 'POST'])
def api_keys():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        key_name = request.form['key_name']
        permissions = request.form.getlist('permissions')

        if not key_name.isalnum():
            flash("Schlüsselname muss alphanumerisch sein", "error")
        else:
            api_key = generate_api_key()
            deta_keys.put({"key_name": key_name, "api_key": api_key, "permissions": permissions})
            flash("API-Schlüssel erstellt", "success")

    keys = deta_keys.fetch().items
    return render_template('api_keys.html', keys=keys)

# --- API-Schlüsselgenerierung ---

def generate_api_key():
    return secrets.token_hex(16)

# --- Login/Logout ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = deta_users.get(username)

        if user and bcrypt.checkpw(password.encode(), user['password']):
            session['logged_in'] = True
            session['user'] = username
            return redirect(url_for('admin_panel'))
        else:
            flash("Ungültiger Benutzername oder Passwort", "error")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('login'))

# --- Benutzerverwaltung ---

@app.route('/users', methods=['GET', 'POST'])
def users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if not username.isalnum() or not password:
            flash("Benutzername muss alphanumerisch sein und Passwort darf nicht leer sein", "error")
        elif deta_users.get(username):
            flash("Benutzername bereits vergeben", "error")
        else:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt

.gensalt())
            deta_users.put({"key": username, "password": hashed_password, "role": role})
            flash("Benutzer erstellt", "success")

    users = deta_users.fetch().items
    return render_template('users.html', users=users)

# --- Registrierungsfunktion mit E-Mail-Bestätigung ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not username.isalnum() or not password:
            flash("Benutzername muss alphanumerisch sein und Passwort darf nicht leer sein", "error")
        elif deta_users.get(username):
            flash("Benutzername bereits vergeben", "error")
        else:
            token = secrets.token_urlsafe(16)
            deta_tokens.put({"key": token, "username": username, "password": password, "email": email})
            confirm_url = url_for('confirm_email', token=token, _external=True)
            msg = Message("Bitte bestätigen Sie Ihre E-Mail-Adresse", recipients=[email])
            msg.body = f"Bitte klicken Sie auf den folgenden Link, um Ihre Registrierung abzuschließen: {confirm_url}"
            mail.send(msg)
            flash("Bitte überprüfen Sie Ihre E-Mails, um die Registrierung abzuschließen", "success")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/confirm/<token>')
def confirm_email(token):
    data = deta_tokens.get(token)
    if data:
        username = data['username']
        password = data['password']
        email = data['email']
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        deta_users.put({"key": username, "password": hashed_password, "email": email})
        deta_tokens.delete(token)
        flash("E-Mail erfolgreich bestätigt. Sie können sich jetzt einloggen.", "success")
        return redirect(url_for('login'))
    else:
        flash("Ungültiger oder abgelaufener Token", "error")
        return redirect(url_for('register'))

# --- Passwort zurücksetzen ---

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = next((user for user in deta_users.fetch().items if user.get('email') == email), None)
        if user:
            token = secrets.token_urlsafe(16)
            deta_tokens.put({"key": token, "username": user['key']})
            reset_url = url_for('reset_password_confirm', token=token, _external=True)
            msg = Message("Passwort zurücksetzen", recipients=[email])
            msg.body = f"Bitte klicken Sie auf den folgenden Link, um Ihr Passwort zurückzusetzen: {reset_url}"
            mail.send(msg)
            flash("Bitte überprüfen Sie Ihre E-Mails, um das Passwort zurückzusetzen", "success")
            return redirect(url_for('login'))
        else:
            flash("E-Mail-Adresse nicht gefunden", "error")
    return render_template('reset_password.html')

@app.route('/reset_password_confirm/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    data = deta_tokens.get(token)
    if data:
        if request.method == 'POST':
            password = request.form['password']
            if not password:
                flash("Passwort darf nicht leer sein", "error")
            else:
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                deta_users.update({"password": hashed_password}, data['username'])
                deta_tokens.delete(token)
                flash("Passwort erfolgreich zurückgesetzt. Sie können sich jetzt einloggen.", "success")
                return redirect(url_for('login'))
        return render_template('reset_password_confirm.html')
    else:
        flash("Ungültiger oder abgelaufener Token", "error")
        return redirect(url_for('reset_password'))

# --- HTTP-API-Endpunkte ---

@app.route('/api/<endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api(endpoint):
    api_key = request.headers.get('X-API-Key')
    key_data = deta_keys.get(api_key)

    if not key_data:
        return jsonify({"error": "Ungültiger API-Schlüssel"}), 401

    permissions = key_data.get("permissions", [])
    if request.method not in permissions:
        return jsonify({"error": "Unzureichende Berechtigungen"}), 403

    if endpoint == 'data':
        if request.method == "GET":
            data = deta_base.fetch().items
            return jsonify(data), 200
        elif request.method == "POST":
            data = request.get_json()
            deta_base.put(data)
            return jsonify({"message": "Daten gespeichert"}), 201
        elif request.method == "PUT":
            data = request.get_json()
            key = data.get("key")
            if not key:
                return jsonify({"error": "Schlüssel erforderlich"}), 400
            deta_base.put(data, key)
            return jsonify({"message": "Daten aktualisiert"}), 200
        elif request.method == "DELETE":
            key = request.args.get("key")
            if not key:
                return jsonify({"error": "Schlüssel erforderlich"}), 400
            deta_base.delete(key)
            return jsonify({"message": "Daten gelöscht"}), 200

    return jsonify({"message": "API-Endpunkt nicht gefunden"}), 404

# --- Suchfunktion ---

@app.route('/search', methods=['GET'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    query = request.args.get('query')
    logs = deta_base.fetch({"command?contains": query}).items
    api_keys = deta_keys.fetch({"key_name?contains": query}).items
    users = deta_users.fetch({"key?contains": query}).items

    return render_template('search_results.html', logs=logs, api_keys=api_keys, users=users)

# --- Fehlerbehandlung ---

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error_500.html'), 500

# CSRF-Schutz für alle POST-Anfragen
@app.before_request
def csrf_protect():
    if request.method == "POST":
        try:
            csrf.validate_csrf_token(request.form['csrf_token'])
        except:
            return jsonify({"message": "Ungültiges CSRF-Token", "status": "error"}), 400

if __name__ == '__main__':
    app.run(debug=True)
