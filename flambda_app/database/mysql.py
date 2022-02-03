from time import sleep



from flambda_app.config import get_config
from flambda_app.logging import get_logger
import pymysql

logger = get_logger()

_CONNECTION = False
_RETRY_COUNT = 0
_MAX_RETRY_ATTEMPTS = 3


def reset():
    global _CONNECTION
    _CONNECTION = False


# TODO aplicar class aos moldes da pasta aws
def get_connection(config=None, connect=True, retry=False):
    global _CONNECTION, _RETRY_COUNT, _MAX_RETRY_ATTEMPTS
    if not _CONNECTION:
        connection = None
        if config is None:
            config = get_config()
        try:
            params = {
                'host': config.DB_HOST,
                'user': config.DB_USER,
                'password': config.DB_PASSWORD,
                'db': config.DB
            }

            connection = pymysql.connect(host=params['host'],
                                         user=params['user'],
                                         password=params['password'],
                                         database=params['db'],
                                         cursorclass=pymysql.cursors.DictCursor)
            if connect:
                connection.connect()
            _CONNECTION = connection
            _RETRY_COUNT = 0
            logger.info('Connected')
        except Exception as err:
            if _RETRY_COUNT == _MAX_RETRY_ATTEMPTS:
                _RETRY_COUNT = 0
                logger.error(err)
                connection = None
                return connection
            else:
                logger.error(err)
                logger.info('Trying to reconnect... {}'.format(_RETRY_COUNT))

                sleep(0.1)
                # retry
                if not retry:
                    _RETRY_COUNT += 1
                    # Fix para tratar diff entre docker/local
                    if config.DB_HOST == 'mysql':
                        old_value = config.DB_HOST
                        config.DB_HOST = 'localhost'
                        logger.info(
                            'Changing the endpoint from {} to {}'.format(old_value, config.DB_HOST))
                    return get_connection(config, True)
    else:
        connection = _CONNECTION

    return connection
