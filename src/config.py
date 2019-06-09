import os

CN_CLOUD_NAME = None
CN_API_KEY = None
CN_API_SECRET = None
EMAIL = None
PASSWORD = None
PORT = None
URI = None
DEBUG = True


if os.environ['environment'] != 'production':
    import src.config_local as config_local
    CN_CLOUD_NAME = config_local.CN_CLOUD_NAME
    CN_API_KEY = config_local.CN_API_KEY
    CN_API_SECRET = config_local.CN_API_SECRET
    EMAIL = config_local.EMAIL
    PASSWORD = config_local.PASSWORD
    PORT = config_local.PORT
    URI = config_local.URI

else:
    import src.config_server as config_server
    CN_CLOUD_NAME = config_server.CN_CLOUD_NAME
    CN_API_KEY = config_server.CN_API_KEY
    CN_API_SECRET = config_server.CN_API_SECRET
    EMAIL = config_server.EMAIL
    PASSWORD = config_server.PASSWORD
    PORT = config_server.PORT
    URI = config_server.URI
