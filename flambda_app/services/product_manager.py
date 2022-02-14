from flambda_app.config import get_config
from flambda_app.http_resources.request import ApiRequest
from flambda_app.logging import get_logger
from flambda_app.services.v1.product_service import ProductService as ProductServiceV1


class ProductManager:
    def __init__(self, logger=None, config=None, product_service=None):
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # service
        self.product_service = product_service if product_service is not None else ProductServiceV1(self.logger)

        # exception
        self.exception = None

    def debug(self, flag: bool = False):
        self.DEBUG = flag
        self.product_service.debug(self.DEBUG)

    def list(self, request: ApiRequest):
        data = self.product_service.list(request)
        if (data is None or len(data) == 0) and self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return data

    def count(self, request: ApiRequest):
        total = self.product_service.count(request)
        if self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return total

    def get(self, request: ApiRequest, uuid):
        data = self.product_service.get(request, uuid)
        if (data is None or len(data) == 0) and self.product_service.exception:
            self.exception = self.product_service.exception
            raise self.exception
        return data

    def create(self):
        pass

    def soft_update(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
