import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pygame

# Inicializar pygame
pygame.mixer.init()

# Crear la ventana principal ajustable
root = tk.Tk()
root.title("Control de Peso")
root.geometry("800x600")  # Tamaño inicial más grande
root.resizable(True, True)  # Hacer la ventana ajustable

# Archivo donde se almacenarán los datos
filename = 'weights.csv'

# Crear archivo CSV si no existe
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Fecha', 'Peso'])
    df.to_csv(filename, index=False)

# Función para agregar un nuevo registro de peso
def add_weight():
    try:
        weight = float(entry_weight.get())
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = {'Fecha': date, 'Peso': weight}
        df = pd.read_csv(filename)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(filename, index=False)
        messagebox.showinfo("Info", f'Peso {weight}kg agregado en la fecha {date}.')
        entry_weight.delete(0, tk.END)
        show_image(weight)
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un número válido.")

# Función para mostrar la imagen y reproducir el audio basado en el peso
def show_image(weight):
    try:
        if weight < 50:
            img_path = "huesudo.png"
            audio_file = "under_50.mp3"
            msg = "Bajo peso"
            animate = False
        elif weight == 70:
            img_path = "gigachad.png"
            audio_file = "gigachad.mp3"
            msg = "Peso ideal"
            animate = False
        elif weight == 90:
            img_path = "gordas.png"
            audio_file = "oyegelda.mp3"
            msg = "Sobrepeso"
            animate = True
        else:
            messagebox.showinfo("Info", "Peso no específico para imagen.")
            return

        # Verificar si la imagen existe
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró la imagen: {img_path}")
            return

        img = img.resize((400, 400), Image.LANCZOS)  # Incrementar tamaño de la imagen
        img = ImageTk.PhotoImage(img)

        panel.config(image=img)
        panel.image = img

        # Reproducir audio
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Mostrar mensaje personalizado
        messagebox.showinfo("Estado del Peso", msg)

        # Iniciar animación si es la imagen de "gordas.png"
        if animate:
            animate_image(img_path)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Función para rotar la imagen de "gordas.png"
def animate_image(img_path):
    def perform_rotation_zoom(angle, size):
        img = Image.open(img_path)
        rotated_img = img.rotate(angle)
        resized_img = rotated_img.resize((size, size), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized_img)
        panel.config(image=img_tk)
        panel.image = img_tk

        # Incremento de ángulo y tamaño
        angle += 10
        if angle >= 360:
            angle = 0
        size += 5
        if size > 500:
            size = 400  # Regresar al tamaño original después del zoom out

        root.after(50, perform_rotation_zoom, angle, size)

    perform_rotation_zoom(0, 400)

# Función para graficar el progreso del peso
def plot_weights():
    try:
        df = pd.read_csv(filename)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        plt.plot(df['Fecha'], df['Peso'], marker='o')
        plt.xlabel('Fecha')
        plt.ylabel('Peso (kg)')
        plt.title('Progreso de Peso')
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al graficar: {e}")

# Crear los widgets
label = tk.Label(root, text="Introduce tu peso (kg):")
label.pack(pady=10)

entry_weight = tk.Entry(root)
entry_weight.pack(pady=5)

button_add = tk.Button(root, text="Agregar Peso", command=add_weight)
button_add.pack(pady=10)

button_plot = tk.Button(root, text="Ver Progreso", command=plot_weights)
button_plot.pack(pady=10)

# Panel para mostrar la imagen
panel = tk.Label(root)
panel.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()