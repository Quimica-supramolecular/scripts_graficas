from tkinter import *
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import astropy.io.ascii as ascii
import astropy.table as table
import xlsxwriter 
from scipy.signal import savgol_filter

# This function opern window to open several excel files and return a list of names of the files
def get_files():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("asci files","*.asc"),("all files","*.*")))
    root.destroy()
    return root.filename

frame = get_files()

lista = []
for j in range(1, len(frame)+1):
    lista.append('df_%s' % j)
        
print(lista)

dic = {}
for i, j in zip(frame, lista):
    a = ascii.read(i, data_start=54) #54, 23
    dic[j] = pd.DataFrame(a.as_array())

#df = *dataframe with identifiers for rows and dates for columns*
#for date in list_of_dates:
#    df['New Column Name'] = *a new column with a new date to be added to the df*

def add_columns(dic,lista_nombres):  
    df_0 = dic["df_1"]["col1"]
    n = 0
    for i in lista:
        c = dic[i]['col2']
        s_c = savgol_filter(c, 51, 3)
        s_c = pd.DataFrame(s_c, columns= ["df_"+ str(n)])
        df = pd.concat([df_0, s_c], axis=1)
        df_0 = df
        n += 1
    return df_0

dataframe = add_columns(dic,lista)

plt.plot(dataframe["col1"], dataframe.iloc[:,2:-1])
plt.show()

#This code plot df.iloc[:,0] and df.iloc[:,1] to every df_i
#df.iloc[:,0] is the wavelength and df.iloc[:,1] is the property
for i in lista:
    d = dic[i]
    plt.plot(d['col1'], d['col2'])
    plt.xlabel('Wavelength')
    plt.ylabel('Fluorescence')
    plt.xlim(332,600)

#archivo = str(input("Ingrese el nombre del archivo: "))
#archivo_0 = archivo + ".xlsx"

#this function open windows to save the file in xlsx format
def save_file():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("Excel files","*.xlsx"),("all files","*.*")))
    root.destroy()
    return root.filename

archivo_1 = save_file() + ".xlsx"
print(archivo_1)

with pd.ExcelWriter(archivo_1, engine='xlsxwriter') as writer:
    dataframe.to_excel(writer, sheet_name="datos_titulacion")
    

