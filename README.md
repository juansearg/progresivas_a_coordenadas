# Georreferenciador de Puntos Kilométricos sobre Trazas Lineales (.geojson)

Este proyecto permite georreferenciar puntos intermedios ubicados sobre trazas ferroviarias, utilizando datos en formato Excel y archivos de trazado en formato `.geojson`.

## 🧾 Requisitos previos

- Python 3.x
- Bibliotecas necesarias:
  - `pandas`
  - `geopandas`
  - `shapely`
  - `openpyxl`

Instalación rápida:
```bash
pip install pandas geopandas openpyxl
```

## 📝 Uso

1. **Completar `POSICIONES.xlsx`:**
   - Rellenar las columnas `Ramal` y `Punto Medio` (progresiva en kilómetros).
   - El archivo no necesita más columnas, las demás se completarán automáticamente.

2. **Ejecutar el script:**
   - Al ejecutar el script `Georeferencias_v1.py`, se solicitará:
     1. La ruta del archivo `POSICIONES.xlsx`.
     2. El directorio donde se encuentran los archivos `.geojson` con las trazas lineales.
   - El script interpolará las posiciones de acuerdo con la progresiva (km) sobre la traza correspondiente.

3. **Salida:**
   - Se genera un archivo Excel nuevo (`*_post.xlsx`) en el mismo directorio del archivo original, con las siguientes columnas completadas:
     - `Coordenadas` (latitud, longitud).
     - `ID` (número secuencial).
     - `Ubicación` (identificador único por ubicación, necesario para uso en Power BI con el visual [IconMap](https://icon-map.com) (compatible con versiones previas a marzo 2025)).

## ⚠️ Recomendaciones

- Las trazas `.geojson` **deben ser lineales**, sin bifurcaciones. Si hay ramas, deben ser tratadas como ramales independientes.
- El archivo `Georeferencias_v1.py` contiene una tabla interna (`ramales_inicio_final`) que indica el inicio y final (en km) de cada ramal. Asegúrate de que los nombres coincidan con los ingresados en el Excel.

---

## 🌍 English Section — Adaptable for Any Linear GeoJSON Track

This script georeferences kilometer-based intermediate points onto linear `.geojson` tracks.

### How it works:
1. Input an Excel file with:
   - A column `Ramal` (or segment ID).
   - A column `Punto Medio` (middle point in kilometers).
2. Select the folder with `.geojson` files representing **linear paths**.
3. The script:
   - Interpolates the provided kilometer value over the corresponding line.
   - Outputs a new Excel file with latitude/longitude (`Coordenadas`), sequential `ID`, and unique `Ubicación`.

> Note: Each `.geojson` file must represent a single, non-branching path. For branched segments, separate them into different `.geojson` files.

This can be adapted for any infrastructure involving linear references: railways, pipelines, roads, etc.

## 📂 Ejemplo de archivo de entrada

| Ramal | Punto Medio |
|-------|-------------|
| TY-AK | 22.5        |
| ZZ-CÑ | 41.2        |

## 📤 Salida esperada

| Ramal | Punto Medio | Coordenadas         | ID | Ubicación |
|-------|-------------|---------------------|----|-----------|
| TY-AK | 22.5        | -34.1234, -58.4567  | 1  | 1         |
| ZZ-CÑ | 41.2        | -34.2345, -58.6789  | 2  | 2         |