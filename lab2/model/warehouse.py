from settings import is_valid_str
from model import BaseModel


class Warehouse:
    def __init__(self, city: str, office_number: str, warehouse_id: int = None):
        self.warehouse_id = warehouse_id
        self.city = city
        self.office_number = office_number

    def __str__(self):
        return f"Warehouse [warehouse_id={self.warehouse_id}, city={self.city}, " \
               f"office_number={self.office_number}]"

    @property
    def __dict__(self):
        return {'warehouse_id': self.warehouse_id, 'city': self.city,
                'office_number': self.office_number}

    @property
    def office_number(self):
        return self.__office_number

    @office_number.setter
    def office_number(self, office_number: str):
        self.__office_number = office_number[:15]


class WarehouseModel(BaseModel):
    def __init__(self, connection):
        insert_query = "INSERT INTO warehouses (city, office_number) " \
                       "VALUES (%(city)s, %(office_number)s) RETURNING warehouse_id"
        select_query = "SELECT * FROM warehouses WHERE warehouse_id = %s"
        update_query = "UPDATE warehouses SET city = %(city)s, " \
                       "office_number = %(office_number)s" \
                       "WHERE warehouse_id = %(warehouse_id)s"
        delete_query = "DELETE FROM warehouses WHERE warehouse_id = %s"
        select_all_query = "SELECT * FROM warehouses ORDER BY warehouse_id OFFSET %(offset)s LIMIT %(limit)s"
        count_query = "SELECT COUNT(*) FROM warehouses"
        primary_key_name = "warehouse_id"
        super().__init__(connection, insert_query, select_query, update_query,
                         delete_query, select_all_query, count_query, primary_key_name)

    def _is_valid_item_dict(self, item: dict, pk_required: bool = True):
        return is_valid_str(item['city']) \
               and is_valid_str(item['office_number']) \
               and super()._is_valid_item_dict(item, pk_required)

    @staticmethod
    def _get_item_from_row(row: dict):
        return Warehouse(row['city'], row['office_number'], row['warehouse_id'])
