# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 20:08:48 2021

@author: jan_c
"""
import pandas as pd
from tkinter import *
from tkinter import filedialog


if __name__ == '__main__':
    
    def frame():
        
        def abrir_archivo():
            global archivo
            archivo = filedialog.askopenfilename(title="Abrir archivo .xlsx", initialdir="F:/", filetypes=(("Archivo .xlsx", "*.xlsx"), ("Archivo .xls", "*.xls")))
            raiz.destroy()
            
        raiz = Tk()
        mi_frame = Frame(raiz, width=200, height=60)
        mi_frame.pack()
        boton = Button(raiz, text="Abrir archivo", command=abrir_archivo)
        boton.pack(fill=X)
        boton.config(cursor="hand2")
        boton.config(bd=4)
        boton.config(relief="groove")
        raiz.mainloop()
        return archivo
    
    archivo = frame()
    
    #Leer archivo de entrada
    datos = pd.read_excel(archivo, sheet_name="Resumen de resultados", header=4)

    # Se filtran las columnas de interes y se generan los datos ordenados
    filtro_fluorescencia = datos.filter(regex = "Fluorescencia") # filtra columnas
    datos_f = pd.DataFrame(filtro_fluorescencia)
    muestra = pd.DataFrame(datos["Muestra"])
    datos_gen = pd.concat([muestra, datos_f], axis=1) # Concatenamos los datos
    datos_generales = datos_gen.set_index("Muestra")
    print(datos_generales)
    
    # Se prepara el archivo de salida
    with pd.ExcelWriter(archivo[:-5] + "_salida" + ".xlsx") as writer:
        datos_generales.to_excel(writer, sheet_name="datos_generales")