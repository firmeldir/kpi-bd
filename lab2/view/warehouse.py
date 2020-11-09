from view import BaseView
from model.warehouse import Warehouse


class WarehouseView(BaseView):
    @staticmethod
    def _item_to_text(item: object):
        if not isinstance(item, Warehouse):
            raise Exception('Item was not a type of Warehouse')
        return f'Id: {item.warehouse_id}\nCity: {item.city}\nOffice number: {item.office_number}\n'

    @staticmethod
    def _items_table_header():
        return ' #id  | city                         | office number|'

    @staticmethod
    def _table_row_from_item(item: object):
        if not isinstance(item, Warehouse):
            raise Exception('Item was not a type of Warehouse')
        return f' {item.warehouse_id:6}| {item.city:32.32}| {item.office_number}|'
