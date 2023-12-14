import sqlite3


def crear_tabla():
    """Crea la base de datos y la tabla.
    """
    with sqlite3.connect("Ranking_Dino.db") as conexion:
        try:
            sentencia = ''' create table ranking
                            (
                                nombre text primary key,
                                puntaje integer
                            )
                    ''' 
            conexion.execute(sentencia)
            print("Se creo la tabla ranking")
        except sqlite3.OperationalError:
            print("La tabla ranking ya existe")

def insertar_campos(nombre_jugador:str, puntaje:int):
    """Inserta campos si no existen.
    """
    with sqlite3.connect("Ranking_Dino.db") as conexion:
        try:
            if not chequear_existencias(nombre_jugador):
                conexion.execute("INSERT INTO ranking (nombre,puntaje) values(?,?)", (nombre_jugador, puntaje))
                conexion.commit()
            else:
                sentencia = "UPDATE ranking SET puntaje = ? WHERE nombre=?"
                conexion.execute(sentencia, (puntaje, nombre_jugador))
        except Exception as e:
            print("Error al insertar el campo.")

def chequear_existencias(value:str):
    """Verifica si existe una posicion en la base de datos.

    Recibe: nombre del jugador.
    Retorna: Una lista con las filas encontradas.
    """
    with sqlite3.connect("Ranking_Dino.db") as conexion:
        sentencia = "SELECT * FROM ranking WHERE nombre=?"
        cursor = conexion.execute(sentencia, (value,))
        filas=cursor.fetchall()
        return filas

def get_lista():
    with sqlite3.connect("Ranking_Dino.db") as conexion:
        sentencia = "SELECT * FROM ranking ORDER BY puntaje DESC LIMIT 5"
        cursor = conexion.execute(sentencia)
        filas=cursor.fetchall()
        return filas

def obtener_puntuaciones():
    #Conecto a la base de datos
    conexion = sqlite3.connect('Ranking')
    cursor = conexion.cursor()

    #Obtengo las puntuaciones ordenadas por puntaje descendente
    cursor.execute("SELECT nombre, puntuacion FROM tabla_puntuaciones ORDER BY puntuacion DESC")
    puntuaciones = cursor.fetchall()

    #Cierro la conexión a la base de datos
    conexion.close()

    return puntuaciones


