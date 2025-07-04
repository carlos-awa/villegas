

import serial, time
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot():
    x = np.random.randint(0,10,10)
    y = np.random.randint(0, 10, 10)
    ax.scatter(x,y)
    canvas.draw()

def conexion_arduino():
    arduino = serial.Serial(port='COM5', baudrate=9600)
    time.sleep(2)
    for i in range(0, 10000, 1):
        datos = arduino.readline()
        print(datos)
    arduino.close()


ventana = tk.Tk()
ventana.title("Monitoreo Salud Estructural")

frame = tk.Frame(ventana)
label = tk.Label(text="Salud Estructural")
label.config(font=("Courier", 32))
label.pack()

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 2, 0, 0.5])
plt.show()

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()

# Obtener las dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()  # método para obtener Ancho
alto_pantalla = ventana.winfo_screenheight()  # método para obtener Alto

# Calcular las coordenadas para centrar la ventana
ancho_ventana = 1000
alto_ventana = 700
posicion_x = (ancho_pantalla - ancho_ventana) // 2
posicion_y = (alto_pantalla - alto_ventana) // 2

# Establecer el tamaño y la posición de la ventana
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

tk.Button(frame, text= "Gráfica Principal", command= plot).pack(pady = 10)
frame.pack()

ventana.mainloop()
conexion_arduino()