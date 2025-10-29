import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class SistemaGestionTablas:
    def __init__(self):
        # Determinar si estamos ejecutando como .exe o como script
        if getattr(sys, 'frozen', False):
            # Ejecutando como .exe
            self.base_path = Path(sys.executable).parent
        else:
            # Ejecutando como script
            self.base_path = Path(__file__).parent
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Tablas Vendidas - PORTABLE")
        self.root.geometry("1000x800")
        self.root.configure(bg='#f8f9fa')
        
        # Archivo para guardar los datos (en la misma carpeta del .exe)
        self.data_file = self.base_path / "tablas_vendidas.json"
        
        # Obtener ruta de la carpeta de Descargas
        self.descargas_path = self.obtener_carpeta_descargas()
        
        # Cargar datos existentes
        self.tablas_vendidas = self.cargar_datos()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def obtener_carpeta_descargas(self):
        """Obtener la ruta de la carpeta de Descargas del usuario"""
        try:
            # Para Windows
            if os.name == 'nt':
                import ctypes
                from ctypes import wintypes, windll
                
                CSIDL_PERSONAL = 5  # My Documents
                SHGFP_TYPE_CURRENT = 0
                
                buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
                windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
                
                documents_path = buf.value
                downloads_path = Path(documents_path) / "Descargas"
                
                if not downloads_path.exists():
                    downloads_path = Path.home() / "Downloads"
                
            else:
                # Para Linux/Mac
                downloads_path = Path.home() / "Downloads"
            
            # Crear la carpeta si no existe
            downloads_path.mkdir(exist_ok=True)
            
            return downloads_path
            
        except Exception as e:
            # Si hay error, usar la carpeta del programa
            print(f"Error obteniendo carpeta Descargas: {e}")
            return self.base_path
    
    def cargar_datos(self):
        """Cargar datos desde archivo JSON"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error cargando datos: {e}")
                return {}
        return {}
    
    def guardar_datos(self):
        """Guardar datos en archivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tablas_vendidas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando datos: {e}")
    
    def crear_interfaz(self):
        """Crear todos los elementos de la interfaz"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(main_frame, text="🎫 SISTEMA DE GESTIÓN DE TABLAS VENDIDAS - PORTABLE", 
                         font=("Arial", 16, "bold"), bg='#f8f9fa', fg='#2c3e50')
        titulo.pack(pady=15)
        
        # Frame para controles
        controles_frame = tk.Frame(main_frame, bg='#f8f9fa')
        controles_frame.pack(fill="x", padx=10, pady=15)
        
        # Contador de tablas vendidas
        self.actualizar_contador()
        self.contador_label = tk.Label(controles_frame, 
                                      text=f"📊 TABLAS VENDIDAS: {self.contador_vendidas}/200",
                                      font=("Arial", 12, "bold"), 
                                      bg='#3498db', fg='white',
                                      padx=20, pady=10, relief="raised", bd=2)
        self.contador_label.pack(side="left", padx=5)
        
        # Frame para botones de importar/exportar
        import_export_frame = tk.Frame(controles_frame, bg='#f8f9fa')
        import_export_frame.pack(side="right", padx=5)
        
        # Botón de exportar datos
        self.btn_exportar = tk.Button(import_export_frame, text="📤 EXPORTAR DATOS", 
                                     command=self.exportar_datos,
                                     bg="#9b59b6", fg="white", font=("Arial", 9, "bold"),
                                     padx=10, pady=8, relief="raised", bd=2, cursor="hand2")
        self.btn_exportar.pack(side="left", padx=2)
        
        # Botón de importar datos
        self.btn_importar = tk.Button(import_export_frame, text="📥 IMPORTAR DATOS", 
                                     command=self.importar_datos,
                                     bg="#f39c12", fg="white", font=("Arial", 9, "bold"),
                                     padx=10, pady=8, relief="raised", bd=2, cursor="hand2")
        self.btn_importar.pack(side="left", padx=2)
        
        # Botón de reset
        self.btn_reset = tk.Button(controles_frame, text="🔄 RESETEAR TODO", 
                                  command=self.resetear_sistema,
                                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                                  padx=15, pady=10, relief="raised", bd=2, cursor="hand2")
        self.btn_reset.pack(side="right", padx=5)
        
        # Frame para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña 1: Tablas
        self.tab_tablas = ttk.Frame(notebook)
        notebook.add(self.tab_tablas, text="🎫 TABLAS NUMERADAS")
        
        # Pestaña 2: Asignaciones
        self.tab_asignaciones = ttk.Frame(notebook)
        notebook.add(self.tab_asignaciones, text="👥 ASIGNACIONES")
        
        # Crear contenido de la pestaña de tablas
        self.crear_pestana_tablas(self.tab_tablas)
        
        # Crear contenido de la pestaña de asignaciones
        self.crear_pestana_asignaciones(self.tab_asignaciones)
    
    def exportar_datos(self):
        """Exportar datos a un archivo JSON en la carpeta de Descargas"""
        try:
            # Crear nombre de archivo con timestamp
            nombre_archivo = f"backup_tablas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            ruta_exportacion = self.descargas_path / nombre_archivo
            
            # Guardar datos en el archivo
            with open(ruta_exportacion, 'w', encoding='utf-8') as f:
                json.dump(self.tablas_vendidas, f, ensure_ascii=False, indent=2)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Exportación Exitosa", 
                f"✅ Datos exportados correctamente:\n\n"
                f"📁 {nombre_archivo}\n\n"
                f"📊 Tickets vendidos: {self.contador_vendidas}\n"
                f"💾 Guardado en: {ruta_exportacion}\n\n"
                f"💡 Puedes llevar este archivo a otra computadora\n"
                f"y usar la opción 'IMPORTAR DATOS' para cargarlo."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al exportar datos:\n\n{str(e)}")
    
    def importar_datos(self):
        """Importar datos desde un archivo JSON"""
        try:
            # Abrir diálogo para seleccionar archivo
            archivo = filedialog.askopenfilename(
                title="Seleccionar archivo de datos",
                filetypes=[
                    ("Archivos JSON", "*.json"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if not archivo:
                return  # Usuario canceló
            
            # Leer datos del archivo seleccionado
            with open(archivo, 'r', encoding='utf-8') as f:
                nuevos_datos = json.load(f)
            
            # Validar que sea un diccionario
            if not isinstance(nuevos_datos, dict):
                messagebox.showerror("Error", "❌ El archivo no contiene datos válidos")
                return
            
            # Preguntar confirmación
            respuesta = messagebox.askyesno(
                "Confirmar Importación",
                f"¿Está seguro de que desea importar estos datos?\n\n"
                f"📊 Tickets en el archivo: {sum(1 for estado in nuevos_datos.values() if estado.get('vendido', False))}\n"
                f"📊 Tickets actuales: {self.contador_vendidas}\n\n"
                f"⚠️ Los datos actuales serán reemplazados completamente."
            )
            
            if respuesta:
                # Reemplazar datos actuales
                self.tablas_vendidas = nuevos_datos
                self.guardar_datos()
                self.actualizar_interfaz()
                
                messagebox.showinfo(
                    "Importación Exitosa", 
                    f"✅ Datos importados correctamente:\n\n"
                    f"📊 Tickets vendidos: {self.contador_vendidas}\n"
                    f"👥 Personas registradas: {len(set(datos.get('nombre', '') for datos in self.tablas_vendidas.values() if datos.get('vendido', False)))}\n\n"
                    f"💾 Datos cargados desde: {Path(archivo).name}"
                )
            
        except json.JSONDecodeError:
            messagebox.showerror("Error", "❌ El archivo seleccionado no es un JSON válido")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al importar datos:\n\n{str(e)}")
    
    def crear_pestana_tablas(self, parent):
        """Crear la pestaña de tablas numeradas"""
        # Frame para controles de la pestaña de tablas
        controles_tablas_frame = tk.Frame(parent, bg='#f8f9fa')
        controles_tablas_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón para descargar tickets disponibles
        self.btn_descargar_disponibles = tk.Button(controles_tablas_frame, 
                                                  text="📄 DESCARGAR TICKETS DISPONIBLES",
                                                  command=self.descargar_tickets_disponibles,
                                                  bg="#27ae60", fg="white", font=("Arial", 9, "bold"),
                                                  padx=12, pady=6, relief="raised", bd=2, cursor="hand2")
        self.btn_descargar_disponibles.pack(side="left", padx=5)
        
        # Frame contenedor principal
        contenedor_principal = tk.Frame(parent, bg='#f8f9fa')
        contenedor_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para los números que ocupará todo el espacio
        self.frame_contenedor_numeros = tk.Frame(contenedor_principal, bg='#f8f9fa')
        self.frame_contenedor_numeros.pack(fill="both", expand=True)
        
        # Canvas con scrollbar
        self.canvas = tk.Canvas(self.frame_contenedor_numeros, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_contenedor_numeros, orient="vertical", command=self.canvas.yview)
        
        # Frame scrollable que se expandirá
        self.frame_numeros = tk.Frame(self.canvas, bg='#f8f9fa')
        
        self.frame_numeros.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.frame_numeros, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear todos los botones
        self.crear_botones_numeros()
        
        # Configurar el canvas para que se redimensione
        self.canvas.bind("<Configure>", self.redimensionar_botones)
    
    def crear_pestana_asignaciones(self, parent):
        """Crear la pestaña de asignaciones con mejor diseño"""
        # Frame para controles de la pestaña de asignaciones
        controles_asignaciones_frame = tk.Frame(parent, bg='#f8f9fa')
        controles_asignaciones_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón para descargar asignaciones
        self.btn_descargar_asignaciones = tk.Button(controles_asignaciones_frame, 
                                                   text="📄 DESCARGAR ASIGNACIONES",
                                                   command=self.descargar_asignaciones,
                                                   bg="#e67e22", fg="white", font=("Arial", 9, "bold"),
                                                   padx=12, pady=6, relief="raised", bd=2, cursor="hand2")
        self.btn_descargar_asignaciones.pack(side="left", padx=5)
        
        # Frame principal para asignaciones
        asignaciones_frame = tk.Frame(parent, bg='#f8f9fa')
        asignaciones_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        titulo_asignaciones = tk.Label(asignaciones_frame, 
                                      text="👥 ASIGNACIONES DE TICKETS", 
                                      font=("Arial", 16, "bold"), 
                                      bg='#f8f9fa', fg='#2c3e50')
        titulo_asignaciones.pack(pady=10)
        
        # Frame para el contenido con scroll
        contenido_frame = tk.Frame(asignaciones_frame, bg='#f8f9fa')
        contenido_frame.pack(fill="both", expand=True)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(contenido_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(contenido_frame, orient="vertical", command=canvas.yview)
        self.scrollable_asignaciones = tk.Frame(canvas, bg='white')
        
        self.scrollable_asignaciones.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_asignaciones, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")
        
        self.canvas_asignaciones = canvas
        self.actualizar_pestana_asignaciones()
    
    def descargar_tickets_disponibles(self):
        """Descargar lista de tickets disponibles en formato TXT en la carpeta Descargas"""
        try:
            # Obtener tickets disponibles
            disponibles = [num for num in range(1, 201) if str(num) not in self.tablas_vendidas or not self.tablas_vendidas[str(num)].get('vendido', False)]
            
            # Crear contenido del archivo
            contenido = []
            contenido.append("=" * 50)
            contenido.append("LISTA DE TICKETS DISPONIBLES")
            contenido.append("=" * 50)
            contenido.append(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            contenido.append(f"Total disponibles: {len(disponibles)}/200")
            contenido.append("")
            contenido.append("TICKETS DISPONIBLES:")
            contenido.append("-" * 50)
            
            if disponibles:
                for i in range(0, len(disponibles), 10):
                    grupo = disponibles[i:i + 10]
                    linea = ", ".join(f"{num:3}" for num in grupo)
                    contenido.append(linea)
            else:
                contenido.append("NO HAY TICKETS DISPONIBLES")
                contenido.append("TODOS LOS TICKETS ESTÁN VENDIDOS")
            
            contenido.append("")
            contenido.append("=" * 50)
            
            # Guardar archivo en la carpeta de Descargas
            nombre_archivo = f"tickets_disponibles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ruta_completa = self.descargas_path / nombre_archivo
            
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                f.write('\n'.join(contenido))
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Descarga Exitosa", 
                f"✅ Archivo guardado en Descargas:\n\n"
                f"📁 {nombre_archivo}\n\n"
                f"📊 Tickets disponibles: {len(disponibles)}\n"
                f"💾 Ruta: {ruta_completa}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al generar el archivo:\n\n{str(e)}")
    
    def descargar_asignaciones(self):
        """Descargar lista de asignaciones en formato TXT en la carpeta Descargas"""
        try:
            # Agrupar tickets por persona
            personas_tickets = {}
            for numero, datos in self.tablas_vendidas.items():
                if datos.get('vendido', False):
                    nombre = datos.get('nombre', '')
                    if nombre not in personas_tickets:
                        personas_tickets[nombre] = []
                    personas_tickets[nombre].append(int(numero))
            
            # Crear contenido del archivo
            contenido = []
            contenido.append("=" * 50)
            contenido.append("REPORTE DE ASIGNACIONES DE TICKETS")
            contenido.append("=" * 50)
            contenido.append(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            contenido.append(f"Total de tickets vendidos: {self.contador_vendidas}/200")
            contenido.append("")
            contenido.append("DETALLE POR PERSONA:")
            contenido.append("-" * 50)
            
            if personas_tickets:
                for nombre, tickets in sorted(personas_tickets.items()):
                    contenido.append(f"👤 {nombre}:")
                    contenido.append(f"   Tickets: {', '.join(map(str, sorted(tickets)))}")
                    contenido.append(f"   Cantidad: {len(tickets)} ticket(s)")
                    contenido.append("")
            else:
                contenido.append("No hay asignaciones registradas")
                contenido.append("")
            
            contenido.append("RESUMEN:")
            contenido.append("-" * 50)
            contenido.append(f"Total de personas: {len(personas_tickets)}")
            contenido.append(f"Total de tickets vendidos: {self.contador_vendidas}")
            contenido.append(f"Tickets disponibles: {200 - self.contador_vendidas}")
            contenido.append("")
            contenido.append("=" * 50)
            
            # Guardar archivo en la carpeta de Descargas
            nombre_archivo = f"asignaciones_tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ruta_completa = self.descargas_path / nombre_archivo
            
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                f.write('\n'.join(contenido))
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "Descarga Exitosa", 
                f"✅ Archivo guardado en Descargas:\n\n"
                f"📁 {nombre_archivo}\n\n"
                f"👥 Personas: {len(personas_tickets)}\n"
                f"🎫 Tickets vendidos: {self.contador_vendidas}\n"
                f"💾 Ruta: {ruta_completa}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al generar el archivo:\n\n{str(e)}")
    
    def redimensionar_botones(self, event=None):
        """Redimensionar los botones cuando cambia el tamaño del canvas"""
        if hasattr(self, 'frame_numeros'):
            ancho_disponible = self.canvas.winfo_width()
            if ancho_disponible > 1:
                self.crear_botones_numeros()
    
    def crear_botones_numeros(self):
        """Crear los 200 botones organizados en 20 filas x 10 columnas"""
        for widget in self.frame_numeros.winfo_children():
            widget.destroy()
        
        ancho_canvas = self.canvas.winfo_width()
        if ancho_canvas < 100:
            ancho_canvas = 800
        
        ancho_boton = (ancho_canvas - 40) // 10
        alto_boton = 70
        
        for i in range(20):
            self.frame_numeros.grid_rowconfigure(i, weight=1, minsize=alto_boton)
        for i in range(10):
            self.frame_numeros.grid_columnconfigure(i, weight=1, minsize=ancho_boton)
        
        for numero in range(1, 201):
            fila = (numero - 1) // 10
            columna = (numero - 1) % 10
            
            estado_numero = self.tablas_vendidas.get(str(numero), {})
            vendido = estado_numero.get('vendido', False)
            nombre = estado_numero.get('nombre', '')
            
            if vendido:
                texto_boton = f"#{numero}\n✅ Vendido\n{nombre.split()[0]}"
                color_bg = "#27ae60"
            else:
                texto_boton = f"#{numero}\n🟢 Disponible"
                color_bg = "#3498db"
            
            btn = tk.Button(
                self.frame_numeros,
                text=texto_boton,
                command=lambda n=numero: self.abrir_modal(n),
                bg=color_bg,
                fg="white",
                font=("Arial", 9, "bold"),
                relief="raised",
                bd=2,
                cursor="hand2",
                justify='center',
                wraplength=ancho_boton - 10
            )
            
            btn.grid(row=fila, column=columna, padx=2, pady=2, sticky="nsew")
    
    def actualizar_pestana_asignaciones(self):
        """Actualizar la pestaña de asignaciones"""
        for widget in self.scrollable_asignaciones.winfo_children():
            widget.destroy()
        
        personas_tickets = {}
        for numero, datos in self.tablas_vendidas.items():
            if datos.get('vendido', False):
                nombre = datos.get('nombre', '')
                if nombre not in personas_tickets:
                    personas_tickets[nombre] = []
                personas_tickets[nombre].append(int(numero))
        
        if not personas_tickets:
            frame_vacio = tk.Frame(self.scrollable_asignaciones, bg='white', relief='solid', bd=1)
            frame_vacio.pack(fill="x", padx=10, pady=20)
            
            lbl_vacio = tk.Label(frame_vacio, 
                                text="🎯 No hay tickets asignados aún\n\nAsigna tickets en la pestaña 'Tablas Numeradas'", 
                                font=("Arial", 12, "italic"), 
                                bg='white', fg='#7f8c8d', justify='center')
            lbl_vacio.pack(pady=30)
            return
        
        for nombre, tickets in sorted(personas_tickets.items()):
            tarjeta_frame = tk.Frame(self.scrollable_asignaciones, 
                                    bg='#ecf0f1', 
                                    relief='solid', 
                                    bd=1,
                                    padx=15, 
                                    pady=12)
            tarjeta_frame.pack(fill="x", padx=10, pady=8)
            
            header_frame = tk.Frame(tarjeta_frame, bg='#ecf0f1')
            header_frame.pack(fill="x", pady=(0, 10))
            
            lbl_icono = tk.Label(header_frame, text="👤", font=("Arial", 14), bg='#ecf0f1')
            lbl_icono.pack(side="left", padx=(0, 10))
            
            lbl_nombre = tk.Label(header_frame, text=nombre, 
                                 font=("Arial", 14, "bold"), 
                                 bg='#ecf0f1', fg='#2c3e50')
            lbl_nombre.pack(side="left")
            
            badge_frame = tk.Frame(header_frame, bg='#e74c3c', relief='raised', bd=1)
            badge_frame.pack(side="right", padx=10)
            
            lbl_badge = tk.Label(badge_frame, text=f"{len(tickets)} ticket{'s' if len(tickets) > 1 else ''}", 
                               font=("Arial", 10, "bold"), 
                               bg='#e74c3c', fg='white',
                               padx=8, pady=3)
            lbl_badge.pack()
            
            tickets_frame = tk.Frame(tarjeta_frame, bg='#ecf0f1')
            tickets_frame.pack(fill="x")
            
            lbl_tickets_titulo = tk.Label(tickets_frame, text="Tickets asignados:", 
                                        font=("Arial", 10, "bold"), 
                                        bg='#ecf0f1', fg='#34495e')
            lbl_tickets_titulo.pack(anchor="w", pady=(0, 5))
            
            tickets_ordenados = sorted(tickets)
            for i in range(0, len(tickets_ordenados), 10):
                grupo_tickets = tickets_ordenados[i:i + 10]
                
                grupo_frame = tk.Frame(tickets_frame, bg='#ecf0f1')
                grupo_frame.pack(fill="x", pady=2)
                
                for ticket in grupo_tickets:
                    btn_ticket = tk.Button(grupo_frame, 
                                         text=f"#{ticket} ❌", 
                                         command=lambda t=ticket: self.cancelar_venta(t),
                                         font=("Arial", 8, "bold"), 
                                         bg="#e67e22", 
                                         fg="white",
                                         relief="raised",
                                         bd=1,
                                         cursor="hand2",
                                         padx=8,
                                         pady=2)
                    btn_ticket.pack(side="left", padx=2, pady=2)
    
    def cancelar_venta(self, numero):
        """Cancelar la venta de un ticket"""
        respuesta = messagebox.askyesno(
            "Cancelar Venta", 
            f"¿Está seguro de que desea cancelar la venta del ticket #{numero}?\n\n"
            f"Actualmente asignado a: {self.tablas_vendidas[str(numero)].get('nombre', '')}"
        )
        
        if respuesta:
            if str(numero) in self.tablas_vendidas:
                del self.tablas_vendidas[str(numero)]
            
            self.guardar_datos()
            self.actualizar_interfaz()
            messagebox.showinfo("Éxito", f"✅ Venta del ticket #{numero} cancelada\n\nEl ticket está disponible nuevamente.")
    
    def actualizar_contador(self):
        """Actualizar el contador de tablas vendidas"""
        self.contador_vendidas = sum(1 for estado in self.tablas_vendidas.values() if estado.get('vendido', False))
    
    def abrir_modal(self, numero):
        """Abrir modal para asignar o ver información del ticket"""
        estado_actual = self.tablas_vendidas.get(str(numero), {})
        
        if estado_actual.get('vendido', False):
            modal = tk.Toplevel(self.root)
            modal.title(f"🎫 Información del Ticket #{numero}")
            modal.geometry("500x350")
            modal.configure(bg='#f8f9fa')
            modal.transient(self.root)
            modal.grab_set()
            
            modal.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
            y = (self.root.winfo_screenheight() // 2) - (350 // 2)
            modal.geometry(f"500x350+{x}+{y}")
            
            frame_modal = tk.Frame(modal, bg='#f8f9fa', padx=25, pady=25)
            frame_modal.pack(fill="both", expand=True)
            
            lbl_icono = tk.Label(frame_modal, text="✅", font=("Arial", 24), bg='#f8f9fa')
            lbl_icono.pack(pady=10)
            
            lbl_titulo = tk.Label(frame_modal, text=f"TICKET #{numero} - VENDIDO", 
                                 font=("Arial", 16, "bold"), bg='#f8f9fa', fg='#27ae60')
            lbl_titulo.pack(pady=5)
            
            lbl_nombre = tk.Label(frame_modal, text=f"👤 Asignado a: {estado_actual.get('nombre', '')}", 
                                font=("Arial", 14), bg='#f8f9fa', fg='#2c3e50')
            lbl_nombre.pack(pady=15)
            
            frame_botones = tk.Frame(frame_modal, bg='#f8f9fa')
            frame_botones.pack(pady=25)
            
            def cancelar_venta():
                modal.destroy()
                self.cancelar_venta(numero)
            
            btn_cancelar = tk.Button(frame_botones, text="❌ CANCELAR VENTA", 
                                   command=cancelar_venta,
                                   bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                                   width=15, height=2, padx=15, pady=10, cursor="hand2")
            btn_cancelar.pack(side="left", padx=10)
            
            btn_cerrar = tk.Button(frame_botones, text="👌 CERRAR", 
                                 command=modal.destroy,
                                 bg="#95a5a6", fg="white", font=("Arial", 12, "bold"),
                                 width=12, height=2, padx=15, pady=10, cursor="hand2")
            btn_cerrar.pack(side="left", padx=10)
            
            return
        
        # Modal para nueva venta
        modal = tk.Toplevel(self.root)
        modal.title(f"🎫 Asignar Ticket #{numero}")
        modal.geometry("500x300")
        modal.configure(bg='#f8f9fa')
        modal.transient(self.root)
        modal.grab_set()
        
        modal.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        modal.geometry(f"500x300+{x}+{y}")
        
        frame_modal = tk.Frame(modal, bg='#f8f9fa', padx=25, pady=25)
        frame_modal.pack(fill="both", expand=True)
        
        lbl_titulo = tk.Label(frame_modal, text=f"🎫 ASIGNAR TICKET #{numero}", 
                             font=("Arial", 16, "bold"), bg='#f8f9fa', fg='#2c3e50')
        lbl_titulo.pack(pady=15)
        
        lbl_nombre = tk.Label(frame_modal, text="👤 Nombre completo de la persona:", 
                             font=("Arial", 11), bg='#f8f9fa')
        lbl_nombre.pack(pady=8)
        
        entry_nombre = tk.Entry(frame_modal, width=40, font=("Arial", 12), 
                               relief="solid", bd=2)
        entry_nombre.pack(pady=15, ipady=10)
        entry_nombre.focus()
        
        frame_botones = tk.Frame(frame_modal, bg='#f8f9fa')
        frame_botones.pack(pady=20)
        
        def asignar_venta():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "❌ Por favor ingrese un nombre")
                return
            
            self.tablas_vendidas[str(numero)] = {
                'vendido': True,
                'nombre': nombre
            }
            
            self.guardar_datos()
            self.actualizar_interfaz()
            modal.destroy()
            
            messagebox.showinfo("Éxito", f"✅ Ticket #{numero} asignado a:\n{nombre}")
        
        def cancelar():
            modal.destroy()
        
        btn_asignar = tk.Button(frame_botones, text="✅ ASIGNAR", 
                               command=asignar_venta, 
                               bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                               width=12, height=2, padx=15, pady=12, cursor="hand2")
        btn_asignar.pack(side="left", padx=15)
        
        btn_cancelar = tk.Button(frame_botones, text="❌ CANCELAR", 
                                command=cancelar, 
                                bg="#95a5a6", fg="white", font=("Arial", 12, "bold"),
                                width=12, height=2, padx=15, pady=12, cursor="hand2")
        btn_cancelar.pack(side="left", padx=15)
        
        modal.bind('<Return>', lambda e: asignar_venta())
        modal.bind('<Escape>', lambda e: cancelar())
        
        modal.focus_force()
        entry_nombre.focus()
    
    def resetear_sistema(self):
        """Resetear todo el sistema"""
        respuesta = messagebox.askyesno(
            "Confirmar Reset", 
            "⚠️ ¿Está seguro de que desea resetear todo el sistema?\n\nEsta acción eliminará todas las asignaciones y no se puede deshacer."
        )
        
        if respuesta:
            self.tablas_vendidas = {}
            self.guardar_datos()
            self.actualizar_interfaz()
            messagebox.showinfo("Éxito", "🔄 Sistema reseteado correctamente")
    
    def actualizar_interfaz(self):
        """Actualizar toda la interfaz"""
        self.actualizar_contador()
        self.contador_label.configure(text=f"📊 TABLAS VENDIDAS: {self.contador_vendidas}/200")
        self.crear_botones_numeros()
        self.actualizar_pestana_asignaciones()
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SistemaGestionTablas()
    app.ejecutar()