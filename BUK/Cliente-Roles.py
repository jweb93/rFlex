import requests

url='https://cliente.buk.cl/api/v1/roles'
query='?page=1&page_size=100'
header={'auth_token':'aca pegar el token'}
param={} 
data={}
#requests.get(url+query,params=param,data=data,headers=header)

r=requests.get(url+query,headers=header).json()
page=r['pagination']['total_pages']

#Variables
rol_id=[]
rol_name=[]

#Extraccion
for p in range(1,page+1,1):
    query='?page='+str(p)+'&page_size=100'
    r=requests.get(url+query,headers=header).json()
    d=r['data'] #llega en formato lista
    for i in range(0,len(d)):
        rol_id.append(d[i]['id'])
        rol_name.append(d[i]['name'])

#Estructura de datos
import pandas as pd
from pandas import ExcelWriter
from datetime import *

df = pd.DataFrame({
    'rol_id': rol_id,
    'rol_name': rol_name
    })

df = df[['rol_id','rol_name']]

hoy=str(date.today().strftime('%Y%m%d'))
writer = ExcelWriter(hoy+' Cliente-Roles.xlsx')

df.to_excel(writer, sheet_name='Roles', index=False)
writer.save()
