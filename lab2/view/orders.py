from view import BaseView
from model.orders import Orders


class OrdersView(BaseView):
    @staticmethod
    def _item_to_text(item: object):
        if not isinstance(item, Orders):
            raise Exception('Item was not a type of Invoice')
        item_date_arrival = f'{item.order_date.strftime("%d.%m.%Y")}' if item.order_date is not None else '<empty>'
        return f'Num: {item.order_id}\nRecipients date: {item.recipients_date.strftime("%d.%m.%Y")}\n' \
               f'Order date: {item_date_arrival}\nShipping cost: {item.shipping_cost} ₴\n' \
               f'Sender IPN: {item.sender_ipn}\nRecipient IPN: {item.recipient_ipn}\n' \
               f'Warehouse departure number: {item.warehouse_id}'

    @staticmethod
    def _items_table_header():
        return ' #id | recipients date  | order date  | cost, ₴  | send#ipn| recp#ipn| w #id|'

    @staticmethod
    def _table_row_from_item(item: object):
        if not isinstance(item, Orders):
            raise Exception('Item was not a type of Invoice')
        item_date_arrival = f'{item.order_date.strftime("%d.%m.%Y")}' if item.order_date is not None else 'NULL'
        return f' {item.order_id:5}| {item.recipients_date.strftime("%d.%m.%Y")}| {item_date_arrival:10}|' \
               f' {item.shipping_cost:9}| {item.sender_ipn:8}| {item.recipient_ipn:8}|' \
               f' {item.warehouse_id:7}|'
