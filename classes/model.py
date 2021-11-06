from numpy import ndarray
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics._scorer import make_scorer
from sklearn.metrics import matthews_corrcoef, precision_recall_fscore_support
from sklearn.preprocessing import StandardScaler

from utils.setup_logger import logger

from time import time

import numpy as np

class Model():
    """Classe que contém as definições do modelo de ML que será usado no projeto"""

    def __init__(self) -> None:
        pass
    
    def precision_0(y_true, y_pred, labels=None, average='binary', sample_weight=None):
        '''
        :param y_true:
        :param y_pred:
        :param labels:
        :param average:
        :param sample_weight:
        :return: calculate prec for neg class
        '''
        p, _, _, _ = precision_recall_fscore_support(y_true, y_pred,
                                                     beta=1,
                                                     labels=labels,
                                                     pos_label=0,
                                                     average=average,
                                                     warn_for=('f-score',),
                                                     sample_weight=sample_weight)
        return p

    def recall_0(y_true, y_pred, labels=None, average='binary', sample_weight=None):
        '''
        :param y_true:
        :param y_pred:
        :param labels:
        :param average:
        :param sample_weight:
        :return: calculate recall for neg class
        '''
        _, r, _, _ = precision_recall_fscore_support(y_true, y_pred,
                                                     beta=1,
                                                     labels=labels,
                                                     pos_label=0,
                                                     average=average,
                                                     warn_for=('f-score',),
                                                     sample_weight=sample_weight)
        return r

    def f1_0(y_true, y_pred, labels=None, average='binary', sample_weight=None):
        '''
        :param y_true:
        :param y_pred:
        :param labels:
        :param average:
        :param sample_weight:
        :return: calculate f1 for neg class
        '''
        _, _, f, _ = precision_recall_fscore_support(y_true, y_pred,
                                                     beta=1,
                                                     labels=labels,
                                                     pos_label=0,
                                                     average=average,
                                                     warn_for=('f-score',),
                                                     sample_weight=sample_weight)
        return f
    
    def grid_search(self, x, y):
        """Define o gridsearch para ser utilizado para valorar os melhores parâmetros para o modelo passado como parâmetro"""

        logger.info("Iniciando GridSearchCV para o modelo")

        time_init = time()

        model = SVC(probability=True)

        cross_valid = StratifiedKFold(n_splits=5)

        scoring = { 'auc_score': 'roc_auc',
                    'accuracy': 'accuracy',
                    'scores_p_1': 'precision',
                    'scores_r_1': 'recall',
                    'scores_f_1_1': 'f1',
                    'scores_p_0': make_scorer(Model.precision_0),
                    'scores_r_0': make_scorer(Model.recall_0),
                    'scores_f_1_0': make_scorer(Model.f1_0),
                    'mcc': make_scorer(matthews_corrcoef),
                    'precision_micro': 'precision_micro',
                    'precision_macro': 'precision_macro', 
                    'recall_macro': 'recall_macro',
                    'recall_micro': 'recall_micro', 
                    'f1_macro': 'f1_macro', 
                    'f1_micro': 'f1_micro'
                    }

        params = {  'kernel': ['rbf'],
                    'C': [1000, 500, 250, 100, 50, 25, 1, 0.1, 0.01, 0.001, 0.0001],
                    'gamma': [100, 10, 1, 0.1, 0.01, 0.001, 0.0001]
                    }
        

        grid_search = GridSearchCV(estimator=model,
                                   param_grid=params,
                                   scoring=scoring, 
                                   cv=cross_valid,
                                   refit='auc_score',
                                   n_jobs=-1, 
                                   verbose=3)

    
        grid_search.fit(x, y)

        time_end = time()

        logger.debug(f"Tempo gasto em segundos para executar o GridSearchCV: {time_end - time_init} segundos")
        logger.info("FInalizado GridSearchCV para o modelo")
        
        return grid_search

    def prepare_x_and_y(self, features: ndarray, target: list):
        """Método que irá transformar as features e os rótulos em objetos que podem ser interpretados pelo GridSearchCV"""
    
        logger.info("Iniciando preparação das features e dos rótulos passados como parâmetro")

        time_init = time()

        scaling = StandardScaler()
        scaling.fit(features[:,1:])
        x = scaling.transform(features[:,1:])

        y = np.array(target)

        time_end = time()

        logger.debug(f"Tempo gasto em segundos para realizar as tratativas das features e dos rótulos: {time_end - time_init} segundos")
        logger.info("Finalizada a preparação das features e dos rótulos")


        return x, y