import mysql.connector
import serial
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Actividad 09")

        # Configuración del puerto serie
        self.serial_port = serial.Serial("COM6", 9600, timeout=1)

        # Campos de entrada
        self.label_usuario = tk.Label(master, text="Usuario:")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.insert(0, "Ingrese su nombre")
        self.entry_usuario.bind("<FocusIn>", self.clear_placeholder)
        self.entry_usuario.bind("<FocusOut>", self.set_placeholder)
        self.entry_usuario.pack()

        self.label_fecha = tk.Label(master, text="Fecha (YYYY-MM-DD):")
        self.label_fecha.pack()
        self.entry_fecha = tk.Entry(master)
        self.entry_fecha.insert(0, "Ingrese la fecha (YYYY-MM-DD)")
        self.entry_fecha.bind("<FocusIn>", self.clear_placeholder)
        self.entry_fecha.bind("<FocusOut>", self.set_placeholder)
        self.entry_fecha.pack()

        self.button_registrar = tk.Button(master, text="Registrar", command=self.registrar_datos)
        self.button_registrar.pack()

        self.label_temperaturaC = tk.Label(master, text="Temperatura C: ")
        self.label_temperaturaC.pack()
        self.label_temperaturaF = tk.Label(master, text="Temperatura F: ")
        self.label_temperaturaF.pack()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def clear_placeholder(self, event):
        if self.entry_usuario.get() == "Ingrese su nombre":
            self.entry_usuario.delete(0, tk.END)
            self.entry_usuario.config(fg='black')
        elif self.entry_fecha.get() == "Ingrese la fecha (YYYY-MM-DD)":
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.config(fg='black')

    def set_placeholder(self, event):
        if not self.entry_usuario.get():
            self.entry_usuario.insert(0, "Ingrese su nombre")
            self.entry_usuario.config(fg='gray')
        if not self.entry_fecha.get():
            self.entry_fecha.insert(0, "Ingrese la fecha (YYYY-MM-DD)")
            self.entry_fecha.config(fg='gray')

    def registrar_datos(self):
        try:
            # Leer datos de Arduino
            datos = self.serial_port.readline().decode('utf-8').strip().split(',')
            temperaturaC = float(datos[0].split(':')[1].strip())
            temperaturaF = float(datos[1].split(':')[1].strip())

            # Mostrar las temperaturas en las etiquetas
            self.label_temperaturaC.config(text=f"Temperatura C: {temperaturaC}")
            self.label_temperaturaF.config(text=f"Temperatura F: {temperaturaF}")

            # Validar la fecha
            fecha_str = self.entry_fecha.get()
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Fecha no válida. Por favor ingresa una fecha en el formato YYYY-MM-DD.")
                return

            self.guardar_datos(temperaturaC, temperaturaF, self.entry_usuario.get(), fecha)
        except Exception as ex:
            messagebox.showerror("Error", f"Error al registrar datos: {ex}")

    def guardar_datos(self, temperaturaC, temperaturaF, usuario, fecha):
        connection = mysql.connector.connect(
            host='localhost',
            database='Actividad9',
            user='root',
            password='gsmn71acD*'
        )
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Registro (fecha, temperaturaC, temperaturaF, usuario) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (fecha, temperaturaC, temperaturaF, usuario))
            connection.commit()
            messagebox.showinfo("Éxito", "Datos guardados exitosamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al guardar datos: {err}")
        finally:
            cursor.close()
            connection.close()

    def on_closing(self):
        if self.serial_port.is_open:
            self.serial_port.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
