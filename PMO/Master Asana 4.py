## LIBRERIAS Y PARÁMETROS
import asana
from datetime import *  #Necesaria para computar fecha actual
personal_access_token = 'pegar tu token'
client = asana.Client.access_token(personal_access_token)
project_id='pegar el id proyecto asana'

##  CONSTRUCTORES
Campos = ['seccion','nombre','start_on','due_on','completed','completed_at']
Custom_Field=[]
Registros =[]
Fecha=str(date.today())

##  SECCIONES
params = {}
path = ("/projects/"+project_id+"/sections")
Sections=client.get_collection(path, params)
S=[]
for Section in Sections:
    if Section['name']!='Template Proyecto':
        S.append(Section)
#S[0]['name']=template, S[1]['name']=sanatorio, etc len(S)=13
#S[0]['gid']=1231231231

##  TAREAS
params = {"opt_fields":"name,start_on,due_on,completed,completed_at,custom_fields.name,custom_fields.enum_value"}

for Sec in S:
    path = ("/sections/"+Sec['gid']+"/tasks")
    Tasks=client.get_collection(path, params)
    T=[]
    for Task in Tasks:
        T.append(Task)
    for Tar in T:
        R=[]
        R.append(Sec['name'])
        R.append(Tar['name'])
        R.append(Tar['start_on'])
        R.append(Tar['due_on'])
        R.append(Tar['completed'])
        if Tar['completed_at']==None:
            R.append(Tar['completed_at'])
        else:
                R.append(Tar['completed_at'][:10])
        for CF in Tar['custom_fields']:
            if CF['enum_value'] == None:
                R.append(None)
            else:
                R.append(CF['enum_value']['name'])
            if len(Custom_Field)<len(Tar['custom_fields']):
                Custom_Field.append(CF['name'])
        R.append(Fecha)
        Registros.append(R)
        
Campos.extend(Custom_Field)
Campos.append('Consulted_at')

## GENERAR ARCHIVO EXCEL
import pandas as pd
from pandas import ExcelWriter  

#Crear data frame df
registros={} #registros={"campo":[valores],"campo2":[valores]}
for campo in Campos:
    registros[campo]=[]
for Fila in Registros:
    for i in range(0,len(Fila)):
        registros[Campos[i]].append(Fila[i])
        
df1=pd.DataFrame(registros)

#Definir orden de las columnas
df1 = df1[Campos]

#Nombrar archivo
Hoy=str(date.today().strftime('%Y%m%d'))
writer = ExcelWriter(Hoy+' Estatus Reunión PMO 4.xlsx')

#Nombrar hoja de calcula
#df1.to_excel(writer, sheet_name='Asana', index=False)

#Guardar archivo
#writer.save()


## MÉTRICAS ASANA

section_task={}         #Total de tareas de c/seccion
completed_task={}       #Tareas completadas de c/seccion
late_days={}            #Días de atraso de las tareas de c/seccion. solo si due_on!=none
early_days={}           #Dias de adelanto de las tareas de c/seccion. solo si due_on!=none
status_days={}          #late_days+early_days
completed={}            #total de seccions sin tareas sin completar.

section_task2={}       
completed_task2={}      
late_days2={}           
early_days2={}         
status_days2={}
completed2={}  


Secciones=list(set(registros['seccion'])) #set() para quitar duplicados
   
for seccion in Secciones:
    section_task[seccion]=0
    completed_task[seccion]=0
    late_days[seccion]=0
    early_days[seccion]=0
    status_days[seccion]=0
    completed[seccion]=1

    section_task2[seccion]=0
    completed_task2[seccion]=0
    late_days2[seccion]=0
    early_days2[seccion]=0
    status_days2[seccion]=0
    completed2[seccion]=1
    
def workdays(start, end, excluded=(6, 7)): #Dias habiles para computar timeless
    days = 0
    while start.date() <= end.date():
        if start.isoweekday() not in excluded:
            days+=1
        start += timedelta(days=1)
    return days

for i in range(0,len(registros['seccion'])): #recorrer todos los registros conociendo su index. Podría haber sido seccion, due_on, completed, etc cualqueir campo
    if registros['Implementación'][i]== 'Base':
        section_task[registros['seccion'][i]]+=1
        if registros['completed'][i]==False:        #No completa
            completed[registros['seccion'][i]]*=0   #solo los registros sin pendientes quedarán en 1
            if (registros['due_on'][i]!= None and registros['Timeless'][i]=='Late'):
                due_on= datetime.strptime(registros['due_on'][i],'%Y-%m-%d')
                Consulted_at= datetime.strptime(registros['Consulted_at'][i],'%Y-%m-%d')
                late_days[registros['seccion'][i]]+=workdays(due_on,Consulted_at)
        else:                                       #Completa
            completed_task[registros['seccion'][i]]+=1 
            if registros['Timeless'][i] in {'On time','Early',None,''}:
                if (registros['Timeless'][i] == 'Early' and registros['due_on'][i]!= None):
                    due_on= datetime.strptime(registros['due_on'][i],'%Y-%m-%d')
                    completed_at= datetime.strptime(registros['completed_at'][i],'%Y-%m-%d')
                    early_days[registros['seccion'][i]]+=workdays(completed_at,due_on)
            else:
                if registros['due_on'][i]!= None:
                    due_on= datetime.strptime(registros['due_on'][i],'%Y-%m-%d')
                    completed_at= datetime.strptime(registros['completed_at'][i],'%Y-%m-%d')
                    late_days[registros['seccion'][i]]+=workdays(due_on,completed_at)

    else:
        section_task2[registros['seccion'][i]]+=1
        if registros['completed'][i]==False:        #No completa
            completed2[registros['seccion'][i]]*=0   #solo los registros sin pendientes quedarán en 1
            if (registros['due_on'][i]!= None and registros['Timeless'][i]=='Late'):
                due_on= datetime.strptime(registros['due_on'][i],'%Y-%m-%d')
                Consulted_at= datetime.strptime(registros['Consulted_at'][i],'%Y-%m-%d')
                late_days2[registros['seccion'][i]]+=workdays(due_on,Consulted_at)
        else:                                       #Completa
            completed_task2[registros['seccion'][i]]+=1 
            if registros['Timeless'][i] in {'On time','Early',None,''}:
                if (registros['Timeless'][i] == 'Early' and registros['due_on'][i]!= None):
                    due_on= datetime.strptime(registros['due_on'][i],'%Y-%m-%d')
                    completed_at= datetime.strptime(registros['completed_at'][i],'%Y-%m-%d')
                    early_days2[registros['seccion'][i]]+=workdays(completed_at,due_on)
            else:
                if registros['due_on'][i]!= None:
                    due_on= datetime.strptime(registros['due_on'][i],'%Y-%m-%d')
                    completed_at= datetime.strptime(registros['completed_at'][i],'%Y-%m-%d')
                    late_days2[registros['seccion'][i]]+=workdays(due_on,completed_at)


c=0
for comp in completed:
    c+=completed[comp]
project=len(Secciones)-c

c2=0
for comp in completed2:
    c2+=completed2[comp]
project2=len(Secciones)-c2

for est in status_days:
    status_days[est]=early_days[est]-late_days[est]

for est in status_days2:
    status_days2[est]=early_days2[est]-late_days2[est]

## KPI ASANA
from decimal import Decimal
KPI={'n°':[],
     'Abrev':[],
     'Name':[],
     'Completion':[],
     'Previo':[],
     'Q':[],
     'Progress':[],
     'Timeless':[],
     'Previo2':[],
     'Delta':[]}

KPI2={'n°':[],
     'Abrev':[],
     'Name':[],
     'Completion':[],
     'Previo':[],
     'Q':[],
     'Progress':[],
     'Timeless':[],
     'Previo2':[],
     'Delta':[]}

Nabrev={}
Nabrev['Cierre Clínica Dávila']=['Davila',1]
Nabrev['Clínica Santamaría']=['CSM',2]
Nabrev['Clínica RedSalud Vitacura']=['Tabancura',3]
Nabrev['Clínica Ciudad del Mar']=['CCDM',4]
Nabrev['Clínica Cordillera']=['Cordillera',5]
Nabrev['Tarapacá']=['Tarapaca',6]
Nabrev['Los Carrera']=['Los Carrera',7]
Nabrev['Los Leones']=['Los Leones',8]
Nabrev['Clínica Las Condes']=['CLC',9]
Nabrev['UC Christus']=['Christus',10]
Nabrev['Ambar']=['Ambar',11]
Nabrev['Marina Hotel Santiago']=['Marina S.',12]
Nabrev['FALP']=['FALP',13]
Nabrev['CETEP']=['CETEP',14]
Nabrev['Clínica Sanatorio Alemán']=['SA',15]
Nabrev['Clínica Hospital del Profesor']=['CHP',16]
Nabrev['ARDAC ADMINISTRADORA']=['ARDAC A.',17]
Nabrev['Clínica Biobío']=['BioBio',18]
Nabrev['Grupo Medical']=['GM',19]
Nabrev['Hospital del Trabajador - ACHS']=['ACHS',20]
Nabrev['Pilotos']=['Pilotos',21]
Nabrev['Marina Hotel Viña']=['Marina V.',22]
Nabrev['Marcaje App NO CLIENTES Banmédica']=['APP Bmdca',23]
Nabrev['Clínica Vespucio']=['Vespucio',24]
Nabrev['GEMCO']=['GEMCO',25]
Nabrev['Clínica U. de los Andes']=['U.Andes',26]
Nabrev['Salud Responde']=['SR',27]
Nabrev['Nexans']=['Nexans',28]
Nabrev['Help']=['Help',29]
Nabrev['Complejo Asistencial Sótero del Río']=['CASR',30]
Nabrev['Clínica Andes Salud Concepción']=['CASC',31]
Nabrev['Clínica Andes Salud Chillán']=['CASCH',32]
Nabrev['Clínica Andes Salud El Loa']=['CASEL',33]
Nabrev['Clínica Andes Salud Puerto Montt']=['CASPM',34]
Nabrev['Hospital del Salvador']=['HDS',35]
Nabrev['ARDAC CONSTRUCTORA']=['ARDAC C.',36]
Nabrev['Home Hilfe']=['HH',37]
Nabrev['REVICENTRO']=['RC',38]
Nabrev['Bupa Santiago']=['CBS',39]
Nabrev['Bupa Reñaca']=['CBR',40]
Nabrev['Bupa Antofagasta']=['CBA',41]
Nabrev['Bupa San José']=['CBSJ',42]
Nabrev['Clínica Alemana']=['CA',43]
Nabrev['Clínica Maitenes']=['CM',44]
Nabrev['Clínica MEDS']=['MEDS',45]
Nabrev['Cotelsa']=['Cotelsa',46]
Nabrev['Acalis']=['Acalis',47]
Nabrev['Clínica Puerto Varas']=['CPV',48]
Nabrev['Sanatorio Alemán - Médicos']=['Sanatorio Alemán - Médicos',49]
Nabrev['Gourmet']=['Gourmet',50]
Nabrev['Cramer']=['Cramer',51]


#Data frame de KPI
for sec in section_task:
    KPI['n°'].append(Nabrev[sec][1])
    KPI['Abrev'].append(Nabrev[sec][0])
    KPI['Name'].append(sec)
    KPI['Timeless'].append(status_days[sec])
    KPI['Q'].append(section_task[sec])
    if section_task[sec] == 0:
        KPI['Completion'].append(1)
    else:
        KPI['Completion'].append(round(completed_task[sec]/section_task[sec],2))
    KPI['Previo']=0
    KPI['Previo2']=0
    KPI['Progress']=0
    KPI['Delta']=0

for sec in section_task2:
    KPI2['n°'].append(Nabrev[sec][1])
    KPI2['Abrev'].append(Nabrev[sec][0])
    KPI2['Name'].append(sec)
    KPI2['Timeless'].append(status_days2[sec])
    KPI2['Q'].append(section_task2[sec])
    if section_task2[sec] == 0:  ### Acá limitar solo a secciones que tengan tareas, sino saltar a la siguiente
        KPI2['Completion'].append(1)
    else:
        KPI2['Completion'].append(round(completed_task2[sec]/section_task2[sec],2))
    KPI2['Previo']=0
    KPI2['Previo2']=0
    KPI2['Progress']=0
    KPI2['Delta']=0
    

Campos_KPI=['n°','Abrev','Name','Completion','Previo','Progress','Q','Timeless','Previo2','Delta']
        
df2=pd.DataFrame(KPI)
df2=df2[Campos_KPI]

df3=pd.DataFrame(KPI2)
df3=df3[Campos_KPI]

#Nombrar hoja de calculo. 'writer' ya creado
df1.to_excel(writer, sheet_name='Asana', index=False)
df2.to_excel(writer, sheet_name='KPI Base', index=False)
df3.to_excel(writer, sheet_name='KPI2 Adicionales', index=False)


#Guardar archivo
writer.save()

#Para escribir en un archivo existente se hace:
#writer=ExcelWriter('path_to_file.xlsx', mode='a')
#dfn.to_excel(writer, sheet_name='Sheet3')

'''
## GRAFICOS

## Get the xlsxwriter objects from the dataframe writer object.
#workbook  = writer.book
#worksheet = writer.sheets['Sheet1']

# Create a chart object.
chart = workbook.add_chart({'type': 'column'})
#tipo: https://xlsxwriter.readthedocs.io/working_with_pandas.html

# Configure the series of the chart from the dataframe data.
chart.add_series({'values': '=Sheet1!$B$2:$B$8'})

# Insert the chart into the worksheet.
worksheet.insert_chart('D2', chart)

# Apply a conditional format to the cell range.
worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})

#writer.save()
'''

## METRICAS BBDD

## KPI BBDD
