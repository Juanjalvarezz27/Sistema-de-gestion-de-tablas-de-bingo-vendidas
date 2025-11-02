import json
import os
import random
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
import webbrowser

# Constantes para generación de cartones
LETRAS_BINGO = ['B', 'I', 'N', 'G', 'O']
RANGOS_BINGO = {
    'B': list(range(1, 16)),
    'I': list(range(16, 31)),
    'N': list(range(31, 46)),
    'G': list(range(46, 61)),
    'O': list(range(61, 76))
}

class Bingo:
    def __init__(self, nombre, cantidad_cartones, precio_carton=0):
        self.nombre = nombre
        self.cantidad_cartones = cantidad_cartones
        self.precio_carton = precio_carton
        self.cartones_vendidos = {}
        self.cartones_apartados = {}
        self.cartones_generados = {}  # Nuevo: almacenar los cartones generados
        
        # Cargar datos existentes inmediatamente
        self.cargar_datos()
        
        # Generar cartones si no existen
        if not self.cartones_generados:
            self.generar_cartones()

    def obtener_ruta_archivo(self):
        """Obtener la ruta del archivo para este bingo (interno)"""
        from utils.helpers import crear_directorio_bingos
        directorio_bingos = crear_directorio_bingos()

        # Crear un nombre de archivo único y seguro
        nombre_seguro = "".join(c for c in self.nombre if c.isalnum() or c in (' ', '-', '_')).rstrip()
        nombre_seguro = nombre_seguro.replace(' ', '_')
        if not nombre_seguro:
            nombre_seguro = "bingo"

        nombre_archivo = f"{nombre_seguro}.json"
        return directorio_bingos / nombre_archivo

    def cargar_datos(self):
        """Cargar datos desde archivo JSON interno"""
        archivo = self.obtener_ruta_archivo()
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.cartones_vendidos = datos.get('cartones_vendidos', {})
                    self.cartones_apartados = datos.get('cartones_apartados', {})
                    self.cartones_generados = datos.get('cartones_generados', {})  # Nuevo
                    if 'precio_carton' in datos:
                        self.precio_carton = datos['precio_carton']
                    if 'cantidad_cartones' in datos:
                        self.cantidad_cartones = datos['cantidad_cartones']
                    if 'nombre' in datos:
                        self.nombre = datos['nombre']
            except Exception as e:
                print(f"Error cargando datos: {e}")
                self.cartones_vendidos = {}
                self.cartones_apartados = {}
                self.cartones_generados = {}
        else:
            # Si no existe el archivo, guardar los datos iniciales
            self.guardar_datos()

    def guardar_datos(self):
        """Guardar datos en archivo JSON interno"""
        try:
            archivo = self.obtener_ruta_archivo()
            datos = {
                'nombre': self.nombre,
                'cantidad_cartones': self.cantidad_cartones,
                'precio_carton': self.precio_carton,
                'cartones_vendidos': self.cartones_vendidos,
                'cartones_apartados': self.cartones_apartados,
                'cartones_generados': self.cartones_generados,  # Nuevo
                'ultima_actualizacion': datetime.now().isoformat()
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando datos: {e}")

    def generar_cartones(self):
        """Generar todos los cartones del bingo"""
        self.cartones_generados = {}
        
        for numero_carton in range(1, self.cantidad_cartones + 1):
            carton = self.generar_carton_individual(numero_carton)
            self.cartones_generados[str(numero_carton)] = carton
        
        self.guardar_datos()

    def generar_carton_individual(self, numero_carton):
        """Generar un cartón individual con números válidos"""
        carton = {}
        
        # Generar números para cada columna
        for letra in LETRAS_BINGO:
            # Seleccionar 5 números únicos para cada columna
            numeros_columna = random.sample(RANGOS_BINGO[letra], 5)
            for fila in range(5):
                carton[f'{letra}{fila+1}'] = numeros_columna[fila]
        
        # Casilla FREE (N3)
        carton['N3'] = 'FREE'
        carton['ID_Carton'] = numero_carton
        
        return carton

    def obtener_carton(self, numero):
        """Obtener los números de un cartón específico"""
        numero_str = str(numero)
        if numero_str in self.cartones_generados:
            return self.cartones_generados[numero_str]
        else:
            # Si no existe, generar uno nuevo
            carton = self.generar_carton_individual(numero)
            self.cartones_generados[numero_str] = carton
            self.guardar_datos()
            return carton

    def obtener_estado_carton(self, numero):
        """Obtener estado de un cartón específico"""
        numero_str = str(numero)
        if numero_str in self.cartones_vendidos:
            return self.cartones_vendidos[numero_str]
        elif numero_str in self.cartones_apartados:
            return self.cartones_apartados[numero_str]
        else:
            return {'vendido': False, 'apartado': False, 'nombre': '', 'fecha_asignacion': ''}

    def obtener_cartones_vendidos(self):
        """Obtener lista de cartones vendidos"""
        return [int(num) for num in self.cartones_vendidos.keys()]

    def obtener_cartones_apartados(self):
        """Obtener lista de cartones apartados"""
        return [int(num) for num in self.cartones_apartados.keys()]

    def obtener_ganancias(self):
        """Calcular ganancias totales"""
        cartones_vendidos = len(self.obtener_cartones_vendidos())
        return cartones_vendidos * self.precio_carton

    def asignar_carton(self, numero, nombre):
        """Marcar cartón como vendido"""
        numero_str = str(numero)
        # Remover de apartados si estaba ahí
        if numero_str in self.cartones_apartados:
            del self.cartones_apartados[numero_str]

        self.cartones_vendidos[numero_str] = {
            'vendido': True,
            'apartado': False,
            'nombre': nombre,
            'fecha_asignacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.guardar_datos()
        return True  # Añadido return True para indicar éxito

    def apartar_carton(self, numero, nombre):
        """Marcar cartón como apartado"""
        numero_str = str(numero)
        # Remover de vendidos si estaba ahí
        if numero_str in self.cartones_vendidos:
            del self.cartones_vendidos[numero_str]

        self.cartones_apartados[numero_str] = {
            'vendido': False,
            'apartado': True,
            'nombre': nombre,
            'fecha_asignacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.guardar_datos()
        return True  # Añadido return True para indicar éxito

    def vender_carton(self, numero, nombre):
        """Cambiar cartón de apartado a vendido - CORREGIDO"""
        numero_str = str(numero)
        
        # Verificar que el cartón esté apartado
        if numero_str not in self.cartones_apartados:
            print(f"Error: Cartón {numero} no está apartado")
            return False
        
        # Obtener los datos del cartón apartado
        carton_apartado = self.cartones_apartados[numero_str]
        
        # Remover de apartados
        del self.cartones_apartados[numero_str]
        
        # Agregar a vendidos con los mismos datos pero actualizando el estado
        self.cartones_vendidos[numero_str] = {
            'vendido': True,
            'apartado': False,
            'nombre': carton_apartado['nombre'],  # Usar el nombre existente
            'fecha_asignacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.guardar_datos()
        return True  # Retornar True para indicar éxito

    def liberar_carton(self, numero):
        """Liberar un cartón (quitar asignación)"""
        numero_str = str(numero)
        if numero_str in self.cartones_vendidos:
            del self.cartones_vendidos[numero_str]
        if numero_str in self.cartones_apartados:
            del self.cartones_apartados[numero_str]
        self.guardar_datos()
        return True

    def resetear(self):
        """Resetear todos los cartones a disponibles"""
        self.cartones_vendidos = {}
        self.cartones_apartados = {}
        self.guardar_datos()

    def eliminar(self):
        """Eliminar completamente el bingo"""
        try:
            archivo = self.obtener_ruta_archivo()
            if archivo.exists():
                os.remove(archivo)
                return True
        except:
            return False

    def exportar_pdf(self):
        """Exportar reporte en PDF (sí va a Descargas)"""
        try:
            from utils.helpers import obtener_carpeta_descargas
            downloads_path = obtener_carpeta_descargas()

            nombre_archivo = f"reporte_{self.nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            ruta_pdf = downloads_path / nombre_archivo

            # Crear contenido HTML estilizado
            html_content = self.generar_html_estilizado()

            with open(ruta_pdf, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Abrir en el navegador para imprimir como PDF
            webbrowser.open(f'file://{ruta_pdf}')

            messagebox.showinfo("Éxito",
                f"📊 Reporte generado!\n\n"
                f"El archivo se abrirá en tu navegador.\n"
                f"Usa Ctrl+P para guardar como PDF.\n\n"
                f"💾 Guardado en: {ruta_pdf}")

        except Exception as e:
            messagebox.showerror("Error", f"Error generando PDF: {e}")

    def generar_html_estilizado(self):
        """Generar contenido HTML estilizado para el reporte"""
        cartones_vendidos = self.obtener_cartones_vendidos()
        cartones_apartados = self.obtener_cartones_apartados()
        ganancias = self.obtener_ganancias()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Reporte - {self.nombre}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }}
                .header {{
                    text-align: center;
                    background: linear-gradient(135deg, #4CAF50, #45a049);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    border-left: 4px solid #4CAF50;
                }}
                .stat-card.apartados {{
                    border-left-color: #f39c12;
                }}
                .stat-card.disponibles {{
                    border-left-color: #3498db;
                }}
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #4CAF50;
                }}
                .apartados .stat-number {{
                    color: #f39c12;
                }}
                .disponibles .stat-number {{
                    color: #3498db;
                }}
                .cartones-list {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    margin-top: 20px;
                }}
                .carton-item {{
                    background: white;
                    margin: 10px 0;
                    padding: 15px;
                    border-radius: 8px;
                    border-left: 4px solid #2196F3;
                }}
                .carton-item.apartado {{
                    border-left-color: #f39c12;
                    background: #fff9e6;
                }}
                .ganancias {{
                    background: linear-gradient(135deg, #FF9800, #F57C00);
                    color: white;
                    padding: 25px;
                    border-radius: 10px;
                    text-align: center;
                    margin-top: 20px;
                }}
                .ganancias-total {{
                    font-size: 2.5em;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-style: italic;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 {self.nombre}</h1>
                    <p>Reporte de Gestión - {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                </div>

                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{self.cantidad_cartones}</div>
                        <div>Total Cartones</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(cartones_vendidos)}</div>
                        <div>Cartones Vendidos</div>
                    </div>
                    <div class="stat-card apartados">
                        <div class="stat-number">{len(cartones_apartados)}</div>
                        <div>Cartones Apartados</div>
                    </div>
                    <div class="stat-card disponibles">
                        <div class="stat-number">{self.cantidad_cartones - len(cartones_vendidos) - len(cartones_apartados)}</div>
                        <div>Cartones Disponibles</div>
                    </div>
                </div>

                <div class="ganancias">
                    <h2>💰 GANANCIAS TOTALES</h2>
                    <div class="ganancias-total">${ganancias:,.2f}</div>
                    <p>Precio por cartón: ${self.precio_carton:,.2f}</p>
                </div>

                <h2>📋 Cartones Vendidos</h2>
                <div class="cartones-list">
        """

        # Cartones vendidos
        if cartones_vendidos:
            # Agrupar cartones por persona
            personas = {}
            for num in cartones_vendidos:
                estado = self.obtener_estado_carton(num)
                nombre = estado.get('nombre', 'Sin nombre')
                if nombre not in personas:
                    personas[nombre] = []
                personas[nombre].append(num)

            for nombre, cartones in sorted(personas.items()):
                cartones_str = ", ".join(map(str, sorted(cartones)))
                html += f"""
                    <div class="carton-item">
                        <strong>👤 {nombre}</strong><br>
                        <span>Cartones: {cartones_str}</span><br>
                        <small>Cantidad: {len(cartones)} | Total: ${len(cartones) * self.precio_carton:,.2f}</small>
                    </div>
                """
        else:
            html += "<p style='text-align: center; color: #666;'>No hay cartones vendidos</p>"

        html += """
                </div>

                <h2>⏳ Cartones Apartados</h2>
                <div class="cartones-list">
        """

        # Cartones apartados
        if cartones_apartados:
            # Agrupar cartones por persona
            personas = {}
            for num in cartones_apartados:
                estado = self.obtener_estado_carton(num)
                nombre = estado.get('nombre', 'Sin nombre')
                if nombre not in personas:
                    personas[nombre] = []
                personas[nombre].append(num)

            for nombre, cartones in sorted(personas.items()):
                cartones_str = ", ".join(map(str, sorted(cartones)))
                html += f"""
                    <div class="carton-item apartado">
                        <strong>👤 {nombre}</strong><br>
                        <span>Cartones: {cartones_str}</span><br>
                        <small>Cantidad: {len(cartones)} | Estado: ⏳ APARTADO</small>
                    </div>
                """
        else:
            html += "<p style='text-align: center; color: #666;'>No hay cartones apartados</p>"

        html += """
                </div>

                <div class="footer">
                    <p>Generado automáticamente por Sistema de Bingos Profesional</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def exportar_tablas_excel(self):
        """Exportar todas las tablas del bingo a Excel"""
        try:
            from utils.helpers import obtener_carpeta_descargas
            import pandas as pd
            
            downloads_path = obtener_carpeta_descargas()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            excel_file = downloads_path / f"Tablas_Bingo_{self.nombre}_{timestamp}.xlsx"
            
            # Crear lista para almacenar todos los cartones
            cartones_data = []
            
            for numero in range(1, self.cantidad_cartones + 1):
                carton = self.obtener_carton(numero)
                estado = self.obtener_estado_carton(numero)
                
                # Crear fila para este cartón
                fila_carton = {
                    'ID_Carton': numero,
                    'Estado': 'VENDIDO' if estado.get('vendido') else 'APARTADO' if estado.get('apartado') else 'DISPONIBLE',
                    'Nombre_Asignado': estado.get('nombre', ''),
                    'Fecha_Asignacion': estado.get('fecha_asignacion', '')
                }
                
                # Añadir números del cartón
                letras = ['B', 'I', 'N', 'G', 'O']
                for letra in letras:
                    for fila in range(1, 6):
                        clave = f'{letra}{fila}'
                        fila_carton[clave] = carton.get(clave, '')
                
                cartones_data.append(fila_carton)
            
            # Crear DataFrame y exportar a Excel
            df = pd.DataFrame(cartones_data)
            df.to_excel(excel_file, index=False)
            
            messagebox.showinfo(
                "✅ Exportación Exitosa",
                f"📊 Tablas exportadas a Excel correctamente!\n\n"
                f"📁 Archivo: {excel_file.name}\n"
                f"🎫 Cartones exportados: {self.cantidad_cartones}\n"
                f"💾 Ubicación: {downloads_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error exportando tablas a Excel: {str(e)}")