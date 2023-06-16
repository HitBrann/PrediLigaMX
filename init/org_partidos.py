
#Importar librerias de mysql
from mysql.connector import Error,connect
#Importar librerias para manejo de archivos
import pandas as pd
import os
from os.path import abspath, dirname
import tqdm
def org_partidos(año_strt:str,año_end:str,host_db:str,user_db:str,password_db:str,port_db:int)->None:
    '''Esta función organiza los partidos en una tabla de la base de datos

    Parameters
    ----------
    año_strt : str
        Año de inicio de la temporada
    año_end : str
        Año de fin de la temporada
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
        Esta función no retorna nada, solo organiza los partidos en una tabla de la base de datos
    
    Examples
    --------
    >>> org_partidos(2010,2011,"localhost","root","password",3306)
    Conectado a la base de datos
    base de datos creada
    Tabla "PARTIDOS" creada o ya existente
    Insertando datos en PARTIDOS, debido a limitaciones con el servidor, este proceso puede tardar hasta varios minutos
    Datos de partidos insertados correctamente
    
    '''




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
            print("base de datos creada")
            #Creamos la tabla de la base de datos
            cursor.execute("USE LIGA_MX")
            cursor.execute("CREATE TABLE IF NOT EXISTS PARTIDOS (ID INT AUTO_INCREMENT PRIMARY KEY, temporada VARCHAR(255), fecha VARCHAR(255), jornada VARCHAR(255), equipo_local VARCHAR(255), equipo_visitante VARCHAR(255), goles_local INT, goles_visitante INT, estadio VARCHAR(255))")
            print('Tabla "PARTIDOS" creada o ya existente')

    #Preparamos nuestro CSV para poder leerlo
            file_path=os.path.join(abspath(dirname(__file__)), "out-docs", "Partidos"+str(año_strt)+"-"+str(año_end)+".csv")
            df = pd.read_csv(file_path)
    #Insertamos los datos del CSV a la tabla
            cursor.execute("TRUNCATE TABLE PARTIDOS")
            print("Insertando datos en PARTIDOS, debido a limitaciones con el servidor, este proceso puede tardar hasta varios minutos")
            progress_bar = tqdm.tqdm(total=len(df))
            for row in df.itertuples():
                cursor.execute("INSERT INTO PARTIDOS (ID, temporada, fecha, jornada, equipo_local, equipo_visitante, goles_local, goles_visitante, estadio) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",row[1:])
                progress_bar.update(1)
            conn.commit()
            progress_bar.close()
            print("Datos de partidos insertados correctamente")
    except Error as e:
        print("Error al conectar con la base de datos", e)


