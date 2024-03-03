import json
import requests
from business_logic_layer.bll import BusinessLogicLayer
from business_logic_layer.messaging_queue import receveoir_message_a_queue
from business_logic_layer.models import UserInformation, Orders, Order
from data_access_layer.models import Status


def get_product_list():
    response = requests.get("http://127.0.0.1:8080/products_list")
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
    print(request_message)
    response = requests.post("http://127.0.0.1:8080/place_order", json=request_message)
    return response.json()


def valider_operation(devis: dict):
    try:
        while True:
            decision = input("Est ce que tu valides le devis  ? (oui/non) ").strip() \
                .lower()
            if decision in ["oui", "ok", "valide"]:
                new_status = Status.confiremd_by_customer
                message = "Devis validée. Passage à la prochaine étape."
                break
            elif decision in ["non", "no", "pas", "valide pas"]:
                new_status = Status.cancelled_by_customer
                # .update_status_order(order_bll_model, new_status)
                message = "Opération non validée. Annulation de la commande."
                # customer_side_response = send_confirmation(customer_number=customer_bll_model.customer_number,
                #                                            order_number=order_number,
                #                                            customer_id=customer_bll_model.customer_id,
                #                                            order_id=order_bll_model.order_id
                #                                            , email=customer_bll_model.email, status=new_status,
                #                                            decision=message)
                # print(customer_side_response['message'])
                # new_status = Status.cancelled_and_finished
                break
            else:
                print("Entrée invalide. Veuillez répondre par 'oui' ou 'non'.")

        # order_bll_model = BusinessRulesOrder.update_status_order(order_bll_model, new_status)
        print(message)

        # return customer_bll_model, order_bll_model, products_quantities

    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        # Optionnellement, vous pouvez gérer ou propager l'exception ici


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    devis = {
        "products": data.get("products"),
        "total_price": data.get("total_price")
    }
    print("******************************DEVIS***************************************")
    pretty_devis = json.dumps(devis, indent=4)
    print(pretty_devis)
    print("******************************DEVIS***************************************")

    ch.basic_ack(delivery_tag=method.delivery_tag)


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
    print(orders)
    print(passer_commande(orders, last_order))
    print("##########################################################################################")
    receveoir_message_a_queue('place_order', on_message_received)


if __name__ == "__main__":
    main()
