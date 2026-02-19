import ee
import xarray as xr
import rioxarray
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
import os
from datetime import datetime, timedelta
import requests
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Autentica com o Google Earth Engine
# ee.Authenticate()

# Inicializa o Earth Engine com a ID do Projeto
ee.Initialize(project='id_do_proj')

# Define o diretório de saída (MUDE ESTE CAMINHO)
output_dir = r"C:\"  # Windows

# Cria o diretório se não existir
os.makedirs(output_dir, exist_ok=True)
print(f"Arquivos serão salvos em: {output_dir}")

# Lista de datas
date_strings = [
    '10/04/2025', '13/04/2025', '15/04/2025', '20/04/2025', '25/04/2025',
    '01/05/2025', '03/05/2025', '05/05/2025', '06/05/2025', '12/05/2025',
    '18/05/2025', '21/05/2025', '25/05/2025', '01/06/2025', '07/06/2025',
    '09/06/2025', '13/06/2025', '18/06/2025', '24/06/2025', '01/07/2025',
    '03/07/2025', '06/07/2025', '11/07/2025', '17/07/2025', '22/07/2025',
    '25/07/2025', '30/07/2025', '02/08/2025', '07/08/2025', '12/08/2025',
    '18/08/2025', '22/08/2025', '27/08/2025', '01/09/2025', '05/09/2025',
    '09/09/2025', '12/09/2025', '17/09/2025', '22/09/2025', '27/09/2025',
    '01/10/2025', '05/10/2025', '10/10/2025', '15/10/2025', '20/10/2025',
    '25/10/2025', '01/11/2025', '05/11/2025', '11/11/2025', '16/11/2025',
    '23/11/2025', '29/11/2025'
]

# Formata como YYYY-MM-DD
def format_date(date_str):
    parts = date_str.split('/')
    return f"{parts[2]}-{parts[1]}-{parts[0]}"

dates = [format_date(d) for d in date_strings]

# Área de Interesse em Lat/Lon
lon_min, lon_max = -53.5, -45
lat_min, lat_max = -19.5, -11.8
aoi = ee.Geometry.Rectangle(lon_min, lat_min, lon_max, lat_max)

print(f"Processando {len(dates)} datas para AOI: Lon [{lon_min}, {lon_max}], Lat [{lat_min}, {lat_max}]")

def download_and_save_night(date):
    """Download do VIIRS nightlight e salva como NetCDF individual"""
    try:
        start_date = ee.Date(date)
        end_date = start_date.advance(1, 'day')
        
        # Obtém a imagem
        img = ee.ImageCollection("NASA/VIIRS/002/VNP46A2") \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .select('Gap_Filled_DNB_BRDF_Corrected_NTL') \
            .first() \
            .clip(aoi)
        
        # Verifica se a imagem existe
        if img is None:
            print(f"  Sem dados para {date}")
            return False
        
        # URL de download
        url = img.getDownloadURL({
            'scale': 500,
            'crs': 'EPSG:4326',
            'region': aoi,
            'format': 'GEO_TIFF'
        })
        
        # Download
        response = requests.get(url)
        response.raise_for_status()
        
        # Lê o GeoTIFF
        da = rioxarray.open_rasterio(BytesIO(response.content))
        
        # Adiciona metadata
        da = da.squeeze()  # Remove dimensão de banda se for 1
        da = da.expand_dims(time=[np.datetime64(date)])
        da = da.rename('night_radiance')
        da.attrs['long_name'] = 'VIIRS Nighttime Radiance'
        da.attrs['units'] = 'nW/cm2/sr'
        da.attrs['source'] = 'NASA/VIIRS/002/VNP46A2'
        da.attrs['date'] = date
        
        # Nome do arquivo
        filename = f"VIIRS_NIGHT_{date}_LAT_{lat_min}_to_{lat_max}_LON_{lon_min}_to_{lon_max}.nc"
        filepath = os.path.join(output_dir, filename)
        
        # Salva como NetCDF
        da.to_netcdf(filepath)
        
        # Verifica se o arquivo foi criado
        if os.path.exists(filepath):
            tamanho = os.path.getsize(filepath) / (1024 * 1024)  # MB
            print(f"  Salvo: {filename} ({tamanho:.2f} MB)")
            return True
        else:
            print(f"  Falha ao salvar: {filename}")
            return False
        
    except Exception as e:
        print(f"  Erro para {date}: {str(e)[:100]}")
        return False

def download_and_save_day(date):
    """Download do MODIS day reflectance e salva como NetCDF individual"""
    try:
        start_date = ee.Date(date)
        end_date = start_date.advance(1, 'day')
        
        # Obtém a imagem
        img = ee.ImageCollection("MODIS/061/MOD09GA") \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date) \
            .select(['sur_refl_b01', 'sur_refl_b02', 'sur_refl_b03', 'sur_refl_b04']) \
            .first() \
            .clip(aoi)
        
        # Verifica se a imagem existe
        if img is None:
            print(f"  Sem dados para {date}")
            return False
        
        # URL de download
        url = img.getDownloadURL({
            'scale': 500,
            'crs': 'EPSG:4326',
            'region': aoi,
            'format': 'GEO_TIFF'
        })
        
        # Download
        response = requests.get(url)
        response.raise_for_status()
        
        # Lê o GeoTIFF
        da = rioxarray.open_rasterio(BytesIO(response.content))
        
        # Adiciona metadata
        da = da.expand_dims(time=[np.datetime64(date)])
        da = da.rename('surface_reflectance')
        da.attrs['long_name'] = 'MODIS Surface Reflectance'
        da.attrs['units'] = 'reflectance x 10000'
        da.attrs['bands'] = '1:red, 2:nir, 3:blue, 4:green'
        da.attrs['source'] = 'MODIS/061/MOD09GA'
        da.attrs['date'] = date
        
        # Nome do arquivo
        filename = f"MODIS_DAY_{date}_LAT_{lat_min}_to_{lat_max}_LON_{lon_min}_to_{lon_max}.nc"
        filepath = os.path.join(output_dir, filename)
        
        # Salva como NetCDF
        da.to_netcdf(filepath)
        
        # Verifica se o arquivo foi criado
        if os.path.exists(filepath):
            tamanho = os.path.getsize(filepath) / (1024 * 1024)  # MB
            print(f"  Salvo: {filename} ({tamanho:.2f} MB)")
            return True
        else:
            print(f"  Falha ao salvar: {filename}")
            return False
        
    except Exception as e:
        print(f"  Erro para {date}: {str(e)[:100]}")
        return False

# Processa imagens noturnas
print("\nBaixando dados noturnos VIIRS...")
night_success = []
for date in dates:
    print(f"\nProcessando data: {date}")
    success = download_and_save_night(date)
    if success:
        night_success.append(date)

# Processa imagens diurnas
print("\nBaixando dados diurnos MODIS...")
day_success = []
for date in dates:
    print(f"\nProcessando data: {date}")
    success = download_and_save_day(date)
    if success:
        day_success.append(date)

# Relatório final
print("\n" + "="*50)
print("RELATÓRIO FINAL")
print("="*50)
print(f"Diretório de saída: {output_dir}")
print(f"Total de datas solicitadas: {len(dates)}")
print(f"Arquivos noturnos salvos: {len(night_success)}")
print(f"Arquivos diurnos salvos: {len(day_success)}")

if night_success:
    print("\nDatas noturnas com sucesso:")
    print(", ".join(night_success[:10]))  # Mostra primeiras 10
    if len(night_success) > 10:
        print(f"... e mais {len(night_success) - 10} datas")

if day_success:
    print("\nDatas diurnas com sucesso:")
    print(", ".join(day_success[:10]))
    if len(day_success) > 10:
        print(f"... e mais {len(day_success) - 10} datas")

# Lista arquivos no diretório
print("\nArquivos no diretório de saída:")
arquivos = os.listdir(output_dir)
nc_files = [f for f in arquivos if f.endswith('.nc')]
for f in nc_files[:10]:  # Mostra primeiros 10
    tamanho = os.path.getsize(os.path.join(output_dir, f)) / (1024 * 1024)
    print(f"  {f} ({tamanho:.2f} MB)")

print("\nProcesso completo!")
