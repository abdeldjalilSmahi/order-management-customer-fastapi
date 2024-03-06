from pymongo.mongo_client import MongoClient
import uuid

from business_logic_layer.models import Order, Orders


#
# uri = "mongodb+srv://abdeldjalilsmahi:Awtbp!718293@cluster0.hslawmh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#
# # Create a new client and connect to the server
# client = MongoClient(uri)
#
# # Sélectionnez votre base de données
# db = client['ordermanagement']
#
# # Sélectionnez votre collection
# collection = db['customers']
#
#
# new_customer = {
#     "customer_number": 2,  # Supposons que c'est un entier, pas besoin de $numberInt
#     "customer_id": None,     # Idem, supposons entier
#     "firstname": "John",
#     "lastname": "Smith",
#     "email": "john@abc.com",
#     "phone_number": "0123456789",
#     "products": {
#         "product1": 5,
#         "product2": 1
#     }
# }
#
# # Insérer un nouveau client
# result = collection.insert_one(new_customer)
#
# # Afficher l'ID du nouveau document inséré
# print("Nouveau client inséré avec l'ID:", result.inserted_id)


class DataAccess:

    def __init__(self,
                 uri="mongodb+srv://abdeldjalilsmahi:Awtbp!718293@cluster0.hslawmh.mongodb.net/?retryWrites=true&w"
                     "=majority&appName=Cluster0"):
        # Create a new client and connect to the server
        self.client = MongoClient(uri)

        # Sélectionnez votre base de données
        self.db = self.client['ordermanagement']

        # Sélectionnez votre collection
        self.collection = self.db['customers']

    @staticmethod
    def get_order_customer(customer_number: str):

        search_criteria = {"customer_number": customer_number}
        # Récupérer le document
        try:
            customer = DataAccess().collection.find_one(search_criteria)
            if not customer:
                raise Exception("Aucun client trouvé avec ce critère de recherche.")
            return customer
        except Exception as e:
            print(e)

    @staticmethod
    def get_order_by_email(email: str):

        search_criteria = {"email": email}
        # Récupérer le document
        try:
            customer = DataAccess().collection.find_one(search_criteria)
            if not customer:
                raise Exception("Aucun client trouvé avec ce critère de recherche.")
            return customer
        except Exception as e:
            print(e)

    @staticmethod
    def push_new_order_for_existing_customer(email, new_order: dict):
        # Ajouter la nouvelle commande à la liste d'orders du client
        search_criteria = {"email": email}
        result = DataAccess().collection.update_one(search_criteria, {'$push': {'orders': new_order}})

        # Vérifier si la mise à jour a réussi
        if result.modified_count > 0:
            return True
        else:
            return False

    @staticmethod
    def add_order(orders: dict, last_order: Order):
        customer = DataAccess.get_order_by_email(orders.get("email"))
        if customer:
            print("client deja exist")
            customer_number = customer.get('customer_number')
            orders = customer.get('orders')
            number_of_order = len(orders)
            order_number = number_of_order + 1
            last_order.order_number = order_number
            result = DataAccess.push_new_order_for_existing_customer(customer.get('email'), last_order.__dict__())

            if result:
                print("Bien rajouté")
                return customer_number, last_order
            else:
                raise Exception("Error")

        print("Nouveau client avec nouvelle commande")

        result = DataAccess().collection.insert_one(orders)
        if result:
            print("Bien rajouté ")
            return orders.get('customer_number'), last_order
        else:
            raise Exception("Error")

    @staticmethod
    def update_customer_orders(customer_number, orders: Orders):
        customer_id = orders.customer_id
        result = DataAccess().collection.update_one(
            {"customer_number": customer_number},
            {"$set": {"customer_id": customer_id}}
        )

        # Convertir l'objet Orders en une structure adaptée à MongoDB
        orders_dict = [order.__dict__() for order in orders.orders]

        # Effectuer la mise à jour dans MongoDB
        try:
            update_result = DataAccess().collection.update_one(
                {"customer_number": customer_number},
                {"$set": {"orders": orders_dict}}
            )
            if update_result.modified_count == 0:
                print("Aucune mise à jour effectuée. Vérifiez le critère de recherche.")
            else:
                print("Mise à jour effectuée avec succès.")
                return "OK"
        except Exception as e:
            print(f"Erreur lors de la mise à jour : {e}")

    @staticmethod
    def get_decision(customer_number, order_number):
        # Requête pour trouver le document correspondant aux critères
        query = {
            "customer_number": customer_number
        }
        document = DataAccess().collection.find_one(query)
        # Extraire et afficher la décision pour l'order_number spécifié, si le document est trouvé
        if document:
            for order in document['orders']:
                dictionnaire = order
                for cle in dictionnaire:
                    if cle == order_number:
                        return dictionnaire[cle]['decision']
        else:
            print("Document non trouvé avec les critères donnés.")


if __name__ == "__main__":
    print(DataAccess.get_order_customer("0df6989558cd4d6ca0ace412ef4f73b1"))
