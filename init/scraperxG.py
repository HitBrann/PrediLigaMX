# ----- seccion de bibliotecas .
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
from os.path import dirname, abspath
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
def scrapper_xG(año_end:int)->None:
    #Obtenemos la fecha de hoy
    hoy = date.today()
    #Obtenemos el año actual
    año = hoy.year
    #Obtenemos el mes actual
    mes = hoy.month

    """
    Esta funcion permite obtener los datos xG de las tablas de la pagina de https://footystats.org/es/mexico/liga-mx/xg#
    y los guarda en un archivo csv.

    Parameters
    ----------
    año_end : int
        año final de la temporada a scrapear.
    
    Returns
    -------
    None

    Examples
    --------
    >>> scrapper_xG(2021)
    Obteniendo datos xG de la temporada 2020-2021
    Datos xG de la temporada 2020-2021 guardados en el archivo xG_2020-2021.csv
    """
    
    #Opciones de navegacion
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    # Configuración de ChromeDriver utilizando webdriver_manager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.set_window_position(0, 0)
    driver.maximize_window()
    time.sleep(2)
    #Ingresar a la pagina
    print("Abriendo navegador...")
    driver.get('https://footystats.org/es/mexico/liga-mx/xg')
    #Esperar 17 segundos
    time.sleep(17)
    print("Obteniendo datos xG de la última temporada...")
    #Eliminamos banners y popups
    try:
        element = driver.find_element('xpath', '//*[@id="header"]')
        driver.execute_script("""var element = arguments[0]; 
        element.parentNode.removeChild(element);""", element)
    except Exception:
        pass
    try:
        element = driver.find_element('xpath', '/html/body/div[19]')
        driver.execute_script("""var element = arguments[0];
        element.parentNode.removeChild(element);""", element)
    except Exception:
        pass
    #Seleccionamos el año que deseamos scrapear
    #buscamos todas las opciones del dropdown
    #Seleccionamos la opcion del año
    if año_end==año and mes<6:
        #Obtenemos los datos de la tabla xG local
        tabla_xG_L=driver.find_element(By.XPATH,'//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[2]')
        #Obtenemos solo el texto de la tabla
        tabla_xG_L=tabla_xG_L.text
        #Dividimos el texto en una lista
        tabla_xG_L=tabla_xG_L.split("\n")
        #Eliminamos los datos que no necesitamos
        tabla_xG_L=tabla_xG_L[2:]
        #Le damos a siguiente
        #Esperamos a que el boton de siguiente este disponible
        try:
            element = driver.find_element('xpath', '//*[@id="fECF_subscribe_text"]')
            driver.execute_script("""var element = arguments[0];
            element.parentNode.removeChild(element);""", element)
        except Exception:
            pass
        try:
            element = driver.find_element('xpath', '//*[@id="fECF"]')
            driver.execute_script("""var element = arguments[0];
            element.parentNode.removeChild(element);""", element)
        except Exception:
            pass
        #Esperamos 2 segundos
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/div/a[2]'))).click()
        #Esperamos 7 segundos
        time.sleep(7)
        #Obtenemos el nuevo texto de la tabla
        tabla_xG_L2=driver.find_element(By.XPATH,'//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[2]')
        #Obtenemos solo el texto de la tabla
        tabla_xG_L2=tabla_xG_L2.text
        #Dividimos el texto en una lista
        tabla_xG_L2=tabla_xG_L2.split("\n")
        #Eliminamos los datos que no necesitamos
        tabla_xG_L2=tabla_xG_L2[2:]
        #Union de las dos tablas
        tabla_xG_L=tabla_xG_L+tabla_xG_L2
        #Obtenemos los datos de la tabla xG visitante
        tabla_xG_V=driver.find_element(By.XPATH,'//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[3]')
        #Obtenemos solo el texto de la tabla
        tabla_xG_V=tabla_xG_V.text
        #Dividimos el texto en una lista
        tabla_xG_V=tabla_xG_V.split("\n")
        #Eliminamos los datos que no necesitamos
        tabla_xG_V=tabla_xG_V[2:]
        #Le damos a siguiente
        #Esperamos dos segundos
        time.sleep(2)
        #Esperamos a que el boton de siguiente este disponible
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[3]/ul/li[1]/div/a[2]'))).click()
        #Esperamos 7 segundos
        time.sleep(7)
        #Obtenemos el nuevo texto de la tabla
        tabla_xG_V2=driver.find_element(By.XPATH,'//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[3]')
        #Obtenemos solo el texto de la tabla
        tabla_xG_V2=tabla_xG_V2.text
        #Dividimos el texto en una lista
        tabla_xG_V2=tabla_xG_V2.split("\n")
        #Eliminamos los datos que no necesitamos
        tabla_xG_V2=tabla_xG_V2[2:]
        #Union de las dos tablas
        tabla_xG_V=tabla_xG_V+tabla_xG_V2
    else:
        #Ponemos el cursor sobre el dropdown
        a = ActionChains(driver)
        m = driver.find_element(By.CSS_SELECTOR, "div.drop-down-parent.fl.boldFont")
        a.move_to_element(m).perform()
        #Esperamos 2 segundos
        time.sleep(2)
        #Seleccionamos la opcion del año
        n=driver.find_element(By.LINK_TEXT, str(año_end-1)+"/"+str(año_end-2000))
        a.move_to_element(n).click().perform()
        a.release()
        a.reset_actions()
        #Esperamos 2 segundos
        time.sleep(7)
        #Obtenemos los datos de la tabla xG local
        tabla_xG_L=driver.find_element(By.XPATH,'//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[2]')
        #Obtenemos solo el texto de la tabla
        tabla_xG_L=tabla_xG_L.text
        #Dividimos el texto en una lista
        tabla_xG_L=tabla_xG_L.split("\n")
        #Eliminamos los datos que no necesitamos
        tabla_xG_L=tabla_xG_L[2:]
        #Le damos a siguiente
        #Esperamos a que el boton de siguiente este disponible
        try:
            element = driver.find_element('xpath', '//*[@id="fECF_subscribe_text"]')
            driver.execute_script("""var element = arguments[0];
            element.parentNode.removeChild(element);""", element)
        except Exception:
            pass
        try:
            element = driver.find_element('xpath', '//*[@id="fECF"]')
            driver.execute_script("""var element = arguments[0];
            element.parentNode.removeChild(element);""", element)
        except Exception:
            pass
        #Esperamos 2 segundos
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/div/a[2]'))).click()
        #Esperamos 7 segundos
        time.sleep(7)
        #Obtenemos el nuevo texto de la tabla
        tabla_xG_L2=driver.find_element(By.XPATH,'//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[2]')
        #Obtenemos solo el texto de la tabla
        tabla_xG_L2=tabla_xG_L2.text
        #Dividimos el texto en una lista
        tabla_xG_L2=tabla_xG_L2.split("\n")
        #Eliminamos los datos que no necesitamos
        tabla_xG_L2=tabla_xG_L2[2:]
        #Union de las dos tablas
        tabla_xG_L=tabla_xG_L+tabla_xG_L2
        #Obtenemos los datos de la tabla xG visitante
        tabla_xG_V=driver.find_element(By.XPATH,'//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[3]')
        #Obtenemos solo el texto de la tabla
        tabla_xG_V=tabla_xG_V.text
        #Dividimos el texto en una lista
        tabla_xG_V=tabla_xG_V.split("\n")
        #Eliminamos los datos que no necesitamos
        tabla_xG_V=tabla_xG_V[2:]
        #Le damos a siguiente
        #Esperamos dos segundos
        time.sleep(2)
        #Esperamos a que el boton de siguiente este disponible
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[3]/ul/li[1]/div/a[2]'))).click()
        #Esperamos 7 segundos
        time.sleep(7)
        #Obtenemos el nuevo texto de la tabla
        tabla_xG_V2=driver.find_element(By.XPATH,'//*[@id="leagueContent"]/div[3]/div[1]/div[3]/div/div[1]/div[3]')
        #Obtenemos solo el texto de la tabla
        tabla_xG_V2=tabla_xG_V2.text
        #Dividimos el texto en una lista
        tabla_xG_V2=tabla_xG_V2.split("\n")
        #Eliminamos los datos que no necesitamos
        tabla_xG_V2=tabla_xG_V2[2:]
        #Union de las dos tablas
        tabla_xG_V=tabla_xG_V+tabla_xG_V2
    #Cerramos el navegador
    driver.quit()
    #Divivimos cada tabla en una lista que serán las columnas del dataframe
    tabla_xG_L_equipos=[]
    tabla_xG_L_xG=[]
    for i in range(len(tabla_xG_L)):
        if i%2==0:
            tabla_xG_L_equipos.append(tabla_xG_L[i])
        else:
            tabla_xG_L_xG.append(tabla_xG_L[i])
    tabla_xG_V_equipos=[]
    tabla_xG_V_xG=[]
    for i in range(len(tabla_xG_V)):
        if i%2==0:
            tabla_xG_V_equipos.append(tabla_xG_V[i])
        else:
            tabla_xG_V_xG.append(tabla_xG_V[i])
    #Creamos el dataframe de cada tabla
    df_xG_L=pd.DataFrame(list(zip(tabla_xG_L_equipos,tabla_xG_L_xG)),columns=["Equipo","xG_L"])
    df_xG_V=pd.DataFrame(list(zip(tabla_xG_V_equipos,tabla_xG_V_xG)),columns=["Equipo","xG_V"])
    #Unimos los dataframes por el nombre del equipo
    df_xG=pd.merge(df_xG_L,df_xG_V,on="Equipo")
    #Eliminamos las unidades de los datos
    df_xG["xG_L"]=df_xG["xG_L"].str.replace("xG","")
    df_xG["xG_V"]=df_xG["xG_V"].str.replace("xG","")
    #Convertimos los datos a float
    df_xG["xG_L"]=df_xG["xG_L"].astype(float)
    df_xG["xG_V"]=df_xG["xG_V"].astype(float)
    #Reemplazamos los nombres de los equipos para que coincidan con los de la base de datos
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Club America","América")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("CSyD Atlas de Guadalajara","Atlas")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Atletico San Luis","Club Atlético de San Luis")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Cruz Azul FC","Cruz Azul")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("FC Juarez","FC Juárez")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("CD Guadalajara","Guadalajara")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Club Leon","León")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Mazatlan FC","Mazatlán FC")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("CF Monterrey","Monterrey")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Club Necaxa","Necaxa")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("CF Pachuca","Pachuca")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Puebla FC","Puebla")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Club Universidad Nacional","Pumas")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Queretaro FC","Querétaro")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Club Santos Laguna","Santos Laguna")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Tigres UANL","Tigres")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Toluca FC","Toluca")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Club Tijuana Xoloitzcuintles de Caliente","Tijuana")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Deportivo Toluca FC","Toluca")
    df_xG["Equipo"]=df_xG["Equipo"].str.replace("Deportivo Toluca","Toluca")
    #Agregamos la temporada
    df_xG["temporada"]=str(año_end-1)+"-"+str(año_end)
    #Carpeta donde se guardaran los archivos
    carpeta = "out-docs"
    #Ruta de la carpeta
    ruta_carpeta = os.path.join(abspath(dirname(__file__)), carpeta)
    #Creación de la carpeta si no existe
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    #Nombre del archivo
    nombre_archivo="xG"+str(año_end-1)+"-"+str(año_end)+".csv"
    #Ruta del archivo
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
    df_xG.to_csv(ruta_archivo, index=False)
    print("Datos xG de la temporada "+str(año_end-1)+"-"+str(año_end)+" guardados en el archivo "+nombre_archivo)
