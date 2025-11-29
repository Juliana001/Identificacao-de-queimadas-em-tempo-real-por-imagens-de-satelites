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
    
    




