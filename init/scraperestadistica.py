#librerias
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import os
from os.path import abspath, dirname
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
def scrapper_estadistica(año_strt:str,año_end: str)->None:
    """
    Esta función obtiene la tabla general, tabla ofensiva y tabla defensiva de la página de estadísticas de la Liga MX
    y las guarda en archivos csv
    
    Parameters
    ----------
    año_strt : str
        Año de inicio de la temporada
    año_end : str
        Año de fin de la temporada
    
    Returns
    -------
    None
    
    Examples
    --------
    >>> scrapper_estadistica('2010','2011')
    Abriendo navegador...
    Obteniendo 2010-2011...
    Obteniendo Clausura...
    Obteniendo Apertura...
    .
    .
    .
    Descargando Tabla General 2010-2011...
    Tabla General 2010-2011 guardada
    Descargando Tabla Ofensiva 2010-2011...
    Tabla Ofensiva 2010-2011 guardada
    Descargando Tabla Defensiva 2010-2011...
    Tabla Defensiva 2010-2011 guardada
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
    driver.get('https://ligamx.net/cancha/estadisticahistorica')
    #Esperar 8 segundos
    time.sleep(8)
    #Almacenamos los datos en listas separadas para cada columna de la tabla
    # Creamos una lista vacia para cada columna
    equipo = []
    JJ = []
    JG = []
    JE = []
    JP = []
    GF = []
    GC = []
    DIF = []
    PTS = []
    JJ_L = []
    JG_L = []
    JE_L = []
    JP_L = []
    GF_L = []
    GC_L = []
    DIF_L = []
    PTS_L = []
    JJ_V = []
    JG_V = []
    JE_V = []
    JP_V = []
    GF_V = []
    GC_V = []
    DIF_V = []
    PTS_V = []
    Temporada = []
    posicion = []
    posicion_of = []
    posicion_def = []
    tabla_of_def_lista_equipo_of = []
    tabla_of_def_lista_equipo_def = []
    tabla_of_def_lista_num_of = []
    tabla_of_def_lista_num_def = []
    print('[Obteniendo Tabla General, Tabla Ofensiva y Tabla Defensiva...]')
    #seleccionamos los años que queremos
    for i in range(año_strt,año_end):
        #Configurar los dropdowns
        #buscamos todas las opciones del dropdown
        dropdownbox = driver.find_elements(by=By.TAG_NAME, value='option')
        for j in range (len(dropdownbox)):
            if dropdownbox[j].text == str(i)+'-'+str(i+1):
                dropdownbox[j].click()
                print("Obteniendo "+str(dropdownbox[j].text)+"...")
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
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#btnBuscar.btn-verde.loadershow'))).click() 
                time.sleep(8)
                #Obtener tabla general de clausura
                tabla_gen = driver.find_element('xpath', '/html/body/section[5]/div/div[2]/div[1]/div/table')
                tabla_gen = tabla_gen.text
                #Partimos los datos en una lista por los saltos de linea
                tabla_gen_lista = re.split('\n',tabla_gen)
                #Eliminamos los datos que no nos interesan
                tabla_gen_lista=tabla_gen_lista[2:]
                #Eliminamos el numero del equipo en cada elemento par de la lista usando una expresion regular
                for k in range(0,len(tabla_gen_lista),2):
                    tabla_gen_lista[k]=re.sub('^\d+\s','',tabla_gen_lista[k])
                #Dividimos cada lista impar por los espacios en blanco
                for m in range(1,len(tabla_gen_lista),2):
                    tabla_gen_lista[m]=re.split('\s',tabla_gen_lista[m])
                #Para los equipos agregamos cada elemento impar de la lista original
                for n in range(0,len(tabla_gen_lista),2):
                    equipo.append(tabla_gen_lista[n])
                #Para las demas columnas agregamos cada elemento par de la lista original
                for o in range(1,len(tabla_gen_lista),2):
                    JJ.append(tabla_gen_lista[o][0])
                    JG.append(tabla_gen_lista[o][1])
                    JE.append(tabla_gen_lista[o][2])
                    JP.append(tabla_gen_lista[o][3])
                    GF.append(tabla_gen_lista[o][4])
                    GC.append(tabla_gen_lista[o][5])
                    DIF.append(tabla_gen_lista[o][6])
                    PTS.append(tabla_gen_lista[o][7])
                    JJ_L.append(tabla_gen_lista[o][8])
                    JG_L.append(tabla_gen_lista[o][9])
                    JE_L.append(tabla_gen_lista[o][10])
                    JP_L.append(tabla_gen_lista[o][11])
                    GF_L.append(tabla_gen_lista[o][12])
                    GC_L.append(tabla_gen_lista[o][13])
                    DIF_L.append(tabla_gen_lista[o][14])
                    PTS_L.append(tabla_gen_lista[o][15])
                    JJ_V.append(tabla_gen_lista[o][16])
                    JG_V.append(tabla_gen_lista[o][17])
                    JE_V.append(tabla_gen_lista[o][18])
                    JP_V.append(tabla_gen_lista[o][19])
                    GF_V.append(tabla_gen_lista[o][20])
                    GC_V.append(tabla_gen_lista[o][21])
                    DIF_V.append(tabla_gen_lista[o][22])
                    PTS_V.append(tabla_gen_lista[o][23])
                    Temporada.append(str(i)+'-'+str(i+1)+'_C')
                    posicion.append((o+1)/2)
                #Ahora buscamos las tablas de ofensiva y defensiva
                tabla_of_def = driver.find_element('xpath', '/html/body/section[7]/div/section')
                tabla_of_def = tabla_of_def.text
                #Partimos los datos en una lista por los saltos de linea
                tabla_of_def_lista = re.split('\n',tabla_of_def)
                #Eliminamos los elementos que comienzan en '#'
                tabla_of_def_lista = [x for x in tabla_of_def_lista if not x.startswith('#')]
                #Eliminamos los números al inicio de cada elemento de la lista
                for p in range(len(tabla_of_def_lista)):
                    tabla_of_def_lista[p]=re.sub('^\d+\s','',tabla_of_def_lista[p])
                #Dividimos cada lista en 2, una para los numeros y otra para los equipos
                tabla_of_def_lista_num = []
                tabla_of_def_lista_equipo = []
                #Para los numeros usaremos regex para eliminar cualquier caracter que no sea un numero
                for q in range(0,len(tabla_of_def_lista)):
                    tabla_of_def_lista_num.append(re.sub('[^0-9]','',tabla_of_def_lista[q]))
                #Para los equipos eliminamos los numeros al final de cada elemento
                for r in range(0,len(tabla_of_def_lista)):
                    tabla_of_def_lista_equipo.append(re.sub('\s\d+$','',tabla_of_def_lista[r]))
                #Dividimos cada lista en mitad de elementos, una para ofensiva y otra para defensiva
                for s in range(0,len(tabla_of_def_lista_num)//2):
                    tabla_of_def_lista_num_of.append(tabla_of_def_lista_num[s])
                for t in range(len(tabla_of_def_lista_num)//2,len(tabla_of_def_lista_num)):
                    tabla_of_def_lista_num_def.append(tabla_of_def_lista_num[t])
                #Hacemos lo mismo para los equipos
                for u in range(0,len(tabla_of_def_lista_equipo)//2):
                    tabla_of_def_lista_equipo_of.append(tabla_of_def_lista_equipo[u])
                for v in range(len(tabla_of_def_lista_equipo)//2,len(tabla_of_def_lista_equipo)):
                    tabla_of_def_lista_equipo_def.append(tabla_of_def_lista_equipo[v])
                dropdownbox = driver.find_elements(by=By.TAG_NAME, value='option')
                #Agregamos indicador de posicion para la tabla de ofensiva
                for w in range(0,len(tabla_of_def_lista_num)//2):
                    posicion_of.append((w+1))
                #Agregamos indicador de posicion para la tabla de defensiva
                for x in range(0,len(tabla_of_def_lista_num)//2):
                    posicion_def.append((x+1))
                #Repetimos el proceso para los partidos de Apertura
        for l in range(len(dropdownbox)):
            if dropdownbox[l].text == 'Apertura':
                dropdownbox[l].click()
                print('Obteniendo '+str(dropdownbox[l].text)+'...')
                time.sleep(2)
                #Apretar boton buscar
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#btnBuscar.btn-verde.loadershow'))).click() 
                time.sleep(8)
                #Obtener tabla general de Apertura
                tabla_gen = driver.find_element('xpath', '/html/body/section[5]/div/div[2]/div[1]/div/table')
                tabla_gen = tabla_gen.text
                #Partimos los datos en una lista por los saltos de linea
                tabla_gen_lista = re.split('\n',tabla_gen)
                #Eliminamos los datos que no nos interesan
                tabla_gen_lista=tabla_gen_lista[2:]
                #Eliminamos el numero del equipo en cada elemento par de la lista usando una expresion regular
                for k in range(0,len(tabla_gen_lista),2):
                    tabla_gen_lista[k]=re.sub('^\d+\s','',tabla_gen_lista[k])
                #Dividimos cada lista impar por los espacios en blanco
                for m in range(1,len(tabla_gen_lista),2):
                    tabla_gen_lista[m]=re.split('\s',tabla_gen_lista[m])
                #Para los equipos agregamos cada elemento impar de la lista original
                for n in range(0,len(tabla_gen_lista),2):
                    equipo.append(tabla_gen_lista[n])
                #Para las demas columnas agregamos cada elemento par de la lista original
                for o in range(1,len(tabla_gen_lista),2):
                    JJ.append(tabla_gen_lista[o][0])
                    JG.append(tabla_gen_lista[o][1])
                    JE.append(tabla_gen_lista[o][2])
                    JP.append(tabla_gen_lista[o][3])
                    GF.append(tabla_gen_lista[o][4])
                    GC.append(tabla_gen_lista[o][5])
                    DIF.append(tabla_gen_lista[o][6])
                    PTS.append(tabla_gen_lista[o][7])
                    JJ_L.append(tabla_gen_lista[o][8])
                    JG_L.append(tabla_gen_lista[o][9])
                    JE_L.append(tabla_gen_lista[o][10])
                    JP_L.append(tabla_gen_lista[o][11])
                    GF_L.append(tabla_gen_lista[o][12])
                    GC_L.append(tabla_gen_lista[o][13])
                    DIF_L.append(tabla_gen_lista[o][14])
                    PTS_L.append(tabla_gen_lista[o][15])
                    JJ_V.append(tabla_gen_lista[o][16])
                    JG_V.append(tabla_gen_lista[o][17])
                    JE_V.append(tabla_gen_lista[o][18])
                    JP_V.append(tabla_gen_lista[o][19])
                    GF_V.append(tabla_gen_lista[o][20])
                    GC_V.append(tabla_gen_lista[o][21])
                    DIF_V.append(tabla_gen_lista[o][22])
                    PTS_V.append(tabla_gen_lista[o][23])
                    Temporada.append(str(i)+'-'+str(i+1)+'_A')
                    posicion.append((o+1)/2)
                #Ahora buscamos las tablas de ofensiva y defensiva
                tabla_of_def = driver.find_element('xpath', '/html/body/section[7]/div/section')
                tabla_of_def = tabla_of_def.text
                #Partimos los datos en una lista por los saltos de linea
                tabla_of_def_lista = re.split('\n',tabla_of_def)
                #Eliminamos los elementos que comienzan en '#'
                tabla_of_def_lista = [x for x in tabla_of_def_lista if not x.startswith('#')]
                #Eliminamos los números al inicio de cada elemento de la lista
                for p in range(len(tabla_of_def_lista)):
                    tabla_of_def_lista[p]=re.sub('^\d+\s','',tabla_of_def_lista[p])
                #Dividimos cada lista en 2, una para los numeros y otra para los equipos
                tabla_of_def_lista_num = []
                tabla_of_def_lista_equipo = []
                #Para los numeros usaremos regex para eliminar cualquier caracter que no sea un numero
                for q in range(0,len(tabla_of_def_lista)):
                    tabla_of_def_lista_num.append(re.sub('[^0-9]','',tabla_of_def_lista[q]))
                #Para los equipos eliminamos los numeros al final de cada elemento
                for r in range(0,len(tabla_of_def_lista)):
                    tabla_of_def_lista_equipo.append(re.sub('\s\d+$','',tabla_of_def_lista[r]))
                #Dividimos cada lista en mitad de elementos, una para ofensiva y otra para defensiva
                for s in range(0,len(tabla_of_def_lista_num)//2):
                    tabla_of_def_lista_num_of.append(tabla_of_def_lista_num[s])
                for t in range(len(tabla_of_def_lista_num)//2,len(tabla_of_def_lista_num)):
                    tabla_of_def_lista_num_def.append(tabla_of_def_lista_num[t])
                #Hacemos lo mismo para los equipos
                for u in range(0,len(tabla_of_def_lista_equipo)//2):
                    tabla_of_def_lista_equipo_of.append(tabla_of_def_lista_equipo[u])
                for v in range(len(tabla_of_def_lista_equipo)//2,len(tabla_of_def_lista_equipo)):
                    tabla_of_def_lista_equipo_def.append(tabla_of_def_lista_equipo[v])
                dropdownbox = driver.find_elements(by=By.TAG_NAME, value='option')
                #Agregamos indicador de posicion para la tabla de ofensiva
                for w in range(0,len(tabla_of_def_lista_num)//2):
                    posicion_of.append((w+1))
                #Agregamos indicador de posicion para la tabla de defensiva
                for x in range(0,len(tabla_of_def_lista_num)//2):
                    posicion_def.append((x+1))
    #Creamos un dataframe para la tabla general con los datos obtenidos y lo guardamos en un archivo csv
    df=pd.DataFrame({'POS':posicion,'equipo':equipo,'JJ':JJ,'JG':JG,'JE':JE,'JP':JP,'GF':GF,'GC':GC,'DIF':DIF,'PTS':PTS,'JJ_L':JJ_L,'JG_L':JG_L,'JE_L':JE_L,'JP_L':JP_L,'GF_L':GF_L,'GC_L':GC_L,'DIF_L':DIF_L,'PTS_L':PTS_L,'JJ_V':JJ_V,'JG_V':JG_V,'JE_V':JE_V,'JP_V':JP_V,'GF_V':GF_V,'GC_V':GC_V,'DIF_V':DIF_V,'PTS_V':PTS_V,'temporada':Temporada}) 
    #Reemplazamos los nombres de los equipos para que coincidan con los de la tabla de partidos
    df['equipo'] = df['equipo'].replace('Puebla F.C.','Puebla')
    df['equipo'] = df['equipo'].replace('Gallos Blancos de Querétaro','Querétaro')
    df['equipo'] = df['equipo'].replace('Lobos BUAP','Lobos')
    df['equipo'] = df['equipo'].replace('Tigres de la U.A.N.L.','Tigres')
    #Carpeta donde se guardaran los archivos
    carpeta = "out-docs"
    #Ruta de la carpeta
    ruta_carpeta = os.path.join(abspath(dirname(__file__)), carpeta)
    #Creación de la carpeta si no existe
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    nombre_archivo = "Tabla_General"+str(año_strt)+"-"+str(año_end)+".csv"
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
    #Guardamos el archivo
    df.to_csv(ruta_archivo,index=False)
    print('Tabla General '+str(año_strt)+'-'+str(año_end)+' guardada')
    #Creamos un dataframe para la tabla de ofensiva con los datos obtenidos y lo guardamos en un archivo csv
    df=pd.DataFrame({'POS':posicion_of,'equipo':tabla_of_def_lista_equipo_of,'goles':tabla_of_def_lista_num_of,'temporada':Temporada})
    #Reemplazamos los nombres de los equipos para que coincidan con los de la tabla de partidos
    df['equipo'] = df['equipo'].replace('Puebla F.C.','Puebla')
    df['equipo'] = df['equipo'].replace('Gallos Blancos de Querétaro','Querétaro')
    df['equipo'] = df['equipo'].replace('Lobos BUAP','Lobos')
    df['equipo'] = df['equipo'].replace('Tigres de la U.A.N.L.','Tigres')
    #Carpeta donde se guardaran los archivos
    carpeta = "out-docs"
    #Ruta de la carpeta
    ruta_carpeta = os.path.join(abspath(dirname(__file__)), carpeta)
    #Creación de la carpeta si no existe
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    nombre_archivo = "Tabla_Ofensiva"+str(año_strt)+"-"+str(año_end)+".csv"
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
    #Guardamos el archivo
    df.to_csv(ruta_archivo,index=False)
    print('Tabla Ofensiva '+str(año_strt)+'-'+str(año_end)+' guardada')
    #Creamos un dataframe para la tabla de defensiva con los datos obtenidos y lo guardamos en un archivo csv
    df=pd.DataFrame({'POS':posicion_of,'equipo':tabla_of_def_lista_equipo_def,'goles_contra':tabla_of_def_lista_num_def,'temporada':Temporada})
        #Reemplazamos los nombres de los equipos para que coincidan con los de la tabla de partidos
    df['equipo'] = df['equipo'].replace('Puebla F.C.','Puebla')
    df['equipo'] = df['equipo'].replace('Gallos Blancos de Querétaro','Querétaro')
    df['equipo'] = df['equipo'].replace('Lobos BUAP','Lobos')
    df['equipo'] = df['equipo'].replace('Tigres de la U.A.N.L.','Tigres')
    #Carpeta donde se guardaran los archivos
    carpeta = "out-docs"
    #Ruta de la carpeta
    ruta_carpeta = os.path.join(abspath(dirname(__file__)), carpeta)
    #Creación de la carpeta si no existe
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    nombre_archivo = "Tabla_Defensiva"+str(año_strt)+"-"+str(año_end)+".csv"
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
    #Guardamos el archivo
    df.to_csv(ruta_archivo,index=False)
    print('Tabla Defensiva '+str(año_strt)+'-'+str(año_end)+' guardada')
    #Cerramos el navegador
    driver.quit()
    time.sleep(1)
    print('[Tabla General, Tabla Ofensiva y Tabla Defensiva obtenidas]')

#scrapper_estadistica(2010,2013)
