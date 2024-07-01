from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import json
import paypalrestsdk

app = Flask(__name__)

# PayPal configuration
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
})

# In-memory database substitute
deta_users = {}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_panel():
    return render_template('admin_panel.html', users=deta_users)

@app.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
    if request.method == 'POST':
        user_id = request.form['user_id']
        subscription_plan = request.form['subscription_plan']
        if user_id in deta_users:
            deta_users[user_id]['subscription'] = subscription_plan
        else:
            deta_users[user_id] = {'subscription': subscription_plan}
        return redirect(url_for('admin_panel'))
    return render_template('subscriptions.html')

@app.route('/api/subscriptions', methods=['POST'])
def create_subscription():
    api_key = request.headers.get('X-API-Key')
    # Verify API key here
    data = request.get_json()
    user_id = data.get('user_id')
    subscription_plan = data.get('subscription_plan')

    # PayPal payment processing would go here

    # Assuming payment is successful
    if user_id in deta_users:
        deta_users[user_id]['subscription'] = subscription_plan
    else:
        deta_users[user_id] = {'subscription': subscription_plan}

    return jsonify({"message": "Abonnement erfolgreich erstellt"}), 201

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error_500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
