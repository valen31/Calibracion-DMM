# Se importa esta biblioteca para la creación de la interfaz del programa
import tkinter as tk
# Se importa esta biblioteca para la estimación de incertidumbres
import numpy as np


# Se crea la función que ejecuta el método Monte Carlo para la estimación de incertidumbres del error de indicación del DMM
def DMM_MC(promedio,senal, resolucion, correccion, porcentaje, numdigitos, incertidumbre,desv):
    
    Indicacion = promedio #promedio de las 5 lecturas realizadas con el DMM
    DesvEst = desv #desviación estándar experimental de las 5 lecturas realizadas con el DMM

    Calibrador = senal #valor nominal de la señal de referencia
    CorreccionCert = correccion #corrección por calibración certificada del calibrador
    ValorRef = Calibrador + CorreccionCert #valor de la señal de referencia corregido

    Res = resolucion #resolución del rango de medida del DMM
    EMP = ((porcentaje/100)*Indicacion + numdigitos)/3 #estimación del error máximo permitido del calibrador
    Cal = incertidumbre #incertidumbre expandida certificada de la corrección por calibración del calibrador

    iter = 1000000 #número de iteraciones del Monte Carlo

    # Fuentes de incertidumbre de la indicación del DMM
    ures = np.random.uniform(-Res/2, Res/2, iter) #distribución de probabilidad de la incertidumbre por resolución
    ures0 = np.random.uniform(-Res/2, Res/2, iter) #distribución de probabilidad de la incertidumbre por resolución del cero
    urep = np.random.normal(0, DesvEst/np.sqrt(5), iter) #distribución de probabilidad de la incertidumbre por repetibilidad

    # Fuentes de incertidumbre de la indicación de referencia
    uemp = np.random.uniform(2*-EMP, 2*EMP, iter) #distribución de probabilidad de la incertidumbre por error máximo permitido del calibrador
    uder = np.random.uniform(-0.7*EMP, 0.7*EMP, iter) #distribución de probabilidad de la incertidumbre por deriva del calibrador
    ucal = np.random.normal(0, Cal/2, iter) #distribución de probabilidad de la incertidumbre por calibración del calibrador

    # Definición del modelo de la indicación del DMM
    Iix = Indicacion + ures + ures0 + urep
    
    # Definición del modelo de la indicación de referencia
    if CorreccionCert == 0:
        Iref = ValorRef + uemp + uder #Esta expresión se utiliza cuando no hay trazabilidad metrológica del patrón.
    else:
        Iref = ValorRef + ucal + uder #Esta expresión se utiliza cuando sí existe certificado de calibración vigente del calibrador.


    # Definición del modelo del mensurando
    E = Iix - Iref 

    #Variables de salida
    error_indicacion = round(np.mean(E),8) #error de indicación del DMM
    incertidumbre_estandar = round(np.std(E),8) #incertidumbre estándar del error de indicación del DMM
    incertidumbre_expandida = round(2*incertidumbre_estandar,8) #incertidumbre expandida del error de indicación del DMM para un factor de cobertura k=2
    intervalo = [-incertidumbre_expandida, incertidumbre_expandida] #intervalo de cobertura del error de indicación del DMM para una probabilidad del 95,45%


    return error_indicacion, incertidumbre_estandar, intervalo


# Se crea la función que extrae los valores ingresados en la interfaz y muestra los resultados de las variables de salida
def interfaz():
    #Se extraen las 5 lecturas del DMM
    lectura1=float(lect_1.get())
    lectura2=float(lect_2.get())
    lectura3=float(lect_3.get())
    lectura4=float(lect_4.get())
    lectura5=float(lect_5.get())
    lecturas = np.array([lectura1, lectura2, lectura3, lectura4, lectura5])
    
    promedio=np.mean(lecturas) #promedio de lecturas
    desv=np.std(lecturas) #desviación estándar experimental de lecturas

    
    senal=float(sen.get()) #Se extrae el valor nominal de la señal de referencia
    resolucion=float(resol.get()) #Se extrae la resolución del rango de medida del DMM
    correccion=float(corr.get()) #Se extrae la corrección por calibración del calibrador certificada
    porcentaje=float(perout.get()) #Se extrae el porcentaje del output de la señal del calibrador para la estimación del EMP
    numdigitos=float(dig.get()) #Se extrae el número de dígitos de la señal del calibrador para la estimación del EMP
    incertidumbre=float(incer.get()) #Se extrae la incertidumbre expandida de la corrección por calibración del calibrador certificada
    
    #Se llama a la función que ejecuta el método Monte Carlos
    error_indicacion, incertidumbre_estandar, intervalo = DMM_MC(promedio,senal, resolucion, correccion, porcentaje, numdigitos, incertidumbre,desv)

    prom["text"] = str(promedio) #Se muestra el promedio de lecturas
    prom_lbl["text"] = "Promedio:"
    error["text"] = str(error_indicacion) #Se muestra el error de indicación del DMM
    incer_est["text"] =  str(incertidumbre_estandar) #Se muestra la incertidumbre estándar del error de indicación del DMM
    intervalo_str = [str(valor) for valor in intervalo] #Se muestra el intervalo de cobertura del error de indicación del DMM para una probabilidad del 95,45%
    inter["text"] = "["+', '.join(intervalo_str)+"]"


#----- Interfaz -----#
window=tk.Tk()
window.title("DMM MC")
window.geometry("750x500")
window.resizable(width=False, height=False)
window['background']='#FFFFFF'

tit = tk.Label(window,text="Estimación de Incertidumbres de Calibración \n de Multimetros Digitales por MC",font=("Helvetica", 11, "bold"))
tit.config(bg="white")
#tit.pack(side=tk.TOP)
tit.place(x=230,y=0)

#Lecturas Título
lbl_0 = tk.Label(window, text="Indicación Promedio de DMM", font=("Helvetica", 9, "bold"))
lbl_0.config(bg="white")
lbl_0.place(x=10, y=50)

#Lectura 1
lect_lbl_1 = tk.Label(window, text="Lectura 1:",font=("Helvetica", 9))
lect_lbl_1.place(x=10, y=80)
lect_lbl_1.config(bg="white")

lect_1 = tk.Entry(window, width=10,font=("Helvetica", 9))
lect_1.config(bg="AliceBlue")
lect_1.place(x=70, y=80)

#Lectura 2
lect_lbl_2 = tk.Label(window, text="Lectura 2:",font=("Helvetica", 9))
lect_lbl_2.place(x=10, y=110)
lect_lbl_2.config(bg="white")

lect_2 = tk.Entry(window, width=10,font=("Helvetica", 9))
lect_2.config(bg="AliceBlue")
lect_2.place(x=70, y=110)

#Lectura 3
lect_lbl_3 = tk.Label(window, text="Lectura 3:",font=("Helvetica", 9))
lect_lbl_3.place(x=10, y=140)
lect_lbl_3.config(bg="white")

lect_3 = tk.Entry(window, width=10,font=("Helvetica", 9))
lect_3.config(bg="AliceBlue")
lect_3.place(x=70, y=140)

#Lectura 4
lect_lbl_4 = tk.Label(window, text="Lectura 4:",font=("Helvetica", 9))
lect_lbl_4.place(x=10, y=170)
lect_lbl_4.config(bg="white")

lect_4 = tk.Entry(window, width=10,font=("Helvetica", 9))
lect_4.config(bg="AliceBlue")
lect_4.place(x=70, y=170)

#Lectura 5
lectt_lbl_5 = tk.Label(window, text="Lectura 5:",font=("Helvetica", 9))
lectt_lbl_5.place(x=10, y=200)
lectt_lbl_5.config(bg="white")

lect_5 = tk.Entry(window, width=10,font=("Helvetica", 9))
lect_5.config(bg="AliceBlue")
lect_5.place(x=70, y=200)


#Señal de Referencia
sen_lbl = tk.Label(window, text="Señal de referencia del calibrador:",font=("Helvetica", 9))
sen_lbl.place(x=260, y=80)
sen_lbl.config(bg="white")

sen = tk.Entry(window, width=10,font=("Helvetica", 9))
sen.config(bg="AliceBlue")
sen.place(x=450, y=80)

#Resolución del rango de medida del DMM
resol_lbl = tk.Label(window, text="Resolución del rango de medida \n del DMM:",font=("Helvetica", 9))
resol_lbl.place(x=260, y=120)
resol_lbl.config(bg="white")

resol = tk.Entry(window, width=10,font=("Helvetica", 9))
resol.config(bg="AliceBlue")
resol.place(x=450, y=120)

#Corrección por calibración del calibrador
corr_lbl = tk.Label(window, text="Corrección por calibración del calibrador:",font=("Helvetica", 9))
corr_lbl.place(x=255, y=160)
corr_lbl.config(bg="white")

corr = tk.Entry(window, width=10,font=("Helvetica", 9))
corr.config(bg="AliceBlue")
corr.place(x=450, y=160)

#Incertidumbre expandida de la corrección por calibración del calibrador
incer_lbl = tk.Label(window, text="Incertidumbre expandida de la corrección \n por calibración del calibrador:",font=("Helvetica", 9))
incer_lbl.place(x=250, y=200)
incer_lbl.config(bg="white")

incer = tk.Entry(window, width=10,font=("Helvetica", 9))
incer.config(bg="AliceBlue")
incer.place(x=450, y=205)

#EMP del calibrador
emp_lbl = tk.Label(window, text="EMP del calibrador", font=("Helvetica", 9, "bold"))
emp_lbl.config(bg="white")
emp_lbl.place(x=625, y=50)

# %output
perout_lbl = tk.Label(window, text="% output:",font=("Helvetica", 9))
perout_lbl.place(x=625, y=80)
perout_lbl.config(bg="white")

perout = tk.Entry(window, width=7,font=("Helvetica", 9))
perout.config(bg="AliceBlue")
perout.place(x=680, y=80)

#número de dígitos
dig_lbl = tk.Label(window, text="# digitos:",font=("Helvetica", 9))
dig_lbl.place(x=625, y=120)
dig_lbl.config(bg="white")

dig = tk.Entry(window, width=7,font=("Helvetica", 9))
dig.config(bg="AliceBlue")
dig.place(x=680, y=120)


#Botón de cálculo
boton = tk.Button(window,text="Calcular", font=("Helvetica", 11, "bold"),command=interfaz)
boton.config(bg="AliceBlue")
boton.place(x=340, y=455)

#----------RESULTADOS---------#
#Promedio de lecturas del DMM
prom = tk.Label(window)
prom.place(x=80, y=235)
prom.config(bg="white")

prom_lbl = tk.Label(window,font=("Helvetica", 9, "bold"))
prom_lbl.place(x=15, y=235)
prom_lbl.config(bg="white")

#Error de indicación del DMM
error = tk.Label(window,font=("Helvetica", 9))
error.place(x=140, y=290)
error.config(bg="white")

error_lbl = tk.Label(window,text="Error de indicación: ",font=("Helvetica", 9, "bold"))
error_lbl.place(x=20, y=290)
error_lbl.config(bg="white")

#Incertidumbre estándar del error de indicación del DMM
incer_est = tk.Label(window,font=("Helvetica", 9))
incer_est.place(x=295, y=340)
incer_est.config(bg="white")

incer_lbl = tk.Label(window,text="Incertidumbre estándar del error de indicación: ",font=("Helvetica", 9, "bold"))
incer_lbl.place(x=20, y=340)
incer_lbl.config(bg="white")

#Intervalo de conbertura del error de indicación del DMM
inter = tk.Label(window,font=("Helvetica", 9))
inter.place(x=295, y=405)
inter.config(bg="white")

inter_lbl = tk.Label(window,text="Intervalo de confianza del error de indicación \n para una probabilidad de cobertura del 95,45%:",font=("Helvetica", 9, "bold"))
inter_lbl.place(x=15, y=390)
inter_lbl.config(bg="white")

window.mainloop()
