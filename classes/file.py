import sys

from utils.setup_logger import logger
from time import time

class File():
    """ Classe para manipulação de arquivos"""

    def __init__(self) -> None:
        pass

    def get_sequences_from_file(self, seq_file: str) -> list:
        """ Retorna uma lista de peptídeos em upper case a partir do arquivo enviado como parâmetro"""

        logger.info(f"Iniciando a leitura das sequências de peptídeos do arquivo: {seq_file}")

        time_init = time()

        file = None
        sequences = []

        try:
            file = open(seq_file, 'r')
        except FileNotFoundError:
            logger.error(f"O arquivo \"{seq_file}\" não foi encontrado!")
            sys.exit()

        for line in file.readlines():
            sequences.append(line.strip().upper())

        time_end = time()

        logger.debug(f"Tempo gasto em segundos para ler todas as sequências do arquivo {seq_file}: {time_end - time_init} segundos")
        logger.info(f"Finalizada a leitura das sequências de peptídeos do arquivo: {seq_file}")

        return sequences