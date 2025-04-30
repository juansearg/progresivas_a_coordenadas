import pandas as pd
import geopandas as gpd

ramales_inicio_final= pd.DataFrame( data=  [["PC-TY",	0.000,	16.000, "PC-Temperley"],
                                           ["TY-AK", 18.200,	55.000, "TY-A.Korn"],
                                           ["TY-ZZ", 16.000,	32.000, "TY-Ezeiza"],
                                           ["ZZ-CÑ", 32.000,	64.730, "Ezeiza-Cañuelas"],
                                           ["TY-HO", 17.400,	42.714, "TY-Haedo"],
                                           ["HE-JM", 18.433,	20.523, "ETY-Marmol"],
                                           ["ALL-LP",   4.000,	52.890, "ALL-La plata"],
                                           ["LP-TAVO", 52.890, 63.337, "LP-TAVO"],
                                           ["TY-BQ",    17.474,	34.006, "TY-Bosques"],
                                           ["BQ-VE",	34.006,	47.900, "Bosques-V.Elisa"],
                                           ["BZ-BQ",	25.004,	31.737, "Berazategui-Bosques"],
                                           ["AK-GG",	55.000,	235.000, "A.Korn-Guido"],
                                           ["GG-MPN",	235.000, 399.800, "Guido-MPN"],
                                           ["GG-DPN",	245.626,	345.759, "Guido-Pinamar"]]
                                           , columns=["ramal", "inicio", "final", "archivo"])


file = input("Ingrese ruta del archivo excel con las posiciones:\n")
file = file.replace("\"","")
trazas = input("Ingrese ruta de los archivos de las trazas:\n")
trazas = trazas.replace("\"","")

data = pd.read_excel(file)

from shapely.geometry import Point


for i in data.index:
    ramal = data.loc[i,"Ramal"]
    archivo = ramales_inicio_final[ramales_inicio_final["ramal"]==ramal]["archivo"].item()
    inicio = ramales_inicio_final[ramales_inicio_final["ramal"]==ramal]["inicio"].item()
    final = ramales_inicio_final[ramales_inicio_final["ramal"]==ramal]["final"].item()
    kms = data.loc[i,"Punto Medio"]
    # Load the GeoJSON file
    path_gdf = gpd.read_file(trazas+"\\"+archivo+".geojson")

    line = path_gdf.geometry.iloc[0]  # Asumo que es una linea
    # Defino inicio y final KMS
    kms_initial = inicio
    kms_final = final # en km

    total_length = line.length


    point = line.interpolate((kms - kms_initial) / (kms_final - kms_initial) * total_length)
    data.loc[i,"Coordenadas"]=f"{point.y}, {point.x}"
    data.loc[i,"ID"]=i+1

i=1
for coord in data["Coordenadas"].drop_duplicates():
    data.loc[data["Coordenadas"]==coord,"Ubicación"]=i
    i+=1


data.to_excel(str(file[:-5]+"_post.xlsx"),index=False)
