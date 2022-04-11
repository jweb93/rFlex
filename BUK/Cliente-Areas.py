import requests

url='https://cliente.buk.cl/api/v1/areas'
query='?page=1&page_size=100'
header={'auth_token':'aca pegar el token'}
param={} 
data={}
#requests.get(url+query,params=param,data=data,headers=header)

r=requests.get(url+query,headers=header).json()
page=r['pagination']['total_pages']

#Variables
area_id=[]
area_name=[]
cost_center=[]
depto_id=[]
depto_name=[]
div_id=[]
div_name=[]

#Extraccion
for p in range(1,page+1,1):
    query='?page='+str(p)+'&page_size=100'
    r=requests.get(url+query,headers=header).json()
    d=r['data'] #llega en formato lista
    for i in range(0,len(d)):
        area_id.append(d[i]['id'])
        area_name.append(d[i]['name'])
        cost_center.append(d[i]['cost_center'])
        depto_id.append(d[i]['department']['id'])
        depto_name.append(d[i]['department']['name'])
        div_id.append(d[i]['department']['division']['id'])
        div_name.append(d[i]['department']['division']['name'])

#Estructura de datos
import pandas as pd
from pandas import ExcelWriter
from datetime import *

df = pd.DataFrame({
    'area_id': area_id,
    'area_name':area_name,
    'cost_center':cost_center,
    'depto_id':depto_id,
    'depto_name':depto_name,
    'div_id':div_id,
    'div_name':div_name
    })

df = df[['area_id','area_name','cost_center','depto_id','depto_name','div_id','div_name']]

hoy=str(date.today().strftime('%Y%m%d'))
writer = ExcelWriter(hoy+' Cliente-Areas.xlsx')

df.to_excel(writer, sheet_name='Areas', index=False)
writer.save()
