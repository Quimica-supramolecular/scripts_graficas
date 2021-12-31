#Algoritm of Gamp 

from autograd.differential_operators import jacobian
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from autograd import elementwise_grad as egrad 
from autograd import grad

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

def read_file(filename, sheet_name, index_col):
    data = pd.read_excel(filename, sheet_name= sheet_name, header=0, index_col=index_col)
    return data 

df_spec = read_file(filename,"datos_titulacion", 0)
df_conc = read_file(filename,"conc", None)

C_T = df_conc#[:,0:-1] 
G = C_T.iloc[:,1]
H = C_T.iloc[:,0]
nc = len(C_T)
nw = len(df_spec)

u, s, v = np.linalg.svd(df_spec, full_matrices=False)

plt.plot(range(0, nc), np.log10(s), "o")
plt.ylabel("log(EV)")
plt.xlabel("# de autovalores")
plt.show()

EV = int(input("¿Cuantos autovalores incluirá en el cálculo?: ", ))

Y = u[:,0:EV] @ np.diag(s[0:EV:]) @ v[0:EV:]

# =============================================================================
# plt.plot(range(0, nw), u[:,0:EV])
# plt.ylabel("Matriz U de SVD")
# plt.xlabel("# de autovalores")
# plt.show()
# =============================================================================

#EFA fijo
 
L = range(1,(nc + 1), 1)
L2 = range(0, nc, 1)

X = []
for i in L:
    uj, sj, vj = np.linalg.svd(df_spec.T.iloc[:i,:], full_matrices=False)
    X.append(sj**2)

ev_s = pd.DataFrame(X)
ev_s0 = np.array(ev_s)

X2 = []
for i in L2:
    ui, si, vi = np.linalg.svd(df_spec.T.iloc[i:,:], full_matrices=False)
    X2.append(si**2)

ev_s1 = pd.DataFrame(X2)
ev_s10 = np.array(ev_s1) 

plt.figure()
plt.plot(G, np.log10(ev_s0), "k-o")
plt.plot(G, np.log10(ev_s10), "b:o")
plt.ylabel("log(EV)")
plt.xlabel("[G], M")
plt.show()
    
C1 = (ev_s.iloc[:,0:EV]).fillna(0)
C2 = (ev_s1.iloc[:,0:EV]).fillna(0) 
 
EFA0 = []
for i in range(0, EV):
    EFA1 = np.array([C1.iloc[:,i], C2.iloc[:,-1-i]]) 
    EFA2 = np.min(EFA1, 0)
    EFA0.append(EFA2)
    
EFA = np.array(EFA0) 

plt.plot(G, EFA.T, ":o")
plt.show()

print("\n Escriba la tolerancia para separar los autovalores del ruido. Para obtener el valor por default escriba 0", end="")
tolerancia = float(input("¿Cual es el nivel de tolerancia deseada?: ", ))
if tolerancia == 0:
    tolerancia = 0.25

EFA = np.log10(abs(EFA / EFA[EFA != 0].min())) - tolerancia

c_e = EFA / EFA.max()
c_e[c_e < 0] = 0

C = c_e * max(H)

plt.plot(G, C.T, ":o")
plt.ylabel("[H_libre], M")
plt.xlabel("[G], M")
plt.show()

n_K = EV - 1

if n_K == 1:
    k_e = float(input("Indique un valor estimado para la constante de asociación: ",))
else:
    k_e = []
    for i in range(n_K):
        print("K" + str(i+1) + ":", end="")
        i = float(input("Indique un valor estimado para esta constante de asociación: ",))
        k_e.append(i)

k_p = np.array(k_e)
k_u = np.array([1, 1])
A = (np.linalg.pinv(C.T) @ Y.T) 

C_t = np.concatenate((C_T, C.T), axis=1) 
model = np.array([[1, 0, 1, 1],[0,1,1,2]])

def el_finito(fun, x):       
        dfdx = []
        delta = 1e-20
        for i in range(len(x)):
            step = np.zeros(len(x), dtype=complex)
            step[i] = complex(0, delta)
            dfdx.append(np.imag(fun(x + step)) / delta)
        return np.array(dfdx)
    
def conteo(lista, u_lista):
    cont = 0
    for ele in lista: 
        if (ele == u_lista): 
            cont = cont + 1
    return cont

def multiply(L):
    new_list = []
    for i in range(len(L)):
        if i == 0:
            new_list.append(L[i])
        else:
            new_list.append(L[i] * new_list[i-1])
    return np.array(new_list)

def fun_obj(g, h):
    f = abs(H - h) + abs(G - g)
    return f

def g_free(C, args = (k_e, G)):
    g_f = []
    for m in range(1, len(k_e)+1):
        g_st = m * C[:,m]
        g_st += g_st
        g_f.append(g_st.T)
    g_f = G - np.sum(np.array(g_f), axis=0)
    return np.array(g_f)

def c_complex(K, C, args = (H, G)):
    g = g_free(C)
    hg_p = []
    for z in range(1, len(K)+1):
        hg = multiply(K[0:z])[-1] * g**z * C[:,0]
        hg += hg
        hg_p.append(hg.T)

    hg_p = np.array(hg_p)
    h_f = np.array(H - np.sum(hg_p, axis=0))
    c = np.column_stack((h_f, hg_p.T))
    C = np.array(c)        
    return C

def loss(K, C):
    g = g_free(C)
    c_0 = c_complex(K, C)
    h = np.sum(c_0, axis= 1)
    f = fun_obj(g, h)
    C = c_0
    return f, c_0

f, c_0 = loss(k_e, C.T)

#C_cal = c_complex(k_e, C.T, H, G)

plt.plot(G, c_0, ":o")
plt.show()

