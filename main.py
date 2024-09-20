import pandas as pd
from datetime import datetime

# Cargar el archivo CSV
ruta_archivo = 'BaseDeLibros.csv'
libros_df = pd.read_csv(ruta_archivo)

# Función para calcular la relevancia
def calcular_relevancia(libro, palabra_clave_busqueda):
    # Pesos fijos
    peso_palabra_clave = 0.4
    peso_popularidad = 0.3
    peso_actualidad = 0.2
    peso_calificacion_usuario = 0.1

    # Verifica la palabra clave en título, resumen y lista de palabras clave
    puntuacion_palabra_clave = 0
    if palabra_clave_busqueda.lower() in libro['Title'].lower():
        puntuacion_palabra_clave += 2  # Puntuación más alta para coincidencia en el título
    if palabra_clave_busqueda.lower() in libro['Abstract'].lower():
        puntuacion_palabra_clave += 1.5
    if palabra_clave_busqueda.lower() in libro['Keywords'].lower():
        puntuacion_palabra_clave += 1

    # Convertir la fecha de publicación a formato de año y normalizar la actualidad
    try:
        anio_publicacion = datetime.strptime(libro['PublicationDate'], "%Y-%m-%d").year
    except:
        anio_publicacion = 2000  # Año predeterminado si falla el análisis
    anio_actual = datetime.now().year
    puntuacion_actualidad = (anio_actual - anio_publicacion) / 100.0  # Normalizar actualidad

    # Puntuación de popularidad (basada en la columna Popularidad)
    puntuacion_popularidad = libro['Popularity'] / 10000.0  # Normalizar popularidad

    # Puntuación de calificación de usuario (combinar calificación y número de calificaciones)
    puntuacion_calificacion_usuario = (libro['UserRating'] * libro['NumberOfRatings']) / 10000.0  # Normalizar calificación

    # Puntuación de relevancia final
    puntuacion_total = (puntuacion_palabra_clave * peso_palabra_clave +
                        puntuacion_popularidad * peso_popularidad +
                        (1 / (puntuacion_actualidad + 0.1)) * peso_actualidad +  # Agregar 0.1 para evitar división por cero
                        puntuacion_calificacion_usuario * peso_calificacion_usuario)

    return puntuacion_total

# Solicitar entrada del usuario
palabra_clave_busqueda = input("Ingrese la palabra clave de búsqueda: ")

# Calcular la relevancia para cada libro
libros_df['Relevancia'] = libros_df.apply(lambda libro: calcular_relevancia(libro, palabra_clave_busqueda), axis=1)

# Ordenar libros por relevancia en orden descendente
libros_clasificados = libros_df.sort_values(by='Relevancia', ascending=False)

# Solicitar al usuario cuántos resultados quiere ver
num_resultados = int(input("\n¿Cuántos resultados desea ver? "))

# Mostrar los resultados
print("\nLos libros más relevantes son:\n")
print(libros_clasificados[['Title', 'Relevancia']].head(num_resultados))

# Opcional: Guardar los resultados en un archivo CSV
guardar_csv = input("\n¿Desea guardar los resultados en un archivo CSV? (s/n): ")
if guardar_csv.lower() == 's':
    nombre_archivo = input("Ingrese el nombre del archivo (ejemplo: resultados.csv): ")
    libros_clasificados.to_csv(nombre_archivo, index=False)
    print(f"Resultados guardados en {nombre_archivo}")
