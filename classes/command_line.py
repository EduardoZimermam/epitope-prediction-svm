import argparse

from utils.setup_logger import logger

class Cli():
    """Define a classe para gerenciar a linha de comando"""

    def __init__(self) -> None:
        """ Inicialização da linha de comando """

        ap = argparse.ArgumentParser()

        ap.add_argument("-p", "--positive-file", required=True,
            help="Caminho completo para o arquivo que contém as sequências de aminoácido positivas")

        ap.add_argument("-n", "--negative-file", required=True,
            help="Caminho completo para o arquivo que contém as sequências de aminoácido negativas")
      
        args = vars(ap.parse_args())

        self.argparse = args

    def get_arg_from_cli(self, arg_flag: str) -> str:
        """ Retorna o valor de um argumento caso a flag passada esteja presente na linha de comando"""

        logger.debug(f"Buscando argumento com a flag: {arg_flag}")
        
        arg_value = ''

        try:
            arg_value = self.argparse[arg_flag]
        except NameError:
            logger.error("Argumento não encontrado!")

        return arg_value.strip()