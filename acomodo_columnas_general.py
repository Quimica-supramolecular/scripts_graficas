import pandas as pd
import numpy as np
import scipy.stats as st

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

dataframe = read_file(filename, sheet_name="datos_ajustados")

lon_onda = str(input("Ingrese longitud de onda: "))
df = pd.DataFrame(dataframe[lon_onda])
print(df)

#This function agroup iteratively dataframe by index name and return a numpy array with columns with diferent lenghts
#and perform ANOVA test with columns
indice = pd.DataFrame(list(dataframe.index))
indice = pd.DataFrame(indice.drop_duplicates())

def agrupar_columnas_iterativo(dataframe, indice):
    datos_t = []
    for i in indice[0]:
        lista = str(i)
        datos = []
        df = dataframe.loc[lista]
        df = datos.append(df)
        datos = np.column_stack(datos)
        datos = np.hstack(datos)
        datos_t.append(datos)
    return pd.DataFrame(datos_t)

datos_agrupados = agrupar_columnas_iterativo(df, indice)
#print(pd.DataFrame(datos_agrupados))

indice_i = pd.DataFrame(indice.values, columns=["Muestra"])
datos_agrupados = pd.concat([datos_agrupados, indice_i], axis=1)
datos_agrupados = datos_agrupados.set_index("Muestra")
print(datos_agrupados)

sales1 = ["R-Free", "R-TBAA", "R-TMABS", "R-TMAB", "R-TMAC", "R-TMAF", "R-TBAP", "R-TMAI", "R-TMAN"]
#sales1 = ["R-Free", "R-KCl", "R-KI", "R-LiCl","R-Na2HPO4","R-Na2SO4", "R-NaCH3CO2","R-NaCl", "R-NaF"]
sales = ["R-Free", "R-TMAC", "R-TMAN", "R-TMABS", "R-TMAI", "R-TMAB", "R-TMAF", "R-TBAP", "R-TBAA"]
#sales = ["R-Free", "R-NaCH3CO2", "R-LiCl", "R-Na2SO4", "R-NaF", "R-Na2HPO4", "R-KI", "R-KCl", "R-NaCl"]

serie = list(indice_i["Muestra"])
nom_receptor = serie[0]

IC = []
for i in serie:
    d = datos_agrupados.loc[i].dropna(axis=0)
    IC_95 = st.t.interval(alpha=0.95, df = len(d)-1, loc= np.mean(d), scale= st.sem(d))
    IC.append(IC_95)

IC = pd.DataFrame(IC, index=sales1) 
promedio = np.mean(datos_agrupados, axis=1)
DE = np.std(datos_agrupados, axis=1)
m_dispersion = np.array([promedio, DE, IC[0], IC[1]], dtype=object)
m_dispersion = pd.DataFrame(m_dispersion.T, index=sales1, columns=["promedio", "DE", "IC_i", "IC_s"])
datos_dispersion = m_dispersion.reindex(sales)
print(datos_dispersion)

     
libro = str(input("¿Quieres crear el libro .xlsx: "))
if libro == "y":
    data_null = {}
    df_null = pd.DataFrame(data_null)
    df_null.to_excel("Cualitativo_DMSO.xlsx", index = False)
    
    with pd.ExcelWriter("Cualitativo_DMSO.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
         datos_dispersion.to_excel(writer, sheet_name=nom_receptor)

else:
    with pd.ExcelWriter("Cualitativo_DMSO.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
         datos_dispersion.to_excel(writer, sheet_name=nom_receptor)
   
