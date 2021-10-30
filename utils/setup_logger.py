import logging

"""Definições básicas para o logger da aplicação"""

formatter = '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=formatter)
logger = logging.getLogger('default_logger')