import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog


# Obtencion y acomod de datos

# This function opern window to open several excel files and return a list of names of the files
def get_files():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Excel files","*.xlsx"),("all files","*.*")))
    root.destroy()
    return root.filename

frame = get_files()

datos = pd.read_excel(frame, sheet_name="datos_generales", header=0, index_col=0)

def get_data(datos, start):
    tit_0 = pd.DataFrame([])
    for i in range(start, len(datos), 8):
        tit_0 = tit_0.append(datos.iloc[i:i+1,])
    return tit_0

df_ = {}
for i in range(0, 8):        
    df_[i] = get_data(datos, i)


long_onda = str(input("¿Cual es la longitud de onda?: "))

titulaion_interes = pd.concat([df_[0][long_onda],df_[1][long_onda],df_[2][long_onda],
            df_[3][long_onda],df_[4][long_onda],df_[5][long_onda],df_[6][long_onda],
            df_[7][long_onda]], axis=1, ignore_index=True)
print(titulaion_interes)

with pd.ExcelWriter(frame[:-14] +'_tit_sort_DMSO.xlsx') as writer:
    df_[0].to_excel(writer, sheet_name='df_0')
    df_[1].to_excel(writer, sheet_name='df_1')
    df_[2].to_excel(writer, sheet_name='df_2')
    df_[3].to_excel(writer, sheet_name='df_3')
    df_[4].to_excel(writer, sheet_name='df_4')
    df_[5].to_excel(writer, sheet_name='df_5')
    df_[6].to_excel(writer, sheet_name='df_6')
    df_[7].to_excel(writer, sheet_name='df_7')
    titulaion_interes.to_excel(writer, sheet_name='titulaion_interes')


plt.figure(figsize=(10,10))
plt.plot(range(0,8), df_[0], ':o')
plt.plot(range(0,8), df_[1], ':o')
plt.plot(range(0,8), df_[2], ':o')
plt.plot(range(0,8), df_[3], ':o')
plt.plot(range(0,8), df_[4], ':o')
plt.plot(range(0,8), df_[5], ':o')
plt.plot(range(0,8), df_[6], ':o')
plt.plot(range(0,8), df_[7], ':o')
plt.show()
