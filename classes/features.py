from utils.setup_logger import logger
from time import time

from pydpi.pypro import PyPro

import math
import numpy as np

class AAT():
    """ Classe Amino Acid Triplets (AAT)"""

    def __init__(self) -> None:
        pass

    def generate_aat_scale(self, pos_seq, neg_seq) -> dict:
        """Gera a escala de antigenicidade tripla entre as sequências positivas e negativas passadas como parâmetro"""

        logger.info("Iniciando a geração da escala de antigenicidade tripla dos aminoácidos.")

        time_init = time()

        # Inicialização das váriáveis para contagem dos trios de aminoácidos.
        pos_count = {}
        neg_count = {}

        # Inicialização das variáveis com todas as combinações possíveis de trios de aminoácidos.
        for i in ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                  'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']:
            for j in ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                      'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']:
                for k in ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                          'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']:
                    pos_count[i + j + k] = 1
                    neg_count[i + j + k] = 1

        # Inicialização das variáveis com o total combinações possíveis (20 x 20 x 20) entre os aminoácidos.
        # As inicializações feitas até aqui são necessárias para evitar problemas de divisões por 0 na sequência do código.
        pos_total = neg_total = 8000

        # Iteração de todas as sequências positivas para calcular a frequência do aparecimento de um determinado trio de aminoácidos. 
        for seq in pos_seq:

            # A iteração da sequência é feita com uma janela deslizante de tamanho 3
            for i in range(0, len(seq) - 3):
                tp = seq[i: i + 3]
                
                if 'X' in tp:
                    logger.info(f"A key {tp} contém um aminoácido inválido: X.")
                    continue
                
                try:
                    pos_count[tp] += 1
                    pos_total += 1
                except KeyError:
                    logger.error(f"A key {tp} não existe entre os trio de aminoácidos possíveis.")
                    continue
        
        # Iteração de todas as sequências positivas para calcular a frequência do aparecimento de um determinado trio de aminoácidos.
        for seq in neg_seq:

            # A iteração da sequência é feita com uma janela deslizante de tamanho 3
            for i in range(0, len(seq) - 3):
                tp = seq[i: i + 3]

                if 'X' in tp:
                    logger.info(f"A key {tp} contém um aminoácido inválido: X.")
                    continue
                
                try:
                    neg_count[tp] += 1
                    neg_total += 1
                except KeyError:
                    logger.error(f"A key {tp} não existe entre os trios de aminoácidos possíveis.")
                    continue
        
        # Definição da variável que irá conter toda a escala de antigenicidade para o dataset.
        aat_scale = {}

        # Geração da escala de antigenicidade para todas as possibilidades possíveis.
        # O uso da variável pos_count aqui é porque ela contém todas as possibilidades possíveis de trios de aminoácidos, como a variável neg_count
        # também tem.
        for i in pos_count.keys():
            try:

                # Cálculo da frequência do trio.
                pos_freq = (pos_count[i] / pos_total)
                neg_freq = (neg_count[i] / neg_total)

                # Log da razão entre a frequência positiva e a frequência negativa.
                aat_scale[i] = math.log(pos_freq/neg_freq)

            except KeyError:
                logger.error(f"A key {tp} não existe entre os trios de aminoácidos possíveis.")                
                continue

        # Cálculo do valor máximo entre todos os logs calculados para cada trio de aminoácido.
        raat_max = max(aat_scale.values())
        raat_min = min(aat_scale.values())

        # Para o cálculo da normalização é necessário a constante aqui calculada. Foi realizado dessa maneira para fins de performance, assim a aplicação
        # não precisa calcular o mesmo valor a cada iteração
        raat_constant = raat_max - raat_min

        # Normalização dos valores entre -1 e +1 para evitar o domínio de uma característica individual na aprendizagem do classificador
        for aat in aat_scale:
            aat_scale[aat] = 2 * ((aat_scale[aat] - raat_min)/raat_constant) - 1

        time_end = time()

        logger.debug(f"Tempo gasto em segundos para criar a escala de antigenicidade tripla do dataset: {time_end - time_init} segundos")
        logger.info("Finalizada a geração da escala de antigenicidade tripla dos aminoácidos.")
        
        return aat_scale

    def extract_aat_feature(self, dataset: list, aat_scale: dict) -> np.ndarray:
        """ Extraí a feature AAT para todo o dataset"""

        logger.info("Iniciando o calculo para extração da feature AAT do dataset")

        time_init = time()
        
        # Inicialização das variáveis para extrair a feature
        avg_aat = 0.0
        feature_list = []

        # Para cada peptídeo no dataset será realizada a extração da feature
        for peptideo in dataset:

            # Inicialização das variáveis para realizar o cálculo da média depois
            score = 0
            count = 0

            # Iteração da sequência em uma janela deslizante de tamanho 3
            for i in range(0, len(peptideo) - 3):
                try:
                    # Coleta o cálculo da escala de antigenicidade para determinada combinação de 3 aminoácidos.
                    score += float(aat_scale[peptideo[i:i + 3]])
                    count += 1
                except KeyError:
                    logger.error(f"A key {aat_scale[peptideo[i:i + 3]]} não existe!")
                    continue
            
            # Caso exista um problema e o count é diferente de 0 é realizado o cálculo da média, caso contrário a média é 0
            if count != 0:
                avg_aat = score / count
            else:
                avg_aat = 0

            # Adiciona a média calculada para a sequência na lista de cálculos do dataset
            feature_list.append(avg_aat)
        
        time_end = time()

        logger.debug(f"Tempo gasto em segundos para extrair a feature AAT do dataset: {time_end - time_init} segundos")
        logger.info("Finalizado o cálculo da feature AAT para o dataset.")

        return np.array(feature_list)
class AAP():
    """ Classe Amino Acid Pair (AAP)"""

    def __init__(self) -> None:
        pass

    def generate_aap_scale(self, pos_seq, neg_seq) -> dict:
        """Gera a escala de antigenicidade em par entre as sequências positivas e negativas passadas como parâmetro"""

        logger.info("Iniciando a geração da escala de antigenicidade em pares dos aminoácidos.")

        time_init = time()

        # Inicialização das váriáveis para contagem dos pares de aminoácidos.
        pos_count = {}
        neg_count = {}

        # Inicialização das variáveis com todas as combinações possíveis de pares de aminoácidos.
        for i in ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                  'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']:
            for j in ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                      'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']:
                pos_count[i + j] = 1
                neg_count[i + j] = 1

        # Inicialização das variáveis com o total combinações possíveis (20 x 20) entre os aminoácidos.
        # As inicializações feitas até aqui são necessárias para evitar problemas de divisões por 0 na sequência do código.
        pos_total = neg_total = 400

        # Iteração de todas as sequências positivas para calcular a frequência do aparecimento de um determinado par de aminoácidos. 
        for seq in pos_seq:

            # A iteração da sequência é feita com uma janela deslizante de tamanho 2
            for i in range(0, len(seq) - 2):
                tp = seq[i: i + 2]
                
                if 'X' in tp:
                    logger.info(f"A key {tp} contém um aminoácido inválido: X.")
                    continue
                
                try:
                    pos_count[tp] += 1
                    pos_total += 1
                except KeyError:
                    logger.error(f"A key {tp} não existe entre os pares de aminoácidos possíveis.")
                    continue
        
        # Iteração de todas as sequências positivas para calcular a frequência do aparecimento de um determinado par de aminoácidos.
        for seq in neg_seq:

            # A iteração da sequência é feita com uma janela deslizante de tamanho 2
            for i in range(0, len(seq) - 2):
                tp = seq[i: i + 2]

                if 'X' in tp:
                    logger.info(f"A key {tp} contém um aminoácido inválido: X.")
                    continue
                
                try:
                    neg_count[tp] += 1
                    neg_total += 1
                except KeyError:
                    logger.error(f"A key {tp} não existe entre os pares de aminoácidos possíveis.")
                    continue
        
        # Definição da variável que irá conter toda a escala de antigenicidade para o dataset.
        aap_scale = {}

        # Geração da escala de antigenicidade para todas as possibilidades possíveis.
        # O uso da variável pos_count aqui é porque ela contém todas as possibilidades possíveis de pares de aminoácidos, como a variável neg_count
        # também tem.
        for i in pos_count.keys():
            try:

                # Cálculo da frequência do trio.
                pos_freq = (pos_count[i] / pos_total)
                neg_freq = (neg_count[i] / neg_total)

                # Log da razão entre a frequência positiva e a frequência negativa.
                aap_scale[i] = math.log(pos_freq/neg_freq)

            except KeyError:
                logger.error(f"A key {tp} não existe entre os pares de aminoácidos possíveis.")                
                continue

        # Cálculo do valor máximo entre todos os logs calculados para cada par de aminoácido.
        raap_max = max(aap_scale.values())
        raap_min = min(aap_scale.values())

        # Para o cálculo da normalização é necessário a constante aqui calculada. Foi realizado dessa maneira para fins de performance, assim a aplicação
        # não precisa calcular o mesmo valor a cada iteração
        raap_constant = raap_max - raap_min

        # Normalização dos valores entre -1 e +1 para evitar o domínio de uma característica individual na aprendizagem do classificador
        for aap in aap_scale:
            aap_scale[aap] = 2 * ((aap_scale[aap] - raap_min)/raap_constant) - 1

        time_end = time()

        logger.debug(f"Tempo gasto em segundos para criar a escala de antigenicidade em pares do dataset: {time_end - time_init} segundos")
        logger.info("Finalizada a geração da escala de antigenicidade em pares dos aminoácidos.")
        
        return aap_scale

    def extract_aap_feature(self, dataset: list, aap_scale: dict) -> np.ndarray:
        """ Extraí a feature AAP para todo o dataset"""

        logger.info("Iniciando o calculo para extração da feature AAP do dataset")

        time_init = time()
        
        # Inicialização das variáveis para extrair a feature
        avg_aap = 0.0
        feature_list = []

        # Para cada peptídeo no dataset será realizada a extração da feature
        for peptideo in dataset:

            # Inicialização das variáveis para realizar o cálculo da média depois
            score = 0
            count = 0

            # Iteração da sequência em uma janela deslizante de tamanho 2
            for i in range(0, len(peptideo) - 2):
                try:
                    # Coleta o cálculo da escala de antigenicidade para determinada combinação de 2 aminoácidos.
                    score += float(aap_scale[peptideo[i:i + 2]])
                    count += 1
                except KeyError:
                    logger.error(f"A key {aap_scale[peptideo[i:i + 2]]} não existe!")
                    continue
            
            # Caso exista um problema e o count é diferente de 0 é realizado o cálculo da média, caso contrário a média é 0
            if count != 0:
                avg_aap = score / count
            else:
                avg_aap = 0

            # Adiciona a média calculada para a sequência na lista de cálculos do dataset
            feature_list.append(avg_aap)
        
        time_end = time()

        logger.debug(f"Tempo gasto em segundos para extrair a feature AAP do dataset: {time_end - time_init} segundos")
        logger.info("Finalizado o cálculo da feature AAP para o dataset.")

        return np.array(feature_list)

class AAC():
    """Classe Amino Acid Composition"""

    def __init__(self) -> None:
        self.pypro = PyPro()

    def extract_aac_feature(self, dataset: list) -> np.ndarray:

        logger.info("Iniciando o calculo para extração da feature AAC do dataset")

        time_init = time()

        feature_list = []

        for pep in dataset:
            self.pypro.ReadProteinSequence(pep)
            aac_feature = self.pypro.GetAAComp()
            print(list(aac_feature.values()))
            feature_list.append(list(aac_feature.values()))

        time_end = time()

        logger.debug(f"Tempo gasto em segundos para extrair a feature AAC do dataset: {time_end - time_init} segundos")
        logger.info("Finalizado o cálculo da feature AAC para o dataset.")

        return np.array(feature_list)