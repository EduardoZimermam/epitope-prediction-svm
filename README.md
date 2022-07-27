# epitope-prediction-svm

Este projeto faz parte do trabalho de conclusão do curso de Informática Biomédica ofertado pela Universidade Federal do Paraná (UFPR).

Este trabalho consistem em um modelo de machine learning baseado em Support Vector Machine (SVM) para a predição de epítopos em vírus. Mais detalhes sobre os arquivos que estão contidos neste repositório serão abordados na sequência deste documento.

### Autores do trabalho
- Annelyse Schatzmann (:octocat: [Schatzmann](https://github.com/Schatzmann))  
- Eduardo Zimermam Pereira (:octocat: [EduardoZimermam](https://github.com/EduardoZimermam))

### Orientador
- Profº Dr. Eduardo Jaques Spinosa

## Dependências do projeto

Neste projeto são utilizadas bibliotecas externas e trechos de códigos que foram implementados por diferentes pessoas. A seguir você irá encontrar um compilado sobre cada recurso utilizado que não foi diretamente implementado pelos [autores deste trabalho](#autores-do-trabalho).
### Arquivos binário para representação de proteínas pelo método ProtVec
Antes de iniciar os testes com este trabalho, você deverá executar o comando abaixo. A execução irá resultar na criação de um diretório chamado protvec onde em seu interior irá conter um arquivo com 2,6GB de dados. Este arquivo é a representação de proteínas para extração da feature ProtVec e torna-se necessária ao tentar ser utilizada essa feature para o seu dataset.

:warning: **IMPORTANTE** :warning:  
Este passo é obrigatório se você utilizar a feature ProtVec. Não mude o diretório onde será realizado o download e só execute o comando abaixo dentro deste repositório, onde está o README.md do projeto. O caminho para este arquivo está fixado no código e alterar o arquivo de lugar irá fazer com que o algoritmo não desempenhe a função esperada.

```
wget http://deepbio.info/embedding_repo/sp_sequences_4mers_vec.txt -P protvec/
