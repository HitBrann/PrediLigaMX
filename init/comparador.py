import sys
import pandas as pd
from mysql.connector import Error,connect
#Importar librerias para manejo de archivos
import pandas as pd
import os
import tqdm
try:
    from monte_carlo import Montecarlo
except ModuleNotFoundError:
    from init.monte_carlo import Montecarlo
import threading
def comparador(host_db:str,user_db:str,password_db:str,port_db:int )->None:
    """
    Función que compara los resultados de la simulación con los resultados reales

    Parameters
    ----------
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
    >>> comparador("127.0.0.1","root","root",3306)
    Conectado a la base de datos
    Simulando partidos: 100%|████████████████████████████████
    Simulación terminada
    Porcentaje de aciertos:  41.17
    """
    #Connect to the database
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
            #Obtenemos los equipos y sus respectivos goles de la tabla de comprobacion
            cursor = conn.cursor()
            cursor.execute("USE LIGA_MX")
            cursor.execute("SELECT equipo_local, equipo_visitante, goles_local, goles_visitante FROM COMPROBACION")
            df = pd.DataFrame(cursor.fetchall())
            df.columns = cursor.column_names
            #Creamos una lista con los equipos locales
            equipos_l = df['equipo_local'].tolist()
            #Creamos una lista con los equipos visitantes
            equipos_v = df['equipo_visitante'].tolist()
            #Creamos una lista con los goles locales
            goles_l = df['goles_local'].tolist()
            #Creamos una lista con los goles visitantes
            goles_v = df['goles_visitante'].tolist()
            #Creamos una lista para guardar los resultados
            resultados = []
            #Haremos un ciclo para comparar los goles de los equipos
            for i in range(len(equipos_l)):
                if goles_l[i] > goles_v[i]:
                    resultados.append(0)
                elif goles_l[i] < goles_v[i]:
                    resultados.append(1)
                else:
                    resultados.append(2)
            #Cerramos la conexión
            cursor.close()
            conn.close()
            #Creamos una lista para guardar los resultados de la simulación
            resultados_sim_th1 = []
            resultados_sim_th2 = []
            resultados_sim_th3 = []
            resultados_sim_th4 = []
            #Apagamos el print de la simulación
            sys.stdout = open(os.devnull, 'w')
            #Creamos las simulaciones por montecarlo
            #Diccionario para guardar los equipos y sus numeros
            equipos = {'América':1, 'Atlas':2, 'Club Atlético de San Luis':3, 'Cruz Azul':4, 'FC Juárez':5, 'Guadalajara':6, 'León':7, 'Mazatlán FC':8, 'Monterrey':9, 'Necaxa':10, 'Pachuca':11, 'Puebla':12, 'Pumas':13, 'Querétaro':14, 'Santos Laguna':15, 'Tigres':16, 'Tijuana':17, 'Toluca':18}
            progress = tqdm.tqdm(total= len(equipos_l), desc="Simulando partidos", position=0, leave=False)
            #Creamos un ciclo para simular los partidos en paralelo manteniendo el orden de la lista usando 4 hilos
            def worker1():
                for i in range(0, (len(equipos_l))//4):
                    resultados_sim_th1.append((i,Montecarlo(host_db,user_db,password_db,port_db,equipos[equipos_l[i]],equipos[equipos_v[i]],100)))
                    progress.update(1)
            def worker2():
                for i in range(len(equipos_l)//4, len(equipos_l)//2):
                    resultados_sim_th2.append((i,Montecarlo(host_db,user_db,password_db,port_db,equipos[equipos_l[i]],equipos[equipos_v[i]],100)))
                    progress.update(1)
            def worker3():
                for i in range(len(equipos_l)//2, (len(equipos_l)//4)*3):
                    resultados_sim_th3.append((i,Montecarlo(host_db,user_db,password_db,port_db,equipos[equipos_l[i]],equipos[equipos_v[i]],100)))
                    progress.update(1)
            def worker4():
                for i in range((len(equipos_l)//4)*3, len(equipos_l)):
                    resultados_sim_th4.append((i,Montecarlo(host_db,user_db,password_db,port_db,equipos[equipos_l[i]],equipos[equipos_v[i]],100)))
                    progress.update(1)
            #Creamos los hilos
            t1=threading.Thread(target=worker1)
            t2=threading.Thread(target=worker2)
            t3=threading.Thread(target=worker3)
            t4=threading.Thread(target=worker4)
            #Iniciamos los hilos
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            #Esperamos a que terminen los hilos
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            #Cerramos el progress bar
            progress.close()
            #Encendemos el print
            sys.stdout = sys.__stdout__
            print("Simulación terminada")
            #Unimos los resultados de la simulación en una sola lista
            resultados_sim=[]
            resultados_sim=resultados_sim_th1+resultados_sim_th2+resultados_sim_th3+resultados_sim_th4
            #Compararemos los resultados de la simulación con los resultados de la tabla de comprobación y crearemos una lista con los resultados
            resultados_totales = []
            for i in range(len(resultados)):
                if resultados[i] == resultados_sim[i][1]:
                    resultados_totales.append(1)
                else:
                    resultados_totales.append(0)
            #Saca el porcentaje de aciertos
            porcentaje = (sum(resultados_totales)/len(resultados_totales))*100
            print("Porcentaje de aciertos: ", porcentaje)
    except Error as e:
        print("Error al conectarse a la base de datos", e)
