import pandas
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox  # Importar messagebox
import serial  # Importar pyserial para gestionar la conexión serial

# Función para verificar si una cadena puede convertirse en un número flotante válido
def es_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

# Función para guardar las gráficas como una imagen
def guardar_imagen(fig):
    archivo = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagen PNG", "*.png"), ("Todos los archivos", "*.*")],
        title="Guardar Gráfica"
    )
    if archivo:
        fig.savefig(archivo, dpi=300, bbox_inches='tight')
        print(f"Gráfica guardada en: {archivo}")

# Función para verificar la conexión serial
def verificar_conexion_serial():
    puerto = 'COM5'  # Puerto serial COM3
    try:
        # Intentamos abrir el puerto serial en el puerto especificado (COM3)
        ser = serial.Serial(puerto, baudrate=9600, timeout=1)
        if ser.is_open:
            # Si la conexión fue exitosa, mostrar un mensaje emergente de éxito
            messagebox.showinfo("Conexión Exitosa", f"Conexión exitosa con el puerto {puerto}")
        ser.close()  # Cerrar el puerto después de verificar
    except serial.SerialException as e:
        # Si no se pudo conectar, mostrar un mensaje emergente de error
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al puerto {puerto}: {e}")

# Función para generar archivo con todos los puntos de la gráfica principal
def generar_archivo_puntos(datos):
    archivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv"), ("Todos los archivos", "*.*")],
        title="Guardar archivo de puntos"
    )
    if archivo:
        datos.to_csv(archivo, index=False)
        print(f"Archivo guardado en: {archivo}")

# Crear la ventana principal de Tkinter
def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Gráficas de Ejes")
    ventana.geometry("1000x700")  # Tamaño inicial de la ventana

    # Frame para el gráfico
    frame_grafico = ttk.Frame(ventana, relief="flat", padding=10)
    frame_grafico.pack(fill=tk.BOTH, expand=True)

    # Leer y procesar datos
    archivo_csv = r'C:\Users\angel\Desktop\prueba_9.csv'
    try:
        datos = pandas.read_csv(archivo_csv)
    except FileNotFoundError:
        print("El archivo CSV no se encuentra.")
        exit()
    except pandas.errors.EmptyDataError:
        print("El archivo CSV está vacío.")
        exit()

    if len(datos.columns) != 3:
        print("El archivo CSV no tiene exactamente tres columnas.")
        exit()

    for columna in datos.columns:
        datos = datos[datos[columna].apply(es_numero)]

    # Crear la figura de Matplotlib
    fig = plt.Figure(figsize=(12, 6))
    gs = GridSpec(3, 4, figure=fig)

    # Gráfica principal
    ax_main = fig.add_subplot(gs[:, :2])
    colors = ['tab:blue', 'tab:orange', 'tab:green']
    ejes = ['Eje X', 'Eje Y', 'Eje Z']
    for color, columna, eje in zip(colors, datos.columns, ejes):
        ax_main.plot(datos.index, datos[columna], label=eje, color=color)  # Cambiar aquí para mostrar el nombre del eje
    ax_main.set_title('Gráfico Principal: x, y, z')
    ax_main.set_ylabel('MicroTeslas')
    ax_main.set_xlabel('Longitud (mm)')
    ax_main.legend()
    ax_main.grid()

    # Subgráficas pequeñas para cada eje
    for i, (color, columna, eje) in enumerate(zip(colors, datos.columns, ejes)):
        ax = fig.add_subplot(gs[i, 2:])
        ax.plot(datos.index, datos[columna], label=eje, color=color)  # Cambiar aquí también para mostrar el nombre del eje
        ax.set_title(eje)
        ax.set_ylabel('MicroTeslas')
        ax.set_xlabel('Longitud (mm)')
        ax.legend()
        ax.grid()

    # Ajustar los espacios entre las gráficas
    fig.subplots_adjust(hspace=0.4, wspace=0.3)  # Espacios entre subgráficas

    # Agregar la figura a Tkinter con FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Frame para los botones (horizontal)
    frame_botones = ttk.Frame(ventana, relief="flat", padding=10)
    frame_botones.pack(pady=20)

    # Establecer estilo de los botones
    estilo = ttk.Style()
    estilo.configure("TButton",
                     font=("Arial", 12),
                     padding=10,
                     relief="flat")

    # Botón para guardar la imagen (más grande y horizontal)
    btn_guardar = ttk.Button(frame_botones, text="Guardar Gráficas", command=lambda: guardar_imagen(fig), width=20, style="TButton")
    btn_guardar.grid(row=0, column=0, padx=10)

    # Botón para generar archivo con puntos de la gráfica
    btn_generar_archivo = ttk.Button(frame_botones, text="Generar Archivo de Puntos", command=lambda: generar_archivo_puntos(datos), width=20, style="TButton")
    btn_generar_archivo.grid(row=0, column=1, padx=10)

    # Botón para verificar la conexión serial
    btn_verificar = ttk.Button(frame_botones, text="Verificar Conexión Serial", command=verificar_conexion_serial, width=20, style="TButton")
    btn_verificar.grid(row=0, column=2, padx=10)

    # Botón para cerrar la ventana
    btn_cerrar = ttk.Button(frame_botones, text="Cerrar", command=ventana.destroy, width=20, style="TButton")
    btn_cerrar.grid(row=0, column=3, padx=10)

    # Label para mostrar el estado de la conexión
    global mensaje
    mensaje = ttk.Label(ventana, text="", font=("Arial", 12))
    mensaje.pack(pady=10)

    # Iniciar el bucle de eventos de Tkinter
    ventana.mainloop()

# Ejecutar la función principal
crear_ventana()
