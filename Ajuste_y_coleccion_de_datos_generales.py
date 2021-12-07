# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 17:15:48 2021

@author: jan_c
"""
from numpy.core.shape_base import vstack
import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize 
from tkinter import *
from tkinter import filedialog
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as st

#%% Obtencion y acomod de datos

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
    df = pd.read_excel(archivo, sheet_name="datos_complementarios", header=0, index_col=0)
    indice = pd.DataFrame(list(df.index))
    indice = pd.DataFrame(indice.drop_duplicates())
    print(indice)

lon_onda = str(input("¿Cúal es la longitud de onda de interés: "))
nom_receptor = str(input("¿Cúal es el nombre del receptor: "))

#This function is used to divide the dataframe by mean of nom_receptor and change his index by list of sales1
def division_df(df, nom_receptor, lon_onda):
    df_receptor = pd.DataFrame(df / np.mean(df.loc[nom_receptor][lon_onda]))
    return df_receptor

sales1 = pd.DataFrame(["R-Free", "R-TBAA", "R-TMABS", "R-TMAB", "R-TMAC", "R-TMAF", "R-TBAP", "R-TMAI", "R-TMAN"], columns=["Muestra"])
sales2 = ["R-Free", "R-KCl", "R-KI", "R-LiCl","R-Na2HPO4","R-Na2SO4", "R-NaCH3CO2","R-NaCl", "R-NaF"]
sales3 = ["R-Free", "R-TBAA", "R-TMABS", "R-TMAB", "R-TMAC", "R-TMAF", "R-TBAP", "R-TMAI", "R-TMAN"]


#This function is used for concatenate columns with different lenghts

def extract_data(df, lon_onda, indice):
    datos = []
    for i in indice:
        df_lon_onda = df[lon_onda]
        lista = str(i)
        df_indice = df_lon_onda.loc[lista]
        df_indice.reset_index().drop('Muestra', axis=1)
        #locals()[j] = df_indice
        datos_acomodados = []
        datos_acomodados.append(df_indice)
        datos_acomodados = np.column_stack(datos_acomodados)
        datos_acomodados = np.hstack(datos_acomodados)
        datos.append(datos_acomodados)
    datos = pd.DataFrame(datos)
    #print(datos)
    return datos
        
#This function take only lon_onda of dataframe and twist it for reindex with list of sales1
def reindex_df(df, lon_onda, new_list):
    df_lon_onda = df[lon_onda]
    df_lon_onda = df_lon_onda.reset_index()
    df_lon_onda = df_lon_onda.drop('Muestra', axis=1)
    print(df_lon_onda.T)
    df_lon_onda = df_lon_onda.T.set_index(new_list)
    return df_lon_onda

datos_incom = division_df(df, nom_receptor, lon_onda)

datos_array = extract_data(datos_incom, lon_onda, indice[0])

datos_listos = pd.DataFrame(datos_array)
datos_listos = pd.concat([datos_listos, sales1], axis=1)
datos_listos.set_index("Muestra", inplace=True)
print(datos_listos)

#
# datos_incom = []
#
# for i in indice[0]:
#
#     lista = str(i)
#
#     datos_it = df.loc[lista][lon_onda] / np.median(df[lon_onda][nom_receptor])
#
#     #datos_it_w = winsorize(datos_it, limits=[0.1, 0.1])
#

#    datos_incom.append(datos_it)
    

IC = []
for i in list(datos_listos.index):
    print(i)
    IC_95 = st.t.interval(alpha=.95, df = len(datos_listos.loc[i])-1, loc= np.mean(datos_listos.loc[i]), scale= st.sem(datos_listos.loc[i]))
    IC.append(IC_95)

IC = pd.DataFrame(IC, index=sales3)    
print(np.mean(datos_listos))
print(np.std(datos_listos))
print(IC)
datos_post = np.array(datos_array)

#%% Gráficas
fig = plt.figure()
sns.barplot(data=datos_listos, capsize = 0.2, palette="deep")
sns.stripplot(data=datos_listos, size=4, color=".3", linewidth=0)
plt.ylim(0,)
plt.show()

fig_2 = plt.figure()
sns.boxplot(data=datos_listos, palette="deep")
sns.stripplot(data=datos_listos, size=4, color=".3", linewidth=0)
plt.show()

#%% Kruskal-Wallis H-test
from scipy.stats import kruskal

# comparacion de muestras
stat, p = kruskal(datos_listos.iloc[:,0],datos_listos.iloc[:,1], datos_listos.iloc[:,2],\
                  datos_listos.iloc[:,3], datos_listos.iloc[:,4], datos_listos.iloc[:,5],\
                  datos_listos.iloc[:,6], datos_listos.iloc[:,7], datos_listos.iloc[:,8])
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
	print('Same distributions (fail to reject H0)')
else:
	print('Different distributions (reject H0)')
    
stats = pd.DataFrame([[stat], [p]], index=["Kruskal-Wallis", "Valor_P"])

#%% Correr Dunn's test usando correccion de Bonferonni o holm-sidak para los valores p (p-values)
import scikit_posthocs as sp
post = sp.posthoc_dunn(datos_post, p_adjust = 'fdr_tsbh')
post = np.array(post)
p_post = pd.DataFrame(post, index = sales3, columns=sales3)
print(p_post)

def bold(x):
    if x <= alpha:
        color = "red"
    else:
        color = 'black'
    return 'color: %s' % color

p_post = p_post.style.applymap(bold)
stats = stats.style.applymap(bold)

#%% Se prepara el archivo de salida
    
#with pd.ExcelWriter(archivo, mode="a", if_sheet_exists='replace') as writer:
#    stats.to_excel(writer, sheet_name="Kruskal-Wallis", index_label = ["Estadistico"])
#    p_post.to_excel(writer, sheet_name="Prueba_Dunn_Bonferroni")
#    datos_listos.to_excel(writer, sheet_name= "datos_listos", index_label = [lon_onda])
