# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 15:19:46 2021

@author: jan_c
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import filedialog

from seaborn.rcmod import axes_style

# Obtencion y acomod de datos

# This function opern window to open several excel files and return a list of names of the files
def get_files():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("Excel files","*.xlsx"),("all files","*.*")))
    root.destroy()
    return root.filename

frame = get_files()
#lon_onda = ["368nm", '363nm', '365nm', '363nm', '430nm', '430nm', '423nm', '363nm', '425nm', '363nm', '428nm', '435nm']

sales1 = ["R-Free", "R-KCl", "R-KI", "R-LiCl","R-Na2HPO4","R-Na2SO4", "R-NaCH3CO2","R-NaCl", "R-NaF"]
sales = ["R-Free", "R-NaCH3CO2", "R-LiCl", "R-Na2SO4", "R-NaF", "R-Na2HPO4", "R-KI", "R-KCl", "R-NaCl"]
sales2 = ["R-Free", "R-NaCH$_3$CO$_2$", "R-LiCl", "R-Na$_2$SO$_4$", "R-NaF", "R-Na$_2$HPO$_4$", "R-KI", "R-KCl", "R-NaCl"]

for i, j in zip(frame, range(1, len(frame)+1)):
    globals()['df_%s' % j] = pd.read_excel(i, sheet_name="datos_agrupados", header=0, index_col=0).set_axis(sales1, axis=1, inplace=False)
    globals()['df_%s' % j] = globals()['df_%s' % j].T.reindex(sales)
    globals()['df_%s' % j] = globals()['df_%s' % j].T
    print(globals()['df_%s' % j])


masy = {"label": "masy ($\lambda_{em} = 370 nm$)"}
masz = {"label": "masz ($\lambda_{em} = 363 nm$)"}
maly = {"label": "maly ($\lambda_{em} = 365 nm$)"}
malz = {"label": "malz ($\lambda_{em} = 363 nm$)"}
mbsy = {"label": "mbsy ($\lambda_{em} = 430 nm$)"}
mbly = {"label": "mbly ($\lambda_{em} = 430 nm$)"}
wasy = {"label": "wasy ($\lambda_{em} = 410 nm$)"}
wasz = {"label": "wasz ($\lambda_{em} = 363 nm$)"}
waly = {"label": "waly ($\lambda_{em} = 425 nm$)"}
walz = {"label": "walz ($\lambda_{em} = 363 nm$)"}
wbsy = {"label": "wbsy ($\lambda_{em} = 428 nm$)"}
wbly = {"label": "wbly ($\lambda_{em} = 435 nm$)"}

alpha = {"alpha":0.7}

fig2=plt.figure(tight_layout=True)
fig2.suptitle("Fluorescence of receptors on solid-phase with tetraalkylammonium salts in DMSO:Water 95:5 (v/v)", size=15)

axes=fig2.subplots(3,4, sharex=True, sharey=True)
sns.set_theme(style="white") #"whitegrid"

sns.barplot(ax = axes[0,0], data=df_1, palette="deep", ci=95, capsize=.2, errwidth=1.5, **masy)
axes[0,0].set_ylim(0,1.7)
sns.stripplot(ax = axes[0,0], data=df_1, size=2, color=".3", linewidth=0, **alpha)
#axes[0,0].legend(["R = masy"], loc='upper right')
axes[0,0].annotate("R = masy", xy=(0.1,1.5))
axes[0,0].set_xticklabels(sales2)

sns.barplot(ax = axes[0,1], data=df_2, palette="deep", ci=95, capsize=.2, errwidth=1.5, **masz)
axes[0,1].set_ylim(0,1.7)
sns.stripplot(ax = axes[0,1], data=df_2, size=2, color=".3", linewidth=0, **alpha)
#axes[0,1].legend(["R = masz"], loc='upper right')
axes[0,1].annotate("R = masz", xy=(0.1,1.5))
axes[0,1].set_xticklabels(sales2)

sns.barplot(ax = axes[0,2], data=df_3, palette="deep", ci=95, capsize=.2, errwidth=1.5, **maly)
axes[0,2].set_ylim(0,1.7)
sns.stripplot(ax = axes[0,2], data=df_3, size=2, color=".3", linewidth=0, **alpha)
#axes[0,2].legend(["R = maly"],loc='upper right')
axes[0,2].annotate("R = maly", xy=(0.1,1.5))
axes[0,2].set_xticklabels(sales2)

sns.barplot(ax = axes[0,3], data=df_4, palette="deep", ci=95, capsize=.2, errwidth=1.5, **malz)
axes[0,3].set_ylim(0,1.7)
sns.stripplot(ax = axes[0,3], data=df_4, size=2, color=".3", linewidth=0, **alpha)
#axes[0,3].legend(["R = malz"], loc='upper right')
axes[0,3].annotate("R = malz", xy=(0.1,1.5))
axes[0,3].set_xticklabels(sales2)

sns.barplot(ax = axes[1,0], data=df_5, palette="deep", ci=95, capsize=.2, errwidth=1.5, **mbsy)
axes[1,0].set_ylim(0,1.7)
sns.stripplot(ax = axes[1,0], data=df_5, size=2, color=".3", linewidth=0, **alpha)
#axes[1,0].legend(["R = mbsy"], loc='upper right')
axes[1,0].annotate("R = mbsy", xy=(0.1,1.5))
axes[1,0].set_xticklabels(sales2)

axes[1,0].set_ylabel("Fluorescence (F/F$_{max\;of\;receptor}$)", size='x-large')
sns.barplot(ax = axes[1,1], data=df_6, palette="deep", ci=95, capsize=.2, errwidth=1.5, **mbly)
axes[1,1].set_ylim(0,1.7)
sns.stripplot(ax = axes[1,1], data=df_6, size=2, color=".3", linewidth=0, **alpha)
#axes[1,1].legend(["R = mbly"], loc='upper right')
axes[1,1].annotate("R = mbly", xy=(0.1,1.5))
axes[1,1].set_xticklabels(sales2)

sns.barplot(ax = axes[1,2], data=df_7, palette="deep", ci=95, capsize=.2, errwidth=1.5, **wasy)
axes[1,2].set_ylim(0,1.7)
sns.stripplot(ax = axes[1,2], data=df_7, size=2, color=".3", linewidth=0, **alpha)
#axes[1,2].legend(["R = wasy"], loc='upper right')
axes[1,2].annotate("R = wasy", xy=(0.1,1.5))
axes[1,2].set_xticklabels(sales2)

sns.barplot(ax = axes[1,3], data=df_8, palette="deep", ci=95, capsize=.2, errwidth=1.5, **wasz)
axes[1,3].set_ylim(0,1.7)
sns.stripplot(ax = axes[1,3], data=df_8, size=2, color=".3", linewidth=0, **alpha)
#axes[1,3].legend(["R = wasz"], loc='upper right')
axes[1,3].annotate("R = wasz", xy=(0.1,1.5))
axes[1,3].set_xticklabels(sales2)

sns.barplot(ax = axes[2,0], data=df_9, palette="deep", ci=95, capsize=.2, errwidth=1.5, **waly)
axes[2,0].set_ylim(0,1.7)
sns.stripplot(ax = axes[2,0], data=df_9, size=2, color=".3", linewidth=0, **alpha)
#axes[2,0].legend(["R = waly"], loc='upper right')
axes[2,0].annotate("R = waly", xy=(0.1,1.5))
axes[2,0].set_xticklabels(sales2)

sns.barplot(ax = axes[2,1], data=df_10, palette="deep", ci=95, capsize=.2, errwidth=1.5, **walz)
axes[2,1].set_ylim(0,1.7)
sns.stripplot(ax = axes[2,1], data=df_10, size=2, color=".3", linewidth=0, **alpha)
#axes[2,1].legend(["R = walz"], loc='upper right')
axes[2,1].annotate("R = walz", xy=(0.1,1.5))
axes[2,1].set_xticklabels(sales2)

sns.barplot(ax = axes[2,2], data=df_11, palette="deep", ci=95, capsize=.2, errwidth=1.5, **wbsy)
axes[2,2].set_ylim(0,1.7)
sns.stripplot(ax = axes[2,2], data=df_11, size=2, color=".3", linewidth=0, **alpha)
#axes[2,2].legend(["R = wbsy"], loc='upper right')
axes[2,2].annotate("R = wbsy", xy=(0.1,1.5))
axes[2,2].set_xticklabels(sales2)

sns.barplot(ax = axes[2,3], data=df_12, palette="deep", ci=95, capsize=.2, errwidth=1.5, **wbly)
axes[2,3].set_ylim(0,1.7)
sns.stripplot(ax = axes[2,3], data=df_12, size=2, color=".3", linewidth=0, **alpha)
#axes[2,3].legend(["R = wbly"], loc='upper right')
axes[2,3].annotate("R = wbly", xy=(0.1,1.5))
axes[2,3].set_xticklabels(sales2)

fig2.autofmt_xdate(rotation=60)
fig2.legend(bbox_to_anchor=(0.51, -0.12), loc='lower center', ncol=3)
plt.tight_layout()
plt.show()

fig2.savefig('Grafica_cual_sns_DMSO-AGUA_FS.png', dpi=1000, bbox_inches="tight")