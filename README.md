# 🧯 Sistema de Inventario de Extintores y equipos contra incendio

Sistema de gestión e inventario de extintores y equipos de seguridad desarrollado con Python y Tkinter. Permite registrar, consultar, actualizar y exportar información de extintores de manera eficiente.

## 📋 Descripción

Esta aplicación de escritorio permite gestionar un inventario completo de extintores y otros equipos de seguridad contra incendios. Incluye funcionalidades para:

- ✅ Agregar nuevos extintores con asignación automática de números
- 🔍 Buscar y filtrar por número, estado, fecha y ubicación
- ✏️ Actualizar información de extintores existentes
- 🗑️ Eliminar registros
- 📊 Exportar inventario a Excel (.xlsx) o PDF
- 📥 Importar registros desde archivos Excel
- 📅 Selector de fechas con calendario integrado
- 💰 Gestión de precios y capacidades
- 📈 Visualización de totales y últimos registros

## 🚀 Características Principales

- **Interfaz gráfica intuitiva** con Tkinter
- **Base de datos SQLite** para almacenamiento local
- **Tipos de extintores soportados**: PQS-ABC, PQS-BC, Agente Limpio, CO2, H2O, Espuma, N2, y más
- **Estados configurables**: Listo, En Mantenimiento, Usado, En recarga, Retirado, Reemplazado
- **Múltiples capacidades**: desde 5 lbs hasta 7700 gal
- **Exportación flexible** a Excel y PDF
- **Importación masiva** desde archivos Excel
- **Filtros de búsqueda** por múltiples criterios
- **Soporte para PyInstaller** para crear ejecutables

## 📦 Requisitos del Sistema

- Python 3.7 o superior
- Sistema operativo: Windows, Linux o macOS

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <https://github.com/Pipebc20/Inventario.git>
cd inventario-extintores
```

### 2. Instalar dependencias

Ejecuta el siguiente comando para instalar todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

O instala las librerías manualmente:

```bash
pip install pandas
pip install tkcalendar
pip install openpyxl
pip install reportlab
```

## 📚 Librerías Necesarias

### Librerías principales:

- **pandas** - Manejo de datos y exportación a Excel
- **tkcalendar** - Widget de calendario para selección de fechas
- **openpyxl** - Lectura y escritura de archivos Excel (.xlsx)
- **reportlab** - Generación de archivos PDF

### Librerías estándar de Python (ya incluidas):

- **tkinter** - Interfaz gráfica (incluida en Python)
- **sqlite3** - Base de datos (incluida en Python)
- **os, sys** - Utilidades del sistema
- **datetime** - Manejo de fechas

## ▶️ Uso

### Ejecutar la aplicación:

```bash
python inventario_extintores.py
```

### Funciones principales:

1. **Agregar extintor**: Click en "Agregar" y completa los campos
2. **Buscar**: Utiliza los filtros superiores por número, estado, fecha o ubicación
3. **Actualizar**: Selecciona un extintor y click en "Actualizar"
4. **Eliminar**: Selecciona un extintor y click en "Eliminar"
5. **Consultar**: Selecciona un extintor y click en "Consultar" para ver detalles
6. **Exportar**: Click en "Exportar archivo" y selecciona el formato (.xlsx o .pdf)
7. **Importar**: Click en "Importar archivo" y selecciona un archivo Excel

## 📁 Estructura del Proyecto

```
inventario-extintores/
│
├── inventario_extintores.py      # Código principal
├── inventario_extintores.db      # Base de datos SQLite (se crea automáticamente)
├── Logo_Inventario.ico           # Icono de la aplicación (opcional)
├── Logo_Inventario.png           # Icono alternativo (opcional)
├── README.md                     # Este archivo
└── requirements.txt              # Dependencias del proyecto
```

## 🗃️ Base de Datos

La aplicación utiliza SQLite con la siguiente estructura:

**Tabla: extintores**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID autoincremental (clave primaria) |
| numero | INTEGER | Número de extintor asignado |
| ubicacion | TEXT | Ubicación del extintor |
| serie | TEXT | Número de serie |
| tipo | TEXT | Tipo de extintor |
| estado | TEXT | Estado actual |
| capacidad | TEXT | Capacidad del extintor |
| precio | REAL | Precio del extintor |
| fecha_inspeccion | TEXT | Fecha de inspección |
| fecha_registro | TEXT | Fecha de registro en el sistema |

## 📤 Exportación e Importación

### Exportar a Excel:
El archivo incluirá todas las columnas del inventario con formato de tabla.

### Exportar a PDF:
Requiere la librería `reportlab`. El archivo incluye una tabla formateada con todos los registros.

### Importar desde Excel:
El archivo debe contener las columnas: `Ubicacion`, `Num_serie` (o `serie`), `Tipo`, `Estado`, `Capacidad`, `Precio`, `Fecha_Inspeccion` (o `Fecha`).

## 🔨 Crear Ejecutable con PyInstaller

Para crear un archivo ejecutable (.exe):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=Logo_Inventario.ico inventario_extintores.py
```

El ejecutable se generará en la carpeta `dist/`.

## 👤 Autor

**- [@Pipebc20](https://github.com/Pipebc20)**

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🐛 Reporte de Bugs

Si encuentras algún bug, por favor abre un issue en el repositorio.

## 📞 Soporte

Para soporte o preguntas, contacta al autor o abre un issue en el repositorio.

---
