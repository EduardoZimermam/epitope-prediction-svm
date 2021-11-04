import sys
import json
import os
import errno

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

    def save_dict_in_file(self, path_to_save: str, content_to_save: dict) -> None:
        """ Salva o conteúdo passado como parâmetro no path enviado como parâmetro"""

        logger.info(f"Iniciando o processo de salvamento do conteúdo passado em: {path_to_save}")

        time_init = time()

        file = None

        # Verifica se precisa criar o diretório antes de salvar o arquivo
        if not os.path.exists(os.path.dirname(path_to_save)):
            try:
                # Cria o diretório para salvar o arquivo se necessário
                os.makedirs(os.path.dirname(path_to_save))
            except OSError as exc: # Guarda contra condições de corrida
                if exc.errno != errno.EEXIST:
                    raise

        try:
            file = open(path_to_save, 'w+')
        except FileNotFoundError as e:
            logger.error(f"Houve um erro ao tentar acessar o arquivo em: \"{path_to_save}\"")
            sys.exit()

        try:
            file.write(json.dumps(content_to_save))
        except FileExistsError:
            logger.error(f"Houve um erro na tentativa de escrever no arquivo: \"{path_to_save}\"")
            sys.exit()

        # Fecha o arquivo para ser salvo
        file.close()
        
        time_end = time()

        logger.debug(f"Tempo gasto em segundos para escrever o arquivo {path_to_save}: {time_end - time_init} segundos")
        logger.info(f"Finalizada a escrita no arquivo: {path_to_save}")