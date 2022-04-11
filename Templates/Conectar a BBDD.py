"""
Objetivos
 - Generar una interfaz que facilite la creación de reportes
 - Generar registros historicos de KPI
 - Usar Google Data studio para KPI online (cambian día a día y nos interesa el valor actual
"""

############################################         MODELO       ###################################################################
import mysql.connector
Bases=[['davila','30001'],
       ['stamaria','30002'],
       ['tabancura','30003'],
       ['ccdm','30004'],
       ['tarapaca','30005'],
       ['losleones','30005'],
       ['loscarrera','30005'],
       ['cordillera','30005'],
       ['clc','30006'],
       ['uchospital','30007'],
       ['ucambulatorio','30007'],
       ['ucsancarlos','30007'],
       ['ucclinica','30007'],
       ['"+Base[0]+"','30008']]

Total=0

for Base in Bases:
    cnx = mysql.connector.connect(user='root', password='123', host='120.75.163.123', port=Base[1], database=Base[0])
    query=("")
	cursor = cnx.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    print (Base[0], records[0][0])
    Total=Total+records[0][0]
    cnx.close()

###########################################       CONTROLADOR       ###################################################################
#de momento este archivo .py solo genera un excel y esa es su funcionalidad como controlador

############################################         VISTA       ###################################################################
import pandas as pd             #libreria pandas facilita creación de excel
from pandas import ExcelWriter  
from datetime import *          #librería para gestion de fechas y asi poder nombrar el archivo


#Create a Pandas dataframe from the data (columnas y registros)"""
df = pd.DataFrame({'Id': [1, 3, 2, 4],
                   'Nombre': ['Juan', 'Eva', 'María', 'Pablo'],
                   'Apellido': ['Méndez', 'López', 'Tito', 'Hernández']})

# Definir el orden de las columnas (si se especifica se ordenan por letra)
df = df[['Id', 'Nombre', 'Apellido']]

#Crear archivo excel contenedor
today = date.today()
fecha=str(today.strftime('%Y%m%d'))
writer = ExcelWriter(fecha+' Panel de Usuarios.xlsx')

# Ingresar el dataframe en el excel. Index = True crea columna de numero fila.
df.to_excel(writer, sheet_name='Hoja de datos', index=False)

# Cerrar archivo excel y generar.
writer.save()


