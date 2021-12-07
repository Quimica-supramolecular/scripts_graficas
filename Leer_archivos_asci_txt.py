#This code open a window to search local file and return the file name
def open_file():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    file_name = filedialog.askopenfilename()
    return file_name

#This function read .asci and .txt files using astropy and pandas and return a dataframe
def read_file(file_name):
    import pandas as pd
    import astropy.io.ascii as ascii
    import astropy.table as table
    data = ascii.read(file_name, data_start=25)
    data = pd.DataFrame(data.as_array())
    return data

df = read_file(open_file())
#df_1 = read_file(open_file())

#plot the dataframe
import matplotlib.pyplot as plt

plt.plot(df.iloc[:,0],df.iloc[:,1])
plt.xlim(max(df.iloc[:,0]), min(df.iloc[:,0]))
#plt.plot(df_1.iloc[:,0],df_1.iloc[:,1])
#plt.xlim(max(df.iloc[:,0]), min(df.iloc[:,0]))
plt.show()