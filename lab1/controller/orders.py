from controller import BaseController
from model.orders import OrdersModel, Orders
from view.orders import OrdersView
from datetime import datetime
from decimal import Decimal


class OrdersController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(OrdersModel(connection), OrdersView('orders', view_driver))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Order date (DD.MM.YYYY)', 'Recipients date (DD.MM.YYYY)',
                   'Shipping cost (₴)', 'Sender IPN', 'Recipient IPN',
                   'Warehouse departure id']
        values = [item.order_date, item.recipients_date, item.shipping_cost, item.sender_ipn,
                  item.recipient_ipn, item.warehouse_id] \
            if isinstance(item, Orders) else None
        return prompts, values

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        order_date = recipients_date = shipping_cost = sender_ipn \
            = recipient_ipn = warehouse_id = None
        for item in input_items:
            value = item['value']
            if item['name'] == 'Date departure (DD.MM.YYYY)':
                order_date = datetime.strptime(value, "%d.%m.%Y").date()
            elif item['name'] == 'Date arrival (DD.MM.YYYY, could be empty)':
                recipients_date = datetime.strptime(value, "%d.%m.%Y").date() if item['value'] is not None else None
            elif item['name'] == 'Shipping cost (₴)':
                shipping_cost = Decimal(value)
                if shipping_cost <= 0:
                    raise Exception(f"Shipping cost should be > 0, got {shipping_cost}")
            elif item['name'] == 'Sender IPN':
                sender_ipn = int(value)
            elif item['name'] == 'Recipient IPN':
                recipient_ipn = int(value)
            elif item['name'] == 'Warehouse departure number':
                warehouse_id = int(value)
        return Orders(order_date, shipping_cost, sender_ipn,
                      recipient_ipn, warehouse_id, recipients_date)
