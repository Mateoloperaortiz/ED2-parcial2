import pandas as pd
from datetime import datetime

# Cargar el archivo CSV
ruta_archivo = 'BaseDeLibros.csv'

try:
    libros_df = pd.read_csv(ruta_archivo)
except FileNotFoundError:
    print(f"Error: El archivo '{ruta_archivo}' no se encontró.")
    exit()
except Exception as e:
    print(f"Error al cargar el archivo: {e}")
    exit()

# Función para calcular la relevancia
def calcular_relevancia(libro, palabra_clave_busqueda):
    try:
        # Pesos fijos
        peso_palabra_clave = 0.4
        peso_popularidad = 0.3
        peso_actualidad = 0.2
        peso_calificacion_usuario = 0.1

        # Verifica la palabra clave en título, resumen y lista de palabras clave
        puntuacion_palabra_clave = 0
        titulo = str(libro['Title'])
        abstract = str(libro['Abstract'])
        keywords = str(libro['Keywords'])

        if palabra_clave_busqueda.lower() in titulo.lower():
            puntuacion_palabra_clave += 2  # Puntuación más alta para coincidencia en el título
        if palabra_clave_busqueda.lower() in abstract.lower():
            puntuacion_palabra_clave += 1.5
        if palabra_clave_busqueda.lower() in keywords.lower():
            puntuacion_palabra_clave += 1

        # Convertir la fecha de publicación a formato de año y normalizar la actualidad
        try:
            anio_publicacion = datetime.strptime(str(libro['PublicationDate']), "%Y-%m-%d").year
        except ValueError:
            anio_publicacion = 2000  # Año predeterminado si falla el análisis
        anio_actual = datetime.now().year
        puntuacion_actualidad = (anio_actual - anio_publicacion) / 100.0  # Normalizar actualidad

        # Puntuación de popularidad (basada en la columna Popularity)
        puntuacion_popularidad = float(libro['Popularity']) / 10000.0  # Normalizar popularidad

        # Puntuación de calificación de usuario (combinar calificación y número de calificaciones)
        puntuacion_calificacion_usuario = (float(libro['UserRating']) * float(libro['NumberOfRatings'])) / 10000.0  # Normalizar calificación

        # Puntuación de relevancia final
        puntuacion_total = (puntuacion_palabra_clave * peso_palabra_clave +
                            puntuacion_popularidad * peso_popularidad +
                            (1 / (puntuacion_actualidad + 0.1)) * peso_actualidad +  # Agregar 0.1 para evitar división por cero
                            puntuacion_calificacion_usuario * peso_calificacion_usuario)

        return puntuacion_total

    except Exception as e:
        print(f"Error al calcular la relevancia para el libro '{libro.get('Title', 'Desconocido')}': {e}")
        return 0  # Asignar relevancia cero si hay un error

# Solicitar entrada del usuario
palabra_clave_busqueda = input("Ingrese la palabra clave de búsqueda: ")

# Validar que la palabra clave no esté vacía
if not palabra_clave_busqueda.strip():
    print("Error: La palabra clave de búsqueda no puede estar vacía.")
    exit()

# Calcular la relevancia para cada libro
try:
    libros_df['Relevancia'] = libros_df.apply(lambda libro: calcular_relevancia(libro, palabra_clave_busqueda), axis=1)
except Exception as e:
    print(f"Error al calcular la relevancia: {e}")
    exit()

# Ordenar libros por relevancia en orden descendente
libros_clasificados = libros_df.sort_values(by='Relevancia', ascending=False)

# Solicitar al usuario cuántos resultados quiere ver
try:
    num_resultados = int(input("\n¿Cuántos resultados desea ver? "))
    if num_resultados <= 0:
        raise ValueError("El número de resultados debe ser un entero positivo.")
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Mostrar los resultados
print("\nLos libros más relevantes son:\n")

# Crear una columna para el año de publicación si no existe
if 'PublicationYear' not in libros_clasificados.columns:
    libros_clasificados['PublicationYear'] = libros_clasificados['PublicationDate'].apply(
        lambda x: x.split('-')[0] if isinstance(x, str) and '-' in x else 'Desconocido'
    )

# Definir las columnas a mostrar
columnas_a_mostrar = ['Title', 'Authors', 'PublicationYear', 'Relevancia']

# Mostrar los resultados sin índices
try:
    print(libros_clasificados[columnas_a_mostrar].head(num_resultados).to_string(index=False))
except KeyError as e:
    print(f"Error: La columna {e} no se encontró en los datos.")
    exit()

# Opcional: Guardar los resultados en un archivo CSV
guardar_csv = input("\n¿Desea guardar los resultados en un archivo CSV? (s/n): ")
if guardar_csv.lower() == 's':
    nombre_archivo = input("Ingrese el nombre del archivo (ejemplo: resultados.csv): ")
    try:
        libros_clasificados.to_csv(nombre_archivo, index=False)
        print(f"Resultados guardados en {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
