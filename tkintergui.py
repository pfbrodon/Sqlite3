import sqlite3 
import tkinter as tk
from tkinter import *
from tkinter import Menu,ttk
from tkinter import Tk, Label, Button, Entry, messagebox
import openpyxl
import os
import re
from tkinter.font import Font



##CORRECCION DE RUTA DE ARCHIVOS#########################################
##########################################################################
dirDeTrabajo = os.path.dirname(__file__)
os.chdir(dirDeTrabajo)
###########################################################################
ventana=Tk()
ventana.geometry("820x680")                                                    
ventana.title("Prueba Carga de Datos en SQLite")

# Crear una fuente con negrita
fuenteNegrita = Font(weight="bold")

cuadro1=Frame(ventana,width=500,height=400)

##FUNCION DE FORMATO DECIMAL Y SEPARADOR DE MILES
def formatoDecimal(value): 
    return "{:,.2f}".format(value)  # Formato con 2 decimales y separadores de miles


##FUNCION DE LISTADO DE PRODUCTOS
def mostarTabla():
    tablaFerreteria.delete(*tablaFerreteria.get_children())#borra el contenido de la tabla
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"SELECT * FROM stockFerreteria"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    for columna in datos:
        tablaFerreteria.insert("",0,text=columna[0], values=(columna[1],columna[2],columna[3],formatoDecimal(columna[4]),formatoDecimal(columna[5])))
    limpiarEntry()

##FUNCIONES DE BUSQUEDA DE PRODUCTOS################################################################


def busquedaCodigo():
    tablaFerreteria.delete(*tablaFerreteria.get_children())#borra el contenido de la tabla
    codigoBusq=entrada2.get()
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"SELECT * FROM stockFerreteria WHERE codigo like '{codigoBusq}'"##columna like '%variable%' busca un item en la columna que contenga el parametro de busqueda
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    for columna in datos:
        tablaFerreteria.insert("",0,text=columna[0], values=(columna[1],columna[2],columna[3],formatoDecimal(columna[4]),formatoDecimal(columna[5])))
        print(datos)

def busquedaDescripcion():
    tablaFerreteria.delete(*tablaFerreteria.get_children())#borra el contenido de la tabla treeview
    codigoBusq=entrada4.get()
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"SELECT * FROM stockFerreteria WHERE descripcion like '%{codigoBusq}%'"##columna like '%variable%' busca un item en la columna que contenga el parametro de busqueda
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    for columna in datos:
        tablaFerreteria.insert("",0,text=columna[0], values=(columna[1],columna[2],columna[3],formatoDecimal(columna[4]),formatoDecimal(columna[5])))
#FUNCION PARA INSERTAR PRODUCTOS############################################################################

def insertarProducto():          
    tablaFerreteria.delete(*tablaFerreteria.get_children())#borra el contenido de la tabla
    varCodigo=int(entrada2.get())
    varCategoria=entrada3.get()
    varDescripcion=entrada4.get()
    varCantidad=int(entrada5.get())
    varPrecioUnit=float(entrada6.get())
    varPrecioVPublico=float(entrada7.get())
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"INSERT INTO stockFerreteria VALUES({varCodigo},'{varCategoria.upper()}','{varDescripcion.upper()}', {varCantidad}, {varPrecioUnit:.2f},{varPrecioVPublico:.2f})"
    cursor.execute(instruccion)
    instruccion=f"SELECT * FROM stockFerreteria WHERE codigo='{varCodigo}'"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    for columna in datos:
        tablaFerreteria.insert("",0,text=columna[0], values=(columna[1],columna[2],columna[3],formatoDecimal(columna[4]),formatoDecimal(columna[5])))
    limpiarEntry()
    
###FUNCION PARA MODIFICAR PRODUCTO############################################################################
def modificarProducto():
    tablaFerreteria.delete(*tablaFerreteria.get_children())#borra el contenido de la tabla
    varCodigo=int(entrada2.get())
    varCategoria=entrada3.get()
    varDescripcion=entrada4.get()
    varCantidad=int(entrada5.get())
    varPrecioUnit=float(entrada6.get())
    varPrecioVPublico=float(entrada7.get())    
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"UPDATE stockFerreteria SET 'categoria' = '{varCategoria.upper()}', 'descripcion'='{varDescripcion.upper()}', 'cantidad'='{varCantidad}', 'precioUnit'='{varPrecioUnit:.2f}', 'precioVPublico'='{varPrecioVPublico}' WHERE codigo='{varCodigo}'"
    cursor.execute(instruccion)
    instruccion= f"SELECT * FROM stockFerreteria WHERE codigo='{varCodigo}'"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    for columna in datos:
        tablaFerreteria.insert("",0,text=columna[0], values=(columna[1],columna[2],columna[3],formatoDecimal(columna[4]),formatoDecimal(columna[5])))
    limpiarEntry()


###FUNCION DE BORRADO DE PRODUCTO############################################################################

def borrarProducto():
    varCodigo=int(entrada2.get())
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"DELETE FROM  stockFerreteria WHERE codigo='{varCodigo}'"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    limpiarEntry()
    
#FUNCION DE SELECCION MOUSE#################################################################################

def imprimirSeleccion(event):
    seleccion=tablaFerreteria.selection()
    #print(seleccion)
    for item in seleccion:
        valor=tablaFerreteria.item(item)["values"]
        #print("CODIGO:", tablaFerreteria.item(item)["text"])   #IMPRESION DE AYUDA
        #print(valor)                                        #IMPRESION DE AYUDA
        entrada3.delete(0, tk.END)  # Limpiar el contenido previo
        entrada3.insert(0,valor[0])
        entrada4.delete(0, tk.END)  # Limpiar el contenido previo
        entrada4.insert(0,valor[1])
        entrada5.delete(0, tk.END)  # Limpiar el contenido previo
        entrada5.insert(0,valor[2])
        #########################################
        print (valor[3])#impresion de ayuda
        digitosPrecio= (valor[3]).replace(',','')
        entrada6.delete(0, tk.END)  # Limpiar el contenido previo
        entrada6.insert(0,digitosPrecio)
        #####################################
        print (valor[4])#impresion de ayuda
        digitosPVP= (valor[4]).replace(',','')
        entrada7.delete(0, tk.END)  # Limpiar el contenido previo
        entrada7.insert(0,digitosPVP)
        ######################################
        entrada2.delete(0, tk.END)  # Limpiar el contenido previo
        entrada2.insert(0,tablaFerreteria.item(item)["text"])
        
##FUNCION DE LIMPIEZA DE ENTRY####################################################################
def limpiarEntry():
    entrada2.delete(0, tk.END)
    entrada3.delete(0, tk.END)
    entrada4.delete(0, tk.END)
    entrada5.delete(0, tk.END)
    entrada6.delete(0, tk.END)
    entrada7.delete(0, tk.END)
    
    
################################################################################ 
##FUNCION PARA VALORIZAR EL TOTAL DEL STOCK#####################################
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
    print(f"El valor acumulado de todo su Stock es de: ${sumaStock:,.2f} ")##IMPRESION EN CONSOLA PARA REFERNCIA
    lbl10.config(text=f'$ {sumaStock:,}.-', font=fuenteNegrita)
    return sumaStock

################################################################################ 
##FUNCION PARA EXPORTAR A UN ARCHIVO EXCEL#####################################
def exportatExcel():
    mi_conexion= sqlite3.connect("basededatosPrueba.db")  
    cursor=mi_conexion.cursor() 
    instruccion= f"SELECT * FROM stockFerreteria"
    cursor.execute(instruccion)
    datos=cursor.fetchall()
    mi_conexion.commit()
    mi_conexion.close()
    libroExcel = openpyxl.Workbook()
    hojaExcel = libroExcel.active
    encabezados=['CODIGO','CATEGORIA','DESCRIPCION','CANTIDAD','PRECIO','PRECIO VP']
    hojaExcel.append(encabezados)
    for valor in datos:
        hojaExcel.append(valor)
    libroExcel.save('lista_Ferreteria.xlsx')
    messagebox.showinfo( "","El Archivo se genero correctamente.")
    
    
##################################################################################################   
#INICIALIZACION DE VARIABLES######################################################################
codigoBusq=int()
descripcionBusq=()
itemTabla=()
sumaStock=()
#ENTRY#############################################################################################
entrada2=Entry(ventana,font=("Arial",10),width=7 ,justify="right",textvariable=codigoBusq)
entrada2.place(x=110,y=60)
entrada3=Entry(ventana,font=("Arial",10),width=12, textvariable=itemTabla)
entrada3.place(x=110,y=90)
entrada4=Entry(ventana,font=("Arial",10),width=40, textvariable=itemTabla)
entrada4.place(x=110,y=120)
entrada5=Entry(ventana,font=("Arial",10),width=5,justify="right",textvariable=itemTabla)
entrada5.place(x=110,y=150)
entrada6=Entry(ventana,font=("Arial",10),width=10,justify="right", textvariable=itemTabla)
entrada6.place(x=110,y=180)
entrada7=Entry(ventana,font=("Arial",10),width=10,justify="right",textvariable=itemTabla)
entrada7.place(x=110,y=210)




#ETIQUETAS#####################################################################################

lbl1=Label(ventana, text='VALOR DE STOCK EXISTENTE:')
lbl1.place(x=10,y=30)
lbl10=Label(ventana, text='')
lbl10.place(x=168,y=28)
lbl2=Label(ventana, text='CODIGO:')
lbl2.place(x=10,y=60)
lbl3=Label(ventana, text='CATEGORIA:')
lbl3.place(x=10,y=90)
lbl4=Label(ventana, text='DESCRIPCION:')
lbl4.place(x=10,y=120)
lbl5=Label(ventana, text='CANTIDAD:')
lbl5.place(x=10,y=150)
lbl6=Label(ventana, text='PRECIO COSTO:')
lbl6.place(x=10,y=180)
lbl7=Label(ventana, text='PRECIO VP:')
lbl7.place(x=10,y=210)

#BOTONES#########################################################################################
btn1=Button(ventana, font=("Arial",9), fg="black",background="light blue", width=25,border= 3,  text='VALORIZAR', command=valorizarStock)
btn1.place(x=620,y=50)
#btn1.config(font=11)
btn2=Button(ventana, font=("Arial",9), fg="black",background="light blue", width=25,border= 3,  text='BUSCAR CODIGO', command=busquedaCodigo)
btn2.place(x=620,y=90)
btn3=Button(ventana, font=("Arial",9), fg="black",background="light blue", width=25,border= 3 ,text='BUSCAR DESCRIPCION', command=busquedaDescripcion)
btn3.place(x=620,y=130)
btn4=Button(ventana, font=("Arial",9), fg="black",border= 3,width=25,  text='CARGAR LISTA DE PRECIOS', command=mostarTabla)
btn4.place(x=620,y=170)
btn5=Button(ventana, font=("Arial",9),fg="black",border= 3, width=25,background="light yellow" ,text='MODIFICAR PRODUCTO', command=modificarProducto)
btn5.place(x=420,y=50)
btn6=Button(ventana, font=("Arial",9), fg="black",border= 3,width=25 ,background="light green" ,text='ALTA PRODUCTO', command=insertarProducto)
btn6.place(x=420,y=90)
btn7=Button(ventana, font=("Arial",9), fg="black",border= 3,width=25, background="red"  ,text='BAJA PRODUCTO', command=borrarProducto)
btn7.place(x=420,y=130)
btn8=Button(ventana, font=("Arial",9), fg="black",width=25,border= 3,  text='LIMPIAR ENTRADA', command=limpiarEntry)
btn8.place(x=620,y=210)
btn9=Button(ventana, font=("Arial",9), fg="black",border= 3,width=25,  text='EXPORTAR', command=exportatExcel)
btn9.place(x=420,y=170)


###TREE VIEW- TABLA#############################################################
tablaFerreteria=ttk.Treeview(height=20,columns=('#0', '#1','#2','#3','#4'))
tablaFerreteria.place(x=10,y=250,width=700,height=400)
tablaFerreteria.column('#0', width=20,anchor='e')
tablaFerreteria.heading('#0',text="CODIGO",anchor='center',)
tablaFerreteria.column('#1', width=40)
tablaFerreteria.heading('#1',text="CATEGORIA",anchor="center")
tablaFerreteria.column('#2', width=250)
tablaFerreteria.heading('#2',text="DESCRIPCION",anchor="center")
tablaFerreteria.column('#3', width=20,anchor='e')
tablaFerreteria.heading('#3',text="CANTIDAD",anchor="center")
tablaFerreteria.column('#4', width=20,anchor='e')
tablaFerreteria.heading('#4',text="PRECIO",anchor="center")
tablaFerreteria.column('#5', width=20,anchor='e')
tablaFerreteria.heading('#5',text="PVP",anchor='center')
tablaFerreteria.bind("<ButtonRelease-1>", imprimirSeleccion)
#tablaFerreteria.bind("<>", imprimirSeleccion)
imprimirSeleccion(Event)
#mostarTabla()

ventana.mainloop()