import enum

import uuid
from typing import Optional, Dict, List


class Status(enum.Enum):
    validated = "Validated"
    cancelled_by_customer = "Cancelled by Customer"
    initiated = "Initiated"
    pending = "Pending"
    processing = "Processing"
    shipped = "Shipped"
    out_for_delivery = "Out for Delivery"
    delivered = "Delivered"
    returned = "Returned"
    refunded = "Refunded"
    awaiting_payment = "Awaiting Payment"
    payment_failed = "Payment Failed"
    awaiting_confirmation = "Awaiting Confirmation"
    awaiting_stock = "Awaiting Stock"
    cancelled_by_seller = "Cancelled by Seller"
    on_hold = "On Hold"
    cancelled_and_finished = "Cancelled & Finished By Customer/Seller"

    @staticmethod
    def get_status_by_name(string_value: str) -> 'Status':
        for status in Status:
            if status.value == string_value:
                return status
        return None  # ou lever une exception si préféré


class UserInformation:
    def __init__(
            self,
            firstname: str,
            lastname: str,
            email: str,
            phone_number: str):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone_number = phone_number


class Order:
    def __init__(self,
                 products: Dict[str, int],
                 order_id_supplier_side: Optional[int] = None,
                 order_number: Optional[int] = 1,
                 actual_status: Optional[str] = 'initiated',
                 decision: Optional[str] = None,
                 devis: Optional[Dict[str, int]] = None,
                 facture: Optional[Dict[str, int]] = None):
        self.order_number = order_number
        self.order_id_supplier_side = order_id_supplier_side  # order_id
        self.products = products

        self.actual_status = actual_status
        self.decision = decision
        self.devis = devis
        self.facture = facture

    def set_decision(self, decision: str):
        self.decision = decision

    def set_actual_status(self, status: Status):
        self.actual_status = status.value

    def __dict__(self) -> dict:
        return {
            str(self.order_number): {
                'order_id_supplier_side': self.order_id_supplier_side,
                'products': self.products,
                'actual_status': self.actual_status,
                'decision': self.decision,
                'devis': self.devis,
                'facture': self.facture

            }
        }


class Orders:
    def __init__(
            self,
            userInformation: UserInformation,
            orders: List[Order],
            customer_number=str(uuid.uuid4()).replace("-", ""),
            customer_id: Optional[int] = None

    ):
        self.customer_id = customer_id
        self.customer_number = customer_number
        self.firstname = userInformation.firstname
        self.lastname = userInformation.lastname
        self.email = userInformation.email
        self.phone_number = userInformation.phone_number
        self.orders = orders

    def get_order_by_order_number(self, order_number):
        for order in self.orders:

            if order.order_number == order_number:
                return order

        return None

    def to_dict(self):
        dictionnaire = self.__dict__.copy()
        dictionnaire.pop('orders')
        list_of_orders = self.orders
        dictionnaire['orders'] = []
        for order in list_of_orders:
            dictionnaire['orders'].append(order.__dict__())

        return dictionnaire
