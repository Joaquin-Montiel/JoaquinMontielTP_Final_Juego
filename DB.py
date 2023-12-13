import sqlite3

def crear_tabla_puntuaciones():
    # Conectar a la base de datos (esto creará la base de datos si no existe)
    conexion = sqlite3.connect('Ranking Dino')
    cursor = conexion.cursor()

    # Crear la tabla "tabla_puntuaciones"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tabla_puntuaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puntuacion INTEGER NOT NULL
        )
    ''')

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

def obtener_puntuaciones():
    # Conectar a la base de datos
    conexion = sqlite3.connect('Ranking Dino')
    cursor = conexion.cursor()

    # Obtener las puntuaciones ordenadas por puntaje descendente
    cursor.execute("SELECT nombre, puntuacion FROM tabla_puntuaciones ORDER BY puntuacion DESC")
    puntuaciones = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    return puntuaciones

# crear_tabla_puntuaciones()