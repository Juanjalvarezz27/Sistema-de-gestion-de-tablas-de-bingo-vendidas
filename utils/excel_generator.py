# utils/excel_generator.py
import pandas as pd
import numpy as np
import random
import os
import matplotlib.pyplot as plt
from pathlib import Path
from tkinter import messagebox
import tkinter as tk
from datetime import datetime

# --- CONFIGURACIÓN DE ESTILOS Y CARPETAS ---
ESTILOS = {
    'Rojo_Claro': {'bg': '#f2dede', 'fg': '#a94442', 'header_bg': '#d9534f', 'header_fg': 'white'},
    'Azul_Oscuro': {'bg': '#d9edf7', 'fg': '#31708f', 'header_bg': '#428bca', 'header_fg': 'white'},
    'Verde_Lima': {'bg': '#dff0d8', 'fg': '#3c763d', 'header_bg': '#5cb85c', 'header_fg': 'white'},
    'Amarillo_Neon': {'bg': '#fcf8e3', 'fg': '#8a6d3b', 'header_bg': '#f0ad4e', 'header_fg': 'white'},
}
LETRAS = ['B', 'I', 'N', 'G', 'O']

class GeneradorExcel:
    def __init__(self, parent):
        self.parent = parent
        self.colors = {
            'bg_primary': '#0f0f23',
            'bg_secondary': '#1a1a2e', 
            'bg_card': '#16213e',
            'accent_primary': '#00ff88',
            'accent_secondary': '#0099ff',
            'accent_danger': '#ff4757',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0'
        }

    def mostrar_modal_cantidad(self):
        """Muestra un modal para que el usuario ingrese la cantidad de tablas"""
        modal = tk.Toplevel(self.parent)
        modal.title("📊 Generar Tablas en Excel")
        modal.geometry("400x300")
        modal.configure(bg=self.colors['bg_primary'])
        modal.transient(self.parent)
        modal.grab_set()

        # Centrar el modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (400 // 2)
        y = (modal.winfo_screenheight() // 2) - (300 // 2)
        modal.geometry(f"400x300+{x}+{y}")

        frame_modal = tk.Frame(modal, bg=self.colors['bg_primary'], padx=25, pady=25)
        frame_modal.pack(fill="both", expand=True)

        # Título
        lbl_titulo = tk.Label(frame_modal, 
                            text="🎯 GENERAR TABLAS EXCEL",
                            font=("Segoe UI", 16, "bold"), 
                            bg=self.colors['bg_primary'], 
                            fg=self.colors['accent_primary'])
        lbl_titulo.pack(pady=15)

        # Descripción
        lbl_desc = tk.Label(frame_modal,
                          text="Ingresa la cantidad de tablas de bingo que deseas generar:",
                          font=("Segoe UI", 11),
                          bg=self.colors['bg_primary'],
                          fg=self.colors['text_secondary'],
                          wraplength=350)
        lbl_desc.pack(pady=10)

        # Frame para entrada de cantidad
        frame_cantidad = tk.Frame(frame_modal, bg=self.colors['bg_primary'])
        frame_cantidad.pack(pady=20)

        lbl_cantidad = tk.Label(frame_cantidad,
                              text="Cantidad de tablas:",
                              font=("Segoe UI", 11, "bold"),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'])
        lbl_cantidad.pack(pady=5)

        self.entry_cantidad = tk.Entry(frame_cantidad,
                                     font=("Segoe UI", 14),
                                     bg='#2a2a4a',
                                     fg='white',
                                     insertbackground='white',
                                     relief='flat',
                                     width=10,
                                     justify='center')
        self.entry_cantidad.pack(pady=10, ipady=8)
        self.entry_cantidad.insert(0, "100")  # Valor por defecto
        self.entry_cantidad.focus()

        # Frame para botones
        frame_botones = tk.Frame(frame_modal, bg=self.colors['bg_primary'])
        frame_botones.pack(pady=20)

        def generar():
            try:
                cantidad = int(self.entry_cantidad.get().strip())
                if cantidad <= 0:
                    messagebox.showerror("Error", "❌ La cantidad debe ser mayor a 0")
                    return
                if cantidad > 1000:
                    messagebox.showerror("Error", "❌ La cantidad máxima es 1000 tablas")
                    return
                
                modal.destroy()
                self.ejecutar_generacion(cantidad)
                
            except ValueError:
                messagebox.showerror("Error", "❌ Por favor ingresa un número válido")

        def cancelar():
            modal.destroy()

        btn_generar = tk.Button(frame_botones,
                              text="🎯 GENERAR EXCEL",
                              command=generar,
                              bg=self.colors['accent_primary'],
                              fg=self.colors['bg_primary'],
                              font=("Segoe UI", 12, "bold"),
                              width=15,
                              height=1,
                              padx=20,
                              pady=12,
                              relief='flat',
                              cursor="hand2")
        btn_generar.pack(side="left", padx=10)

        btn_cancelar = tk.Button(frame_botones,
                               text="❌ CANCELAR",
                               command=cancelar,
                               bg=self.colors['accent_danger'],
                               fg="white",
                               font=("Segoe UI", 12, "bold"),
                               width=12,
                               height=1,
                               padx=20,
                               pady=12,
                               relief='flat',
                               cursor="hand2")
        btn_cancelar.pack(side="left", padx=10)

        # Enter para generar, Escape para cancelar
        modal.bind('<Return>', lambda e: generar())
        modal.bind('<Escape>', lambda e: cancelar())

        modal.focus_force()
        self.entry_cantidad.select_range(0, tk.END)

    def generar_carton_bingo(self, num_cartones):
        """Genera cartones de bingo (75 bolas) con validación."""
        
        # 1. Definir los rangos de números (B=1-15, I=16-30, etc.)
        rangos = {
            'B': list(range(1, 16)),
            'I': list(range(16, 31)),
            'N': list(range(31, 46)),
            'G': list(range(46, 61)),
            'O': list(range(61, 76))
        }
        
        todos_los_cartones = []
        
        for i in range(1, num_cartones + 1):
            carton = {}
            for letra in LETRAS:
                # Seleccionar 5 números únicos para cada columna
                numeros_columna = random.sample(rangos[letra], 5)
                for j in range(5):
                    carton[f'{letra}{j+1}'] = numeros_columna[j]
            
            # Casilla FREE (N3)
            carton['N3'] = 'FREE'
            carton['ID_Carton'] = i
            todos_los_cartones.append(carton)

        df = pd.DataFrame(todos_los_cartones)
        
        # Asegurar el orden de las columnas para el Excel
        column_order = ['ID_Carton'] + [f'{l}{r}' for l in LETRAS for r in range(1, 6)]
        df = df[column_order]
        
        return df

    def crear_imagen_carton(self, df_carton, estilo, output_path):
        """Crea y guarda una imagen PNG de un cartón de bingo."""
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title(f"ID: {df_carton['ID_Carton'].iloc[0]}", fontsize=16, color=estilo['fg'])
        ax.set_xticks(np.arange(6))
        ax.set_yticks(np.arange(6))
        
        # Estilos del tablero
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.set_aspect('equal')
        ax.grid(which='both', color='black', linewidth=2)
        ax.tick_params(which='both', length=0)
        ax.set_xticklabels([''] + LETRAS, fontsize=18, fontweight='bold', color=estilo['header_fg'])
        ax.set_yticklabels([]) # Ocultar etiquetas Y
        
        # Rellenar encabezados de columna
        for i, letra in enumerate(LETRAS):
            rect = plt.Rectangle((i, 5), 1, 0, facecolor=estilo['header_bg'], edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            ax.text(i + 0.5, 5.5, letra, ha='center', va='center', fontsize=24, color=estilo['header_fg'])
        
        # Llenar celdas
        for i in range(5): # Columnas (B, I, N, G, O)
            for j in range(5): # Filas (1, 2, 3, 4, 5)
                col_name = f'{LETRAS[i]}{j+1}'
                valor = df_carton[col_name].iloc[0]
                
                # Fondo de celda
                rect = plt.Rectangle((i, 4-j), 1, 1, facecolor=estilo['bg'], edgecolor='black', linewidth=2)
                ax.add_patch(rect)
                
                # Texto
                color = estilo['fg']
                if valor == 'FREE':
                    color = 'red'
                    
                ax.text(i + 0.5, 4 - j + 0.5, str(valor), 
                        ha='center', va='center', fontsize=20, color=color, fontweight='bold')
        
        plt.tight_layout()
        plt.axis('off') # Quitar el borde principal y ejes
        plt.savefig(output_path, dpi=100, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)

    def ejecutar_generacion(self, total_cartones):
        """Ejecuta la generación de cartones con la cantidad especificada"""
        try:
            from utils.helpers import obtener_carpeta_descargas
            downloads_path = obtener_carpeta_descargas()
            
            # Crear nombre de archivo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            excel_file = downloads_path / f"Bingo_Cartones_{total_cartones}_{timestamp}.xlsx"
            png_dir = downloads_path / f"Cartones_PNG_{timestamp}"
            
            # Mostrar mensaje de progreso
            progress_modal = tk.Toplevel(self.parent)
            progress_modal.title("Generando Cartones...")
            progress_modal.geometry("400x150")
            progress_modal.configure(bg=self.colors['bg_primary'])
            progress_modal.transient(self.parent)
            
            # Centrar el modal
            progress_modal.update_idletasks()
            x = (progress_modal.winfo_screenwidth() // 2) - (400 // 2)
            y = (progress_modal.winfo_screenheight() // 2) - (150 // 2)
            progress_modal.geometry(f"400x150+{x}+{y}")
            
            frame_progress = tk.Frame(progress_modal, bg=self.colors['bg_primary'], padx=20, pady=20)
            frame_progress.pack(fill="both", expand=True)
            
            lbl_progress = tk.Label(frame_progress,
                                  text=f"🔄 Generando {total_cartones} cartones...\n\nPor favor espere...",
                                  font=("Segoe UI", 11),
                                  bg=self.colors['bg_primary'],
                                  fg=self.colors['text_primary'],
                                  justify='center')
            lbl_progress.pack(pady=10)
            
            progress_modal.update()
            
            # Generar cartones
            df_bingo = self.generar_carton_bingo(total_cartones)
            
            # Guardar archivo Excel
            df_bingo.to_excel(excel_file, index=False)
            
            # Generar imágenes PNG (opcional, comentado por ahora para mayor velocidad)
            # self.generar_imagenes_png(df_bingo, total_cartones, png_dir)
            
            progress_modal.destroy()
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "✅ Generación Completada",
                f"📊 Excel generado exitosamente!\n\n"
                f"📁 Archivo: {excel_file.name}\n"
                f"🎫 Cartones generados: {total_cartones}\n"
                f"💾 Ubicación: {downloads_path}\n\n"
                f"Las tablas incluyen números únicos para bingo tradicional."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error generando Excel: {str(e)}")

    def generar_imagenes_png(self, df_bingo, total_cartones, png_dir):
        """Genera imágenes PNG de los cartones (función opcional)"""
        if os.path.exists(png_dir):
            import shutil
            shutil.rmtree(png_dir)
        os.makedirs(png_dir, exist_ok=True)
        
        estilos_nombres = list(ESTILOS.keys())
        
        for i in range(total_cartones):
            carton_id = i + 1
            df_carton = df_bingo[df_bingo['ID_Carton'] == carton_id]
            
            # Determinar estilo y subcarpeta
            estilo_index = i // 100 
            estilo_nombre = estilos_nombres[estilo_index % len(estilos_nombres)]
            estilo_data = ESTILOS[estilo_nombre]
            
            # Crear subcarpeta si no existe
            sub_dir = os.path.join(png_dir, f"{estilo_nombre}_{estilo_index * 100 + 1}-{min(estilo_index * 100 + 100, total_cartones)}")
            os.makedirs(sub_dir, exist_ok=True)
            
            # Crear la imagen y guardar
            output_path = os.path.join(sub_dir, f"Carton_{carton_id}.png")
            self.crear_imagen_carton(df_carton, estilo_data, output_path)