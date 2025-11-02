import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import json
from models.bingo import Bingo

class VistaGestorBingos:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.bingos = self.cargar_bingos_existentes()
        self.colors = {
            'bg_primary': '#0f0f23',
            'bg_secondary': '#1a1a2e', 
            'bg_card': '#16213e',
            'accent_primary': '#00ff88',
            'accent_secondary': '#0099ff',
            'accent_danger': '#ff4757',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'border': '#00ff88'
        }
        
        self.frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        self.crear_interfaz()

    def cargar_bingos_existentes(self):
        from utils.helpers import crear_directorio_bingos
        directorio_bingos = crear_directorio_bingos()
        bingos = []

        if directorio_bingos.exists():
            for archivo in directorio_bingos.glob("*.json"):
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        datos = json.load(f)
                    bingo = Bingo(
                        datos['nombre'],
                        datos['cantidad_cartones'],
                        datos.get('precio_carton', 0)
                    )
                    bingos.append(bingo)
                except Exception as e:
                    print(f"Error cargando bingo {archivo}: {e}")
                    continue
        return bingos

    def crear_interfaz(self):
        header_frame = tk.Frame(self.frame, bg=self.colors['bg_secondary'], height=100)
        header_frame.pack(fill='x', padx=20, pady=15)
        header_frame.pack_propagate(False)

        btn_volver = tk.Button(header_frame,
            text="‹ VOLVER AL MENÚ",
            command=self.volver_menu,
            font=('Segoe UI', 11, 'bold'),
            bg='#2d2d4d',
            fg=self.colors['text_secondary'],
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_volver.pack(side='left', padx=10, pady=10)

        self.titulo = tk.Label(header_frame,
            text="🎯 GESTOR DE BINGOS",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_primary']
        )
        self.titulo.pack(side='left', padx=20, pady=10)

        btn_nuevo = tk.Button(header_frame,
            text="+ NUEVO BINGO",
            command=self.mostrar_formulario_creacion,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent_primary'],
            fg=self.colors['bg_primary'],
            padx=25,
            pady=12,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_nuevo.pack(side='right', padx=10, pady=10)

        self.frame_principal = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        self.frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        self.mostrar_lista_bingos()

    def mostrar_formulario_creacion(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        self.titulo.config(text="🆕 CREAR NUEVO BINGO")

        frame_contenedor = tk.Frame(self.frame_principal, bg=self.colors['bg_primary'])
        frame_contenedor.pack(expand=True, fill='both')
        
        frame_form = tk.Frame(frame_contenedor, 
                            bg=self.colors['bg_card'],
                            relief='flat',
                            bd=1,
                            padx=30, 
                            pady=30)
        frame_form.pack(expand=True)

        titulo_form = tk.Label(frame_form,
            text="CREAR NUEVO BINGO",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_primary']
        )
        titulo_form.pack(pady=(0, 20))

        campos = [
            ("🎯 Nombre del Bingo:", "entry_nombre", ""),
            ("📊 Cantidad de Cartones:", "entry_cartones", ""),
            ("💰 Precio por Cartón ($):", "entry_precio", "")
        ]

        for label_text, attr_name, placeholder in campos:
            frame_campo = tk.Frame(frame_form, bg=self.colors['bg_card'])
            frame_campo.pack(fill='x', pady=12)

            lbl = tk.Label(frame_campo,
                text=label_text,
                font=('Segoe UI', 11, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']
            )
            lbl.pack(anchor='w', pady=(0, 5))

            entry = tk.Entry(frame_campo,
                font=('Segoe UI', 12),
                bg='#2a2a4a',
                fg='white',
                insertbackground='white',
                relief='flat',
                bd=0,
                width=25
            )
            entry.pack(fill='x', ipady=8, padx=2)
            
            entry_frame = tk.Frame(frame_campo, bg=self.colors['border'], height=2)
            entry_frame.pack(fill='x', padx=2)
            entry_frame.pack_propagate(False)
            
            if placeholder:
                entry.insert(0, placeholder)
            
            setattr(self, attr_name, entry)

        frame_ganancias = tk.Frame(frame_form, 
                                 bg='#1a1a3a', 
                                 relief='flat', 
                                 bd=1,
                                 padx=15,
                                 pady=10)
        frame_ganancias.pack(fill='x', pady=15)

        self.lbl_ganancias = tk.Label(frame_ganancias,
            text="🎰 Ganancias potenciales: $0.00",
            font=('Segoe UI', 12, 'bold'),
            bg='#1a1a3a',
            fg=self.colors['accent_primary']
        )
        self.lbl_ganancias.pack()

        frame_botones = tk.Frame(frame_form, bg=self.colors['bg_card'])
        frame_botones.pack(pady=20)

        btn_crear = tk.Button(frame_botones,
            text="🎯 CREAR BINGO",
            command=self.crear_bingo,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent_primary'],
            fg=self.colors['bg_primary'],
            padx=25,
            pady=12,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_crear.pack(side='left', padx=10)

        btn_cancelar = tk.Button(frame_botones,
            text="❌ CANCELAR",
            command=self.mostrar_lista_bingos,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent_danger'],
            fg='white',
            padx=25,
            pady=12,
            relief='flat',
            cursor='hand2',
            bd=0
        )
        btn_cancelar.pack(side='left', padx=10)

        self.entry_cartones.bind('<KeyRelease>', self.actualizar_ganancias)
        self.entry_precio.bind('<KeyRelease>', self.actualizar_ganancias)
        self.actualizar_ganancias()
        self.entry_nombre.focus()

    def actualizar_ganancias(self, event=None):
        try:
            cartones = int(self.entry_cartones.get() or 0)
            precio = float(self.entry_precio.get() or 0)
            ganancias = cartones * precio
            self.lbl_ganancias.config(text=f"🎰 Ganancias potenciales: ${ganancias:,.2f}")
        except:
            self.lbl_ganancias.config(text="🎰 Ganancias potenciales: $0.00")

    def mostrar_lista_bingos(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        self.titulo.config(text="🎯 GESTIONAR BINGOS EXISTENTES")
        self.bingos = self.cargar_bingos_existentes()

        if not self.bingos:
            frame_vacio = tk.Frame(self.frame_principal, bg=self.colors['bg_card'], padx=30, pady=50)
            frame_vacio.pack(expand=True)

            lbl_vacio = tk.Label(frame_vacio,
                text="🎯 No hay bingos creados aún\n\nCrea tu primer bingo para comenzar",
                font=('Segoe UI', 14),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary'],
                justify='center')
            lbl_vacio.pack()

            btn_crear = tk.Button(frame_vacio,
                text="🆕 CREAR PRIMER BINGO",
                command=self.mostrar_formulario_creacion,
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['accent_primary'],
                fg=self.colors['bg_primary'],
                padx=20,
                pady=12,
                relief='flat',
                cursor='hand2')
            btn_crear.pack(pady=20)
            return

        frame_contenedor = tk.Frame(self.frame_principal, bg=self.colors['bg_primary'])
        frame_contenedor.pack(fill='both', expand=True)

        canvas = tk.Canvas(frame_contenedor, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # --- Wrapper y frame de lista dentro del canvas ---
        wrapper = tk.Frame(canvas, bg=self.colors['bg_primary'])
        # Creamos la ventana del canvas y guardamos su id para poder moverla (centrarla)
        window_id = canvas.create_window((0, 0), window=wrapper, anchor="n")

        # --- Contenedor de tarjetas (grid) ---
        frame_lista = tk.Frame(wrapper, bg=self.colors['bg_primary'])
        frame_lista.pack(pady=20)

        def _on_configure(event=None):
            """
            Centrar el contenido dentro del canvas cuando cambie tamaño.
            Se ajusta la coordenada x de la ventana creada en el canvas.
            """
            try:
                canvas_width = canvas.winfo_width()
                # solicitar ancho requerido del wrapper (que contiene frame_lista)
                wrapper.update_idletasks()
                frame_width = wrapper.winfo_reqwidth()
                x_offset = max((canvas_width - frame_width) // 2, 0)
                canvas.coords(window_id, x_offset, 0)
                canvas.configure(scrollregion=canvas.bbox("all"))
            except Exception:
                # en caso de que algo no esté listo aún, ignorar errores temporales
                pass

        # Bind para mantener centrado al redimensionar y cuando se actualice el contenido
        canvas.bind("<Configure>", _on_configure)
        wrapper.bind("<Configure>", _on_configure)
        frame_lista.bind("<Configure>", _on_configure)

        # Soporte de scroll con rueda del mouse
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        frame_lista.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Mostrar los bingos en filas de 2 en 2
        columnas = 2
        for i, bingo in enumerate(self.bingos):
            fila = i // columnas
            columna = i % columnas

            frame_bingo = tk.Frame(frame_lista, 
                                bg=self.colors['bg_card'],
                                relief='flat',
                                bd=1,
                                padx=25, 
                                pady=20)
            frame_bingo.grid(row=fila, column=columna, padx=15, pady=15, sticky='n')

            frame_header = tk.Frame(frame_bingo, bg=self.colors['bg_card'])
            frame_header.pack(fill='x')

            lbl_nombre = tk.Label(frame_header,
                text=f"🎯 {bingo.nombre}",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['accent_primary']
            )
            lbl_nombre.pack(side='left')

            cartones_vendidos = len(bingo.obtener_cartones_vendidos())
            porcentaje = (cartones_vendidos / bingo.cantidad_cartones) * 100 if bingo.cantidad_cartones > 0 else 0
            
            badge_frame = tk.Frame(frame_header, bg='#2d2d4d', relief='flat', bd=1)
            badge_frame.pack(side='right', padx=10)
            
            lbl_badge = tk.Label(badge_frame,
                text=f"{porcentaje:.1f}% Vendido",
                font=('Segoe UI', 10, 'bold'),
                bg='#2d2d4d',
                fg=self.colors['accent_primary'],
                padx=10,
                pady=5
            )
            lbl_badge.pack()

            frame_info = tk.Frame(frame_bingo, bg=self.colors['bg_card'])
            frame_info.pack(fill='x', pady=(10, 0))

            cartones_vendidos = len(bingo.obtener_cartones_vendidos())
            cartones_apartados = len(bingo.obtener_cartones_apartados())

            detalles = [
                f"📊 Cartones: {cartones_vendidos}/{bingo.cantidad_cartones}",
                f"⏳ Apartados: {cartones_apartados}",
                f"💰 Precio: ${bingo.precio_carton:,.2f}",
                f"💵 Ganancias: ${bingo.obtener_ganancias():,.2f}"
            ]

            for detalle in detalles:
                lbl_detalle = tk.Label(frame_info,
                    text=detalle,
                    font=('Segoe UI', 10),
                    bg=self.colors['bg_card'],
                    fg=self.colors['text_secondary']
                )
                lbl_detalle.pack(side='left', padx=(0, 15))

            frame_botones = tk.Frame(frame_bingo, bg=self.colors['bg_card'])
            frame_botones.pack(fill='x', pady=(15, 0))

            botones = [
                ("📊 ABRIR", self.abrir_bingo, self.colors['accent_secondary']),
                ("👥 ASIGNACIONES", self.ver_asignaciones, '#9b59b6'),
                ("📄 PDF", lambda b=bingo: b.exportar_pdf(), '#FF9800'),
                ("🗑️ ELIMINAR", self.eliminar_bingo, self.colors['accent_danger'])
            ]

            for texto, comando, color in botones:
                btn = tk.Button(frame_botones,
                    text=texto,
                    command=lambda b=bingo, c=comando: c(b),
                    font=('Segoe UI', 10, 'bold'),
                    bg=color,
                    fg='white',
                    padx=15,
                    pady=8,
                    relief='flat',
                    cursor='hand2',
                    bd=0
                )
                btn.pack(side='left', padx=5)

        # Asegurar que las columnas tengan el mismo peso
        for c in range(columnas):
            frame_lista.grid_columnconfigure(c, weight=1)

    def abrir_bingo(self, bingo):
        self.controlador.mostrar_vista("vista_tablas", {"bingo": bingo})

    def ver_asignaciones(self, bingo):
        self.controlador.mostrar_vista("vista_asignaciones", {"bingo": bingo})

    def eliminar_bingo(self, bingo):
        if messagebox.askyesno("Confirmar Eliminación",
            f"¿Estás seguro de eliminar el bingo '{bingo.nombre}'?\n\n"
            f"Esta acción no se puede deshacer y se perderán todos los datos."):
            if bingo.eliminar():
                self.bingos.remove(bingo)
                messagebox.showinfo("Éxito", f"Bingo '{bingo.nombre}' eliminado correctamente")
                self.mostrar_lista_bingos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el bingo")

    def crear_bingo(self):
        nombre = self.entry_nombre.get().strip()
        cartones_text = self.entry_cartones.get().strip()
        precio_text = self.entry_precio.get().strip()

        if not nombre:
            messagebox.showerror("Error", "❌ Por favor ingresa un nombre para el bingo")
            return

        try:
            cantidad_cartones = int(cartones_text)
            if cantidad_cartones <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "❌ La cantidad de cartones debe ser un número válido mayor a 0")
            return

        try:
            precio_carton = float(precio_text)
            if precio_carton < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "❌ El precio debe ser un número válido mayor o igual a 0")
            return

        for bingo_existente in self.bingos:
            if bingo_existente.nombre.lower() == nombre.lower():
                messagebox.showerror("Error", f"❌ Ya existe un bingo con el nombre '{nombre}'")
                return

        nuevo_bingo = Bingo(nombre, cantidad_cartones, precio_carton)
        self.bingos.append(nuevo_bingo)

        messagebox.showinfo("Éxito",
            f"✅ Bingo '{nombre}' creado exitosamente!\n\n"
            f"🎫 Cartones: {cantidad_cartones}\n"
            f"💰 Precio: ${precio_carton:,.2f}\n"
            f"💵 Ganancia potencial: ${cantidad_cartones * precio_carton:,.2f}")

        self.controlador.mostrar_vista("vista_tablas", {"bingo": nuevo_bingo})

    def volver_menu(self):
        self.controlador.mostrar_vista("menu_principal")

    def mostrar(self, datos=None):
        self.frame.pack(fill="both", expand=True)
        self.mostrar_lista_bingos()

    def ocultar(self):
        self.frame.pack_forget()
