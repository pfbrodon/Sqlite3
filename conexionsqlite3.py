import sqlite3
from colorama import init,Fore, Back,just_fix_windows_console
from tabulate import tabulate
import os

###CORRECCION DE RUTA DE ARCHIVOS#########################################
##########################################################################
dirDeTrabajo = os.path.dirname(__file__)
os.chdir(dirDeTrabajo)
###########################################################################
init()
just_fix_windows_console()
#PAUSA CON RESPUESTA DE ENTER#############################################
def pausa_con_respuesta():
    input("Presiona Enter para continuar...")
    print("Continuando después de la pausa.")

#BOORADO DE PANTALLA#####################################################
def borrarpantalla():
    # El siguiente código funciona en Windows, macOS y Linux
    os.system('cls' if os.name == 'nt' else 'clear')
#FUNCION DE IMPRESION EN PANTALLA CON TABULATE Y COLORAMA EN LOS ENCABEZADOS
def impresionTabulada(datos):
    print (tabulate(datos,tablefmt="outline", headers=[Fore.GREEN+'CODIGO'+Fore.RESET,Fore.GREEN+'CATEGORIA'+Fore.RESET,Fore.GREEN+'DESCRIPCION'+Fore.RESET, Fore.GREEN+'CANTIDAD'+Fore.RESET, Fore.GREEN+'PRECIO'+Fore.RESET,Fore.GREEN+'PVP'+Fore.RESET],numalign="right",floatfmt=".2f"))
    print()

    
##FUNCION PARA CREAR UNA BASE DE DATOS Y LA TABLA STOCKFERRETERIA
def crearDB():
    try:
        mi_conexion=sqlite3.connect("basededatosPrueba.db")
        cursor=mi_conexion.cursor()
        cursor.execute("CREATE TABLE stockFerreteria (codigo INETGER, categoria VARCHAR(50),descripcion VARCHAR(50), cantidad INTEGER, precioUnit INTEGER, precioVPublico INTEGER)")
    except Exception as ex:
        print(ex)

#FUNCION PARA INSERTAR PRODUCTOS A LA TABLA STOCKFERRETERIA CON CONTROL DE ERRORES
def insertarProducto2():          
    ##INGRESO DE CODIGO################
    while True:
        while True:
            try: 
                codigoAlta=int(input("Ingrese el codigo del Producto: "))
                break
            except:
                print("El codigo debe ser un numer entero")
        ##################BUSQUEDA DE CODIGO
        mi_conexion= sqlite3.connect("basededatosPrueba.db")  
        cursor=mi_conexion.cursor() 
        instruccion= f"SELECT * FROM stockFerreteria WHERE codigo='{codigoAlta}'"
        cursor.execute(instruccion)
        datos=cursor.fetchall()
        mi_conexion.commit()
        mi_conexion.close()
        for item in datos:
            if item[0]==codigoAlta:
                print(f"El Codigo {codigoAlta} ya existe")
                break
        else:
                varCodigo=codigoAlta
                break
    #####################################################################################################################
    #INGRESO DE LA CATEGORIA######################################
    varCategoria=input("ingrese la categoria del Producto: ")
    ##############################################################
    #INGRESO DE LA CANTIDAD#######################################
    while True:
            try: 
                varCantidad=int(input("Ingrese la cantidad del Producto: "))
                break
            except:
                print("La cantidad del producto debe ser un numero entero")
    
    ##############################################################
    #INGRESO DE LA DESCRIPCION####################################
    varDescripcion=input("Ingrese la Descripcion del Producto: ")   
    ###############################################################
    #INGRESO DEL PRECIO UNITARIO###################################
    while True:
            try: 
                varPrecioUnit=float(input("Ingrese el precio Costo Unitario del Producto: "))
                break
            except:
                print("El precio C. Unitario debe ser un numero")
    ###############################################################
    #INGRESO DEL PRECIO VENTA AL PUBLICO############################
    while True:
            try: 
                varPrecioVPublico=float(input("Ingrese el precio Venta al Publico: "))
                break
            except:
                print("El PVP debe ser un numero")
    ######################################################################################################################
    #CONEXION E INGRESO DE LAS VARIABLES A LA TABLA#######################################
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"INSERT INTO stockFerreteria VALUES({varCodigo},'{varCategoria.upper()}','{varDescripcion.upper()}', {varCantidad}, {varPrecioUnit:.2f},{varPrecioVPublico:.2f})"
    cursor.execute(instruccion)
    mi_conexion.commit()
    mi_conexion.close()
    borrarpantalla()


##FUNCION PARA LISTAR LOS PRODUCTOS, DEVUELVE UNA PRINT EN PANTALLA EN FORMATO DE TUPLA
def listarProductos():
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"SELECT * FROM stockFerreteria"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    print(impresionTabulada(datos))
    print()
    salidaArchivo=int(input("Desea generar un Archivo con el listado? [1]: "))
    if salidaArchivo==1:
        archivo= open("reporte.txt","w")
        archivo.write(tabulate(datos,tablefmt="outline", headers=['CODIGO','CATEGORIA','DESCRIPCION', 'CANTIDAD', 'PRECIO','PVP'],numalign="right",floatfmt=".2f"))
        archivo.close()
        borrarpantalla()
    else:
        borrarpantalla()
##FUNCION DE MODIFICACION DE PRODUCTOS
def modificarProductos(codigoProducto):
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"SELECT * FROM stockFerreteria WHERE codigo='{codigoProducto}'"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    print()
    print(impresionTabulada(datos))
    while True:
        print()
        print('Seleccione el item a modificar: ')
        print()
        print(Fore.LIGHTYELLOW_EX+ "[1]"+Fore.RESET+"- CANTIDAD")
        print(Fore.LIGHTYELLOW_EX+ "[2]"+Fore.RESET+"- DESCRIPCION")    
        print(Fore.LIGHTYELLOW_EX+ "[3]"+Fore.RESET+"- CATEGORIA") 
        print(Fore.LIGHTYELLOW_EX+ "[4]"+Fore.RESET+"- PRECIO UNITARIO")
        print(Fore.LIGHTYELLOW_EX+ "[5]"+Fore.RESET+"- PRECIO V. PUBLICO")
        print(Fore.LIGHTRED_EX+ "[0]"+Fore.RESET+"- SALIR")
        print()
        varMenuMod= int(input("Ingrese el la opcion a modificar: "))
        if varMenuMod==1:
            campo= 'cantidad'
            while True:
                try: 
                    varCampo=int(input("Ingrese la cantidad del Producto: "))
                    break
                except:
                    print("La cantidad del producto debe ser un numero entero")
            break        
        elif varMenuMod==2:
            campo='descripcion'
            varCampo= input("Ingresar la descripcion del producto: ").upper()
            break
        elif varMenuMod==3:
            campo='categoria'
            varCampo= input("Ingrese la nueva categoria: ").upper()
            break
        elif varMenuMod==4:
            campo='precioUnit'
            while True:
                try: 
                    varCampo=float(input("Ingrese el precio Costo Unitario del Producto: "))
                    break
                except:
                    print("El precio C. Unitario debe ser un numero")
            break
        elif varMenuMod==5:
            campo= 'precioVPublico'
            while True:
                try: 
                    varCampo=float(input("Ingrese el precio Venta al Publico: "))
                    break
                except:
                    print("El PVP debe ser un numero")
            break
        elif varMenuMod==0:
            campo= 'codigo'
            varCampo= codigoProducto
            break
                
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"UPDATE stockFerreteria SET {campo}= '{varCampo}' WHERE codigo='{codigoProducto}'"
    cursor.execute(instruccion)
    instruccion= f"SELECT * FROM stockFerreteria WHERE codigo='{codigoProducto}'"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    borrarpantalla()
    print()
    print(impresionTabulada(datos))
    pausa_con_respuesta()
    borrarpantalla()
    
##FUNCION DE BUSQUEDA Y LISTADO DE PRODUCTOS
def busquedaProductos(criterioBusq):
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"SELECT * FROM stockFerreteria WHERE descripcion like '%{criterioBusq}%'"##columna like '%variable%' busca un item en la columna que contenga el parametro de busqueda
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    borrarpantalla()
    print(impresionTabulada(datos))
    pausa_con_respuesta()
    borrarpantalla()
    
##FUNCION DE BORRADO DE REGISTRO DE LA TABLA
def  borrarProductos(codigoProducto):
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"DELETE FROM  stockFerreteria WHERE codigo='{codigoProducto}'"
    cursor.execute(instruccion)
    mi_conexion.commit()
    mi_conexion.close()
    print ("El Registro ha sido eliminado")
    
##FUNCION PARA VALORIZAR EL TOTAL DEL STOCK
def valorizarStock():
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"SELECT * FROM stockFerreteria"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    sumaStock=0
    for valor in datos:
        (codigo, categoria ,descripcion, cantidad, preciounit, precioVPublico)=valor
        producto=cantidad*preciounit
        sumaStock=producto+sumaStock
        #print(producto)
    print(f"El valor acumulado de todo su Stock es de: ${sumaStock:.2f} ")
    pausa_con_respuesta()
    borrarpantalla()
#GENERACION DE MENU Y BUCLE PARA EL MANEJO DE LAS FUNCIONES
#varContinuar=True
borrarpantalla()
#print(Back.BLUE + Fore.WHITE+ 'and with a green background')
while True:
    
    print("")
    print("MENU DE OPCIONES")
    print("")
    print(Fore.LIGHTYELLOW_EX+ "[1]"+Fore.RESET+"- Insertar un prudcto")
    print(Fore.LIGHTYELLOW_EX+ "[2]"+Fore.RESET+"- Listar los Productos")
    print(Fore.LIGHTYELLOW_EX+ "[3]"+Fore.RESET+"- Crear una Base de Datos y Tabla de Stock")
    print(Fore.LIGHTYELLOW_EX+ "[4]"+Fore.RESET+"- Busqueda por Descripcion Producto")
    print(Fore.LIGHTYELLOW_EX+ "[5]"+Fore.RESET+"- Borrar un Producto")
    print(Fore.LIGHTYELLOW_EX+ "[6]"+Fore.RESET+"- Valoriar Stock")
    print(Fore.LIGHTYELLOW_EX+ "[7]"+Fore.RESET+"- Modificar Producto")
    print(Fore.LIGHTRED_EX+ "[8]"+Fore.RESET+"- Salir")
    print()
    while True:
            try: 
                varOpcion=int(input("Ingrese una Opcion: "))
                break
            except:
                print("La opcion debe ser un numero")       
    if varOpcion==1:
        borrarpantalla()
        insertarProducto2()
    elif varOpcion==2:
        borrarpantalla()
        listarProductos()
    elif varOpcion==3:
        crearDB()
    elif varOpcion==4:
        borrarpantalla()
        varCriterioBusq=input("Ingrese la Busqueda por Descripcion de Producto: ")
        borrarpantalla()
        busquedaProductos(criterioBusq= varCriterioBusq)
        
    elif varOpcion==5:
        varBorrarProductos= int(input("Ingrese el codigo del Producto a eliminar: "))
        borrarProductos(codigoProducto=varBorrarProductos)
    elif varOpcion==6:
        borrarpantalla()
        valorizarStock()
    elif varOpcion==7:
        borrarpantalla()
        varModificarProductos= int(input("Ingrese el codigo del Producto que desea Modificar: "))
        modificarProductos(codigoProducto=varModificarProductos)
    elif varOpcion==8:
        borrarpantalla()
        break
    elif varOpcion != range(1,9):
        borrarpantalla()
        print("Valor Incorrecto, seleccione una opcion entre 1 y 8")
        pausa_con_respuesta()
        borrarpantalla()
#insertarProducto("Tornillo Allen M12", 101, 53.5)