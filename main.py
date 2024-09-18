import pandas as pd
from datetime import datetime

# Cargar el archivo CSV
ruta_archivo = 'BaseDeLibros.csv'
libros_df = pd.read_csv(ruta_archivo)

# Calcula la puntuación de relevancia basada en palabra clave y otros factores
def calcular_relevancia(libro, palabra_clave_busqueda):
    # Pesos
    peso_palabra_clave = 0.4
    peso_popularidad = 0.3
    peso_actualidad = 0.2
    peso_calificacion_usuario = 0.1
    
    # Verifica la palabra clave en título, resumen y lista de palabras clave
    puntuacion_palabra_clave = 0
    if palabra_clave_busqueda.lower() in libro['Titulo'].lower():
        puntuacion_palabra_clave += 2  # Puntuación más alta para coincidencia en el título
    if palabra_clave_busqueda.lower() in libro['Resumen'].lower():
        puntuacion_palabra_clave += 1.5
    if palabra_clave_busqueda.lower() in libro['PalabrasClave'].lower():
        puntuacion_palabra_clave += 1
    
    # Convertir la fecha de publicación a formato de año y normalizar la actualidad
    try:
        anio_publicacion = datetime.strptime(libro['FechaPublicacion'], "%Y-%m-%d").year
    except:
        anio_publicacion = 2000  # Año predeterminado si falla el análisis
    anio_actual = 2024
    puntuacion_actualidad = (anio_actual - anio_publicacion) / 100.0  # Normalizar actualidad
    
    # Puntuación de popularidad (basada en la columna Popularidad)
    puntuacion_popularidad = libro['Popularidad'] / 10000.0  # Normalizar popularidad
    
    # Puntuación de calificación de usuario (combinar calificación y número de calificaciones)
    puntuacion_calificacion_usuario = (libro['CalificacionUsuario'] * libro['NumeroDeCalidicaciones']) / 10000.0  # Normalizar calificación
    
    # Puntuación de relevancia final
    puntuacion_total = (puntuacion_palabra_clave * peso_palabra_clave +
                        puntuacion_popularidad * peso_popularidad +
                        (1 / (puntuacion_actualidad + 0.1)) * peso_actualidad +  # Agregar 0.1 para evitar división por cero
                        puntuacion_calificacion_usuario * peso_calificacion_usuario)
    
    return puntuacion_total

# Realizar la búsqueda usando una palabra clave y clasificar los resultados por relevancia
palabra_clave_busqueda = "distopia"  # Ejemplo de búsqueda por palabra clave
libros_df['Relevancia'] = libros_df.apply(lambda libro: calcular_relevancia(libro, palabra_clave_busqueda), axis=1)

# Ordenar libros por relevancia en orden descendente
libros_clasificados = libros_df.sort_values(by='Relevancia', ascending=False)

# Guardar los resultados clasificados en un archivo CSV o imprimirlos
libros_clasificados.to_csv('LibrosClasificadosPorRelevancia.csv', index=False)
print(libros_clasificados[['Titulo', 'Relevancia']].head())  # Imprimir los 5 primeros resultados