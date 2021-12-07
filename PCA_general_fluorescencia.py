
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import savgol_filter
from sklearn.decomposition import PCA as sk_pca
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.cluster import KMeans

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
    data = pd.read_excel(filename, sheet_name= sheet_name, header=0)
    return data 


df_0 = read_file(filename, sheet_name="Hoja5")

print(df_0)

# The first column of the Data Frame contains the labels
lab = df_0.iloc[:,0] #.astype('uint8') 
 
# Read the features (scans) and transform data from reflectance to absorbance
feat = np.array(df_0.values[:,2:]).astype('float32') #np.log(1.0/(df_0.values[:,2:]).astype('float32'))
print(feat)
 
# Calculate first derivative applying a Savitzky-Golay filter
dfeat = savgol_filter(feat, len(feat.T), polyorder = 5, deriv=1)

# Initialise
skpca1 = sk_pca(n_components=10)
skpca2 = sk_pca(n_components=10)
 
# Scale the features to have zero mean and standard devisation of 1
# This is important when correlating data with very different variances
nfeat1 = StandardScaler().fit_transform(feat)
nfeat2 = StandardScaler().fit_transform(dfeat)
 
# Fit the spectral data and extract the explained variance ratio
X1 = skpca1.fit(nfeat1)
expl_var_1 = X1.explained_variance_ratio_
 
# Fit the first data and extract the explained variance ratio
X2 = skpca2.fit(nfeat2)
expl_var_2 = X2.explained_variance_ratio_
 
# Plot data
with plt.style.context(('ggplot')):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9,6))
    fig.set_tight_layout(True)
 
    ax1.plot(expl_var_1,'-o', label="Explained Variance %")
    ax1.plot(np.cumsum(expl_var_1),'-o', label = 'Cumulative variance %')
    ax1.set_xlabel("PC number")
    ax1.set_title('Absorbance data')
 
    ax2.plot(expl_var_2,'-o', label="Explained Variance %")
    ax2.plot(np.cumsum(expl_var_2),'-o', label = 'Cumulative variance %')
    ax2.set_xlabel("PC number")
    ax2.set_title('First derivative data')
 
    plt.legend()
    plt.show()


skpca2 = sk_pca(n_components=4)
 
# Transform on the scaled features
Xt2 = skpca2.fit_transform(nfeat2)

# Define the labels for the plot legend
#labplot = ["0/8 Milk","1/8 Milk","2/8 Milk", "3/8 Milk", \
#"4/8 Milk", "5/8 Milk","6/8 Milk","7/8 Milk", "8/8 Milk"]

labplot = df_0.iloc[:,0].tolist() #.drop_duplicates()
 
# Scatter plot
unique = list(set(labplot))
#colors = [plt.cm.jet(float(i)/max(unique)) for i in unique]
with plt.style.context(('ggplot')):
    for i, u in enumerate(unique):
        #col = np.expand_dims(np.array(colors[i]), axis=0)
        xi = [Xt2[j,0] for j in range(len(Xt2[:,0])) if lab[j] == u]
        yi = [Xt2[j,1] for j in range(len(Xt2[:,1])) if lab[j] == u]
        plt.scatter(xi, yi,  s=60, edgecolors='k',label=str(u)) #c=col,
 
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.legend(labplot,loc='lower right')
    plt.title('Principal Component Analysis')
    plt.show()