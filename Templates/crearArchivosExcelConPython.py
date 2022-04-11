#import pandas as pd
#from pandas import ExcelWriter
import pandas as pd
from pandas import ExcelWriter  
# Create a Pandas dataframe from the data (columnas y registros).
df = pd.DataFrame({'Id': [1, 3, 2, 4],
                   'Nombre': ['Juan', 'Eva', 'María', 'Pablo'],
                   'Apellido': ['Méndez', 'López', 'Tito', 'Hernández']})

# Definir el orden de las columnas (si se especifica se ordenan por letra)
df = df[['Id', 'Nombre', 'Apellido']]

#Crear archivo excel contenedor
writer = ExcelWriter('ejemplo.xlsx')

# Ingresar el dataframe en el excel. Index = True crea columna de numero fila.
df.to_excel(writer, sheet_name='Hoja de datos', index=False)

# Cerrar archivo excel y generar.
writer.save()
