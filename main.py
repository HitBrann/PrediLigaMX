import threading
import time
import sys
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
sys.path.append('./init')
ChromeDriverManager().install()
from init.scraperestadistica import scrapper_estadistica
from init.scraperpartidos import scrapper_partidos
from init.scraperxG import scrapper_xG
from init.org_partidos import org_partidos
from init.org_tab_gen import org_tabla_est
from init.org_xG import org_xG
from init.monte_carlo import Montecarlo
from init.org_comp import org_tabla_comp
from init.comparador import comparador
from os.path import abspath, dirname
import os
from getpass import getpass
import mysql.connector
from mysql.connector import Error

#Preparamos nuestro json para leer los datos de la base de datos si es que existen
#Si no existe la carpeta dev la creamos
if not os.path.exists(os.path.join(abspath(dirname(__file__)), "dev")):
    os.mkdir(os.path.join(abspath(dirname(__file__)), "dev"))
#Si no existe el archivo database.json lo creamos
if not os.path.exists(os.path.join(abspath(dirname(__file__)), "dev", "database.json")):
    with open(os.path.join(abspath(dirname(__file__)), "dev", "database.json"), "w") as file:
        data = {}
        data["host"] = "localhost"
        data["user"] = "default"
        data["password"] = "default"
        data["port"] = 3306
        json.dump(data, file)
#Lo leemos
file_path=os.path.join(abspath(dirname(__file__)), "dev", "database.json")
with open(file_path) as file:
    data = json.load(file)
    host_db = data["host"]
    user_db = data["user"]
    password_db = data["password"]
    port_db = data["port"]

password_tries = 0
#Revisamos si los datos de la base de datos son los default
if host_db == "localhost" and user_db == "default" and password_db == "default" and port_db == 3306:
    print("Parece que no se han configurado los datos de la base de datos, ¿Le gustaría configurarlos?")
    while True:
        try:
            inp=input("Configurar datos de la base de datos? (Si/No): ")
            if inp == "S" or inp == "s" or inp == "si" or inp == "Si":
                host_db = input("Ingrese host de la base de datos: ")
                try:
                    print("El puerto default es 3306, dejalo en blanco si quieres usarlo")
                    port_db = int(input("Ingrese puerto de la base de datos: "))
                except ValueError:
                    print("No ingresaste un número, se usará el puerto default 3306")
                    port_db = 3306
                except NameError:
                    print("No ingresaste un número, se usará el puerto default 3306")
                    port_db = 3306
                user_db = input("Ingrese usuario de la base de datos: ")
                with open(file_path, "w") as file:
                    data["host"] = host_db
                    data["user"] = user_db
                    data["password"] = "not default"
                    data["port"] = port_db
                    json.dump(data, file)
                print("La contraseña no se mostrará en pantalla ni se guardará en el archivo, por lo que deberá ingresarla cada vez que inicie el programa")
                while True:
                    password_db = getpass("Ingrese contraseña de la base de datos: ")
                    #Nos conectamos a la base de datos para comprobar la contraseña
                    try:
                        connection = mysql.connector.connect(host=host_db,
                                                            port=port_db,
                                                            user=user_db,
                                                            password=password_db)
                        if connection.is_connected():
                            db_Info = connection.get_server_info()
                            cursor = connection.cursor()
                            print("Contraseña correcta",db_Info)
                            break
                    except Error as e:
                        if "Access denied for user" in str(e):
                            print("Contraseña incorrecta, intenta de nuevo")
                            password_tries += 1
                        else:
                            print("Error al conectar a la base de datos", e)
                            print("Por favor, revisa los datos de la base de datos en el archivo database.json en la carpeta <<dev>> del programa o reinicie propio programa para volver a configurar la base de datos")
                            #Borramos el archivo database.json
                            os.remove(file_path)
                            #Creamos el archivo database.json con los datos default
                            with open(os.path.join(abspath(dirname(__file__)), "dev", "database.json"), "w") as file:
                                data = {}
                                data["host"] = "localhost"
                                data["user"] = "default"
                                data["password"] = "default"
                                data["port"] = 3306
                                json.dump(data, file)
                            time.sleep(5)
                            sys.exit()
                        if password_tries >= 3:
                            print("Demasiados intentos, cerrando programa...")
                            #Borramos el archivo database.json
                            os.remove(file_path)
                            #Creamos el archivo database.json con los datos default
                            with open(os.path.join(abspath(dirname(__file__)), "dev", "database.json"), "w") as file:
                                data = {}
                                data["host"] = "localhost"
                                data["user"] = "default"
                                data["password"] = "default"
                                data["port"] = 3306
                                json.dump(data, file)
                            time.sleep(5)
                            sys.exit()
                print("Datos de la base de datos configurados correctamente")
                print("En caso de haber cometido un error, puedes modificar los datos en el archivo database.json en la carpeta <<dev>> del programa o reiniciar el programa en caso de mensaje de error")
                time.sleep(5)
                break
            elif inp == "N" or inp == "n" or inp == "no" or inp == "No":
                break
            else:
                print("No ingresaste una opción válida, intenta de nuevo")
        except ValueError:
            print("No ingresaste una opción válida, intenta de nuevo")
        except NameError:
            print("No ingresaste una opción válida, intenta de nuevo")
else:
    print("Los datos de la base de datos ya están configurados, si deseas modificarlos, puedes hacerlo en el archivo database.json en la carpeta <<dev>> del programa")
    while True:
        password_db = getpass("Ingrese contraseña de la base de datos: ")
        #Nos conectamos a la base de datos para comprobar la contraseña
        try:
            connection = mysql.connector.connect(host=host_db,
                                                port=port_db,
                                                user=user_db,
                                                password=password_db)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                print("Contraseña correcta",db_Info)
                break
        except Error as e:
            if "Access denied for user" in str(e):
                print("Contraseña incorrecta, intenta de nuevo")
                password_tries += 1
            else:
                print("Error al conectar a la base de datos", e)
                print("Por favor, revisa los datos de la base de datos en el archivo database.json en la carpeta <<dev>> del programa o reinicie propio programa para volver a configurar la base de datos")
                #Borramos el archivo database.json
                os.remove(file_path)
                #Creamos el archivo database.json con los datos default
                with open(os.path.join(abspath(dirname(__file__)), "dev", "database.json"), "w") as file:
                    data = {}
                    data["host"] = "localhost"
                    data["user"] = "default"
                    data["password"] = "default"
                    data["port"] = 3306
                    json.dump(data, file)
                time.sleep(5)
                sys.exit()
            if password_tries >= 3:
                print("Demasiados intentos, cerrando programa...")
                time.sleep(5)
                sys.exit()

#Realizamos una prueba de conexión a la base de datos
try:
    connection = mysql.connector.connect(host=host_db,
                                         port=port_db,
                                         user=user_db,
                                         password=password_db)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Conectado a la base de datos MySQL Server versión ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Conectado a la base de datos ", record)
except Error as e:
    print("Error al conectar a la base de datos", e)
    print("Por favor, revisa los datos de la base de datos en el archivo database.json en la carpeta <<dev>> del programa o reinicie propio programa para volver a configurar la base de datos")
    #Borramos el archivo database.json
    os.remove(file_path) 
    #Creamos un nuevo archivo database.json con valores default
    if not os.path.exists(os.path.join(abspath(dirname(__file__)), "dev")):
        os.mkdir(os.path.join(abspath(dirname(__file__)), "dev"))
    if not os.path.exists(os.path.join(abspath(dirname(__file__)), "dev", "database.json")):
        with open(os.path.join(abspath(dirname(__file__)), "dev", "database.json"), "w") as file:
            data = {}
            data["host"] = "localhost"
            data["user"] = "default"
            data["password"] = "default"
            data["port"] = 3306
            json.dump(data, file)
    time.sleep(3)
    sys.exit()
while True:
    try:
        print("Bienvenido al programa de predicción de partidos de la liga mx")
        print("Este programa requiere de una conexión a internet estable")
        print("Este programa requiere de una computadora con ram sufienciente para ejecutar dos ventanas de chrome de forma simultanea")
        print("Toda la información de este programa es obtenida de las páginas de la liga mx y footystats, por lo que no me pertenece")
        print("Los primeros intentos podrían fallar, pero no te preocupes, conforme generes cookies, el programa se hará más estable")
        print ("*****************************************")
        print ("************Menú de opciones*************")
        print ("*1. Actualizar base de datos            *")
        print ("*2. Simulación de partidos              *")
        print ("*3. Comprobar efectividad de simulación *") 
        print ("*0. Salir                               *")
        print ("*****************************************")
        opcion = int(input("Ingrese un NUMERO de opción: "))
        if opcion == 1:
            print("******************************************************************************************")
            print('*  Realizar esta acción eliminará todos los datos de la base de datos llamada "LIGA_MX"  *')
            print("******************************************************************************************")
            while True:
                try:
                    inp = input("¿Estás seguro que deseas continuar? (S/N): ")
                    if inp == "S" or inp == "s" or inp == "si" or inp == "Si":
                        while True:
                            try:
                                año_strt = int(input("Ingrese año de inicio: "))
                                año_end = int(input("Ingrese año de fin: "))
                                break
                            except ValueError:
                                print("No ingresaste un número, intenta de nuevo")
                            except NameError:
                                print("No ingresaste un número, intenta de nuevo")
                        if año_strt == año_end:
                            año_strt = año_end - 1
                        print("******************************************************************************************")
                        print("*Por favor manten el cursor fuera de las ventanas de chrome hasta que el programa termine*")
                        print("******************************************************************************************")
                        time.sleep(3)
                        t1=threading.Thread(target=scrapper_estadistica, args=(año_strt,año_end))
                        t2=threading.Thread(target=scrapper_partidos, args=(año_strt,año_end))
                        t3=threading.Thread(target=scrapper_xG, args=(año_end,))
                        t1.start()
                        t2.start()
                        t3.start()
                        t1.join()
                        t2.join()
                        t3.join()
                        t1=threading.Thread(target=org_partidos, args=(año_strt,año_end,host_db,user_db,password_db,port_db))
                        t2=threading.Thread(target=org_tabla_est, args=(año_strt,año_end,host_db,user_db,password_db,port_db))
                        t3=threading.Thread(target=org_xG, args=(año_end,host_db,user_db,password_db,port_db))
                        t1.start()
                        t2.start()
                        t3.start()
                        t1.join()
                        t2.join()
                        t3.join()
                        print("Volviedo al menú principal...")
                        time.sleep(5)
                        break
                    elif inp == "N" or inp == "n" or inp == "no" or inp == "No":
                        print("Volviedo al menú principal...")
                        time.sleep(3)
                        break
                    else:
                        print("No ingresaste una opción válida, intenta de nuevo")
                except ValueError:
                    print("No ingresaste una opción válida, intenta de nuevo")
                except NameError:
                    print("No ingresaste una opción válida, intenta de nuevo")
        elif opcion == 2:
            Montecarlo(host_db,user_db,password_db,port_db)
            print("Volviedo al menú principal...")
            time.sleep(5)
        elif opcion == 3:
            while True:
                try:
                    print("¿Desea actualiza la base de datos sobre los partidos de comprobación?")
                    print("\n")
                    print('***********************************************************************************************************')
                    print('* Realizar esta acción eliminará todos los datos de la tabla "COMPROBACION" en la base de datos "LIGA_MX" *')
                    print('***********************************************************************************************************')
                    print("En caso de ser la primera vez, es necesario realizarlo para comprobar la efectividad del programa.")
                    sel=input("Actualizar partidos de comprobación? (Si/No): ")
                    if sel == "S" or sel == "s" or sel == "si" or sel == "Si":
                        print("Seleccione año de comprobación, ejem: 2020 para la temporada 2019-2020")
                        año_comp = int(input("Ingrese año de comprobación: "))
                        scrapper_partidos(año_comp-1,año_comp)
                        org_tabla_comp(año_comp-1,año_comp,host_db,user_db,password_db,port_db)
                        comparador(host_db,user_db,password_db,port_db)
                        break
                    elif sel == "N" or sel == "n" or sel == "no" or sel == "No":
                        comparador(host_db,user_db,password_db,port_db)
                        break
                    else:
                        print("Opción no válida, vuelva a intentarlo")
                except ValueError:
                    print("No ingresaste una opción valida, vuelva a intentarlo")
                except NameError:
                    print("No ingresaste una opción valida, vuelva a intentarlo")
        elif opcion == 0:
            print("Gracias por usar el programa")
            break
        else:
            print("Opción no válida, vuelva a intentarlo")
    except ValueError:
        print("No ingresaste un número vuelva a intentarlo")
    except NameError:
        print("No ingresaste un número vuelva a intentarlo")
    
