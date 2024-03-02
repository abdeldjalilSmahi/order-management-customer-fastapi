import requests
from business_logic_layer.bll import BusinessLogicLayer
from business_logic_layer.models import UserInformation, Orders, Order


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
        "order_number":  last_order.order_number,
        "produits": order.orders[0].products
    }
    print(request_message)
    response = requests.post("http://127.0.0.1:8080/place_order", json=request_message)
    return response.json()


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
    print(orders)
    last_order = BusinessLogicLayer.add_order(orders)
    print(passer_commande(orders, last_order))


if __name__ == "__main__":
    main()
