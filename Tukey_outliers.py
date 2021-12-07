# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 19:40:15 2021

@author: jan_c
"""

import pandas as pd
from tkinter import *
from tkinter import filedialog
import seaborn as sns
import matplotlib.pyplot as plt


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
    indice = indice.drop_duplicates()
    df = df.loc["MACFHX"]
    print(df)
    print(indice)
    
    #Tukey's method
    def tukeys_method(df, variable):
        #Takes two parameters: dataframe & variable of interest as string
        q1 = df[variable].quantile(0.25)
        q3 = df[variable].quantile(0.75)
        iqr = q3-q1
        inner_fence = 1.5*iqr
        outer_fence = 3*iqr
        
        #inner fence lower and upper end
        inner_fence_le = q1-inner_fence
        inner_fence_ue = q3+inner_fence
        
        #outer fence lower and upper end
        outer_fence_le = q1-outer_fence
        outer_fence_ue = q3+outer_fence
        
        outliers_prob = []
        outliers_poss = []
        for index, x in enumerate(df[variable]):
            if x <= outer_fence_le or x >= outer_fence_ue:
                outliers_prob.append(index)
        for index, x in enumerate(df[variable]):
            if x <= inner_fence_le or x >= inner_fence_ue:
                outliers_poss.append(index)
        return outliers_prob, outliers_poss
            
    probable_outliers_tm, possible_outliers_tm = tukeys_method(df, "370nm")
    print(probable_outliers_tm)
    print(possible_outliers_tm)
    
    