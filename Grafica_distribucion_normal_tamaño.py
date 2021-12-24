
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
from tkinter import *
from tkinter import filedialog
from scipy.optimize import curve_fit, minimize

# Obtencion y acomod de datos

# This function opern window to open several excel files and return a list of names of the files
# This function open window for search local file .xlxs and .xlsx in directory and return filename
def open_file():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
    
    return root.filename    

frame = open_file()

datos = pd.read_excel(frame, sheet_name = 'Hoja1', header = 0)

receptores = ["masy", "masz", "maly", "malz", "mbsy", "mbly", "wasy", "wasz", "waly", "walz", "wbsy", "wbly"]

def gauss(x, xmax, width):
    G = np.exp(-np.log(2)*((x-xmax)/(width/2))**2)
    return G

def gaussian(x, mean, amplitude, standard_deviation):
    return amplitude * np.exp( - (x - mean)**2 / (2*standard_deviation ** 2))

fig = plt.figure(tight_layout=True)
axes=fig.subplots(4,3)
axes = axes.ravel()
for i, j in zip(range(12), receptores):
    bin_heights, bins, _= axes[i].hist(datos[j], bins='auto', density=False, color = "grey", alpha = 0.6, label = j, histtype='bar', rwidth=0.8)
    bin_centers = bins[:-1] + np.diff(bins) / 2
    mu, sigma = norm.fit(datos[j].dropna().unique())
    #fit_line = norm.pdf(bins, mu, sigma)
    popt, _ = curve_fit(gaussian, bin_centers, bin_heights, p0=[mu, 1., sigma])
    print('%.2f'% mu, '%.2f'% sigma)
    x_interval_for_fit = np.linspace(bins[0], bins[-1], 1000)
    axes[i].plot(x_interval_for_fit, gaussian(x_interval_for_fit, *popt), 'k:', label = "%.2f"% mu + "$\pm$" + "%.2f"% sigma)
    if axes[i] == axes[9] or axes[i] == axes[10] or axes[i] == axes[11]:
        axes[i].set_xlabel("Diameter ($\mu m$)")
    if axes[i] == axes[0] or axes[i] == axes[3] or axes[i] == axes[6] or axes[i] == axes[9]:
        axes[i].set_ylabel("Frequency")
    axes[i].legend(loc='upper right')
    axes[i].set_ylim(0, np.max(bin_heights) + (np.max(bin_heights)*0.65))
plt.show()            
