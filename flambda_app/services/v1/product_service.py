import datetime
import json

from flambda_app import helper
from flambda_app.enums import messages
from flambda_app.enums.messages import MessagesEnum
from flambda_app.exceptions import DatabaseException, ValidationException
from flambda_app.http_resources.request import ApiRequest
from flambda_app.logging import get_logger
from flambda_app.repositories.v1.mysql.product_repository import ProductRepository
from flambda_app.repositories.v1.redis.product_repository import ProductRepository as RedisProductRepository
from flambda_app.database.mysql import get_connection as mysql_get_connection
from flambda_app.database.redis import get_connection as redis_get_connection
from flambda_app.vos.product import ProductVO


class ProductService:
    DEBUG = False
    REDIS_ENABLED = False

    def __init__(self, logger=None, mysql_connection=None, redis_connection=None, product_repository=None,
                 redis_product_repository=None):
        # logger
        self.logger = logger if logger is None else get_logger()
        # database connection
        self.mysql_connection = mysql_connection if mysql_connection is not None else mysql_get_connection()
        # mysql repository
        self.product_repository = product_repository if product_repository is not None \
            else ProductRepository(mysql_connection=mysql_connection)

        # exception
        self.exception = None

        if self.REDIS_ENABLED:
            # redis connection
            self.redis_connection = redis_connection if redis_connection is not None else redis_get_connection()
            # redis repository
            self.redis_product_repository = redis_product_repository if redis_product_repository is not None \
                else RedisProductRepository(redis_connection=redis_connection)

        self.debug(self.DEBUG)

    def debug(self, flag: bool = False):
        self.DEBUG = flag
        self.product_repository.debug = self.DEBUG
        if self.REDIS_ENABLED:
            self.redis_product_repository.debug = self.DEBUG

    def list(self, request: ApiRequest):
        self.logger.info('method: {} - request: {}'
                         .format('list', request.to_json()))

        data = []
        where = request.where
        if where == dict():
            where = {
                'active': 1
            }

        try:
            data = self.product_repository.list(
                where=where, offset=request.offset, limit=request.limit, order_by=request.order_by,
                sort_by=request.sort_by, fields=request.fields)

            # convert to vo and prepare for api response
            if data:
                vo_data = []
                for item in data:
                    vo_data.append(ProductVO(item).to_api_response())
                data = vo_data

            # set exception if it happens
            if self.product_repository.get_exception():
                raise DatabaseException(MessagesEnum.LIST_ERROR)

        except Exception as err:
            self.logger.error(err)
            self.exception = err

        return data

    def count(self, request: ApiRequest):
        self.logger.info('method: {} - request: {}'
                         .format('count', request.to_json()))

        total = 0
        where = request.where
        if where == dict():
            where = {
                'active': 1
            }

        try:
            total = self.product_repository.count(
                where=where, order_by=request.order_by, sort_by=request.sort_by)
        except Exception as err:
            self.logger.error(err)
            self.exception = DatabaseException(MessagesEnum.LIST_ERROR)

        return total

    def get(self, request: ApiRequest, uuid):
        self.logger.info('method: {} - request: {}'
                         .format('get', request.to_json()))

        self.logger.info('method: {} - uuid: {}'
                         .format('get', uuid))

        data = []
        where = request.where

        try:
            value = uuid
            data = self.product_repository.get(
                value, key='uuid', where=where, fields=request.fields
            )

            if self.DEBUG:
                self.logger.info('data: {}'.format(data))

            # convert to vo and prepare for api response
            if data:
                data = ProductVO(data).to_api_response()

            # set exception if it happens
            if self.product_repository.get_exception():
                raise DatabaseException(MessagesEnum.FIND_ERROR)

        except Exception as err:
            self.logger.error(err)
            self.exception = err

        return data

    def create(self, request: ApiRequest):
        self.logger.info('method: {} - request: {}'.format('create', request.to_json()))

        data = request.where
        if self.DEBUG:
            self.logger.info('method: {} - data: {}'.format('create', data))

        try:

            if data == dict():
                raise ValidationException(MessagesEnum.REQUEST_ERROR)

            now = helper.datetime_now_with_timezone()
            product_vo = ProductVO(data)
            created = self.product_repository.create(product_vo)

            if created:
                # convert to vo and prepare for api response
                data = product_vo.to_api_response()
            else:
                data = None
                # set exception if it happens
                raise DatabaseException(MessagesEnum.CREATE_ERROR)

        except Exception as err:
            self.logger.error(err)
            self.exception = err

        return data
