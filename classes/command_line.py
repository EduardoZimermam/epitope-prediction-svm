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

        ap.add_argument("-d", "--dataset-name", required=True,
            help="Nome do dataset que está sendo usado para realizar o treinamento do modelo")
        
        ap.add_argument("-r", "--result-path", required=True,
            help="Caminho completo onde será salvo o resultado do GridSearchCV")
        
        ap.add_argument("-at", "--aat-feature", action='store_true',
            help="Quando esse parâmetro está selecionado será utilizada a feature AAT (Amino Acid Triplets)")
        
        ap.add_argument("-ap", "--aap-feature", action='store_true',
            help="Quando esse parâmetro está selecionado será utilizada a feature AAP (Amino Acid Pair)")
      
        ap.add_argument("-ac", "--aac-feature", action='store_true',
            help="Quando esse parâmetro está selecionado será utilizada a feature AAC (Amino Acid Composition)")

        ap.add_argument("-pv", "--protvec-feature", action='store_true',
            help="Quando esse parâmetro está selecionado será utilizada a feature ProtVec")

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

        return arg_value.strip() if type(arg_value) == str else arg_value 