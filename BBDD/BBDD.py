import mysql.connector
from datetime import *

def connection(db0,host0,user0,password0,port0):
    mydb = mysql.connector.connect(
        host = host0,
        user = user0,
        password = password0,
        database = db0,
        port = port0
    )
    return mydb
    

def run(db,host,user,password,port):
    ids = []
    now1 = str((datetime.now()).strftime('%Y-%m-%d'))

    #Lectura de casos
    mydb = connection(db,host,user,password,port)

    query1 = 'SELECT IDPERMISO FROM %s_rrhh.PERMISO_TMP where updated_at < "%s" and RUT in (SELECT RUT FROM %s_rrhh.ALTA);' % (db,now1, db)

    mycursor = mydb.cursor()
    
    mycursor.execute(query1)
    
    myresult = mycursor.fetchall()

    for r in myresult:
        ids.append(str(r[0]))
    
    mydb.close()

    #Licencia 1/2 de uc
    # if db=="uchospital":
    #     print(ids)
    #     ids.remove(str(31442))
    #     print(ids)

    #Borrado de casos
    deleted = 0
    for i in ids:
        query2 = 'DELETE FROM %s_rrhh.PERMISO_TMP WHERE (IDPERMISO = %s);' % (db, i)
        mydb = connection(db,host,user,password,port)
        mycursor = mydb.cursor()
        mycursor.execute(query2)
        deleted += mycursor.rowcount
        mydb.commit()
        mydb.close()

    #Historia
    now2=str((datetime.now()).strftime('%Y-%m-%d %H:%M:%S'))
    a=open('Permisos.txt','a')
    a.seek(0,2)
    a.write('\n\n'+now2+' Permisos encontrados/borrados en '+db+': '+str(len(ids))+'/'+str(deleted))
    a.close()

    print("listo con "+db)



if __name__ == '__main__':
    run('cbs',"IP","admin_bupa_proyectos","clave","3306")
    run('cbsj',"IP","admin_bupa_proyectos","clave","3306")
    run('cba',"IP","admin_bupa_proyectos","clave","3306")
    run('cbr',"IP","admin_bupa_proyectos","clave","3306")
    run('chp',"IP","admin_rflex_bd","clave","3306")
    run('grupogemco',"IP","admin_rflex_bd","clave","3306")
    run('sanatorioaleman',"IP","admin_rflex_bd","clave","3306")
    run('tabancura',"IP","jrplwndb7aMUHsnn","clave","3306")
    run('ambar',"IP","jrplwndb7aMUHsnn","clave","3306")
    run('ucsancarlos',"IP","jrplwndb7aMUHsnn","clave","3306")
    run('uchospital',"IP","jrplwndb7aMUHsnn","clave","3306")
    run('ucambulatorio',"IP","jrplwndb7aMUHsnn","clave","3306")

    run('casc',"IP","admin_rflex_bd","clave","3306")
    run('cascal',"IP","admin_rflex_bd","clave","3306")
    run('casch',"IP","admin_rflex_bd","clave","3306")
    run('caspm',"IP","admin_rflex_bd","clave","3306")


