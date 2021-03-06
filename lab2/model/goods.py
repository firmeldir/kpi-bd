from settings import is_valid_str
from model import BaseModel


class Goods:
    def __init__(self, height: int, width: int, depth: int, weight: int,
                 order_id: int,  description: str = None, good_id: int = None):
        self.good_id = good_id
        self.height = height
        self.width = width
        self.depth = depth
        self.weight = weight
        self.description = description
        self.order_id = order_id

    def __str__(self):
        return f"Goods [good_id={self.good_id}, height={self.height}, width={self.width}, depth={self.depth}, " \
               f"weight={self.weight}, description={self.description}, order_id={self.order_id}]"


class GoodsModel(BaseModel):
    def __init__(self, connection):
        insert_query = "INSERT INTO goods (height, width, depth, weight, description, order_id) " \
                       "VALUES (%(height)s, %(width)s, %(depth)s, %(weight)s, %(description)s, %(order_id)s)" \
                       "RETURNING good_id"
        select_query = "SELECT * FROM goods WHERE good_id = %s"
        update_query = "UPDATE goods SET height = %(height)s, width = %(width)s, depth = %(depth)s, " \
                       "weight = %(weight)s, description = %(description)s, order_id = %(order_id)s " \
                       "WHERE good_id = %(good_id)s"
        delete_query = "DELETE FROM goods WHERE good_id = %s"
        select_all_query = "SELECT * FROM goods ORDER BY good_id OFFSET %(offset)s LIMIT %(limit)s"
        count_query = "SELECT COUNT(*) FROM goods"
        primary_key_name = "good_id"
        super().__init__(connection, insert_query, select_query, update_query,
                         delete_query, select_all_query, count_query, primary_key_name)

    def _is_valid_item_dict(self, item: dict, pk_required: bool = True):
        return all(isinstance(item[column], int) for column in ['height', 'width', 'depth',
                                                                'weight', 'order_id']) \
               and (item['description'] is None or is_valid_str(item['description'])) \
               and super()._is_valid_item_dict(item, pk_required)

    @staticmethod
    def _get_item_from_row(row: dict):
        return Goods(row['height'], row['width'], row['depth'], row['weight'],
                     row['order_id'], row['description'], row['good_id'])
