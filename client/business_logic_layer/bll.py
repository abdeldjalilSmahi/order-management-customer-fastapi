import re

from data_access_layer.database import DataAccess
from business_logic_layer.models import Orders, UserInformation, Order, Status
import validators


class BusinessLogicLayer:
    @staticmethod
    def verify_informations(order: UserInformation) -> bool:
        if not order.firstname or order.firstname.lower() == "string" or '':
            print("On vous prie de donner un bon firstname")
            return False
        if not order.lastname or order.lastname.lower() == "string" or '':
            print("On vous prie de donner un bon lastname")
            return False
        if not validators.email(order.email):
            print("On vous prie de donner un bon email")
            return False
        if not BusinessLogicLayer.is_valid_phone_number(order.phone_number):
            print("On vous prie de donner un bon numéro de telephone")
            return False
        return True

    @staticmethod
    def is_valid_phone_number(phone_number: str) -> bool:
        if phone_number is None or phone_number.lower() == "string":
            return False

        # Expression régulière pour valider les formats de numéro de téléphone
        # Accepte les formats comme "0764177198" ou "+33764177198"
        phone_pattern = r'^(?:\+\d{2})?\d{10}$'

        return re.match(phone_pattern, phone_number) is not None

    # @staticmethod
    # def add_order(order: Orders):
    #     data_access = DataAccess()
    #     data_access.add_order(order.__dict__)

    @staticmethod
    def get_customer_order(customer_number) -> Orders:
        customer_dictionnaire = DataAccess.get_order_customer(customer_number)
        customer_dictionnaire.pop('_id')
        user_information = UserInformation(firstname=customer_dictionnaire.pop('firstname'),
                                           lastname=customer_dictionnaire.pop('lastname'),
                                           email=customer_dictionnaire.pop('email'),
                                           phone_number=customer_dictionnaire.pop('phone_number'))
        orders = customer_dictionnaire.pop('orders')  # list
        list_orders = []
        for dictionnaire in orders:
            for cle in dictionnaire:
                order = Order(order_number=cle, **(dictionnaire.get(cle)))
                list_orders.append(order)

        customer_orders = Orders(user_information, list_orders)
        return customer_orders

    @staticmethod
    def update_order_decision(customer_number, decision: dict):
        orders = BusinessLogicLayer.get_customer_order(customer_number)
        orders.customer_id = decision.get('customer_id')
        order = orders.get_order_by_order_number(str(decision.get('order_number')))
        if order.actual_status == 'initiated':
            order_decision = decision.get('decision')
            order_status = Status.get_status_by_name(decision.get('status'))
            order.set_decision(order_decision)
            order.set_actual_status(order_status)
            order.order_id_supplier_side = decision.get('order_id')
            print(orders.to_dict())
            DataAccess().update_customer_orders(customer_number, orders)
            return "Votre décision a été bien reçu"
        else:
            return 'Decision deja prise'

    @staticmethod
    def update_order_devis(customer_number, devis: dict):
        orders = BusinessLogicLayer.get_customer_order(customer_number)
        orders.customer_id = devis.pop('customer_id')
        order = orders.get_order_by_order_number(str(devis.pop('order_number')))
        order.order_id_supplier_side = devis.pop('order_id')
        order.devis = devis
        print(orders.to_dict())
        DataAccess().update_customer_orders(customer_number, orders)
        return "devis a été bien reçu"


    @staticmethod
    def add_order(orders: Orders):
        order_list = orders.orders
        # print(order_list)
        last_order = order_list[0].__dict__()
        last_order = last_order.get('1')
        derniere_ordre = Order(**last_order)
        print(derniere_ordre.__dict__())
        customer_number, derniere_ordre = DataAccess.add_order(orders.to_dict(), derniere_ordre)
        print("Commande inserée avec succès.")

        return customer_number, derniere_ordre

        # else:
        #     return last_order.get('order_id')


if __name__ == '__main__':
    print(BusinessLogicLayer.get_customer_order("e4d909c290d0fb1ca068ffaddf22cbd0").__dict__)
