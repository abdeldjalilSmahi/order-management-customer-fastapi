from pymongo.mongo_client import MongoClient
import uuid

from business_logic_layer.models import Order, Orders



uri = "mongodb+srv://abdeldjalilsmahi:Awtbp!718293@cluster0.hslawmh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Sélectionnez votre base de données
db = client['ordermanagement']

# Sélectionnez votre collection
collection = db['customers']

# Critères de recherche
customer_number = "43a23d3f2f5c4280bf2be714be2d32fc"
order_number = "1"

# Requête pour trouver le document correspondant aux critères
query = {
    "customer_number": customer_number
}
document = collection.find_one(query)
# Extraire et afficher la décision pour l'order_number spécifié, si le document est trouvé
if document:
    print(document['orders'])
    for order in document['orders']:
        dictionnaire = order
        print(dictionnaire)
        for cle in dictionnaire:
            if cle == order_number:
                print(cle)
                decision = dictionnaire[cle]['decision']
                if decision is None: print ("hi")
else:
    print("Document non trouvé avec les critères donnés.")