import unittest

from flambda_app.config import get_config
from flambda_app.database.mysql import MySQLConnector
from flambda_app.database.redis import RedisConnector
from flambda_app.logging import get_logger
from flambda_app.repositories.v1.mysql.product_repository import ProductRepository
from flambda_app.services.v1.healthcheck import HealthCheckResult
from flambda_app.services.v1.healthcheck.resources import MysqlConnectionHealthCheck, \
    RedisConnectionHealthCheck, \
    SelfConnectionHealthCheck
from flambda_app.services.v1.healthcheck_service import HealthCheckService
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.database.mysql_helper import MySQLHelper
from tests.unit.testutils import get_function_name


class HealthCheckServiceTestCase(BaseComponentTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseComponentTestCase.setUpClass()
        cls.CONFIG = get_config()
        cls.CONFIG.SQS_ENDPOINT = cls.SQS_LOCALSTACK

        # fixture
        if cls.EXECUTE_FIXTURE:
            logger = get_logger()

            logger.info("Fixture: MYSQL Database connection")
            logger.info("Fixture: drop table")

            mysql_connection = MySQLHelper.get_connection()
            database_name = ProductRepository.BASE_SCHEMA
            table_name = ProductRepository.BASE_TABLE
            cls.fixture_table(logger, mysql_connection, table_name, database_name)

            logger.info('Fixture: create sqs queue')

            queue_url = cls.CONFIG.APP_QUEUE
            cls.fixture_sqs(logger, queue_url)

    def setUp(self):
        super().setUp()
        self.config = get_config()
        self.mysql_connection = MySQLConnector().get_connection()
        self.redis_connection = RedisConnector().get_connection()
        self.service = HealthCheckService(self.logger, self.config)

    def test_add_check(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("MysqlConnection", MysqlConnectionHealthCheck(
            self.logger, self.config, self.mysql_connection), ["db"])

        result = self.service.get_result()
        self.logger.info(result)

        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_add_lambda_check(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("Lambda test", lambda: HealthCheckResult.healthy("test success"), ["lambda_test"])

        result = self.service.get_result()
        self.logger.info(result)

        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_add_multi_checks(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("self", SelfConnectionHealthCheck(self.logger, self.config), [])
        self.service.add_check("mysql", MysqlConnectionHealthCheck(
            self.logger, self.config, self.mysql_connection), ["db"])
        self.service.add_check("redis", RedisConnectionHealthCheck(
            self.logger, self.config, self.redis_connection), ["redis"])

        result = self.service.get_result()
        self.logger.info(result)

        self.assertIsInstance(result, dict)
        self.assertTrue('status' in result)

    def test_get_response(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.service.add_check("self", SelfConnectionHealthCheck(self.logger, self.config), [])
        self.service.add_check("mysql", MysqlConnectionHealthCheck(self.logger, self.config), ["db"])
        self.service.add_check("redis", RedisConnectionHealthCheck(self.logger, self.config), ["redis"])

        response = self.service.get_response()
        self.logger.info(response.data)
        self.assertIsNotNone(response.data)


if __name__ == '__main__':
    unittest.main()
