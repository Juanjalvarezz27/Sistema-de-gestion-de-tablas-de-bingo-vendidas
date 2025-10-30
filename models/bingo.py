import json
import os
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
import webbrowser

class Bingo:
    def __init__(self, nombre, cantidad_cartones, precio_carton=0):
        self.nombre = nombre
        self.cantidad_cartones = cantidad_cartones
        self.precio_carton = precio_carton
        self.cartones_vendidos = {}
        
        # Cargar datos existentes inmediatamente
        self.cargar_datos()
    
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
                    if 'precio_carton' in datos:
                        self.precio_carton = datos['precio_carton']
                    if 'cantidad_cartones' in datos:
                        self.cantidad_cartones = datos['cantidad_cartones']
                    if 'nombre' in datos:
                        self.nombre = datos['nombre']
            except Exception as e:
                print(f"Error cargando datos: {e}")
                self.cartones_vendidos = {}
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
                'ultima_actualizacion': datetime.now().isoformat()
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando datos: {e}")
    
    # ... (el resto de los métodos se mantienen igual)
    def obtener_estado_carton(self, numero):
        """Obtener estado de un cartón específico"""
        return self.cartones_vendidos.get(str(numero), {})
    
    def obtener_cartones_vendidos(self):
        """Obtener lista de cartones vendidos"""
        return [int(num) for num, estado in self.cartones_vendidos.items() if estado.get('vendido', False)]
    
    def obtener_ganancias(self):
        """Calcular ganancias totales"""
        cartones_vendidos = len(self.obtener_cartones_vendidos())
        return cartones_vendidos * self.precio_carton
    
    def asignar_carton(self, numero, nombre):
        """Asignar un cartón a una persona"""
        self.cartones_vendidos[str(numero)] = {
            'vendido': True,
            'nombre': nombre,
            'fecha_asignacion': datetime.now().isoformat()
        }
        self.guardar_datos()
    
    def liberar_carton(self, numero):
        """Liberar un cartón asignado"""
        if str(numero) in self.cartones_vendidos:
            del self.cartones_vendidos[str(numero)]
            self.guardar_datos()
            return True
        return False
    
    def resetear(self):
        """Resetear todos los cartones"""
        self.cartones_vendidos = {}
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
                    grid-template-columns: repeat(3, 1fr);
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
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #4CAF50;
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
                    <div class="stat-card">
                        <div class="stat-number">{self.cantidad_cartones - len(cartones_vendidos)}</div>
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
                
                <div class="footer">
                    <p>Generado automáticamente por Sistema de Bingos Profesional</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html