from _typeshed import NoneType
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

    def save_file(self, path_to_save: str, content_to_save: NoneType) -> None:
        """ Salva o conteúdo passado como parâmetro no path enviado como parâmetro"""

        logger.info(f"Iniciando o processo de salvamento do conteúdo passado em: {path_to_save}")

        time_init = time()

        file = None

        try:
            file = open(path_to_save, 'w+')
        except FileNotFoundError:
            logger.error(f"Houve um erro ao tentar acessar o arquivo em: \"{path_to_save}\"")
            sys.exit()

        try:
            file.write(content_to_save)
        except FileExistsError:
            logger.error(f"Houve um erro na tentativa de escrever no arquivo: \"{path_to_save}\"")
            sys.exit()
        
        time_end = time()

        logger.debug(f"Tempo gasto em segundos para escrever o arquivo {path_to_save}: {time_end - time_init} segundos")
        logger.info(f"Finalizada a escrita no arquivo: {path_to_save}")