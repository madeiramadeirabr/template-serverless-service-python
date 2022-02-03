from gevent.pywsgi import WSGIServer
from app import APP

http_server = WSGIServer(('0.0.0.0', 5000), APP)
http_server.serve_forever()
