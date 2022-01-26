# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 09:40:23 2022

@author: jan_c
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from tkinter import *
from tkinter import filedialog

# This function opern window to open several excel files and return a list of names of the files
def get_file():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Excel files","*.xlsx"),("all files","*.*")))
    root.destroy()
    return root.filename

n_archivo = get_file()
datos = pd.read_excel(n_archivo, sheet_name= "Hoja2", index_col=0, header = 0)
datos_g = round(datos["log(beta)"], 2)

lista = ["R1-OAc$^-$", "[R1 + Li$^+$]-OAc$^-$", "[R1 + Na$^+$]-OAc$^-$", "[R1 + K$^+$]-OAc$^-$",\
         "R2-OAc$^-$", "[R2 + Li$^+$]-OAc$^-$", "[R2 + Na$^+$]-OAc$^-$", "[R2 + K$^+$]-OAc$^-$",\
         "R3-OAc$^-$", "[R3 + Li$^+$]-OAc$^-$", "[R3 + Na$^+$]-OAc$^-$", "[R3 + K$^+$]-OAc$^-$"]

valores = list(datos_g)

colores = ["dimgrey", "r", "b", "g", "dimgrey", "r", "b", "g", "dimgrey", "r", "b", "g"]

fig = plt.figure()
plt.bar(lista,datos_g, color = colores, alpha = 0.85, edgecolor="k")
for i in range(len(valores)):
    plt.text(x = lista[i], y = datos_g[i]+0.1, s = valores[i], horizontalalignment='center', size = 10)
fig.autofmt_xdate(rotation=60)
plt.ylabel(r'log $\beta$', size= "xx-large")
plt.xticks(size = "large")
plt.yticks(size = "large")
plt.tight_layout()
plt.show()

fig.savefig('logbeta_barras.png', dpi=500)