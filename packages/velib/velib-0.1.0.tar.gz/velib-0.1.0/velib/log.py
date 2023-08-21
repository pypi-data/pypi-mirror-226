import logging
#from logging.config import dictConfig
#from . telegram import AdminTelegramHandler

LOG_DIR =  '/logs'
APP_NAME = __name__


# dictConfig({
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(levelname)s] (%(name)s) %(message)s'
#         },
#         'custom1': {
#             'format': '%(asctime)s [%(levelname)s] (%(name)s.%(funcName)s:%(lineno)s) %(message)s'
#         },
#         'request': {
#             'format': '%(asctime)s [%(levelname)s] (%(name)s.%(funcName)s:%(lineno)s) %(message)s'
#         },

#     },
#     'handlers': {
#         'console': {
#             'level': 'ERROR',
#             'formatter': 'standard',
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://sys.stdout',  # Default is stderr
#         },
#         'app-debug': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '{0}/{1}-app.log'.format(LOG_DIR, APP_NAME),
#             'maxBytes': 1024 * 1024 * 10,  # 5 MB
#             'backupCount': 100,
#             'formatter': 'custom1',
#         },
#         'app-info': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '{0}/{1}-app.log'.format(LOG_DIR, APP_NAME),
#             'maxBytes': 1024 * 1024 * 10,  # 5 MB
#             'backupCount': 100,
#             'formatter': 'custom1',
#         },
#         'app-error': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '{0}/{1}-error.log'.format(LOG_DIR, APP_NAME),
#             'maxBytes': 1024 * 1024 * 10,  # 10 MB
#             'backupCount': 100,
#             'formatter': 'custom1',
#         },
#         'request': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '{0}/{1}-request.log'.format(LOG_DIR, APP_NAME),
#             'maxBytes': 1024 * 1024 * 10,  # 10 MB
#             'backupCount': 100,
#             'formatter': 'custom1',
#         },

#     },
#     'loggers': {
#         '': {
#             'handlers': ['console', 'app-debug', 'app-error', 'app-info'],
#             'level': 'NOTSET',
#             'propagate': False
#         },
#         'uvicorn': {
#             'handlers': ['request'],
#             'level': 'NOTSET',
#             'propagate': False
#         }
#     }

# })

log = logging.getLogger(APP_NAME)

#telegram = AdminTelegramHandler()
#telegram.setLevel(logging.ERROR)
#log.addHandler(telegram)

