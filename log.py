from logging.config import dictConfig
import logging
import os

path = "log/"
if not os.path.exists(path):
    os.makedirs(path)

dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/app.log',
            'formatter': 'default',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file', 'console']
    },
})

logger = logging.getLogger(__name__)