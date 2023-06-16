# PrediLigaMX
Proyecto realizado para la clase de Manejo de Datos en la Universidad Nacional Autónoma de México, en el cual se ocupan técnicas de web scraping, manejo de bases de datos y metodos de Montecarlo.

## Demostración

[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://youtu.be/0lqG1xp7ymc)

## Requisitos

- Python 3.11 o superior
- Librerías de python: numpy, pandas, mysql-connector-python, selenium (versión 4), webdriver-manager, prettytable
- Google Chrome, versión acorde a tu versión de Selenium
- Una base de datos ya sea local o remota
- Hardware suficiente para ejecutar 3 pestañas de chrome simultáneas de manera estable
- Conexión de internet estable y de al menos 10mb de velocidad (de lo contrario podrías tener problemas en el web scraping)

## Modo de uso (Primera vez)

Una vez instalado todo y funcinando correctamente, asegurate de tener una cuenta en tu base de datos que permita crear bases de datos, tablas y subir datos a través de la librería mysql-connector-python, abre el programa ejecutando el archivo "main.py" con python e introduce los datos de conexión a tu base de datos.

Una vez realizado eso, selecciona la opción 1. "Actualizar base de datos" y asegurate de leer las advertencias, pues podrías borrar accidentalmente información en tu base de datos. En caso de continuar con la operación, espera a que se realice el proceso de web scraping, recuerda mantener el cursor fuera de cualquier ventana de chrome. Recuerda que sólo puedes obtener datos a partir de la temporada 2021-2022, de lo contrario el programa podría fallar.

Si los datos que extrajiste son de una temporada anterior a alguna de la cual se tengan datos, puedes calcular la efectividad de tus predicciones con la opción 3. "Comprobar efectividad", seleccionando el año que buscabas predecir. Te preguntará si deseas actualizar la sección de comprobación de la base de datos, a lo cual en caso de querer usar esa opción es necesario al menos la primera vez.

Finalmente puedes realizar tus predicciones con la opción 2. "Simular partidos" la cual te pedirá un equipo local y uno visitante, a lo cual posteriormente comenzará tu simulación y te devolverá información interesante sobre esas simulaciones, así como la recomendación del propio programa hacia cual equipo piensa que ganará, para más información puedes ver la demostración
