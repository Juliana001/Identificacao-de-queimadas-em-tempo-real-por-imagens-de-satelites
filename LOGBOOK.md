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
- Fazer um pan sharpening em um netcdf de fogo e comparar o antes e depois da resolução dando um zoom em uma região específica (goiânia e regiâo em um raio de 300km)
  Abaixo segue o primeiro resultado de pan sharpening da banda 7(2km) pela banda 2(500m). Foi em um dia de incêndio, mas não indentifiquei que região é essa. Mas pelo menos funcionou. Agora é fazer para a região de Goiás e montar o dataset logo em seguida. (cmap='inferno' pois é melhor para identificar calor) 
  ![Apresentacao](https://drive.google.com/uc?export=view&id=1ovQSPPD10mo2Ok2kSivPCPw_CHDWg22A)
- Se tudo der certo, montar o dataset (ainda não foi decidido quantos netcdf comporão o dataset)
  24/11 - 28/11
Consegui encotrar o estado de Goiás fazendo as marcações dos estados no netcdf original.
  próximos passos: encontrar o estado de Goiás na imagem com pan-sharpening e validar como ele funciona em focos de incêndio. O esperado é que ele realmente tenha aumentado a resolução espacial do netcdf.
  O aumento da resolução dos netcdfs é crucial não só para a detecção dos incêndios em si, mas também para o monitoramento dos incêndios.
  ![Apresentacao](https://drive.google.com/uc?export=view&id=1bzMV1hNZYThMzbFahlWzwT7UyWeYFgB0)

  O PCA, da forma que foi calculado, perdeu o georreferenciamento. Será necessário encontrar outra forma de calcular o pca sem perder os dados espectrais, nem o georreferenciamento.

  A biblioteca numpy está dando conflito de versão com as outras bibliotecas utilizadas para o pan sharpening.

  1/12- 5/12

  Com os resucrsos computacionais disponíveis, não será possível realizar o pan sharpening para aumnetar a resolução espacial da banda 7, uma vez que o método que consome menos memória ram é o Brovey, que é um método que não preserva as características espectrais. O ideal seria utilizar o PCA, mas ele consome muito ram (a ram disponível é de 12.7 GB do colab), então paralizaremos o pan sharpening e buscaremos outras técnicas que satisfaçam as seguintes necessidades:
  - aumentar a resolução espacial
  - preservar as características espectrais da(s) banda(s) necessária(s)
  - preservar o georregferenciamento
  - ser de rápido processamento, uma vez que utilzaremos essa tecnica no produto final para fazer um pre-processamento nos arquivos antes de serem injetados na rede neural para detectar e monitorar incêndios.
 
  O principal motivo que faz com que o aumento da resolução seja indispensável é a necessidade de conseguir detectar incêndios no inicío, ou próximo disso, para que assim eles tenham menores proporções e também para auxiliar no monitoramento do incêndio, uma vez que se conseguirmos prever para onde o incêndio vai, com uma resolução espacial de 500m, teremos muito mais sucesso na contenção do fogo, do que se fizermos esse monitoramento com uma resolução espacial de 2km.

Encontrei a técnica super-resolução por interpolação bilinear
  ela gasta uma quantidade considerável de memória RAM, mas ainda dentro do suportado pelo Colab.

  O resultado encontrado é mostrado abaixo pegando a mesma fatia da imagem. Podemos ver que teve sim um aumento na resolução.
   ![Apresentacao](https://drive.google.com/uc?export=view&id=1xpdnTLuLpqnVnKm87R0nm9pKCAMSWnLT)
  Essa técnica:
  -  aumenta a resolução espacial
  -  preserva o georreferenciamento
  -  em teoria preserva as características espectrais, uma vez que tudo é feito em cima de só uma banda (ainda precisa ser provado)

Com isso, os próximos passos são: plotar o estado de Goiás e validar com um plot de da banda original também do estado de Goiás.

Caso ela não tenha preservado as características espectrais, buscarei outra técnica, mas ao que tudo indica essa técnica atendeu todas as necessidades.

Se ela estiver ok, logo disponibilizarei o código tanto de puxar os dados do GOES19, quanto o de aplicar a técnica de super resolução por interpolação bilinear.

Como a nova resolução foi para 1,33km, vou tentar aumentar para pelo menos 1km, se não der certo, vamos seguir com a resolução de 1,33km, pois ela ainda é melhor que 2km. 
O principal motivo para usarmos o ABI do GOES19 e não qualquer outro satélite com reolução maior é a resolução temporal, também conhecida como taxa de revista: enquanto a do GOES19 é de aproximadamente 10 em 10 minutos, satélites como o Sentinel ultrapassa os 10 dias. A resolução de a cada 10 dias impossibilita o monitoramento de incêndios.
Globo todo
![Apresentacao](https://drive.google.com/uc?export=view&id=1rVwRDlmFhzqzFcz13dGr-nVv4xXOw41n)

Goiás com super resolução e sem super resolução
Com a super resolução é possível ver que a iamgem fica um pouco mais nitida (a resolução espacial caiu de 2km para 1.33km), preservando os dados espectrais e o georreferenicamento. O próximo passo será dar um super zoom para ver o comportamento dos pixels mais de perto para saber se realmente almentou a resolução. Visivelmente aumentou, mas precisamos provar.
![Apresentacao](https://drive.google.com/uc?export=view&id=1Up1fD6vepOOil8bWZxn7d7-YUVzRoIjp)

Goiás sem super resolução (banda 7)
![Apresentacao](https://drive.google.com/uc?export=view&id=1rF_6tH-U6AchhPe48LsHxQtfogc4EpWT)

Goiás com super resolução (banda 7)
![Apresentacao](https://drive.google.com/uc?export=view&id=1GhJ61_uaYIkPhL43UlaUo513RL4IrvVc)


RAM gasta para plotar o globo (todos os dados da banda 7)

![Apresentacao](https://drive.google.com/uc?export=view&id=1Scf54irW94mdI5zNkz7OH-V4Ys-OGbjF)


RAM gasta para plotar os dados da banda 7 de Goiás com super resolução

![Apresentacao](https://drive.google.com/uc?export=view&id=1QwAt6DWvi2qFSVTg5ohWMvOT-hiruWXx)


RAM gasta para plotar a imagem com super resolução e sem super resolução

![Apresentacao](https://drive.google.com/uc?export=view&id=1i9Bf8f0B0DPuwxhOiZo8KiitTTP5RSkz)

Com os dados da RAM podemos perceber que esse é um processo muito caro computacionalmente, mas sem ele se torna inviável o procedimento da pesquisa de detecção e monitoramento de incênidos. Sendo assim, fica justificado o motivo de despender mais tempo para a confecção do dataset. O ideal seria que a resolução caisse abaixo de 1km e tentarei alcançar essa resolução, mas na inviabilidade deste objetivo, seguiremos com 1.33km de resolução.

A Super Resolução por interpolação bilinear se mostrou ineficiente, quando comparada com imagens do dsat, que também usa os dados do GOES19. A interpolação aumentou, de fato, o número de pixels, mas perdeu os dados que já tinha. 

Agora entramos em um dilema: abrir mão do monitoramento de incêndios para preservar a detecção, ou desconsiderar a detecção de incêndios no início priorizando o monitoramento? Mas se pararmos para pensar, se priorizarmos o monitoramento, até ele será prejudicado, uma vez que a resolução é de 2km. Sendo assim, pela continuidade da pesquisa buscaremos outro satélite que tenha uma resolução maior, pelo menos uma vez por dia ou a cada dois dias e usaremos uma combinação de bandas do GOES19 apenas para auxiliar na previsão de para onde os incêndios detectador podem ir. Todo o conjunto de redes neurais (precisaremos usar mais de uma, especializando cada uma em sua respectiva função) será arquitetado como uma cadeia de Markov.

Os satélites mais promissores são:

* VIIRS – Suomi-NPP e NOAA-20
  * Resolução espacial: 375 m (bandas I)
  * Resolução temporal: 1–2 passagens por dia
  * Cobertura no Brasil: excelente
    
* MODIS – Terra e Aqua
  * Resolução espacial: 1 km
  * Resolução temporal: 2 passagens/dia
  * Cobertura: total do Brasil
 
Nada impede uma possível combinação dos 3 satélites para um produto final, tudo vai depender da forma de obter os dados. Uma das vantgens do GOES19 é que é muito fácil puxar dados dele, os dados são abertos. Fora do Brasil, muitas pesquisas que li enquanto montava o estado da arte utilizava os satélites Himawari, só que o campo de visão dele é oriental: Asia e Ocenaia. As resoluções dele são bem parecidas com as do GOES, mas praticamente todos os trabalhos analisados eram patrocinados de modo que os pesquisadores tinham boas GPUs para todo o processamento de rede neural para aumentar a resolução das bandas espectrais. 
       

O maior problema de utilizar o VIIRS é a continuidade do sistema para além do que será entregue no relatório final, uma vez que acessar os dados do VIIRS é muito complicado via API, para não dizer impossível. Para acessar os dados é necessário uma conta, não é possível automatizar de forma que ele fique puxando os dados todos os dias igual seria possível no GOES. A depender de como a pesquisa seguir, não descarto a possibilidade de criar um modelo de algoritmo de detecção, instruindo sobre o que fazer com cada banda (comprimento de onda) e quando surgir um satélite de maior resolução apontado para o Brasil, apenas fazer a troca de qual satélite será usado.

Em questão de visão de futuro, o MODIS não é uma boa escolha, visto que ele tem previsão de descomissionamento para o final de 2026 início de 2027, enquanto que o GOES19 é para depois de 2030 e o VIIRS depois de 2040.


Fiz uma nova tentativa de aumentar a resolução usando transformada de Wavelet, mas não funcionou. Seguindo os passos de várias outras pesquisas que analisei enquanto fazia o relatorio de estado da arte, vou seguir com os 2km mesmo. Vou priorizar a técnica e a escalabilidade. Quando surgir um novo satélite com outros sensores melhores, conseguiremos alterar.

O desafio agora é montar o dataset. Os arquivos, mesmo tendo resolução de 2km, ainda não enormes. Montar um dataset com umas 10 mil imagens, deve ultrapassar com muita facilidade os 100gb de memória.

Mas o próximo passo é: montar o dataset.

Outro fator que vai de encontro à nossa necessidade é o tamanho dos arquivos VIIRS. O VIIRS possui produtos de resolução de até 375m, o que faz com que os arquivos sejam extremamente pesados, se para alguns processamentos básicos do GOES foi possível atingir mais de 30gb de RAM, o VIIRS ultrapassaria com muita facilidade esse marco. Sendo assim, por enquanto o GOES ainda é a melhor opção.

A parte da montagem do dataset se dará em duas etapas:
1- validação de quais bandas serão úteis para a detecção (por enquanto não vamos trabalhar com detecção e monitoramento, vamos usar a estratégia dividir para conquistar).
2- montagem do dataset com aproximadamente 1000 netcdfs. Esse número pode parecer pouco, mas é o máximo que conseguimos gerir, uma vez que não temos meios de hospedar tantos netcdfs.

Uma possível solução para o armazenamento dos netcdfs é o Zenodo. Como ele tem um limite de 50Gb, acredito que ele consiga guardar os netcdfs. Agora, precisamos descobrir se tem como automatizar o processo de colocar os dados, ou se será necessário colocar na minha máquina para depois fazer o upload no zenodo.

Quantos as bandas que comporão o dataset: a banda 7 é muito importante, mas diversas pesquisas que li apontaram que a utilização apenas da banda 7 trouxe mais falsos positivos do que verdadeiros positivos, assim, comporemos nosso dataset com mais bnadas, inclusive dados climáticos, que se mostraram importante em diversas pesquisas.

Para fins de entender o comportamento das bandas em incêndios, vou puxar um netcdf de um dia de incêndio e plotar em todas bandas.
Vou tentar plotar as bandas capturadas no dia 04/10/2025, pois nesse dia houve incêndio em Goiás, mais especificamente na Chapada dos Veadeiros.

Muito embora ainda seja preliminar, mas é válido contar que das bandas analisadas, a banda 5 teve um excelente desempenho, podendo ser uma das que comporão o dataset. É válido destacar que, por mais que algumas bandas como a 7 e a 15 sejam muito utilizadas para a detecção de incêndios ao redor do mundo, quando falamos de Cerrado, essa aplicação pode ter muitas limitações, uma vez que o Cerrado é um dos hotspots do mundo, ou seja, é um lugar quente. Se o Cerrado por si só já apresenta altas temperaturas em condições normais, a utilização única e exclusiva dessas bandas pode ser prejudicial para a acurácia do modelo. 

Vou começar fazendo uma composição das bandas.

A imagem abaixo foi retirada do BDQueimadas, do dia 25/09/2025. Todos os pontos vermelhos são incêndios.
  ![Apresentacao](https://drive.google.com/uc?export=view&id=18vChJpqOrVR2dZv6wRC_lmY2n0XktAtu)

  Analisando a banda 7:
    ![Apresentacao](https://drive.google.com/uc?export=view&id=1M0_CMC-v5liHtghjqXHfnPT0L2EtSk91)
    
Analisando a banda 14:
  ![Apresentacao](https://drive.google.com/uc?export=view&id=1IDSNjqP_rXyPVHcjEjwgl7YLiTgh2raA)



