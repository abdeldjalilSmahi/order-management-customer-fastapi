from flask import Flask, request

app = Flask(__name__)

@app.route('/order_confirmation/<customer_number>', methods=['POST'])
def order_confirmation(customer_number):
    data = request.json
    print(f"Notification reçue pour le client {customer_number}: {data}")
    # Traiter la notification ici
    return {"status": "success"}, 200

if __name__ == '__main__':
    app.run(port=5000)  # Exécuter le serveur sur le port 5000
