
#Importar librerias de mysql
from mysql.connector import Error,connect
#Importar librerias para manejo de archivos
import pandas as pd
import os
from os.path import abspath, dirname
import tqdm

def org_xG(año_end:int, host_db, user_db, password_db, port_db)->None:
    """
    Funcion que organiza los datos de xG en una tabla de MySQL
    
    Parameters
    ----------
    año_end : int
        Año de final de temporada
    host_db : str
        Host de la base de datos
    user_db : str
        Usuario de la base de datos
    password_db : str
        Contraseña de la base de datos
    port_db : int
        Puerto de la base de datos
    Returns
    -------
    None

    Examples
    --------
    >>> org_xG(2021, "127.0.0.1", "root", "password", 3306)
    Conectado a la base de datos
    Tabla "xG" creada con exito o ya existente
    .
    .
    .
    Datos insertados correctamente en tabla xG
    """


    #Se crea la conexion a la base de datos
    try:
        with connect(
            host=host_db,
            user=user_db,
            password=password_db,
            autocommit = True,
            port = port_db 
        ) as conn:
            if conn.is_connected():
                print("Conectado a la base de datos"
        )
            #Creamos la base de datos
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS LIGA_MX")
            #Creamos la tabla para tabla xG en la base de datos
            cursor.execute("USE LIGA_MX")
            cursor.execute("CREATE TABLE IF NOT EXISTS xG (equipo VARCHAR(255), xG_L FLOAT, xG_V FLOAT, temporada VARCHAR(255))")
            print('Tabla "xG" creada con exito o ya existente')
            #Preparamos nuestro CSV para poder leer los datos de la tabla xG
            file_path=os.path.join(abspath(dirname(__file__)), "out-docs", "xG"+str(año_end-1)+"-"+str(año_end)+".csv")
            df = pd.read_csv(file_path)
            #Insertamos los datos del CSV a la tabla
            cursor.execute("TRUNCATE TABLE xG")
            progress_bar = tqdm.tqdm(total=len(df),desc="Insertando datos en xG, debido a limitaciones con el servidor, este proceso puede tardar hasta varios minutos")
            for row in df.itertuples():
                cursor.execute("INSERT INTO xG (equipo, xG_L, xG_V, temporada) VALUES (%s,%s,%s,%s)",row[1:])
                progress_bar.update(1)
            conn.commit()
            progress_bar.close()
            print("Datos insertados correctamente en tabla xG")
    except Error as e:
        print("Error al conectar con MySQL", e)
