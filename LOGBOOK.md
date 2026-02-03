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

 Banda 7:
    ![Apresentacao](https://drive.google.com/uc?export=view&id=1M0_CMC-v5liHtghjqXHfnPT0L2EtSk91)
    
Banda 14:
  ![Apresentacao](https://drive.google.com/uc?export=view&id=1IDSNjqP_rXyPVHcjEjwgl7YLiTgh2raA)

Ambas as bandas tiveram um comportamento parecido com o dos dados oficiais do BDQueimadas, com excessão para a região norte, que nenhuma das bandas captou incêndios, mas na reigião central e nordeste foram captados de forma bem parecida com o real. Como o objetivo da pesquisa está em detectar incêndios no cerrado goiano, as bandas se mostraram úteis. Faltam as bandas 15, 5 e 6 para análise. 

Acho que para esse problema não faremos uma composição de bandas e sim um algoritmo que funcione como um funil: começa por uma banda que pode haver falsos positivos até chegar em uma que (pode ser uma composição) tenha os falsos positivos e falsos negativos tendendo a zero.

Antes de continuarmos o desenvolvimento do dataset precisamos primeiro responder à perqunta: o que é o fogo espectralmente falando?
Precisamos definir não só o que é o fogo, mas também o que é o fogo em um ambiente naturalmente muito quente.

#Assinatura espectral do fogo

O Delta BT (Diferença de Temperatura de Brilho) entre as bandas do infravermelho médio (MIR ~3.9 µm) e térmico (TIR ~11 µm) explora uma propriedade fundamental da física da radiação: a Lei do Deslocamento de Wien. Esta lei estabelece que o comprimento de onda de emissão máxima de um corpo negro é inversamente proporcional à sua temperatura.

Para incêndios ativos (600-1200 K), o pico de emissão ocorre entre 2.4-4.8 µm, exatamente na região espectral da banda 7 do GOES (3.9 µm). Em contraste, superfícies terrestres típicas (280-320 K) emitem predominantemente na região de 9-12 µm (banda 14).

Superfícies quentes como desertos, telhados metálicos ou solo exposto podem apresentar temperaturas elevadas na banda 7. No entanto, essas superfícies aquecem de forma relativamente uniforme em ambas as bandas, resultando em um Delta BT pequeno (tipicamente < 5-8K). Um incêndio ativo, com chamas e brasas, apresenta uma diferença muito maior (10-50K ou mais) devido à emissão seletiva no MIR.

 ![Apresentacao](https://drive.google.com/uc?export=view&id=1QsE8b0AZsorJyr3hNIDCI7lCKtum_KdA)

Foi possível extrair as seguintes informações:
* ΔBT máximo nos hotspots: 75.77 K
* ΔBT médio nos hotspots: 12.77 K
* Temperatura máxima B07: 386.10 K
* Temperatura média B07: 322.38 K

Creio que informações assim serão úteis para o treinamento do modelo de redes neurais. Um dos primeiros testes que farei é com o modelo LSTM (Long Short-Term Memory). Ele se autobalanceia escolhendo o que esquecer e o que manter. 

Anteriormente havia comentado que foi possível detectar grande parte dos incêndios detectados pelo DBQueimadas, exceto os da região amazônica. Acho que isso aconteceu devido a quantidade e concentração de nuvens da região.
O $\Delta$ BT é útil na detecção de incêndios, mas não consegue detectar incêndios abaixo de nuvens densas, esse será um novo problema que teremos que resolver. Nuvens do tipo cumulonimbo, estrato espesso ou nimbostratus são efetivamente corpos opacos nas bandas do infravermelho termal (3.9 µm e 11 µm). A radiação emitida por qualquer fonte abaixo da nuvem não consegue atravessar a camada de gotículas/partículas de gelo para atingir o sensor do satélite.

Por enquanto acho que a estratégia mais simples e eficaz para montar o dataset vai ser apenas fazer o corte da região de Goiás e guardar as bands necessárias e fazer o processamento direto no algoritmo principal.
Encontrar alguma técnica que resete o gasto de Ram assim que o processamento acabar para liberar memoria para o proximo


Por enquanto, ficou decidido que o dataset sera composto pelos netcdf diretamente puxados do aws, o único processamento feito será a escolha das bandas necessárias e o recorte para Goiás.

Na busca por desenvolver uma metodologia eficaz para a detecção de incêndios florestais encontrei o Índice MIRBI que foi desenvolvido especialmente para hotspots como Cerrado e Savanas, mas como ele njão foi feito para os tipos de banda disponíveis no GOES19, fiz uma adaptação que até então tem se mostrado eficaz.

Os índices que estão sendo estudados são:

NDVI

TIR

NTIR

BT

MIRBI

E uma coisa que descobri é que pode ser útil tratar a detecção de incêndios como um processo estocástico, uma vez que os índices trabalham melhor se forem calculados como variação ao longo do tempo, sendo assim, a ordem das imagens vai importar e vamos ter que descobrir uma forma de guardar as imagens quando o sistema estiver funcionando.

No trabalho original de TRIGG e FLASSE, a dupla de bandas que entregou maior separação de áreas queimadas e não queimadas foi SMIR(1.628–1.652)-LMIR(2.105–2.155), que são exatamente as bandas 6 e 7 do MODIS, sendo a fórmula utilizada **MIRBI = 10LMIR - 9.8SMIR + 2**.

O equivalente disso no GOES19 seria: Banda 5 e 6, entretando, há uma divergência nas resoluções espaciais das bandas: enquanto ambas as bandas do MODIS tem 500m, as do GOES19 tem respectivamente 1km e 2km. Acho que isso contribuiu negativamente para o resultado encontrado. 
Resultado bandas 5 e 6

 ![Apresentacao](https://drive.google.com/uc?export=view&id=1flo53XwRAduQmDZxn955El-c2I3rc_NJ)

Tentando contornar este problema eu utilizei as bandas 6 e 7, que acabou virando um SWIR-TIR e que teve um resultado muito satisfatório em relação a tentativa de alcançar o MIRBI original.

Resultado bandas 6 e 7

 ![Apresentacao](https://drive.google.com/uc?export=view&id=1JeuLEJM_6AgzVf_F7rlrqdYUelB1lbEY)

 Embora o MIRBI tenha sido originalmente formulado para as bandas 5 e 6 do SEVIRI, o índice é fundamentado no contraste espectral entre o infravermelho médio curto (~3.9 µm), altamente sensível à presença de fogo, e uma banda térmica de janela atmosférica (~10–12 µm), representativa da temperatura de fundo. No sensor ABI do GOES-19, as bandas 6 e 7 ocupam regiões espectrais funcionalmente equivalentes às utilizadas no estudo original, o que explica o desempenho satisfatório do índice mesmo com comprimentos de onda centrais distintos.
 ----------------------------------------------------------------------------------------------------------------------------------------

 Até o presente momento tenho pensado em utilizar os índices NDVI, BT e MIRBI como uma cadeia de Primeiros neurônios. Todos esses índices demosntraram bom desempenho na detecção de incêndios.

 Uma coisa que acabei de perceber e que eu não tinha percebido antes era  o "filtro" de nuvem que o MIRBI usando as bandas 5 e 6 criou. Pelo que vi, restaram apenas as nuvens mais densas, o que limpou muito o mapa.

 Outra coisa que descobri foi o produto L2 LST.
 O produto L2 LST do GOES‑19 é um produto de Nível 2 do sensor ABI (Advanced Baseline Imager) do satélite geoestacionário GOES‑19 que fornece temperatura da superfície terrestre.
 Poderiamos fazer calcular o LST, mas ele não depende apenas das bandas, ele precisa de coeficientes calibrados de emissividade, vapor de água, ângulo de visada, sendo que desses, o único que temos é o de ângulo de visada, os outros não conseguimos obter, nem calcular de forma calibrada.

 # LST vs BT
  O LST vem com a ideia da temperatura real da superfície, com erro entre 1°C e 3°C. Já o BT vem com a ideia de temperatura aparente, sem considerar emissividade e com erro variando entre 5°C e 15°C.
  Como podemos ver nas imagens fornecidas, o BT ele tem sua relevância e mantém as núvens, enquanto que o LST retira todas as núvens e tudo que está abaixo delas.

  Temos então um problema. Mas acho que seria possível fazer uma composição usando o MIRBI das bandas 5 e 7 e o LST. Eu estou pensando em literalmente uma fusão de imagens, mas apenas da parte que está faltando. Acho que com a ideia de análise temporal não teríamos um efeito negativo.

  A ideia mais imples que tive é fazer algo booleano como: nesse pixel do lst é nulo? então ele é igual ao pixel do MIRBI bandas 5 e 6. Mas lembrando que é apenas para a região de Goiás.

 ![Apresentacao](https://drive.google.com/uc?export=view&id=1jdhJ2rDouJTagLKeVB4cbOb64oM0vzWC)

 -------------------------------------------------------------------
 Aparentemente o MIRBI não poderá ser utilizado por não ser confiável devido a assinatura espectral das bandas.

 Outros índices que irei estudar são:
 * FRP

 ![Apresentacao](https://drive.google.com/uc?export=view&id=1lzli-amIHkwXd8IOE51CPJQ8XGiRg0h5)

 Pelo que podemos ver, a plotagem dos dados ficou imprecisa, visto que as nuvens são sinalizadas como fogo e as áreas de fogo como áreas sem fogo. Ainda não identifiquei se isso foi erro na minha plotagem ou se a imprecisão é do produto

 * NDFI

 ![Apresentacao](https://drive.google.com/uc?export=view&id=1uiQr9tIvGx_kFHLiqkjR7jO7J9eINiGB)
 O NDFI calculado com as bandas 6 e 7 também apresenta o mesmo problema. Ambas são bandas de infravermelho curtas.

 Até agora, dos produtos fornecidos pelo GOES, apenas o LST mostrou coerência com os dados que temos do BDQueimadas. E o MIRBI, mesmo sendo calculado de forma espectralmente incorreta também apresentou coerência tanto na minimização de núvens finas, quanto na detecção de áreas quentes.

 Como já mencionei anteriormente, nosso dataset será composto pelos dados do L2 do ABI GOES19, apenas com o processamento de recorte para a área de Goiás. Todos esses índices comporão a nossa rede neural.

 Estou gastando um tempo maior com essa análise para garantir que os dados terão a melhor qualidade quanto possível, pois se os dados forem ruins, o modelo vai devolver respostas ruins, se os dados forem bons, por mais que o modelo não seja tão bom, ainda assim teremos resultados coerentes.


 __________________________________________________________________________________________________________________________________________
Existem redes neurais supervisionadas e não supervisionadas. As supervisionadas são treinadas mostrando o que é e o que não é. Já a não supervisionada aprende sozinha. Vou treinar uma supervisionada e uma não supervisionada para termos nosso primeiro parecer, tanto das redes neurais, quanto do que escolhemos para treiná-las.

Para uma prova de conceito inicial vou utilizar a estratégia 5-fold com 40 dados nos dois tipos de modelo. Deixo claro que é apenas uma prova de conceito para validar se o que pensei em fazer é viável ou não.

O que pretendo validar:
- A escolha de montar o dataset apenas com os dados brutos, apenas com o recorte da área da certo?
- O modelo aprende algo com o netcdf?
  - Se não aprender: será que é melhor usar visão computacional com imagens?
- A solução foi bem formulada?
- Qual é melhor: supervisionado ou não supervisionado?

  ______________________________________________________________________________________________________________________________________________
  O dataset já está sendo montado e foi decidido não recortar o estado de Goiás, nem baixar os dados já com referenciamento de latitude e longetude, uma vez que o algoritmo terá que fazer isso em tempo real quando estiver funcionando. Então, para analisarmos a viabilidade do processo como um todo, vamos baixar o xarray do jeito que ele é puxado sem nenhum processamento, para não maquiarmos possíveis demoras na execução. Os dados estão sendo baixados direto no Google Drive.

Abaixo apresento o tamanho de alguns dos NetCDFs baixados. É possível perceber que são arquivos grandes. Foram baixados um total de 40 arquivos, o que é mais ou menos 12Gb de memória. Sabemos que para treinarmos redes neurais precisamos de milhares de dados, o que mostra que: mesmo que fosse viável utilizarmos dados de satélites com resolução espacial menor que 500m, ainda assim esbarrariamos na questão de ter espaço para armazenar o dataset e posteriormente em ter recursos computacionais para processar dados tão grandes. 
Quanto a estratégia para montar o dataset, eu puxei dados do mês 4 ao mês 11, 5 dados por mês. Procurei pegar dados espaçados para cobrir a maior quantidade de variação de solo no cerrado quanto possível: de 5 em 5 dias, tanto diurnos, quanto noturnos. 

 ![Apresentacao](https://drive.google.com/uc?export=view&id=1Pbv0GXCg-GDZeWuafW51zD9rDsBh_F2I)


 Agora que já temos o dataset, precisamos escolher as redes neurais, que serão duas: uma supervisionada e outra não supervisionada. 
 ________________________________________________________________________________________________________________________________________________________
 Estudando os modelos supervisionados cheguei a conclusão que para essa pesquisa não faz sentido aplicar aprendizado supervisionado uma vez que não há como rotular os dados de forma confiável. Para isso seria necessário profissionais da área do geoprocessamento. Nesse sentido, focarei em aplicar redes neurais profundas não supervisionadas. 
 As entregas serão:
 
 1- PoC
 
 2- MVP
 ----------------------------------------------------------------------------------------------------------------------------------------------------------

 Comecei a montar a rede neural, mas me deparei com um problema inesperado: conseguir usar os dados que estão no drive. Individualmente consegui acessar a todas as variáveis que fazem parte de cada NetCDF, mas ao tentar puxar todos os 40 arquivos 40 GB de RAM não suporta. 

 O modelo de rede neural que escolhi para começar é o VAE, que é um autoencoder. Como ele é indicado para detectar anomalias, vou fazer um teste utilizando alguns ínidces espectrais que se mostraram promisssores.
 
  ![Apresentacao](https://drive.google.com/uc?export=view&id=1p39dShlGrSQUYcw_GZOHZxZ-wwHhZsB3)

  ____________________________________________________________________________________________________________________________________________________
  A maior dificuldade agora é conseguir acessar os dados. Eu consigo ter acesso aos netcdfs, mas eles estão com dados nan. Enquanto eu montava o dataset no drive, eu testei todos os dados e individualmente era possível acessar a todos os recursos, mas agora que eles estão juntos eu não consigo acessar aos dados para conseguir aplicá-los nas redes neurais.

A minha ideia era montar o dataset com os dados originais, sem nenhuma alteração, para quando começarmos as simulações, ser possível quantificar o tempo total desde o recebimento dos dados, inserção de latitude e longetude que não são dados presentes nos netcdfs, o recorte para o estado de goiás e só então a aplicação da rede neural, porque afinal é assim que ela tem que funcionar. 

Um questionamento que fica é: como vamos fazer para treinar a rede neural oficial que irá compor o relatório final uma vez que para um simples PoC com apenas 40 dados temos essa dificuldade. São arquivos grandes. Arquivos netcdf são enormes. Para treinarmos uma rede neural, normalmente se usa milhares, milhões de dados. Temo que o trabalho não alcance a excelência dos resultados por conta dessa limitação.

Consegui ter acesso às variaveis do dataset. Agora é implementar uma rede neural.

Para a rede neural, penso em implementar uma estrutura tipo VAE (Variational Autoencoder) e um LSTM (Long Short Term Memory). O target é a latitude e longetude dos possíveis incêndios. Sabemos que a arquitetura da rede neural tem que conseguir suportar dados pesados sem consumir muita RAM.

_______________________________________________________________________________________________________________________________________________________
As estruturas das redes neurais não serão compartilhadas, mas os resultados sim.

Justificadno o porque eu preferi montar o dataset colocando os netcdfs na integra: a forma como o problema será resolvido pode mudar, sendo assim eu prefiro manter todos os dados até chegar em um resultado final satisfatório.

Na tentativa de calcular a latitude e longetude dos netcdfs, com os 12Gb de RAM do colab só foi possível calcular de 20. A pesquisa fica muito limitada com os recursos computacionais que tenho atualmente. É inviável calcular tudo manualmente uma vez que são muitos netcdfs e ainda nem são os dados que comporão o MVP, ainda é apenas um PoC de 40 netcdfs.
![Apresentacao](https://drive.google.com/uc?export=view&id=19-kwSP43G4b0LL4E8c13Gey8B9gEi_7k)

___________________________________________________________________________________________________________________________________________________________
Consegui os 47Gb de RAM do colab gratuito e estou concluindo o pipeline de dados. Um dos arquivos estava corrompido. Removi o arquivo corrompido. Agora, antes de implementar o VAE, terei que fazer um estudo mais aprofundado sobre a arquitetura e implementação dele.


Para entender o VAE é preciso compreender primeiro 3 assuntos:
* Reparametrization Trick
* Divergência de Kullback-Leibler
* Evidence Lower Bound

Esses três asssuntos diferenciam Variational Autoencoder de um Autoencoder. 

Outro ponto crucial é o Backpropagation, já tinha ouvido falar antes mas nunca implementei.

Os dados espectrais dos netcdfs de resolução de 2km geram imagens de 5024X5024, se fossemos criar uma rede neural para todo campo de visão do satélite, precisariamos de 25.24x 10^6  neurônios. Eu não consigo nem imaginar quanto processamento precisariamos para conseguir tratar tudo. Como Goiás tem aproximadamente 340 mil km^2 e a resolução espacial é de 2km, vamos precisar de pouco mais de 85 mil neurônios, o que é mais viável.

_____________________________________________________________________________________________________________________________________________________________
Estava relendo e procurando mais trabalhos que possam servir de referência para o meu e vi que a maioria de metodologias de detecção de incêndios florestais envolvem CNN. Ainda não achei nenhum que relaciona VAE e dados de satélites. Entretanto, achei um trabalho de detecção de incêndios prediais que combina justamente os dois tipos de redes neurais que pretendo utilizar: VAE e LSTM. Surpreendentemente, para o fim proposto do trabalho, essas duas redes neurais tiveram desempenho superior à outras redes.

Encontrei um trabalho excelente desenvolvido por pesquisadores da KTH Royal Institute of Technology. Eles utilizaram o GOES, mas como rede neural utilizaram GRU. Alcançaram bons resultados. Utilizaram cerca de 60.000 amostras da regiâo da Califórnia. Eu só não descobri de quanto poder computacional eles precisaram para poder finalizar a pesquisa. Na pesquisa deles, o índice que eles utilizaram foi o dNBR. Lembro que eu cheguei a implementar esse índice, mas acabei não inserindo aqui porque não obtive o que eu queria ver. (Vou implementar novamente, vai que né). Se ele funcionar, será mais um índice que comporá as variáveis utilizadas na rede neural. Realmente muito bom o trabalho deles. Se sobrar tempo antes do final do ciclo 2025-2026 tentarei desenvolver um GRU. 

Os algoritmos de otimização que estou considerando são: 
- ADAM
- RMSprop
- SGD
- GD

A tecnica que escolhi para montar o dataset do PoC foi ruim. Por mais que a ideia seja validar o tempo que gasta, toda vez que eu implementar um modelo novo, gastarei no mínimo 2 horas (se o colab deixar usar a TPU de graça) para rodar tudo.Sem a TPU do colab fica impossível. Então, a próxima vez que eu conseguir acessar a TPU do colab, irei montar um novo dataset, só que dessa vez seguindo o fluxo:
Puxar o xarray -> inserir latitude e longetude -> recortar o estado de Goiás -> armazenamento do netcdf. Assim, acredito que será mais rápido.

Uma coisa que eu não esperava é que o netcdf de Goiás pudesse muito maior que o do netcdf original. Ele ficou mais que o dobro do tamanho do original. Mas em todo o caso é menos custoso salvar assim do que fazer o processamento toda vez que for fazer algum teste. Acredito que o PoC terá que ser com ainda menos dados.

![Apresentacao](https://drive.google.com/uc?export=view&id=1GIOe_e7ZWmdaY7Uxfk-1jO-1zFmfL_wm)

Agora estou em um dilema: priorizar o tempo de processamento deixando apenas a região de interesse, mas perdendo quantidade de dados ou priorizar a quantidade de dados deixando de lado o tempo de processamento, uma vez que tratar todos os datasets toda vez que for usar a rede neural despenderá muito tempo e muito processamento.

Como a quantidade de dados anteriormente escolhida já era baixa, vou optar por manter os 40 netcdfs e ter paciência com o tempo de processamento.


Atualizações sobre o NBR: no Goes funcionou (teve um resultado próximo do correto) utilizando a banda 6 como nir e a banda 2 como swir.

![Apresentacao](https://drive.google.com/uc?export=view&id=1H5cwcoS2P3qJQ5t8cSlTsA-5Tc3COqeF)


Eu estava pensando em criar um dataset do goes19 dentro do GEE, mas os dados do Goes são netcdf e o GEE tem suporte para geotiff. Para a presente pesquisa utilizarei tanto netcdf quanto geotiff. Ou talvez só netcdf. 


Como a metologia que desenvolvi precisa de dados do VIIRS, estou tentando acessá-los, mas advirto que não é uma tarefa fácil de se fazer. Os dados para baixar do viirs são em formato txt. Uma das maiores vantagens do Goes é a facilidade de puxar dados. 
Esbarramos em um problema: para ter acesso ao viirs é preciso baixar os dados e são terabytes de dados. Como viabilizar isso? A melhor ideia é a utilização de APIs para puxar apenas alguns dados, quase da mesma forma que é feito no GOES. O desafio é descobrir como fazer isso. Bem complexo conseguir pegar dados via API.

Para processar de forma mais eficiente vou tentar comprimir os netcdfs. Digo tentar porque já tentei algumas compressões, mas acabei aumentado o tamanho do arquivo.
