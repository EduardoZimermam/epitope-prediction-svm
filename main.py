from classes.features import AAP, AAT
from classes.command_line import Cli
from classes.file import File
from utils.setup_logger import logger

from time import time

# Definição para inicializar a Interface de linha de comando
cli = Cli()

# Definição para iniciar o manipulador de arquivos
file_handler = File()


if __name__=='__main__':
    logger.info("Iniciando aplicação")

    time_init = time()

    # Buscando o caminho completo dos arquivos de peptídeos passado como parâmetro
    positive_file = cli.get_arg_from_cli('positive_file')
    negative_file = cli.get_arg_from_cli('negative_file')

    # Nome do dataset para salvar os dicionários de antigenicidade
    dataset_name = cli.get_arg_from_cli('dataset_name')

    # Realização da leitura dos arquivos com as sequências de peptídeos
    positive_sequences = file_handler.get_sequences_from_file(positive_file)
    negative_sequences = file_handler.get_sequences_from_file(negative_file)

    # Removação das variáveis que apontam para os arquivos de sequência
    # A partir desse ponto do código, apenas as variáveis com as sequências serão utilizadas
    del positive_file
    del negative_file

    # Inicializa a classe AAT
    aat = AAT()

    # Inicializa a classe AAP
    aap = AAP()

    # Realiza a criação dos arquivos com a escala AAT para as sequências passadas como parâmetro
    aat_scale = aat.generate_aat_scale(positive_sequences, negative_sequences)

    # Realiza a criação dos arquivos com a escala AAP para as sequências passadas como parâmetro
    aap_scale = aap.generate_aap_scale(positive_sequences, negative_sequences)

    time_end = time()

    logger.debug(f"Tempo gasto em segundos para executar toda a aplicação: {time_end - time_init} segundos")
    logger.info("Aplicação finalizada")
