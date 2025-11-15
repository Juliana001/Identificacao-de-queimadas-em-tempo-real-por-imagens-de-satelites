DATA: 01/09/2025 - . (previsão de conclusão :31/10/2025)

OBJETIVO:  Compreender o estado da arte em detecção e monitoramento de queimadas por sensoriamento remoto, identificar as principais técnicas, algoritmos e plataformas utilizadas, e levantar dados de satélite e informações auxiliares relevantes para a área de estudo.

ATIVIDADES REALIZADAS: Revisão bibliográfica e levantamento dos dados existentes.

RESULTADOS / ACHADOS: Identifiquei os principais modelos de redes neurais profundas utilizados para identificação de queimadas e os principais sensores fontes dos dados.

DIFICULDADES: Não tive

DECISÕES: Atualemnte opto pela utilização do ABI do GOES-16 devido a facilidade de aquisição de dados, não só para treinamento, como também para manter o modelo funcionando ao longo do tempo, e devido a sua atualização diária que é de 10 em 10 minutos (Sentinel 2 revisita o mesmo ponto diariamente). O GOES-16 tem 16 bandas espectrais, com resolução espacial variando de 500m a 2km, sendo assim, vamos plotar as imagens de todas as bandas espectrais de um dia com incêndio para vermos se outras bandas espectrais além das de infravermelho podem ajudar, uma vez que a resolução de infravermelho é de 2km. 

PRÓXIMOS PASSOS: Aquisição dos dados para identificar as variáveis e derivados das variáveis que serão importantes para o modelo.

DATA: 29/10/2025

Ao tentar fazer um guia mostrando todas as bandas do GOES16, descobrimos que ele foi substituido pelo satélite GOES19. Todo código que tinhamos até então era sobre o GOES16, logo teremos que alterar tudo. Tanto o GOES16 quanto o GOES19 operam na posição 75,2° de longitude oeste e 35.766 km de altitude.

11/11/2025
Encontrei um artigo sobre fazer uma super resolução das bandas do goes19 usando ML e canais do VIIRS, mas o poder conputacional necessário me impede de replicar o resultado. Existe a opção de pan sharpening, só que ele só daria certo se os dados dos dois satélites coincidisse sempre, logo o ideal é realmente algum modelo de ML. Só resta encontrar um que atenda as necessidades, sem necessitar de tanto poder computacional.

13/11/2025
Como foi proposto no plano de trabalho, é chegada a hora de montar o dataset. O dataset será pré-processado com o pan sharpening, que é uma técnica utilizada para aumentar a resolução de uma imagem com base em uma imagem de maior resolução. Aumentarei a resolução das bandas 7(2km) e 14(2km) com base na banda 2(0,5km) uma vez que foi identificado no relatório do estado da arte que essas são as bandas de maior interesse na detecção e monitoramento de incêndios. O formato do dataset ainda não foi definido, mas vai ter que ser no mesmo formato dos arquivos que serão processados em tempo real no produto final da presente pesquisa.

15/11/2025
Com o relatório de estado da arte pronto, podemos seguir para a montagem do dataset

Previsão 17/11 - 21/11
Pegar um netcdf que é certeza de ter incêndio e transformar em um csv
Fazer um pan sharpening em um netcdf de fogo e comparar o antes e depois da resolução dando um zoom em uma região específica (goiânia e regiâo em um raio de 300km)
Se tudo der certo, montar o dataset (ainda não foi decidido quantos netcdf comporão o dataset)
