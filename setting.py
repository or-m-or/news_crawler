import logging
import logging.config
import sys

NO_KEY = "no key"

settings = {
    "config":{
        "env":{
            "OPENAI_API_KEY":"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"
        }
    },
    "logger": {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "complex": {
                "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d]\n%(message)s"
            },
            "simple": {
                "datefmt":"%H:%M:%S",
                "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)d] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": "DEBUG",
                "stream": "ext://sys.stdout"
            },
            "app": {
                "backupCount": 20,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "./logs/index.log",
                "encoding": "utf-8",
                "formatter": "complex",
                "level": "DEBUG",
                "maxBytes": 10485760
            }
        },
        "root": {
            "handlers": ["console", "app"],
            "level": "INFO"
        },
        "loggers": {
            "rb_faq_index": {
                "level": "DEBUG"
            },
            "llama_index": {
                "level": "DEBUG"        
            },
            "tests": {
                "level": "DEBUG"
            }      
        }
    }
}

config, logger = settings['config'], settings["logger"]

package_name = "crawler_test" # 이름 바꾸기
logger_prefix = f"{package_name}." if sys.modules['__main__'].__package__ is None else '' # 찾아보기

logging.config.dictConfig(logger) # 찾아보기

class Logger:
    def __new__(cls, name:str):
      return logging.getLogger(f"{logger_prefix}{name}")

    @staticmethod
    def exception(*args, **kwargs): 
      kwargs.get()
      logging.exception(*args, **kwargs)


def env(key, default=NO_KEY):
    return config['env'].get(key, default)