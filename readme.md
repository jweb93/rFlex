# VS Code

## Instalación
1. Descarga e instalación siguiendo pasos de: [VS Code](https://code.visualstudio.com/).
2. Instalar dependencias: 
* **color highlight**: para previsualizar el color css que estamos asignando
* **Live Server**: para actualizar automáticamente los cambios html
* **Path Intellisense**: para autocompletar rutas
* **Auto Rename Tag**: al renombrar un tag se renombra su pareja (de cierre o inicio)
* **Material Icon Theme**: diferencia el formato de los archivos con íconos
* **vscode-icons:** diferencia el formato de los archivos con íconos
* **Prettier - Code Formatter**:
* **Bracket Pair Colorizer:** para diferenciar con colores los brackets que hacen par

## Atajos
* ctrl+K ctrl+C : para comentar
* ctrl+K ctrl+U : para descomentar
* Alt+Z : para hacer wrap al texto
* Ctrl+Shift+P : para buscar aplicaciones

## Consola
En el menú superior es posible activar una consola

# Python

## Instalación
1. Descarga e instalación siguiendo pasos de: [python](https://www.python.org/). Es importante añadir Python al PATH (si no se hizo, más abajo explico como hacerlo después).
2. Validar en consola usando : python --version

## Añadir Python al PATH
1. Tecla Windows y escribir Python
2. Al .exe de Python dar clic derecho y abrir la ubicación
3. Copiar la Ubicación, ejemplo: C:\Users\javie\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.9
4. Abrir cualquier carpeta y dar clic derecho a Este Equipo para abrir sus propiedades
5. Ir a configuraciones avanzadas
6. Clic en variables de entorno
7. En variables de usuario dar doble clic en PATH y pegar la ubicación de python en una nueva linea
8. Si no existe PATH se debe crear con botón Nuevo llamando PATH a la variable y pegando la ubicación de python en su valor
9. Verificar en consola usando python --version

# pip

## Descarga
1. Acceder a: [pip](https://bootstrap.pypa.io/get-pip.py)
2. clic derecho y guardar

## Instalacion
1. En consola buscar la ubicación del archivo descargado
2. Ejecutar: python get-pip.py

## Ejemplo
pip install pandas
pip install requests

## Freeze
* pip freeze : Para listar dependencias instaladas
* pip freeze > requirements.txt : para generar un txt con la lista de dependencias instaladas y su versión
* pip install -r requirements.txt : para instalar las dependencias del archivo requirements

# Directorios

## BUK
* cliente: consulta el api buk para crear un excel con la nómina de trabajadores
* areas: consulta el api buk para crear un excel con las áreas, id área, centro costo, departamentos y divisiones
* cargos: consulta el api buk para crear un excel con los roles (CARGOS) y su ID

Para cada nuevo cliente se debe:
1. Copiar estos 3 archivos
2. Renombrar al nombre del cliente
3. Actuaizar token y URL
4. Actualizar el nombre con que se generarán los excel's

Nota:
* Cada archivo se genera con la fecha de hoy. Para generar nuevamente un archivo se debe borrar el de la fecha actual o bien cambiar su nombre para que no entre en conflicto con el nuevo archivo.

## PMO
* nombre_archivo

Para usar:
1. Generar token Asana y actualizar el archivo python (sólo 1 vez por nuevo usuario rFlex a cargo de esta labor)
2. Actualizar nombre proyecto 
3. Cada vez que se genera un nuevo cliente, se debe incluir en el listado de abreviaturas

## BBDD

### Borrado de permiso_tmp desactualizado y trabajador vigente
¿Cómo saber que permisos BUK se borraron o editaron?
Cada día el importador consulta el 100% de los permisos buk.
Por cada registro busca si ya existe en rFlex (su id en el meta). Si no existe lo crea. Si existe lo actualiza (update = now()).
Entonces, todos los permisos que no se actualizaron significa que fueron borrados o bien al trabajador se le dió la baja en buk.
No sería correcto borrar todos los permisos desactualizados ya que pueden ser de trabajadores desvinculados y no queremos que en planillas rFlex del pasado desaparezcan sus permisos. Lo correcto es borrar sólo los permisos desactualizados del personal vigente (rut en tabla ALTA).

El archivo _ _ _ realiza justamente esta labor de borrado.

### Cambio nombre CC's (idealmente abordar con procedimiento almacenado)
Existen nombres de CC que no ayudan a la gestión de nómina del cliente usando rFlex. En estos casos se define un nombre más apropiado y se actualiza la tabla Centro de Costo. Al día siguiente el comando importador de ALTA revierte los cambios y es necesario nuevamente el cambio de nombre.

### Enrolamiento GPS MEDS

