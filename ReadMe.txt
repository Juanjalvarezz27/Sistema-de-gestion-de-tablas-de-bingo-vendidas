# 🎫 Sistema de Gestión de Tablas Vendidas

Sistema portable para gestionar la venta de 200 números de tablas/tickets con interfaz gráfica moderna. Desarrollado en Python con interfaz intuitiva y funcionalidades completas de gestión.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/Licencia-MIT-green.svg)
![Platform](https://img.shields.io/badge/Plataforma-Windows%20|%20Linux%20|%20Mac-orange.svg)

## ✨ Características Principales

- ✅ **200 tickets numerados** del 1 al 200
- ✅ **Interfaz visual intuitiva** con colores (Verde=Vendido, Azul=Disponible)
- ✅ **Asignación de tickets** a personas con modales interactivos
- ✅ **Cancelación de ventas** individuales
- ✅ **Generación de reportes** en formato TXT
- ✅ **Sistema completamente portable** - no necesita instalación
- ✅ **Persistencia automática** de datos
- ✅ **Interfaz en español** y fácil de usar

## 🚀 Instalación y Ejecución

### Opción 1: Usar Ejecutable (Recomendado para usuarios finales)

1. **Descarga** el archivo `SistemaGestorTablas.exe` desde [Releases](https://github.com/tuusuario/sistema-gestion-tablas/releases)
2. **Ejecuta** el archivo haciendo doble clic
3. **¡Listo!** El programa se abre automáticamente

### Opción 2: Ejecutar desde Código Fuente

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/sistema-gestion-tablas.git
cd sistema-gestion-tablas

# Instalar dependencias
pip install -r requirements.txt

📖 Guía de Uso
🎫 Pestaña "Tablas Numeradas"
Botones Azules: Tickets disponibles

Botones Verdes: Tickets vendidos (muestran nombre asignado)

Asignar Ticket:

Clic en cualquier botón azul

Ingresar nombre completo en el modal

Presionar "✅ ASIGNAR" o Enter

Ver Información:

Clic en botón verde para ver detalles y opción de cancelar venta

👥 Pestaña "Asignaciones"
Vista organizada de todas las personas con sus tickets

Cancelación individual de ventas

Descarga de reportes completos

📊 Funcionalidades Adicionales
Contador en tiempo real de tickets vendidos

Reset completo del sistema (con confirmación)

Descarga de reportes en formato TXT

Persistencia automática de datos

📁 Estructura del Proyecto
text
sistema-gestion-tablas/
│
├── sistema_portable.py          # Código fuente principal
├── SistemaGestorTablas.exe      # Ejecutable (en releases)
├── requirements.txt             # Dependencias
├── tablas_vendidas.json         # Base de datos (se crea automáticamente)
└── README.md                    # Este archivo
🛠️ Desarrollo
Requisitos para Desarrollo
Python 3.7 o superior

Librerías: tkinter (incluida en Python)

Compilar Ejecutable
bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar a .exe
pyinstaller --onefile --windowed --name="SistemaGestorTablas" sistema_portable.py
El ejecutable se generará en la carpeta dist/

📄 Formatos de Archivos Generados
Tickets Disponibles
txt
==================================================
LISTA DE TICKETS DISPONIBLES
==================================================
Fecha de generación: 2024-01-15 14:30:25
Total disponibles: 150/200

TICKETS DISPONIBLES:
--------------------------------------------------
  1,   2,   3,   4,   5,   6,   7,   8,   9,  10
 11,  12,  13,  14,  15,  16,  17,  18,  19,  20
...
Reporte de Asignaciones
txt
==================================================
REPORTE DE ASIGNACIONES DE TICKETS
==================================================
👤 Juan Pérez:
   Tickets: 25, 67, 89
   Cantidad: 3 ticket(s)

👤 María García:
   Tickets: 12, 45
   Cantidad: 2 ticket(s)
🔄 Transferir a Otra Computadora
Método Simple:
Copiar solo SistemaGestorTablas.exe

Ejecutar en la nueva computadora

Con Datos Existentes:
Copiar SistemaGestorTablas.exe

Copiar tablas_vendidas.json (opcional, para llevar los datos)

📝 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor:

Haz un Fork del proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

📞 Soporte
Si encuentras algún problema o tienes preguntas:

Abre un Issue

Contacta al desarrollador: tu-email@dominio.com

🎉 Agradecimientos
Desarrollado con Python y Tkinter

Iconos y emojis para mejor experiencia de usuario

Diseño responsive y accesible



# Ejecutar la aplicación
python sistema_portable.py

