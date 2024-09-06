import logging
import os
import sys
#import logging_loki

# Resolvendo as variáveis de ambiente

#Variáveis do multibanco
DB_HOST = os.getenv("DB_HOST") or os.getenv("DATABASE_HOST")#: :meta hide-value:
""":meta hide-value:
string: Module level variable documented inline.
"""

DB_PORT = int(os.getenv("DB_PORT","0") or os.getenv("DATABASE_PORT"))#: :meta hide-value:

DB_BASE = os.getenv("DB_BASE") or os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DB_USER") or os.getenv("DATABASE_USER")
DB_PASS = os.getenv("DB_PASS") or os.getenv("DATABASE_PASS")

if DB_HOST is None:
    raise Exception("Faltando variável de ambiente DB_HOST")
if DB_PORT is None:
    raise Exception("Faltando variável de ambiente DB_PORT")
if DB_BASE is None:
    raise Exception("Faltando variável de ambiente DB_BASE")
if DB_USER is None:
    raise Exception("Faltando variável de ambiente DB_USER")
if DB_PASS is None:
    raise Exception("Faltando variável de ambiente DB_PASS")

ENV = os.getenv("ENV", "DEV").upper()
GRAFANA_URL = os.getenv("GRAFANA_URL")
LOG_DEBUG = os.getenv("LOG_DEBUG", "False").upper() == "TRUE"

# WORKER_NAME=os.getenv("WORKER_NAME", "worker.py")

# MAX_PROCESSES=int(os.getenv("MAX_PROCESSES", "50"))
# MAX_PROCESSES=(1 if MAX_PROCESSES<=0 else MAX_PROCESSES)

# MAX_RETRY=int(os.getenv("MAX_RETRY", "10"))
# MAX_RETRY=(1 if MAX_RETRY<=0 else MAX_RETRY)

APP_NAME='multi-database-adapter'

# Configurando o logger
logger = logging.getLogger(APP_NAME)
if LOG_DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# if GRAFANA_URL is not None and GRAFANA_URL.strip() != "":
#     loki_handler = logging_loki.LokiHandler(
#         url=GRAFANA_URL,
#         tags={ENV.upper() + f"_{APP_NAME}_": ENV.lower() + "_log"},
#         version="1",
#     )
#     loki_handler.setFormatter(log_format)
#     logger.addHandler(loki_handler)