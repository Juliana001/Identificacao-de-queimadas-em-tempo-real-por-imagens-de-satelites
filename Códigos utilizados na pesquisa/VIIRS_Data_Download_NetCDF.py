import ee 
import rioxarray
import numpy as np
import os
import requests
import warnings
warnings.filterwarnings('ignore')

# Autentica com o Google Earth Engine
# ee.Authenticate()

# Inicializa o Earth Engine com a ID do Projeto
ee.Initialize(project='id')  

# Define o diretório de saída
output_dir = r"C:\"  # Windows
os.makedirs(output_dir, exist_ok=True)
print(f"Arquivos serão salvos em: {output_dir}")

# Datas de interesse
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

def format_date(date_str):
    parts = date_str.split('/')
    return f"{parts[2]}-{parts[1]}-{parts[0]}"

dates = [format_date(d) for d in date_strings]

# Área de interesse
lon_min, lon_max = -53.5, -45
lat_min, lat_max = -19.5, -11.8
aoi = ee.Geometry.Rectangle(lon_min, lat_min, lon_max, lat_max)

print(f"Processando {len(dates)} datas para AOI: Lon [{lon_min}, {lon_max}], Lat [{lat_min}, {lat_max}]")

# Função para converter GeoTIFF em NetCDF
def convert_tif_to_netcdf(tif_path, date):
    try:
        da = rioxarray.open_rasterio(tif_path).squeeze()
        da = da.rio.reproject("EPSG:4326")  # Reprojeta para sistema lat/lon convencional
        da = da.rio.clip_box(minx=lon_min, maxx=lon_max, miny=lat_min, maxy=lat_max) # Clipa a Area de Interesse
        da = da.rename({"x": "longitude", "y": "latitude"})

        if da.latitude.values[0] > da.latitude.values[-1]:
            da = da.sortby("latitude")

        da = da.expand_dims(time=[np.datetime64(date)])
        da.attrs.update({"units": "Celsius", "long_name": "Land Surface Temperature"})

        ds = da.to_dataset(name="LST")
        ds["latitude"].attrs["units"] = "degrees_north"
        ds["longitude"].attrs["units"] = "degrees_east"

        encoding = {"LST": {"zlib": True, "complevel": 4, "dtype": "float32"}}
        nc_path = tif_path.replace(".tif", ".nc")
        ds.to_netcdf(nc_path, engine="netcdf4", encoding=encoding)

        ds.close()
        da.close()
        print(f"  NetCDF criado: {os.path.basename(nc_path)}")
        return True
    except Exception as e:
        print(f"  Erro na conversão NetCDF: {repr(e)}")
        return False

# Função para baixar e salvar os dados do viirs
def download_and_save(date, collection_id, suffix):
    try:
        start_date = ee.Date(date)
        end_date = start_date.advance(1, 'day')

        collection = ee.ImageCollection(collection_id) \
            .filterBounds(aoi) \
            .filterDate(start_date, end_date)

        if collection.size().getInfo() == 0:
            print(f"  Sem dados para {date} ({suffix})")
            return False

        img = collection.first().select("LST_1KM")
        
        # Mask for valid temperatures (250-330K)
        valid_mask = img.gt(250).And(img.lt(330))
        img = img.updateMask(valid_mask)
        
        # Convert Kelvin to Celsius (NO multiplication by 0.01)
        img = img.subtract(273.15)

        url = img.getDownloadURL({
            'scale': 1000,
            'region': aoi,
            'format': 'GEO_TIFF'
        })

        response = requests.get(url, timeout=300)
        response.raise_for_status()

        filename = f"VIIRS_LST_{suffix}_{date}_LAT_{lat_min}_to_{lat_max}_LON_{lon_min}_to_{lon_max}.tif"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        if os.path.exists(filepath):
            tamanho = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  Salvo: {filename} ({tamanho:.2f} MB)")
            convert_tif_to_netcdf(filepath, date)
            return True
        else:
            print(f"  Falha ao salvar: {filename}")
            return False
    except Exception as e:
        print(f"  Erro para {date} ({suffix}): {str(e)[:100]}")
        return False

# IDs de coleção
day_collection = "NASA/VIIRS/002/VNP21A1D"
night_collection = "NASA/VIIRS/002/VNP21A1N"

# Processa todas as datas
success_day = []
success_night = []

for date in dates:
    print(f"\nProcessando data: {date} (Daytime)")
    if download_and_save(date, day_collection, "DAY"):
        success_day.append(date)

    print(f"\nProcessando data: {date} (Nighttime)")
    if download_and_save(date, night_collection, "NIGHT"):
        success_night.append(date)

# Relatório final
print("\n" + "="*50)
print("RELATÓRIO FINAL")
print("="*50)
print(f"Diretório de saída: {output_dir}")
print(f"Total de datas solicitadas: {len(dates)}")
print(f"Arquivos daytime salvos: {len(success_day)}")
print(f"Arquivos nighttime salvos: {len(success_night)}")

if success_day:
    print("\nDatas daytime com sucesso:")
    print(", ".join(success_day[:10]))
    if len(success_day) > 10:
        print(f"... e mais {len(success_day) - 10} datas")

if success_night:
    print("\nDatas nighttime com sucesso:")
    print(", ".join(success_night[:10]))
    if len(success_night) > 10:
        print(f"... e mais {len(success_night) - 10} datas")

print("\nProcesso completo!")

import sys

# Suppress repeated sys.excepthook errors
def silent_excepthook(exc_type, exc_value, exc_traceback):
    # Simply print the exception once, no recursion
    print(f"Uncaught exception: {exc_value}")

sys.excepthook = silent_excepthook
