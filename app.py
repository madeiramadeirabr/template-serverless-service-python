"""This is the main file of the lambda application

This module contains the handler method
"""
import boot
import os
import base64
from flambda_app.services.v1.healthcheck import HealthCheckSchema, HealthCheckResult
from flambda_app.services.v1.healthcheck.resources import \
    MysqlConnectionHealthCheck, RedisConnectionHealthCheck, \
    SQSConnectionHealthCheck, SelfConnectionHealthCheck
from flambda_app.services.v1.healthcheck_service import HealthCheckService
from flambda_app.config import get_config
from flambda_app.enums.events import EventType
from flambda_app.enums.messages import MessagesEnum
from flambda_app.events.tracker import EventTracker
from flambda_app.exceptions import ApiException
from flambda_app.http_resources.request import ApiRequest
from flambda_app.http_resources.response import ApiResponse
from flambda_app.vos.events import EventVO
from flambda_app.logging import get_logger
from flambda_app import APP_NAME, APP_VERSION, http_helper
from flambda_app.helper import open_vendor_file, print_routes
from flambda_app.http_helper import CUSTOM_DEFAULT_HEADERS
from flambda_app.flambda import Flambda
from flambda_app.openapi import spec, get_doc, generate_openapi_yml
from flambda_app.openapi import api_schemas
from flambda_app import helper

# load env
ENV = helper.get_environment()
boot.load_dot_env(ENV)

# config
CONFIG = get_config()
# debug
DEBUG = helper.debug_mode()
# logger
LOGGER = get_logger()

APP = Flambda(__name__)


@APP.route('/')
def index():
    """
    API Root path
    :return:
    :rtype: str
    """
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    return http_helper.create_response(body=body, status_code=200)


# general vars
APP_QUEUE = CONFIG.APP_QUEUE


@APP.route('/alive')
def alive():
    """
    Health check path
    :return:
    :rtype: str

    ---

        get:
            summary: Service Health Method
            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: HealthCheckSchema
        """
    service = HealthCheckService()
    service.add_check("self", SelfConnectionHealthCheck(LOGGER, CONFIG), [])
    service.add_check(
        "mysql", MysqlConnectionHealthCheck(LOGGER, CONFIG), ["db"])
    service.add_check("redis", RedisConnectionHealthCheck(
        LOGGER, CONFIG), ["redis"])
    service.add_check("queue", SQSConnectionHealthCheck(
        LOGGER, CONFIG), ["queue"])
    service.add_check("internal", lambda: HealthCheckResult.healthy("connect"), ["example"])

    return service.get_response()


@APP.route('/favicon-32x32.png')
def favicon():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "image/png"
    data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAkFBMVEUAAAAQM0QWNUYWNkYXNkYALjo'
        'WNUYYOEUXN0YaPEUPMUAUM0QVNUYWNkYWNUYWNUUWNUYVNEYWNkYWNUYWM0eF6i0XNkchR0OB5SwzZj'
        '9wyTEvXkA3az5apTZ+4C5DgDt31C9frjU5bz5uxTI/eDxzzjAmT0IsWUEeQkVltzR62S6D6CxIhzpKi'
        'jpJiDpOkDl4b43lAAAAFXRSTlMAFc304QeZ/vj+ECB3xKlGilPXvS2Ka/h0AAABfklEQVR42oVT2XaC'
        'MBAdJRAi7pYJa2QHxbb//3ctSSAUPfa+THLmzj4DBvZpvyauS9b7kw3PWDkWsrD6fFQhQ9dZLfVbC5M'
        '88CWCPERr+8fLZodJ5M8QJbjbGL1H2M1fIGfEm+wJN+bGCSc6EXtNS/8FSrq2VX6YDv++XLpJ8SgDWM'
        'nwqznGo6alcTbIxB2CHKn8VFikk2mMV2lEnV+CJd9+jJlxXmMr5dW14YCqwgbFpO8FNvJxwwM4TPWPo'
        '5QalEsRMAcusXpi58/QUEWPL0AK1ThM5oQCUyXPoPINkdd922VBw4XgTV9zDGWWFrgjIQs4vwvOg6xr'
        '+6gbCTqE+DYhlMGX0CF2OknK5gQ2JrkDh/W6TOEbYDeVecKbJtyNXiCfGmW7V93J2hDus1bDfhxWbIZ'
        'VYDXITA7Lo6E0Ktgg9eB4KWuR44aj7ppBVPazhQH7/M/KgWe9X1qAg8XypT6nxIMJH+T94QCsLvj29I'
        'YwZxyO9/F8vCbO9tX5/wDGjEZ7vrgFZwAAAABJRU5ErkJggg==')
    return http_helper.create_response(
        body=data, status_code=200, headers=headers)


@APP.route('/docs')
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/html"
    html_file = open_vendor_file('./public/swagger/index.html', 'r')
    html = html_file.read()
    return http_helper.create_response(
        body=html, status_code=200, headers=headers)


@APP.route('/openapi.yml')
def openapi():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/yaml"
    html_file = open_vendor_file('./public/swagger/openapi.yml', 'r')
    html = html_file.read()
    return http_helper.create_response(
        body=html, status_code=200, headers=headers)


# doc
spec.path(view=alive, path="/alive", operations=get_doc(alive))

print_routes(APP, LOGGER)
LOGGER.info('Running at {}'.format(os.environ['APP_ENV']))

# generate de openapi.yml
generate_openapi_yml(spec, LOGGER, force=True)
