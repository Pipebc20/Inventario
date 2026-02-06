import sqlite3
import pandas as pd
import os, sys
from tkinter import Tk, Frame, Label, Entry, Button, ttk, messagebox, Toplevel, PhotoImage, filedialog
from tkcalendar import Calendar
from datetime import datetime

# ---------- Recursos empaquetados (PyInstaller) ----------
def resource_path(relative_path: str) -> str:
    """Obtiene la ruta absoluta del recurso (soporta PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class InventarioExtintoresGUI:
    # Opciones para los Combobox
    TIPOS_EXTINTOR = ["Extintor PQS-ABC", "Extintor PQS-BC", "Agente Limpio", "CO2", "H2O", "Espuma", "N2", "Otro Equipo"]
    ESTADOS_EXTINTOR = ["Listo", "En Mantenimiento", "Usado", "En recarga", "Retirado", "Reemplazado"]
    CAPACIDADES_EXTINTOR = ["5 lbs", "10 lbs", "15 lbs", "20 lbs", "30 lbs", "80 lbs", "100 lbs", "150 lbs", "200 lbs", "2.5 gal", "3700 gal", "7700 gal"]

    def __init__(self, root):
        self.root = root
        self.root.title("Inventario de Ingeseg")
        self.conexion = sqlite3.connect('inventario_extintores.db')
        self.cursor = self.conexion.cursor()
        self.crear_tabla()
        self.asegurar_columnas()
        self.crear_interfaz()

    def crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS extintores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER NOT NULL,
                ubicacion TEXT NOT NULL,
                serie TEXT NOT NULL,
                tipo TEXT NOT NULL,
                estado TEXT NOT NULL,
                capacidad TEXT DEFAULT '',
                precio REAL DEFAULT 0.0,
                fecha_inspeccion TEXT NOT NULL,
                fecha_registro TEXT NOT NULL
            )
        ''')
        self.conexion.commit()

    def asegurar_columnas(self):
        self.cursor.execute("PRAGMA table_info(extintores)")
        columnas = [col[1] for col in self.cursor.fetchall()]
        if 'precio' not in columnas:
            print("Agregando columna 'precio' a la tabla extintores...")
            self.cursor.execute("ALTER TABLE extintores ADD COLUMN precio REAL DEFAULT 0.0")
            self.conexion.commit()
        if 'capacidad' not in columnas:
            print("Agregando columna 'capacidad' a la tabla extintores...")
            self.cursor.execute("ALTER TABLE extintores ADD COLUMN capacidad TEXT DEFAULT ''")
            self.conexion.commit()

    def crear_interfaz(self):
        self.totales_frame = Frame(self.root)
        self.totales_frame.pack(pady=5)
        self.actualizar_totales()

        self.filtros_frame = Frame(self.root)
        self.filtros_frame.pack(pady=5)
        Label(self.filtros_frame, text="Buscar por número:").pack(side="left")
        self.entry_numero = Entry(self.filtros_frame)
        self.entry_numero.pack(side="left")
        Button(self.filtros_frame, text="Buscar", command=self.filtrar_numero).pack(side="left")
        Label(self.filtros_frame, text="Buscar por estado:").pack(side="left")
        self.entry_estado = Entry(self.filtros_frame)
        self.entry_estado.pack(side="left")
        Button(self.filtros_frame, text="Buscar", command=self.filtrar_estado).pack(side="left")
        Label(self.filtros_frame, text="Buscar por fecha (DD/MM/AAAA):").pack(side="left")
        self.entry_fecha = Entry(self.filtros_frame)
        self.entry_fecha.pack(side="left")
        Button(self.filtros_frame, text="Buscar", command=self.filtrar_fecha).pack(side="left")
        Label(self.filtros_frame, text="Buscar por ubicación:").pack(side="left")
        self.entry_ubicacion = Entry(self.filtros_frame)
        self.entry_ubicacion.pack(side="left")
        Button(self.filtros_frame, text="Buscar", command=self.filtrar_ubicacion).pack(side="left")

        # Frame para contener Treeview y Scrollbars
        tree_frame = Frame(self.root)
        tree_frame.pack(pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("Numero", "Ubicacion", "Num_serie", "Tipo", "Estado", "Capacidad", "Precio", "Fecha_Inspección"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.botones_frame = Frame(self.root)
        self.botones_frame.pack(pady=5)
        Button(self.botones_frame, text="Agregar", command=self.abrir_ventana_agregar).pack(side="left")
        Button(self.botones_frame, text="Eliminar", command=self.eliminar_extintor).pack(side="left")
        Button(self.botones_frame, text="Actualizar", command=self.abrir_ventana_actualizar).pack(side="left")
        Button(self.botones_frame, text="Consultar", command=self.abrir_ventana_consultar).pack(side="left")
        Button(self.botones_frame, text="Importar archivo", command=self.importar_archivo).pack(side="left")
        Button(self.botones_frame, text="Exportar archivo", command=self.exportar_archivo).pack(side="left")
        Button(self.botones_frame, text="Salir", command=self.root.quit).pack(side="left")

        self.consultar_extintores()

    def actualizar_totales(self):
        for widget in self.totales_frame.winfo_children():
            widget.destroy()
        self.cursor.execute("SELECT COUNT(*) FROM extintores")
        total = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT MAX(numero) FROM extintores")
        ultimo_registro = self.cursor.fetchone()[0] or "N/A"
        Label(self.totales_frame, text=f"Extintores y Equipos registrados: {total}").pack(side="left", padx=10)
        Label(self.totales_frame, text=f"Último registrado (Número): {ultimo_registro}").pack(side="left", padx=10)

    def obtener_siguiente_numero(self):
        self.cursor.execute("SELECT MAX(numero) FROM extintores")
        ultimo = self.cursor.fetchone()[0]
        return (ultimo + 1) if ultimo else 1

    def abrir_ventana_agregar(self):
        ventana = Toplevel(self.root)
        ventana.title("Agregar Extintor u Otro Equipo")
        ventana.geometry("450x750")
        ventana.resizable(True, True)

        numero = self.obtener_siguiente_numero()
        Label(ventana, text=f"Número asignado: {numero}", font=("Arial", 12, "bold")).pack(pady=5)
        # (botones ubicados al final de la ventana)

        # Crear campos normales
        Label(ventana, text="Ubicación:").pack(pady=5)
        entradas = {}
        entradas["Ubicación"] = Entry(ventana, width=35)
        entradas["Ubicación"].pack(pady=5)

        Label(ventana, text="Num_serie:").pack(pady=5)
        entradas["Num_serie"] = Entry(ventana, width=35)
        entradas["Num_serie"].pack(pady=5)

        # Combobox para Tipo
        Label(ventana, text="Tipo:").pack(pady=5)
        entradas["Tipo"] = ttk.Combobox(ventana, values=self.TIPOS_EXTINTOR, state="readonly", width=33)
        entradas["Tipo"].pack(pady=5)

        # Combobox para Estado
        Label(ventana, text="Estado:").pack(pady=5)
        entradas["Estado"] = ttk.Combobox(ventana, values=self.ESTADOS_EXTINTOR, state="readonly", width=33)
        entradas["Estado"].pack(pady=5)

        # Combobox para Capacidad
        Label(ventana, text="Capacidad:").pack(pady=5)
        entradas["Capacidad"] = ttk.Combobox(ventana, values=self.CAPACIDADES_EXTINTOR, state="readonly", width=33)
        entradas["Capacidad"].pack(pady=5)

        Label(ventana, text="Precio:").pack(pady=5)
        entradas["Precio"] = Entry(ventana, width=35)
        entradas["Precio"].pack(pady=5)

        Label(ventana, text="Fecha Inspección:").pack(pady=5)

        # -------- Calendario con fallback seguro --------
        def _crear_calendario_agregar():
            cal_local = Calendar(ventana, selectmode="day", date_pattern="dd/mm/yyyy")
            cal_local.pack(pady=5)
            return cal_local

        cal = None
        get_fecha = None
        try:
            cal = _crear_calendario_agregar()
            def get_fecha():
                return cal.get_date()
        except Exception as e:
            messagebox.showwarning("Aviso", f"No se pudo cargar el calendario.\nIngrese la fecha manualmente (DD/MM/AAAA).\n\nDetalle: {e}")
            fecha_entry = Entry(ventana)
            fecha_entry.pack(pady=5)
            fecha_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
            def get_fecha():
                return fecha_entry.get()

        def guardar():
            try:
                if not entradas["Tipo"].get():
                    messagebox.showwarning("Advertencia", "Por favor selecciona un Tipo.")
                    return
                if not entradas["Estado"].get():
                    messagebox.showwarning("Advertencia", "Por favor selecciona un Estado.")
                    return
                if not entradas["Capacidad"].get():
                    messagebox.showwarning("Advertencia", "Por favor selecciona una Capacidad.")
                    return
                ubicacion = entradas["Ubicación"].get()
                serie = entradas["Num_serie"].get()
                tipo = entradas["Tipo"].get()
                estado = entradas["Estado"].get()
                capacidad = entradas["Capacidad"].get()
                precio = float(entradas["Precio"].get())
                fecha_inspeccion = get_fecha() if get_fecha else datetime.now().strftime("%d/%m/%Y")
                self.cursor.execute('''
                    INSERT INTO extintores (numero, ubicacion, serie, tipo, estado, capacidad, precio, fecha_inspeccion, fecha_registro)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (numero, ubicacion, serie, tipo, estado, capacidad, precio, fecha_inspeccion, datetime.now().strftime("%Y-%m-%d")))
                self.conexion.commit()
                self.consultar_extintores()
                self.actualizar_totales()
                ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos.")

        # marco superior para botones (Guardar a la izquierda, Salir a la derecha)
        top_buttons = Frame(ventana)
        top_buttons.pack(fill="x", padx=8, pady=3)
        Button(top_buttons, text="Guardar", width=12, command=guardar).pack(side="left", padx=12)
        Button(top_buttons, text="Salir", width=12, command=ventana.destroy).pack(side="right", padx=12)

    def eliminar_extintor(self):
        selected = self.tree.selection()
        if selected:
            numero = self.tree.item(selected[0])["values"][0]
            self.cursor.execute("DELETE FROM extintores WHERE numero = ?", (numero,))
            self.conexion.commit()
            self.consultar_extintores()
            self.actualizar_totales()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un extintor u otro equipo para eliminar.")

    def abrir_ventana_actualizar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un extintor u otro equipo para actualizar.")
            return
        values = self.tree.item(selected[0])["values"]
        ventana = Toplevel(self.root)
        ventana.title("Actualizar Extintor")
        ventana.geometry("450x750")
        ventana.resizable(True, True)

        Label(ventana, text=f"Número: {values[0]}", font=("Arial", 12, "bold")).pack(pady=5)
        # (botones ubicados al final de la ventana)

        entradas = {}
        
        Label(ventana, text="Ubicación:").pack(pady=5)
        entradas["Ubicación"] = Entry(ventana, width=35)
        entradas["Ubicación"].insert(0, values[1])
        entradas["Ubicación"].pack(pady=5)

        Label(ventana, text="Num_serie:").pack(pady=5)
        entradas["Num_serie"] = Entry(ventana, width=35)
        entradas["Num_serie"].insert(0, values[2])
        entradas["Num_serie"].pack(pady=5)

        # Combobox para Tipo
        Label(ventana, text="Tipo:").pack(pady=5)
        entradas["Tipo"] = ttk.Combobox(ventana, values=self.TIPOS_EXTINTOR, state="readonly", width=33)
        entradas["Tipo"].set(values[3])
        entradas["Tipo"].pack(pady=5)

        # Combobox para Estado
        Label(ventana, text="Estado:").pack(pady=5)
        entradas["Estado"] = ttk.Combobox(ventana, values=self.ESTADOS_EXTINTOR, state="readonly", width=33)
        entradas["Estado"].set(values[4])
        entradas["Estado"].pack(pady=5)

        # Combobox para Capacidad
        Label(ventana, text="Capacidad:").pack(pady=5)
        entradas["Capacidad"] = ttk.Combobox(ventana, values=self.CAPACIDADES_EXTINTOR, state="readonly", width=33)
        entradas["Capacidad"].set(values[5])
        entradas["Capacidad"].pack(pady=5)

        Label(ventana, text="Precio:").pack(pady=5)
        entradas["Precio"] = Entry(ventana, width=35)
        entradas["Precio"].insert(0, values[6])
        entradas["Precio"].pack(pady=5)

        Label(ventana, text="Fecha Inspección:").pack(pady=5)

        # -------- Calendario con fallback seguro --------
        cal = None
        get_fecha = None
        try:
            cal = Calendar(ventana, selectmode="day", date_pattern="dd/mm/yyyy")
            cal.pack(pady=5)
            try:
                cal.selection_set(datetime.strptime(values[7], "%d/%m/%Y"))
            except Exception:
                pass
            def get_fecha():
                return cal.get_date()
        except Exception as e:
            messagebox.showwarning("Aviso", f"No se pudo cargar el calendario.\nIngrese la fecha manualmente (DD/MM/AAAA).\n\nDetalle: {e}")
            fecha_entry = Entry(ventana)
            fecha_entry.pack(pady=5)
            try:
                fecha_entry.insert(0, values[7])
            except Exception:
                fecha_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
            def get_fecha():
                return fecha_entry.get()

        def guardar():
            try:
                if not entradas["Tipo"].get():
                    messagebox.showwarning("Advertencia", "Por favor selecciona un Tipo.")
                    return
                if not entradas["Estado"].get():
                    messagebox.showwarning("Advertencia", "Por favor selecciona un Estado.")
                    return
                if not entradas["Capacidad"].get():
                    messagebox.showwarning("Advertencia", "Por favor selecciona una Capacidad.")
                    return
                numero = values[0]
                ubicacion = entradas["Ubicación"].get()
                serie = entradas["Num_serie"].get()
                tipo = entradas["Tipo"].get()
                estado = entradas["Estado"].get()
                capacidad = entradas["Capacidad"].get()
                precio = float(entradas["Precio"].get())
                fecha_inspeccion = get_fecha() if get_fecha else datetime.now().strftime("%d/%m/%Y")
                self.cursor.execute('''
                    UPDATE extintores
                    SET ubicacion = ?, serie = ?, tipo = ?, estado = ?, capacidad = ?, precio = ?, fecha_inspeccion = ?, fecha_registro = ?
                    WHERE numero = ?
                ''', (ubicacion, serie, tipo, estado, capacidad, precio, fecha_inspeccion, datetime.now().strftime("%Y-%m-%d"), numero))
                self.conexion.commit()
                self.consultar_extintores()
                self.actualizar_totales()
                ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos.")

        # marco superior para botones (Guardar a la izquierda, Salir a la derecha)
        top_buttons = Frame(ventana)
        top_buttons.pack(fill="x", padx=8, pady=3)
        Button(top_buttons, text="Guardar", width=12, command=guardar).pack(side="left", padx=12)
        Button(top_buttons, text="Salir", width=12, command=ventana.destroy).pack(side="right", padx=12)

    def abrir_ventana_consultar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un extintor u otro equipo para consultar.")
            return
        values = self.tree.item(selected[0])["values"]
        ventana = Toplevel(self.root)
        ventana.title("Detalles del Extintor u Otro Equipo")
        ventana.geometry("250x350")
        etiquetas = ["Número", "Ubicación", "Num_serie", "Tipo", "Estado", "Capacidad", "Precio", "Fecha Inspección"]
        for i, etiqueta in enumerate(etiquetas):
            Label(ventana, text=f"{etiqueta}: {values[i]}").pack(pady=5)
        Button(ventana, text="Salir", command=ventana.destroy).pack(pady=10)

    def consultar_extintores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.cursor.execute("SELECT numero, ubicacion, serie, tipo, estado, capacidad, precio, fecha_inspeccion FROM extintores")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)
        self.actualizar_totales()

    def filtrar(self, columna, valor):
        query = f"SELECT numero, ubicacion, serie, tipo, estado, capacidad, precio, fecha_inspeccion FROM extintores WHERE {columna} LIKE ?"
        self.cursor.execute(query, (f"%{valor}%",))
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def filtrar_numero(self):
        self.filtrar("numero", self.entry_numero.get())

    def filtrar_estado(self):
        self.filtrar("estado", self.entry_estado.get())

    def filtrar_fecha(self):
        self.filtrar("fecha_inspeccion", self.entry_fecha.get())

    def filtrar_ubicacion(self):
        self.filtrar("ubicacion", self.entry_ubicacion.get())

    def exportar_archivo(self):
        """Exporta el inventario actual a .xlsx o .pdf.

        .xlsx: usa pandas.to_excel
        .pdf: intenta usar reportlab (si no está instalado muestra instrucción)
        """
        try:
            df = pd.read_sql_query(
                "SELECT numero AS Numero, ubicacion AS Ubicacion, serie AS Num_serie, tipo AS Tipo, estado AS Estado, capacidad AS Capacidad, precio AS Precio, fecha_inspeccion AS Fecha_Inspección FROM extintores",
                self.conexion
            )
            if df.empty:
                messagebox.showinfo("Exportar", "No hay registros para exportar.")
                return
            initialfile = f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=initialfile,
                title="Guardar inventario como"
            )
            if not file_path:
                return
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ('.xls', '.xlsx'):
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Exportar", f"Inventario exportado correctamente a:\n{file_path}")
                return
            if ext == '.pdf':
                try:
                    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                    from reportlab.lib import colors
                    from reportlab.lib.pagesizes import letter
                except Exception:
                    messagebox.showerror("Error", "Para exportar a PDF instale 'reportlab' (pip install reportlab).")
                    return
                data = [list(df.columns)] + df.values.tolist()
                doc = SimpleDocTemplate(file_path, pagesize=letter)
                table = Table(data)
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ])
                table.setStyle(style)
                elems = [table]
                doc.build(elems)
                messagebox.showinfo("Exportar", f"Inventario exportado correctamente a:\n{file_path}")
                return
            messagebox.showerror("Error", "Formato de archivo no soportado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo.\nDetalle: {e}")

    def importar_archivo(self):
        """Importa registros desde un archivo .xlsx (las columnas esperadas: Ubicacion, Num_serie/serie, Tipo, Estado, Capacidad, Precio, Fecha_Inspeccion).

        Si el archivo es PDF muestra mensaje de no soportado.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx;*.xls"), ("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Seleccionar archivo a importar"
        )
        if not file_path:
            return
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.xls', '.xlsx'):
            try:
                df = pd.read_excel(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo Excel.\nDetalle: {e}")
                return
            if df.empty:
                messagebox.showinfo("Importar", "El archivo no contiene registros.")
                return
            # Normalizar nombres de columnas (lowercase)
            cols = {c.lower(): c for c in df.columns}
            inserted = 0
            for _, row in df.iterrows():
                try:
                    ubicacion = row.get(cols.get('ubicacion', ''), '')
                    serie = row.get(cols.get('num_serie', cols.get('serie', '')), '')
                    tipo = row.get(cols.get('tipo', ''), '')
                    estado = row.get(cols.get('estado', ''), '')
                    capacidad = row.get(cols.get('capacidad', ''), '')
                    precio = row.get(cols.get('precio', ''), 0.0)
                    fecha_val = row.get(cols.get('fecha_inspeccion', cols.get('fecha', '')), '')
                    # Formatear fecha si es Timestamp
                    try:
                        if hasattr(fecha_val, 'strftime'):
                            fecha_inspeccion = fecha_val.strftime('%d/%m/%Y')
                        else:
                            fecha_inspeccion = str(fecha_val)
                    except Exception:
                        fecha_inspeccion = str(fecha_val)
                    numero = self.obtener_siguiente_numero()
                    self.cursor.execute('''
                        INSERT INTO extintores (numero, ubicacion, serie, tipo, estado, capacidad, precio, fecha_inspeccion, fecha_registro)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (numero, str(ubicacion), str(serie), str(tipo), str(estado), str(capacidad), float(precio or 0.0), fecha_inspeccion or datetime.now().strftime('%d/%m/%Y'), datetime.now().strftime('%Y-%m-%d')))
                    inserted += 1
                except Exception:
                    # ignorar fila problematica
                    continue
            self.conexion.commit()
            self.consultar_extintores()
            self.actualizar_totales()
            messagebox.showinfo("Importar", f"Importación completada. Registros insertados: {inserted}")
            return
        if ext == '.pdf':
            messagebox.showerror("Importar", "Importar desde PDF no está soportado. Use un archivo .xlsx.")
            return
        messagebox.showerror("Importar", "Formato de archivo no soportado.")

    def __del__(self):
        self.conexion.close()


if __name__ == "__main__":
    root = Tk()

    # Icono para la ventana y la barra de tareas (Windows)
    # Intentamos primero aplicar un .ico (mejor para la barra de tareas / .exe)
    ico_path = resource_path("Logo_Inventario.ico")
    try:
        if os.path.exists(ico_path):
            try:
                root.iconbitmap(ico_path)
            except Exception as _err:
                # Algunos entornos pueden fallar con iconbitmap; continuamos con PNG
                print(f"Aviso: no se pudo aplicar .ico: {_err}")
    except Exception:
        # No hacemos nada si falla la comprobación de ruta
        pass

    # Como fallback visual para la ventana, usamos el PNG (iconphoto)
    png_path = resource_path("Logo_Inventario.png")
    try:
        if os.path.exists(png_path):
            icon_img = PhotoImage(file=png_path)
            root.iconphoto(False, icon_img)
        else:
            print("Aviso: Logo_Inventario.png no encontrado.")
    except Exception as e:
        print(f"Aviso: no se pudo cargar el icono PNG: {e}")

    app = InventarioExtintoresGUI(root)
    root.mainloop()
