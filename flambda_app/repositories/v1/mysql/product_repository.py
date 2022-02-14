from datetime import datetime

from flambda_app.http_resources.request_control import Order, Pagination, PaginationType
from flambda_app.repositories.v1.mysql import AbstractRepository
from flambda_app.vos.product import ProductVO


class ProductRepository(AbstractRepository):
    BASE_TABLE = 'products'
    BASE_SCHEMA = 'store'
    BASE_TABLE_ALIAS = 'p'
    PK = 'id'

    def __init__(self, logger=None, mysql_connection=None):
        super().__init__(logger, mysql_connection)

    def create(self, product: ProductVO):

        keys = list(product.keys())
        # remove the PK
        keys.remove(self.PK)
        keys_str = ",".join(keys)
        values_count = len(product.values()) - 1
        values_str = ",".join(['%s' for i in range(0, values_count)])

        # query
        sql = "INSERT INTO {} ({}) VALUES ({})".format(self.BASE_TABLE, keys_str, values_str)

        product_dict = product.to_dict()
        del product_dict["id"]
        values = tuple(product_dict.values())

        # try to create
        try:
            created = self._execute(sql, values)
            # get last inserted id
            product.id = self.connection.insert_id()
            # commit
            self.connection.commit()

        except Exception as err:
            self.logger.error(err)
            self.connection.rollback()
            self._exception = err
            created = False
        finally:
            self._close()

        return created

    def get(self, value, key=None, where=dict, fields: list = None):
        key_type = '%s'
        if key is None:
            key = self.PK

        if fields is None or len(fields) == 0:
            fields = '*'
        else:
            fields = [self.BASE_TABLE_ALIAS + '.' + v for v in fields]
            fields = ",".join(fields)

        sql = "SELECT {} FROM {} as {} WHERE {} = {}".format(fields, self.BASE_TABLE, self.BASE_TABLE_ALIAS, key,
                                                             key_type)

        if where != dict():
            where_list = [
                '{} = {}'.format(self.BASE_TABLE_ALIAS + "." + k, '"{}"'.format(v) if isinstance(v, str) else v) for
                k, v in where.items()]
            where_str = ",".join(where_list)

            sql = sql + " AND {}".format(where_str)

        try:
            result = self._execute(sql, value)

            item = result.fetchone()
        except Exception as err:
            self.logger.error(err)
            item = None
        finally:
            self._close()

        return item

    def list(self, where: dict, offset=None, limit=None, fields: list = None, sort_by=None, order_by=None):

        if fields is None or len(fields) == 0:
            fields = '*'
        else:
            fields = [self.BASE_TABLE_ALIAS + '.' + v for v in fields]
            fields = ",".join(fields)

        if order_by is None:
            order_by = Order.ASC

        if sort_by is None:
            sort_by = self.PK
        elif isinstance(sort_by, list):
            sort_by_arr = []
            for v in sort_by:
                sort_by_arr.append(self.BASE_TABLE_ALIAS + '.' + v)
            sort_by = ",".join(sort_by_arr)
        else:
            sort_by = self.BASE_TABLE_ALIAS + '.' + sort_by

        sql = "SELECT {} FROM {} as {}".format(fields, self.BASE_TABLE, self.BASE_TABLE_ALIAS)

        if where != dict():
            where_list = [
                '{} = {}'.format(self.BASE_TABLE_ALIAS + "." + k, '"{}"'.format(v) if isinstance(v, str) else v) for
                k, v in where.items()]
            where_str = ",".join(where_list)

            sql = sql + " WHERE {}".format(where_str)

        sql = sql + " ORDER BY {} {}".format(sort_by, order_by)

        if not offset:
            offset = Pagination.validate(PaginationType.OFFSET, offset)

        if not limit:
            limit = Pagination.validate(PaginationType.LIMIT, limit)

        sql = sql + " LIMIT {},{}".format(offset, limit)

        try:
            result = self._execute(sql)
            result = result.fetchall()
        except Exception as err:
            self.logger.error(err)
            self._exception = err
            result = None
        finally:
            self._close()

        return result

    def count(self, where, sort_by=None, order_by=None):
        if order_by is None:
            order_by = Order.ASC

        if sort_by is None:
            sort_by = self.PK
        elif isinstance(sort_by, list):
            sort_by_arr = []
            for v in sort_by:
                sort_by_arr.append(self.BASE_TABLE_ALIAS + '.' + v)
            sort_by = ",".join(sort_by_arr)
        else:
            sort_by = self.BASE_TABLE_ALIAS + '.' + sort_by

        sql = "SELECT COUNT(1) as total FROM {} as {}".format(self.BASE_TABLE, self.BASE_TABLE_ALIAS)

        if where != dict():
            where_list = [
                '{} = {}'.format(self.BASE_TABLE_ALIAS + "." + k, '"{}"'.format(v) if isinstance(v, str) else v) for
                k, v in where.items()]
            where_str = ",".join(where_list)

            sql = sql + " WHERE {}".format(where_str)

        sql = sql + " ORDER BY {} {}".format(sort_by, order_by)

        try:
            result = self._execute(sql)
            result = result.fetchone()
            result = result['total']
        except Exception as err:
            self.logger.error(err)
            self._exception = err
            result = 0
        finally:
            self._close()

        return result

    def soft_delete(self, sku_parent):
        sql = "UPDATE {}.{} SET deleted_at = %s WHERE sku_parent = %s" \
            .format(self.BASE_SCHEMA, self.BASE_TABLE)

        data = (datetime.today(), sku_parent,)
        try:
            result = self._execute(sql, data)
            self.connection.commit()
        except Exception as err:
            self.logger.error("SQL: {} ".format(sql))
            self.logger.error("Params: {} ".format(data))
            self.logger.error(err)
            result = None
            self.connection.rollback()
        finally:
            self._close()

        return result
