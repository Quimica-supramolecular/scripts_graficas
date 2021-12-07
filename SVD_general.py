# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 11:43:31 2021

@author: jan_c
"""

#gráficas con sales y fase sólida.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

"con este codigo se llama a los datos"

from tkinter import *
from tkinter import filedialog


def abrir_archivo():
    global archivo
    archivo = filedialog.askopenfilename(title="Abrir archivo .xlsx", initialdir="F:/", filetypes=(("Archivo .xlsx", "*.xlsx"), ("Archivo .xls", "*.xls")))
    raiz.destroy()
    

if __name__ == '__main__':

    raiz = Tk()
    mi_frame = Frame(raiz, width=200, height=60)
    mi_frame.pack()
    boton = Button(raiz, text="Abrir archivo", command=abrir_archivo)
    boton.pack(fill=X)
    boton.config(cursor="hand2")
    boton.config(bd=4)
    boton.config(relief="groove")
    raiz.mainloop()

data1 = archivo
spectra="datos_generales"
data= pd.read_excel(data1, spectra, header=0, index_col=0)
data_0 = pd.read_excel(data1, spectra, header=0)
#conce = pd.read_excel(data1, "Hoja3", header=0) 
u, s, v = np.linalg.svd(data, False)

 
plt.plot(range(0, len(s)), np.log10(s), "o")
plt.show()


indices = pd.DataFrame(data_0.columns).values.astype(str) # convertimos los valores a texto
#indices = indices[1:] # separamos la columna "Muestra"

nuevos_nombres = list()
for i in indices:
    a = i[-1]
    d_r =  a[-6:-1] #'f_' + a[-6:-1])
    nuevos_nombres.append(d_r)

datos = u[:,0:1] @ np.diag(s[0:1:]) @ v[0:1:] 

datos_generales = pd.DataFrame(data).set_index(data_0["Muestra"])
datos_generales = datos_generales.set_axis(nuevos_nombres[1:], axis = 1)


plt.plot(range(0, len(u[:,2])), u[:,0:1], ":o")
plt.show()

plt.plot(range(0, len(v)), v[0:1:].T, ":o")
plt.show()


# Se prepara el archivo de salida
with pd.ExcelWriter(data1[:-5] + "_v1" + ".xlsx") as writer:
    datos_generales.to_excel(writer, sheet_name="datos_generales_svd")