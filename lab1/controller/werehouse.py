from controller import BaseController
from model.warehouse import WarehouseModel, Warehouse
from view.warehouse import WarehouseView


class WarehouseController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(WarehouseModel(connection), WarehouseView('warehouses', view_driver))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['City', 'Office number']
        values = [item.city, item.office_number] \
            if isinstance(item, Warehouse) else None
        return prompts, values

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        city = office_number = None
        for item in input_items:
            if item['name'] == 'City':
                city = item['value']
            elif item['name'] == 'Office number':
                office_number = item['value']
        return Warehouse(city, office_number)
