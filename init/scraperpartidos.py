# ----- seccion de bibliotecas .
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import os
from os.path import dirname, abspath
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
def scrapper_partidos(año_strt:int,año_end:int) -> None:
    """
    Esta función obtiene los datos de los partidos de la Liga MX de la página web https://ligamx.net/cancha/partidos

    Parameters
    ----------
    año_strt : str
    Año de inicio de la temporada de la cual se obtendran los datos.
    año_end : str
    Año de fin de la temporada de la cual se obtendran los datos.

    Returns
    -------
    None.

    Examples
    --------
    >>> scrapper_partidos(2010,2011)
    [Iniciando obtención de datos de los partidos de la Liga MX...]

    Obteniendo 2010-2011...
    Obteniendo Clausura...
    Obteniendo Apertura...
    .
    .
    .
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
    driver.get('https://ligamx.net/cancha/partidos')
    #Esperar 8 segundos
    time.sleep(8)
    #Cerrar ventana cambiante que puede causar problemas usando comandos de javascript
    driver.execute_script("""
    var l = document.getElementsByClassName("box-matches")[0];
   l.parentNode.removeChild(l);
""")
    #Borral cabezera de la pagina
    driver.execute_script("""
   var l = document.getElementsByClassName("team-logos")[0];
   l.parentNode.removeChild(l);
""")
    #Borrar el logo de la pagina
    driver.execute_script("""
   var l = document.getElementsByClassName("logo-header")[0];
   l.parentNode.removeChild(l);
""")
    #Borrar el footer de la pagina 1
    driver.execute_script("""
    var l = document.getElementsByClassName("logosFooter")[0];
    l.parentNode.removeChild(l);
""")
    #Borrar el footer de la pagina 2
    driver.execute_script("""
    var l = document.getElementsByClassName("col-sm-4 col-xs-12 menu-footer")[0];
    l.parentNode.removeChild(l);
""")
    #Borrar el footer de la pagina 3
    driver.execute_script("""
    var l = document.getElementsByClassName("col-sm-8 col-xs-12 footer-logos")[0];
    l.parentNode.removeChild(l);
""")
    #Borrar el footer de la pagina 4
    driver.execute_script("""
    var l = document.getElementsByClassName("col-sm-12 col-xs-12 copyright")[0];
    l.parentNode.removeChild(l);
""")             
    """Normalmente no es necesario tanta limpieza de la pagina, pero en este caso se busca que sea replicable el mayor numero de veces posible"""
    #Ejecución de la busqueda de los datos
    #Creación de listas para almacenar los datos
    temporada_A_or_C=[]
    overall_fecha=[]
    overall_equipos_local=[]
    overall_equipos_visitante=[]
    overall_goles_local=[]
    overall_goles_visitante=[]
    overall_estadio=[]
    overall_jornada=[]
    overall_ID_partido=[]
    #Automatización de la selección de año en el menú de búsqueda
    print("[Iniciando obtención de datos de los partidos de la Liga MX...]")
    for j in range(año_strt,año_end):
        #Obtener los elementos de la pagina
        dropdownbox = driver.find_elements(by=By.TAG_NAME, value='option')
        for i in range(len(dropdownbox)):
            if dropdownbox[i].text == str(j)+'-'+str(j+1):
                dropdownbox[i].click()
                print("Obteniendo "+str(dropdownbox[i].text)+"...")
                time.sleep(2)
                break
        #Nueva busqueda para la selección de los partidos de Clausura
        dropdownbox = driver.find_elements(by=By.TAG_NAME, value='option')    
        #Automatización de la selección de los partidos de Clausura en el menú de busqueda
        for l in range(len(dropdownbox)):
            if dropdownbox[l].text == 'Clausura':
                dropdownbox[l].click()
                print('Obteniendo '+str(dropdownbox[l].text)+'...')
                time.sleep(2)
                #Apretar boton buscar
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#btnBuscarMarcador.btn-verde.btn-verde-compacto.pointer'))).click() 
                time.sleep(8)
                #Obtención de la información de clausura
                partidos = driver.find_element('xpath', '//*[@id="bodyPartido"]')
                partidos = partidos.text
                #Partimos los datos en una lista
                partidos_lista = partidos.split('\n')
                #Dividimos la lista en sublistas para su mejor manejo
                fecha=[partidos_lista[i] for i in range(0,len(partidos_lista),7)]
                #Formateamos la fecha para su mejor manejo
                fecha_format=[]
                diccionario_meses={'Enero':'01','Febrero':'02','Marzo':'03','Abril':'04','Mayo':'05','Junio':'06','Julio':'07','Agosto':'08','Septiembre':'09','Octubre':'10','Noviembre':'11','Diciembre':'12'}
                for i in fecha:
                    strc=re.subn('^[A-Záéíóúa-z]+\s','',i)
                    fecha_format.append(strc[0])
                for i in range(len(fecha_format)):
                    for key in diccionario_meses:
                        if key in fecha_format[i]:
                            fecha_format[i]=fecha_format[i].replace(key,diccionario_meses[key])
                            fecha_format[i]=fecha_format[i].replace(' de ','/')
                temporada=[partidos_lista[i] for i in range(1,len(partidos_lista),7)]
                #Uniremos la lista de temporada con si es de clausura o apertura para su mejor manejo
                for i in temporada:
                    strc=str(i.replace('Temporada ',''))+'_1_C'
                    temporada_A_or_C.append(strc)
                #Seguimos definiendo sublistas para su mejor manejo
                jornada=[partidos_lista[i] for i in range(3,len(partidos_lista),7)]
                #Dividimos los goles en local y visitante
                goles_local=[partidos_lista[i].split(' - ')[0] for i in range(5,len(partidos_lista),7)]
                goles_visitante=[partidos_lista[i].split(' - ')[1] for i in range(5,len(partidos_lista),7)]
                estadio=[partidos_lista[i] for i in range(6,len(partidos_lista),7)]
                #Obtención de los equipos mediante las etiquetas de las imagenes
                images=driver.find_elements(By.XPATH,"//img")
                images_alts=[image.get_attribute('alt') for image in images]
                #Filtrado de las imagenes para obtener los equipos
                filtered_list=(images_alts[4:])
                filtered_list= filtered_list[:len(filtered_list)-2]
                #Dividimos los equipos en local y visitante
                equipos_local=[filtered_list[i] for i in range(0,len(filtered_list),2)]
                equipos_visitante=[filtered_list[i] for i in range(1,len(filtered_list),2)]
                #Guardamos los datos de cada iteración en las listas globales
                for i in fecha_format:
                    overall_fecha.append(i)
                for i in jornada:
                    overall_jornada.append(i)
                for i in goles_local:
                    overall_goles_local.append(i)
                for i in goles_visitante:
                    overall_goles_visitante.append(i)
                for i in estadio:
                    overall_estadio.append(i)
                for i in equipos_local:
                    overall_equipos_local.append(i)
                for i in equipos_visitante:
                    overall_equipos_visitante.append(i)
                break
        #Nueva busqueda para la selección de los partidos de Apertura
        dropdownbox = driver.find_elements(by=By.TAG_NAME, value='option')
        #Automatización de la selección d e los partidos de Apertura en el menú de busqueda
        for l in range(len(dropdownbox)):
            if dropdownbox[l].text == 'Apertura':
                dropdownbox[l].click()
                print('Obteniendo '+str(dropdownbox[l].text)+'...')
                time.sleep(2)
                #Apretar boton buscar
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#btnBuscarMarcador.btn-verde.btn-verde-compacto.pointer'))).click() 
                time.sleep(8)
                #Obtención de la información de apertura
                partidos = driver.find_element('xpath', '//*[@id="bodyPartido"]')
                partidos = partidos.text
                #Partimos los datos en una lista
                partidos_lista = partidos.split('\n')
                #Dividimos la lista en sublistas para su mejor manejo
                fecha=[partidos_lista[i] for i in range(0,len(partidos_lista),7)]
                #Formateamos la fecha para su mejor manejo
                fecha_format=[]
                diccionario_meses={'Enero':'01','Febrero':'02','Marzo':'03','Abril':'04','Mayo':'05','Junio':'06','Julio':'07','Agosto':'08','Septiembre':'09','Octubre':'10','Noviembre':'11','Diciembre':'12'}
                for i in fecha:
                    strc=re.subn('^[A-Záéíóúa-z]+\s','',i)
                    fecha_format.append(strc[0])
                for i in range(len(fecha_format)):
                    for key in diccionario_meses:
                        if key in fecha_format[i]:
                            fecha_format[i]=fecha_format[i].replace(key,diccionario_meses[key])
                            fecha_format[i]=fecha_format[i].replace(' de ','/')
                temporada=[partidos_lista[i] for i in range(1,len(partidos_lista),7)]
                #Uniremos la lista de temporada con si es de apertura o clausura para su mejor manejo
                for i in temporada:
                    strc=str(i.replace('Temporada ',''))+'_2_A'
                    temporada_A_or_C.append(strc)
                #Seguimos definiendo sublistas para su mejor manejo
                jornada=[partidos_lista[i] for i in range(3,len(partidos_lista),7)]
                #Dividimos los goles en local y visitante
                goles_local=[partidos_lista[i].split(' - ')[0] for i in range(5,len(partidos_lista),7)]
                goles_visitante=[partidos_lista[i].split(' - ')[1] for i in range(5,len(partidos_lista),7)]
                estadio=[partidos_lista[i] for i in range(6,len(partidos_lista),7)]
                #Obtención de los equipos mediante las etiquetas de las imagenes
                images=driver.find_elements(By.XPATH,"//img")
                images_alts=[image.get_attribute('alt') for image in images]
                #Filtrado de las imagenes para obtener los equipos
                filtered_list=(images_alts[4:])
                filtered_list= filtered_list[:len(filtered_list)-2]
                #Dividimos los equipos en local y visitante
                equipos_local=[filtered_list[i] for i in range(0,len(filtered_list),2)]
                equipos_visitante=[filtered_list[i] for i in range(1,len(filtered_list),2)]
                #Guardamos los datos de cada iteración en las listas globales
                for i in fecha_format:
                    overall_fecha.append(i)
                for i in jornada:
                    overall_jornada.append(i)
                for i in goles_local:
                    overall_goles_local.append(i)
                for i in goles_visitante:
                    overall_goles_visitante.append(i)
                for i in estadio:
                    overall_estadio.append(i)
                for i in equipos_local:
                    overall_equipos_local.append(i)
                for i in equipos_visitante:
                    overall_equipos_visitante.append(i)
                break
    #Asignación de ID a cada partido
    for i in range(len(overall_fecha)):
        overall_ID_partido.append(str(i+1))
    #Cerrar el navegador
    driver.quit()
    #Creamos un dataframe con los datos obtenidos
    df=pd.DataFrame({'id-partido':overall_ID_partido,'temporada':temporada_A_or_C,'fecha':overall_fecha,'jornada':overall_jornada,'equipo-local':overall_equipos_local,'equipo-visitante':overall_equipos_visitante,'goles-local':overall_goles_local,'goles-visitante':overall_goles_visitante,'estadio':overall_estadio})
    #Eliminamos las filas que en el campo de goles_local o goles_visitante tienen un valor vacio el cual es representado por un guion
    df=df[df['goles-local']!='-']
    df=df[df['goles-visitante']!='-']
    #Renombramos en equipo local y visitante por el nombre del equipo los equipos que cambiaron de nombre
    df['equipo-local']=df['equipo-local'].replace('Puebla F.C.','Puebla')
    df['equipo-local']=df['equipo-local'].replace('Gallos Blancos de Querétaro','Querétaro')
    df['equipo-local']=df['equipo-local'].replace('Lobos BUAP','Lobos')
    df['equipo-local']=df['equipo-local'].replace('Tigres de la U.A.N.L.','Tigres')
    df['equipo-local']=df['equipo-local'].replace('Universidad Nacional','Pumas')
    df['equipo-visitante']=df['equipo-visitante'].replace('Puebla F.C.','Puebla')
    df['equipo-visitante']=df['equipo-visitante'].replace('Gallos Blancos de Querétaro','Querétaro')
    df['equipo-visitante']=df['equipo-visitante'].replace('Lobos BUAP','Lobos')
    df['equipo-visitante']=df['equipo-visitante'].replace('Tigres de la U.A.N.L.','Tigres')
    df['equipo-visitante']=df['equipo-visitante'].replace('Universidad Nacional','Pumas')
    #Exportamos el dataframe a un archivo csv en la carpeta del programa usando el modulo os
    #Carpeta donde se guardaran los archivos
    carpeta = "out-docs"
    #Ruta de la carpeta
    ruta_carpeta = os.path.join(abspath(dirname(__file__)), carpeta)
    #Creación de la carpeta si no existe
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    nombre_archivo = "Partidos"+str(año_strt)+"-"+str(año_end)+".csv"
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
    df.to_csv(ruta_archivo, index=False)
    print("El archivo de datos de los partidos se ha guardado con exito.")
    print("Terminó el proceso de obtención de datos de los partidos de la Liga MX.")
    time.sleep(1)

