import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Tabla de correspondencia de ramales con su kilometraje de inicio y final, y el nombre del archivo .geojson correspondiente
# Line segments table: includes ID, start and end kilometers, and matching .geojson filename
ramales_inicio_final = pd.DataFrame(data=[
    ["PC-TY", 0.000, 16.000, "PC-Temperley"],
    ["TY-AK", 18.200, 55.000, "TY-A.Korn"],
    ["TY-ZZ", 16.000, 32.000, "TY-Ezeiza"],
    ["ZZ-CÑ", 32.000, 64.730, "Ezeiza-Cañuelas"],
    ["TY-HO", 17.400, 42.714, "TY-Haedo"],
    ["HE-JM", 18.433, 20.523, "ETY-Marmol"],
    ["ALL-LP", 4.000, 52.890, "ALL-La plata"],
    ["LP-TAVO", 52.890, 63.337, "LP-TAVO"],
    ["TY-BQ", 17.474, 34.006, "TY-Bosques"],
    ["BQ-VE", 34.006, 47.900, "Bosques-V.Elisa"],
    ["BZ-BQ", 25.004, 31.737, "Berazategui-Bosques"],
    ["AK-GG", 55.000, 235.000, "A.Korn-Guido"],
    ["GG-MPN", 235.000, 399.800, "Guido-MPN"],
    ["GG-DPN", 245.626, 345.759, "Guido-Pinamar"]
], columns=["ramal", "inicio", "final", "archivo"])

# Solicita la ruta del archivo con las posiciones / Ask for input Excel file with positions
file = input("Ingrese ruta del archivo excel con las posiciones:
").replace(""", "")
# Solicita la ruta de la carpeta con las trazas en .geojson / Ask for folder containing geojson traces
trazas = input("Ingrese ruta de los archivos de las trazas:
").replace(""", "")

# Carga el archivo Excel con los puntos a interpolar / Load Excel with kilometer points
data = pd.read_excel(file)

# Recorre cada fila del Excel / Loop through each Excel row
for i in data.index:
    ramal = data.loc[i, "Ramal"]  # Nombre del ramal / Segment name
    kms = data.loc[i, "Punto Medio"]  # Progresiva en km / Kilometer reference

    # Obtiene info del ramal / Retrieve matching trace info
    archivo = ramales_inicio_final[ramales_inicio_final["ramal"] == ramal]["archivo"].item()
    inicio = ramales_inicio_final[ramales_inicio_final["ramal"] == ramal]["inicio"].item()
    final = ramales_inicio_final[ramales_inicio_final["ramal"] == ramal]["final"].item()

    # Carga la traza en formato geojson / Load the .geojson trace
    path_gdf = gpd.read_file(trazas + "\" + archivo + ".geojson")
    line = path_gdf.geometry.iloc[0]  # Se asume una única línea / Assumes a single linear geometry

    # Calcula el punto interpolado sobre la traza / Interpolates location along the line
    total_length = line.length
    point = line.interpolate((kms - inicio) / (final - inicio) * total_length)

    # Almacena coordenadas (lat, lon) como string / Store lat, lon as string
    data.loc[i, "Coordenadas"] = f"{point.y}, {point.x}"
    data.loc[i, "ID"] = i + 1  # Asigna ID único / Assign unique ID

# Asigna identificador por ubicación para Power BI / Group duplicate coordinates under single "Ubicación"
i = 1
for coord in data["Coordenadas"].drop_duplicates():
    data.loc[data["Coordenadas"] == coord, "Ubicación"] = i
    i += 1

# Guarda nuevo archivo Excel / Save new Excel file with results
data.to_excel(str(file[:-5] + "_post.xlsx"), index=False)