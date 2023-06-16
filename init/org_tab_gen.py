
#Importar librerias de mysql
from mysql.connector import Error,connect
#Importar librerias para manejo de archivos
import pandas as pd
import os
from os.path import abspath, dirname
import tqdm
def org_tabla_est(año_strt:int, año_end:int, host_db:str, user_db:str, password_db:str, port_db:int)->None:
    """
    Funcion que organiza los datos de la tabla general en una tabla de MySQL

    Parameters
    ----------
    año_strt : int
        Año de inicio de temporada
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
    >>> org_tabla_est(2017,2021, "localhost", "root", "password", 3306)
    Conectado a la base de datos
    Tablas "TABLAGENERAL,OFENSIVA,DEFENSIVA" creadas con exito o ya existentes
    .
    .
    .
    Datos insertados correctamente en tabla TABLAGENERAL
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
            #Creamos la tabla para tabla general en la base de datos
            cursor.execute("USE LIGA_MX")
            cursor.execute("CREATE TABLE IF NOT EXISTS TABLAGENERAL (POS INT, equipo VARCHAR(255), JJ INT, JG INT, JE INT, JP INT, GF INT, GC INT, DIF INT, PTS INT, JJ_L INT, JG_L INT, JE_L INT, JP_L INT, GF_L INT, GC_L INT, DIF_L INT, PTS_L INT,JJ_V INT, JG_V INT, JE_V INT, JP_V INT, GF_V INT, GC_V INT, DIF_V INT, PTS_V INT, temporada VARCHAR(255))")
            #Creamos la tabla para ofensiva en la base de datos
            cursor.execute("CREATE TABLE IF NOT EXISTS OFENSIVA (POS INT, equipo VARCHAR(255), goles INT, temporada VARCHAR(255))")
            #Creamos la tabla para defensiva en la base de datos
            cursor.execute("CREATE TABLE IF NOT EXISTS DEFENSIVA (POS INT, equipo VARCHAR(255), goles_contra INT, temporada VARCHAR(255))")
            print('Tablas "TABLAGENERAL,OFENSIVA,DEFENSIVA" creadas con exito o ya existentes')

            #Preparamos nuestro CSV para poder leer los datos de la tabla general
            file_path=os.path.join(abspath(dirname(__file__)), "out-docs", "Tabla_General"+str(año_strt)+"-"+str(año_end)+".csv")
            df = pd.read_csv(file_path)
            #Insertamos los datos del CSV a la tabla
            cursor.execute("TRUNCATE TABLE TABLAGENERAL")
            progress_bar = tqdm.tqdm(total=len(df),desc="Insertando datos en TABLAGENERAL, debido a limitaciones con el servidor, este proceso puede tardar hasta varios minutos")
            for row in df.itertuples():
                    cursor.execute("INSERT INTO TABLAGENERAL (POS,equipo, JJ, JG, JE, JP, GF, GC, DIF, PTS, JJ_L, JG_L, JE_L, JP_L, GF_L, GC_L, DIF_L, PTS_L,JJ_V, JG_V, JE_V, JP_V, GF_V, GC_V, DIF_V, PTS_V, temporada) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",row[1:])
                    progress_bar.update(1)
            conn.commit()
            progress_bar.close()
            print("Datos insertados correctamente en tabla general")
            #Preparamos nuestro CSV para poder leer los datos de la tabla ofensiva
            file_path=os.path.join(abspath(dirname(__file__)), "out-docs", "Tabla_Ofensiva"+str(año_strt)+"-"+str(año_end)+".csv")
            df = pd.read_csv(file_path)
            #Insertamos los datos del CSV a la tabla
            cursor.execute("TRUNCATE TABLE OFENSIVA")
            progress_bar = tqdm.tqdm(total=len(df),desc="Insertando datos en OFENSIVA, debido a limitaciones con el servidor, este proceso puede tardar hasta varios minutos")
            for row in df.itertuples():
                cursor.execute("INSERT INTO OFENSIVA (POS,equipo, goles, temporada) VALUES (%s,%s,%s,%s)",row[1:])
                progress_bar.update(1)
            conn.commit()
            progress_bar.close()
            print("Datos insertados correctamente en tabla ofensiva")
            #Preparamos nuestro CSV para poder leer los datos de la tabla defensiva
            file_path=os.path.join(abspath(dirname(__file__)), "out-docs", "Tabla_Defensiva"+str(año_strt)+"-"+str(año_end)+".csv")
            df = pd.read_csv(file_path)
            #Insertamos los datos del CSV a la tabla
            cursor.execute("TRUNCATE TABLE DEFENSIVA")
            progress_bar = tqdm.tqdm(total=len(df),desc="Insertando datos en DEFENSIVA, debido a limitaciones con el servidor, este proceso puede tardar hasta varios minutos")
            for row in df.itertuples():
                cursor.execute("INSERT INTO DEFENSIVA (POS,equipo, goles_contra, temporada) VALUES (%s,%s,%s,%s)",row[1:])
                progress_bar.update(1)
            conn.commit()
            progress_bar.close()
            print("Datos insertados correctamente en tabla defensiva")
    except Error as e:
        print("Error al conectar con la base de datos", e)

#org_tabla_est(2010,2011)
