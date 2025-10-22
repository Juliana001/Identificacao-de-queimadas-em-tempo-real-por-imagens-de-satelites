# Monitoramento de Queimadas no Cerrado via Satélites 

## Objetivo
Detectar e monitorar queimadas em tempo quase real na região de Goiânia usando dados MODIS/VIIRS e Google Earth Engine.

## Área de Estudo
Cerrado Goiânia + municípios vizinhos (GeoJSON - NETCDF - GEOTIFF).

## Sensores que poderão ser utilizados, a depender da disponibilidade dos dados
- MODIS (Terra/Aqua)
- VIIRS (NOAA-20/Suomi-NPP)
- Sentinel-2 (validação)
- ABI (GOES-16)

## ⚙️ Metodologia

1. Escolha do(s) sensor(es)
2. Criação do dataset
3. Teste dos dados em modelos já existentes
   3.1 Identificação de Hotspots
   3.2 Identificação de áreas queimadas
   3.3 Validação (INPE/Sentinel 2)
4. Criação de novo(s) modelo(s)
   4.1 Identificação de Hotspots
   4.2 Identificação de áreas queimadas
   4.3 Validação (INPE/Sentinel 2)
5. Comparação de resultados

