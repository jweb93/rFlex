#descargar get-pip.py (goglear)
#pegar en carpeta C:usuarios/Javier Rojas (ya que ahí es donde comienza a buscar el cmd
#Windows->cmd
#python get-pip.py

#pip install requests
#pip install pandas
#pip install openpyxl
#pip install xlsxwriter

import requests
import time
empresas={}     #{id:[name,rut]}
trabajadores={}

ID=[]
Nombre=[]
Rut=[]
Estatus=[]
Rol_Privado=[]
Ficha=[]
Empresa_ID=[]
Empresa_Nombre=[]
Empresa_RUT=[]
Area=[]
Alta=[]
Baja=[]
Jornada=[]
CC=[]
ID_CARGO=[]
Cargo=[]
#Tipo_Cargo=[]
#Familia=[]
    
url='https://cliente.buk.cl/api/v1/'
tokens=[
{'auth_token':'aca pegar el token'}
]
Instancias=['Cliente']
k=-1
# Obtener Empresas
for token in tokens:
    k+=1
    query='companies'
    r=requests.get(url+query, headers=token)
    R=r.json()
    D=R['data']
    for i in range(0,len(D)):
        empresas[D[i]['id']]=[D[i]['name'],D[i]['rut']]
        print(Instancias[k]+' Empresa '+str(D[i]['id']))

k=-1    
for token in tokens:
    k+=1
    # Obtener Trabajadores
    query='employees?page_size=100&page='
    p=1
    P=12345
    while p<=P:
        print(Instancias[k]+' Pagina '+str(p)+' de '+str(P))
        r=requests.get(url+query+str(p), headers=token)
        p+=1
        R=r.json()
        if P==12345:
            P=R['pagination']['total_pages']
        D=R['data']
        for i in range(0,len(D)):
            if D[i]['current_job']=={}:
                trabajadores[D[i]['id']]=[D[i]['full_name'],
                                      D[i]['rut'],
                                      D[i]['status'],
                                      D[i]['private_role'],
                                      D[i]['code_sheet'],
                                      '',
                                      '',
                                      '',
                                      '',
                                      '',
                                      '',
                                      '',
                                      '',
                                      '',
                                      '',
                                      #,D[i]['current_job']['role']['custom_attributes']['Tipo de Cargo']
                                      #,D[i]['current_job']['role']['custom_attributes']['Subfamilia']
                                      ]
            else:
                trabajadores[D[i]['id']]=[D[i]['full_name'],
                                      D[i]['rut'],
                                      D[i]['status'],
                                      D[i]['private_role'],
                                      D[i]['code_sheet'],
                                      D[i]['current_job']['company_id'],
                                      empresas[D[i]['current_job']['company_id']][0],
                                      empresas[D[i]['current_job']['company_id']][1],
                                      D[i]['current_job']['area_id'],
                                      D[i]['current_job']['start_date'],
                                      D[i]['current_job']['end_date'],
                                      D[i]['current_job']['weekly_hours'],
                                      D[i]['current_job']['cost_center'],
                                      D[i]['current_job']['role']['id'],
                                      D[i]['current_job']['role']['name']
                                      #,D[i]['current_job']['role']['custom_attributes']['Tipo de Cargo']
                                      #,D[i]['current_job']['role']['custom_attributes']['Subfamilia']
                                      ]





#Exportable
import pandas as pd
from pandas import ExcelWriter
from datetime import *

for trabajador in trabajadores:
    ID.append(trabajador)
    Nombre.append(trabajadores[trabajador][0])
    Rut.append(trabajadores[trabajador][1])
    Estatus.append(trabajadores[trabajador][2])
    Rol_Privado.append(trabajadores[trabajador][3])
    Ficha.append(trabajadores[trabajador][4])
    Empresa_ID.append(trabajadores[trabajador][5])
    Empresa_Nombre.append(trabajadores[trabajador][6])
    Empresa_RUT.append(trabajadores[trabajador][7])
    Area.append(trabajadores[trabajador][8])
    Alta.append(trabajadores[trabajador][9])
    Baja.append(trabajadores[trabajador][10])
    Jornada.append(trabajadores[trabajador][11])
    CC.append(trabajadores[trabajador][12])
    ID_CARGO.append(trabajadores[trabajador][13])
    Cargo.append(trabajadores[trabajador][14])
    #Tipo_Cargo.append(trabajadores[trabajador][14])
    #Familia.append(trabajadores[trabajador][15])

df = pd.DataFrame({'ID': ID,
                   'Nombre': Nombre,
                   'Rut': Rut,
                   'Estatus': Estatus,
                   'Rol_Privado': Rol_Privado,
                   'Ficha': Ficha,
                   'Empresa_ID': Empresa_ID,
                   'Empresa_Nombre': Empresa_Nombre,
                   'Empresa_RUT': Empresa_RUT,
                   'Area': Area,
                   'Alta': Alta,
                   'Baja': Baja,
                   'Jornada': Jornada,
                   'CC': CC,
                   'ID_CARGO': ID_CARGO,
                   'Cargo': Cargo
                   #,'Tipo_Cargo': Tipo_Cargo
                   #,'Familia': Familia
                   })

df = df[['ID','Nombre','Rut','Estatus','Rol_Privado','Ficha','Empresa_ID','Empresa_Nombre',
         'Empresa_RUT','Area','Alta','Baja','Jornada','CC','ID_CARGO','Cargo']]#,'Tipo_Cargo','Familia',]]

Hoy=str(date.today().strftime('%Y%m%d'))
writer = ExcelWriter(Hoy+' Cliente.xlsx')

# Ingresar el dataframe en el excel. Index = True crea columna de numero fila.
df.to_excel(writer, sheet_name='Empleados', index=False)

# Cerrar archivo excel y generar.
writer.save()
