import logging
import os
import random
import string
import unittest

from boot import reset, load_dot_env, load_env
from flambda_app.config import reset as reset_config, get_config
from flambda_app.helper import get_function_name as get_fn

def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def get_function_name(class_name=""):
    return get_fn(class_name)


class BaseUnitTestCase(unittest.TestCase):
    SQS_LOCALSTACK = 'http://localhost:4566'
    REDIS_LOCALSTACK = 'localhost'
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        # pass
        # reset config and env
        reset()
        reset_config()
        # load integration
        APP_TYPE = os.environ['APP_TYPE']
        if APP_TYPE == 'Flask':
            load_dot_env()
        else:
            load_env()

        cls.CONFIG = get_config()

    """
    Classe base para testes de unidade
    """

    def setUp(self):
        log_name = 'unit_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.DEBUG)
        self.logger = logging.getLogger(log_name)