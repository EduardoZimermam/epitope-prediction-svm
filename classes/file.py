
import sys

from utils.setup_logger import logger


class File():
    """ Classe para manipulação de arquivos"""

    def __init__(self) -> None:
        pass

    def get_sequences_from_file(self, seq_file: str) -> list:
        """ Retorna uma lista de peptídeos a partir do arquivo enviado como parâmetro"""

        logger.debug(f"Iniciando a leitura das sequências de peptídeos do arquivo: {seq_file}")

        file = None
        sequences = []

        try:
            file = open(seq_file, 'r')
        except FileNotFoundError:
            logger.error(f"O arquivo \"{seq_file}\" não foi encontrado!")
            sys.exit()

        for line in file.readlines():
            sequences.append(line)

        logger.debug(f"Finalizada a leitura das sequências de peptídeos do arquivo: {seq_file}")
        
        return sequences