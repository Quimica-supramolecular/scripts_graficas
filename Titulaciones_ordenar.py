import pandas as pd
from tkinter import *
from tkinter import filedialog


# Obtencion y acomod de datos

# This function opern window to open several excel files and return a list of names of the files
def get_files():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("Excel files","*.xlsx"),("all files","*.*")))
    root.destroy()
    return root.filename

frame = get_files()
#print(frame)

# This function is for obtain index list from datos_generales without no duplicates
def get_index_list(dataframe):
    index_list = dataframe.index.tolist()
    index_list = list(dict.fromkeys(index_list))
    return index_list

nombre = str(input("Escrba el nombre del complejo: "))

datos_generales = pd.DataFrame([])
dg_promedio = pd.DataFrame([])
for i in frame:
    j = 0
    globals()["df_"+str(j)] = pd.read_excel(i, sheet_name="datos_generales", header=0, index_col=0)
    datos_generales = datos_generales.append(globals()["df_"+str(j)].loc[nombre,].dropna(1))
    dg_promedio = dg_promedio.append(globals()["df_"+str(j)].loc[nombre,].dropna(1).mean(axis=0), ignore_index=True)
    print(datos_generales)
    print("promedio: ", dg_promedio)
    j = j + 1

with pd.ExcelWriter(nombre +'_tit_DMSO.xlsx') as writer:
    datos_generales.to_excel(writer, sheet_name='datos_generales')
    dg_promedio.to_excel(writer, sheet_name='datos_promedio')
    