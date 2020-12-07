from datetime import date
from decimal import Decimal
from model import BaseModel


class Orders:
    def __init__(self, order_date: date, shipping_cost: Decimal, sender_ipn: int, recipient_ipn: int,
                 warehouse_id: int, recipients_date: date, order_id: int = None):
        self.order_id = order_id
        self.recipients_date = recipients_date
        self.order_date = order_date
        self.shipping_cost = shipping_cost
        self.sender_ipn = sender_ipn
        self.recipient_ipn = recipient_ipn
        self.warehouse_id = warehouse_id

    def __str__(self):
        return f"Orders [order_id={self.order_id}, recipients_date={self.recipients_date}, " \
               f"order_date={self.order_date}, sender_ipn={self.sender_ipn}, recipient_ipn={self.recipient_ipn}, " \
               f"shipping_cost={self.shipping_cost}," \
               f"warehouse_id={self.warehouse_id}]"


class OrdersModel(BaseModel):
    def __init__(self, connection):
        insert_query = "INSERT INTO orders (recipients_date, order_date, shipping_cost, " \
                       "sender_ipn, recipient_ipn, warehouse_id) " \
                       "VALUES (%(recipients_date)s, %(order_date)s, %(shipping_cost)s, " \
                       "%(sender_ipn)s, %(recipient_ipn)s, %(warehouse_id)s) " \
                       "RETURNING order_id"
        select_query = "SELECT order_id, recipients_date, order_date, shipping_cost::numeric, " \
                       "sender_ipn, recipient_ipn, warehouse_id " \
                       "FROM orders WHERE order_id = %s"
        update_query = "UPDATE orders SET recipients_date = %(recipients_date)s, " \
                       "order_date = %(order_date)s, shipping_cost = %(shipping_cost)s, " \
                       "sender_ipn = %(sender_ipn)s, recipient_ipn = %(recipient_ipn)s, " \
                       "warehouse_id = %(warehouse_id)s " \
                       "WHERE order_id = %(order_id)s"
        delete_query = "DELETE FROM orders WHERE order_id = %s"
        select_all_query = "SELECT order_id, recipients_date, order_date, shipping_cost::numeric, " \
                           "sender_ipn, recipient_ipn, warehouse_id FROM orders " \
                           "ORDER BY order_id OFFSET %(offset)s LIMIT %(limit)s"
        count_query = "SELECT COUNT(*) FROM orders"
        primary_key_name = "order_id"
        super().__init__(connection, insert_query, select_query, update_query,
                         delete_query, select_all_query, count_query, primary_key_name)
        self.__select_all_with_join_query = ""
        self.__select_with_join_query = ""

    def get_extremum_shipping_cost(self):
        query = "SELECT min(shipping_cost)::numeric, max(shipping_cost)::numeric from orders"
        self._cursor.execute(query)
        row = self._cursor.fetchone()
        if row is not None and isinstance(row['max'], Decimal) and isinstance(row['min'], Decimal):
            return row['min'], row['max']
        else:
            raise Exception(f"No rows was found")

    @staticmethod
    def _get_item_from_row(row: dict):
        return Orders(row['recipients_date'], row['shipping_cost'], row['sender_ipn'], row['recipient_ipn'],
                      row['warehouse_id'], row['order_date'], row['order_id'])

    def _is_valid_item_dict(self, item: dict, pk_required: bool = True):
        return all(isinstance(item[column], int) for column in ['sender_ipn', 'recipient_ipn',
                                                                'warehouse_id']) \
               and isinstance(item['order_date'], (type(None), date)) and isinstance(item['recipients_date'], date) \
               and isinstance(item['shipping_cost'], Decimal) \
               and super()._is_valid_item_dict(item, pk_required)
