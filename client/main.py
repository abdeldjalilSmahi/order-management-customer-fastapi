import json
import requests
from business_logic_layer.bll import BusinessLogicLayer
from business_logic_layer.messaging_queue import receveoir_message_a_queue
from business_logic_layer.models import UserInformation, Orders, Order
from data_access_layer.models import Status


def get_product_list():
    response = requests.get("http://127.0.0.1:8000/products_list")
    proucts_dict = response.json()

    for cle in proucts_dict:
        print(f"{cle}: {proucts_dict[cle]}€")
    return proucts_dict


def proposer_produit(dictionnaire: dict):
    commande = {}
    for cle in dictionnaire:
        quantite = int(input(f"Combien vous voulez prendre de ce produit {cle} : "))
        while quantite < 0:
            quantite = int(input(f"Combien vous voulez prendre de ce produit 'quantite sup à 0 SVP' {cle} : "))

        commande[cle] = quantite
        if quantite == 0:
            commande.pop(cle)
    return commande


def passer_commande(order: Orders, last_order: Order):
    request_message = {
        "customer_number": order.customer_number,
        "firstname": order.firstname,
        "lastname": order.lastname,
        "email": order.email,
        "phone_number": order.phone_number,
        "order_number": last_order.order_number,
        "produits": order.orders[0].products
    }
    response = requests.post("http://127.0.0.1:8000/place_order", json=request_message)
    return response.json()


def valider_operation(devis: dict):
    print(devis)
    try:
        while True:
            decision = input("Est ce que tu valides le devis  ? (oui/non) ").strip() \
                .lower()
            if decision in ["oui", "ok", "valide"]:
                new_status = Status.confiremd_by_customer
                BusinessLogicLayer.update_order_actual_status(devis.get("customer_number"), devis.get('order_number'),
                                                              new_status)
                message = "Devis validée. Passage à la prochaine étape."
                return message, True
            elif decision in ["non", "no", "pas", "valide pas"]:
                new_status = Status.cancelled_by_customer
                BusinessLogicLayer.update_order_actual_status(devis.get("order_number"), new_status)
                message = "Devis non validée. Passage à la prochaine étape."
                return message, False
            else:
                print("Entrée invalide. Veuillez répondre par 'oui' ou 'non'.")
        print(message)


    except Exception as e:
        print(f"Une erreur est survenue: {e}")


def send_decision(customer_id:int, customer_number: str, order_id: int, order_number: int, status: Status):
    customer_decision_to_send = {
        "customer_number": customer_number,
        "order_id": order_id,
        "order_number": order_number,
        "status": status.value
    }
    response = requests.post(f"http://127.0.0.1:8080/customer_decision/{customer_id}", json=customer_decision_to_send)
    return response.json()


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    print(data)
    devis = {
        "products": data.get("products"),
        "total_price": data.get("total_price")
    }
    print("******************************DEVIS***************************************")
    pretty_devis = json.dumps(devis, indent=4)
    print(pretty_devis)
    print("******************************DEVIS***************************************")
    message, boolean = valider_operation(data)
    if boolean:
        customer_decision_to_send = {
            "customer_id": int(data.get("customer_id")),
            "customer_number": data.get('customer_number'),
            "order_id": data.get('order_id'),
            "order_number": data.get('order_number'),
            "status": Status.confiremd_by_customer
        }
        print(send_decision(**customer_decision_to_send))
    else:
        customer_decision_to_send = {
            "customer_id": int(data.get("customer_id")),
            "customer_number": data.get('customer_number'),
            "order_id": data.get('order_id'),
            "order_number": data.get('order_number'),
            "status": Status.cancelled_by_customer
        }
        print(send_decision(**customer_decision_to_send))
        print("Nous allons envoyer votre refus de devis au fournisseur")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    ch.stop_consuming()


def main():
    print("Bonjour, et bienvenue chez votre fournisseur fidèle")
    print("-----------------------------------------------------------")
    print("Nous vous prions de bien vouloir passer vos informations: \n")
    checked = False
    userInformation = None
    while not checked:
        firstname = input("Your first name: ")
        lastname = input("Your last name: ")
        email = input("Your email : ")
        phone_number = input("Your phone number : ")
        userInformation = UserInformation(firstname, lastname, email, phone_number)
        checked = BusinessLogicLayer.verify_informations(userInformation)
    print("-----------------------------------------------------------")
    print("\t \t \t Nous vous remercions !  ")
    print("Nous Trouvez ci dessous les produits que nous offerons! : \n")
    dictoinnaire_produits = get_product_list()
    print("-----------------------------------------------------------")
    print("Nous vous prions de bien vouloir choisir le produit et la quantité ")
    print("-----------------------------------------------------------")
    products = proposer_produit(dictoinnaire_produits)
    order = Order(products)
    list_of_orders = [order]
    orders = Orders(userInformation, list_of_orders)
    customer_number, last_order = BusinessLogicLayer.add_order(orders)
    orders.customer_number = customer_number

    print(passer_commande(orders, last_order))
    print("##########################################################################################")
    queue_name = customer_number + "-devis"
    ##Check decision ! si validé entre dans la queue si non exit
    decision = BusinessLogicLayer.get_decision(customer_number, str(last_order.order_number))
    while decision is None:
        decision = BusinessLogicLayer.get_decision(customer_number, str(last_order.order_number))
    print("######################################DECISION############################################")
    print(f"Decision reçu : {decision}")
    print("##########################################################################################")
    actual_order = BusinessLogicLayer.get_order(customer_number, str(last_order.order_number))
    if actual_order.get('actual_status')== "Validated":
        receveoir_message_a_queue(queue_name, on_message_received)
    else:
        print("Malheureusement votre commande a été refusé par le fournisserur")


if __name__ == "__main__":

    main()
# a.i@temp.com
