# Admin App

## Projektstruktur

```
admin-app/
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── admin_panel.html
│   ├── error_404.html
│   ├── error_500.html
│   ├── subscriptions.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
└── tests/
    ├── test_app.py
```

## Installation

1. Klonen Sie das Repository:
```bash
git clone <repository-url>
cd admin-app
```

2. Erstellen und aktivieren Sie eine virtuelle Umgebung:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Installieren Sie die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

4. Setzen Sie Ihre PayPal-API-Schlüssel in `app.py` ein:
```python
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox oder live
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
})
```

5. Starten Sie die Anwendung:
```bash
python app.py
```

## Tests ausführen

```bash
python -m unittest discover -s tests
```

## Verwendung

- Rufen Sie die Startseite auf: `http://localhost:5000`
- Navigieren Sie zum Admin-Panel: `http://localhost:5000/admin`
- Verwalten Sie Abonnements: `http://localhost:5000/subscriptions`

## Weitere Überlegungen und Verbesserungen

1. **Persistente Datenbank:** Ersetzen Sie die In-Memory-Datenbank durch eine persistente Datenbank wie Deta Base.
2. **Sicherheitsmaßnahmen:** Implementieren Sie Eingabevalidierung und sichere Speicherung von API-Schlüsseln.
3. **Fehlerbehandlung:** Fügen Sie robuste Fehlerbehandlungsroutinen hinzu.
4. **UI/UX:** Verbessern Sie die Benutzeroberfläche und das Benutzererlebnis.
5. **PayPal-Integration:** Ersetzen Sie Platzhalter durch tatsächliche API-Aufrufe an PayPal.

## Ressourcen

1. [Deta Space - HTTP API](https://deta.space/docs/en/build/reference/http-api)
2. [Deta Space - Deta Base](https://deta.space/docs/en/build/reference/deta-base)
3. [Deta Space - SDK](https://deta.space/docs/en/build/reference/sdk)
4. [Deta Space - Spacefile](https://deta.space/docs/en/build/reference/spacefile)
5. [Deta Space - Projects](https://deta.space/docs/en/build/fundamentals/development/projects#creating-a-project)
6. [Mit API-Schlüsseln authentifizieren](https://deta.space/docs/en/build/reference/http-api)
7. [Configuring Function Spaces](https://deta.space/docs/en/build/reference/runtime)
```

## 🌐 Sources

1. [developer.paypal.com - Upgrade your Checkout integration](https://developer.paypal.com/docs/checkout/standard/upgrade-integration/)
2. [help.shopify.com - Shopify Subscriptions einrichten](https://help.shopify.com/de/manual/products/purchase-options/shopify-subscriptions/setup)
3. [paypal.com - Abonnementzahlungen verwalten](https://www.paypal.com/de/money-hub/article/how-to-manage-subscription-payments)
4. [paypal.com - Code herunterladen](https://demo.paypal.com/de/demo/code_samples)
5. [stripe.com - Die Funktionen der Abonnementverwaltung](https://stripe.com/de/resources/more/subscription-management-features-explained-and-how-to-choose-a-software-solution)
6. [paypal.com - Was sind API-Signatur- und Zertifikat-Anmeldedaten?](https://www.paypal.com/de/cshelp/article/was-sind-api-signatur--und-zertifikat-anmeldedaten-help487)
