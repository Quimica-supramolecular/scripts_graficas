# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:51:30 2021

@author: jan_c
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.core.series import Series

# This function open window for search local file .xlxs and .xlsx in directory and return filename
def open_file():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
    
    return root.filename    


# This function read data from file and return dataframe

filename = open_file()

def read_file(filename, sheet_name):
    data = pd.read_excel(filename, sheet_name= sheet_name, header=0, index_col=0)
    return data 


dataframe = read_file(filename, sheet_name="datos_complementarios")

#indices = pd.DataFrame(dataframe.columns).values.astype(str)

def get_index_list(dataframe):
    index_list = dataframe.index.tolist()
    index_list = list(dict.fromkeys(index_list))
    return index_list

indice_depurado = get_index_list(dataframe)


#This function delete outliers of dataframe using IQR method
def delete_outliers(dataframe):
    dataframe_new = dataframe.copy()
    IQR = dataframe.quantile(.75) - dataframe.quantile(.25)
    lower_bound = dataframe.quantile(.25) - 1.5*IQR
    upper_bound = dataframe.quantile(.75) + 1.5*IQR
    dataframe_new = dataframe_new[(dataframe_new >= lower_bound) & (dataframe_new <= upper_bound)]
    dataframe_new.dropna(inplace=True)
    return dataframe_new

#dataframe_new = delete_outliers(dataframe)
print(indice_depurado)
datos_generales_woutliers = pd.DataFrame([])
for i in indice_depurado:
    globals()[i] = delete_outliers(dataframe.loc[i])
    datos_generales_woutliers = datos_generales_woutliers.append(globals()[i])

print(datos_generales_woutliers)

#This function normalize dataframe using min-max with mean method

receptor = str(input("Ingrese el receptor: "))
lon_onda = str(input("Ingrese la longitud de onda: "))

def data_ajustada(dataframe, receptor, lon_onda):
    dataframe_new = dataframe.copy()
    dataframe_new = dataframe_new / dataframe_new.loc[receptor][lon_onda].mean()
    return dataframe_new

def normalize_data(dataframe, receptor, lon_onda):
    dataframe_new = dataframe.copy()
    dataframe_new = (dataframe_new - dataframe_new.loc[receptor][lon_onda].mean()) / (dataframe_new.max() - dataframe_new.min())
    return dataframe_new

datos_normnalizados = normalize_data(datos_generales_woutliers, receptor, lon_onda)
datos_ajustados = data_ajustada(datos_generales_woutliers, receptor, lon_onda)

#This function take datos_ajustados and agroup them by name index and lon_onda
def agrupar_columnas_iterativo(dataframe, indice):
    datos_t = []
    for i in indice:
        lista = str(i)
        datos = []
        df = dataframe.loc[lista]
        df = datos.append(df)
        datos = np.column_stack(datos)
        datos = np.hstack(datos)
        datos_t.append(datos)
    return pd.DataFrame(datos_t)

datos_agrupados = agrupar_columnas_iterativo(datos_ajustados[lon_onda], indice_depurado)
#print(pd.DataFrame(datos_agrupados))

indice_i = pd.DataFrame(indice_depurado, columns=["Muestra"])
datos_agrupados = pd.concat([datos_agrupados, indice_i], axis=1)
datos_agrupados = datos_agrupados.set_index("Muestra")
print(datos_agrupados.T)

#This function asign to each name in indice the corresponding number of orden
indice = pd.DataFrame(list(datos_ajustados.index), columns=["Muestra"])
orden = (indice.groupby(["Muestra"]).cumcount()==0).astype(int)
orden = pd.DataFrame(list(orden.cumsum()), columns=["Orden"])

"""
Existe tambien la opcion utilizar la funcion groupby("Muestra).ngroup(), el problema para mi proposito es que 
comienza la numeración con cero, por lo que no me sirve para el orden de las muestras
"""
datos_ajustados_interes = pd.DataFrame(datos_ajustados[lon_onda].values, columns=[lon_onda])
orden_grupos = pd.concat([indice.T, datos_ajustados_interes.T, orden.T], ignore_index=False)
print(orden_grupos.T)

with pd.ExcelWriter(filename[:-5]+'_woutliers'+'.xlsx') as writer:
    datos_generales_woutliers.to_excel(writer, sheet_name='datos_complementarios')
    datos_normnalizados.to_excel(writer, sheet_name='datos_normalizados')
    datos_ajustados.to_excel(writer, sheet_name='datos_ajustados')
    datos_agrupados.T.to_excel(writer, sheet_name='datos_agrupados')
    orden_grupos.T.to_excel(writer, sheet_name='orden_grupos')
    

















