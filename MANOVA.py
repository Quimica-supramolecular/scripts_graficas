import pandas as pd
from statsmodels.multivariate.manova import MANOVA
from statsmodels.stats.multicomp import pairwise_tukeyhsd

datos = pd.read_excel('Datos_de_salida.xlsx', 'datos_totales')
#print(datos)
datos = pd.DataFrame(datos)

datos.set_index("Muestra")
indices = pd.DataFrame(datos.columns).values.astype(str) # convertimos los valores a texto
#indices = indices[1:] # separamos la columna "Muestra"

#%% Este ciclo separa el texto deseado usando indicadores entre corchetes
nuevos_nombres = list()
for i in indices:
    a = i[-1]
    d_r = 'f_' + (a[-6:-1])
    nuevos_nombres.append(d_r)

print(nuevos_nombres)

datos_0 = datos.set_axis(nuevos_nombres, axis = 1)

maov = MANOVA.from_formula('f_361nm + f_362nm + f_363nm + f_364nm + f_365nm +\
                    f_392nm + f_393nm + f_394nm + f_395nm + f_396nm + f_419nm +\
                    f_420nm + f_421nm + f_422nm + f_423nm + f_472nm + f_473nm +\
                    f_474nm + f_475nm + f_476nm ~ f_uestr', data=datos_0)

print(maov.mv_test())

mc = pairwise_tukeyhsd(datos_0['f_363nm'], datos_0['f_uestr'])

print(mc)
