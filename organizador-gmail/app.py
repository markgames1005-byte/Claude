"""Organizador de Gmail — aplicación de escritorio.

Lee los correos de Gmail, los ordena por temas (Universidad, Farmacia,
Psicología, Spam y Otros), permite descartarlos y, con doble clic, abre el
correo en Gmail de verdad.

Ejecutar:  python app.py
"""
import json
import os
import queue
import threading
import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk

import clasificador
from gmail_imap import ClienteGmail

APP_NOMBRE = "Organizador de Gmail"
CARPETA_DATOS = os.path.join(os.path.expanduser("~"), ".organizador_gmail")
ARCHIVO_CONFIG = os.path.join(CARPETA_DATOS, "config.json")
ARCHIVO_DESCARTADOS = os.path.join(CARPETA_DATOS, "descartados.json")
ARCHIVO_REGLAS = os.path.join(CARPETA_DATOS, "reglas.json")
URL_CONTRASENA_APP = "https://myaccount.google.com/apppasswords"
ACTUALIZAR_CADA_MS = 5 * 60 * 1000  # cada 5 minutos

TODOS = "Todos"
DESCARTADOS = "Descartados"
ICONOS = {
    TODOS: "📥", "Universidad": "🎓", "Farmacia": "💊", "Psicología": "🧠",
    "Spam": "🚫", "Otros": "📁", DESCARTADOS: "🗑",
}
COLORES = {
    "Universidad": "#2563eb", "Farmacia": "#059669", "Psicología": "#9333ea",
    "Spam": "#dc2626", "Otros": "#6b7280",
}


# ---------------------------------------------------------------- utilidades
def leer_json(ruta, defecto):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return defecto


def guardar_json(ruta, datos):
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ruta)


def direccion_de(remitente):
    if "<" in remitente and remitente.endswith(">"):
        return remitente.rsplit("<", 1)[1][:-1].strip().lower()
    return remitente.strip().lower()


# ------------------------------------------------------------ ventana login
class VentanaLogin(tk.Toplevel):
    def __init__(self, padre, cuenta="", al_entrar=None):
        super().__init__(padre)
        self.title("Conectar con Gmail")
        self.resizable(False, False)
        self.transient(padre)
        self.al_entrar = al_entrar
        marco = ttk.Frame(self, padding=20)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Conecta tu cuenta de Gmail",
                  font=("Segoe UI", 13, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(marco, wraplength=380, justify="left", text=(
            "Necesitas una «contraseña de aplicación» de Google (16 letras), "
            "no tu contraseña normal. Se crea en tu cuenta de Google → "
            "Seguridad → Contraseñas de aplicaciones (requiere tener activada "
            "la verificación en dos pasos).")).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 4))
        enlace = ttk.Label(marco, text="Abrir la página para crearla →",
                           foreground="#2563eb", cursor="hand2")
        enlace.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 12))
        enlace.bind("<Button-1>", lambda e: webbrowser.open(URL_CONTRASENA_APP))

        ttk.Label(marco, text="Correo:").grid(row=3, column=0, sticky="w")
        self.var_cuenta = tk.StringVar(value=cuenta)
        e1 = ttk.Entry(marco, textvariable=self.var_cuenta, width=36)
        e1.grid(row=3, column=1, sticky="ew", pady=3)
        ttk.Label(marco, text="Contraseña de aplicación:").grid(row=4, column=0, sticky="w", padx=(0, 8))
        self.var_pass = tk.StringVar()
        e2 = ttk.Entry(marco, textvariable=self.var_pass, show="•", width=36)
        e2.grid(row=4, column=1, sticky="ew", pady=3)
        self.var_recordar = tk.BooleanVar(value=True)
        ttk.Checkbutton(marco, text="Recordar en este ordenador",
                        variable=self.var_recordar).grid(row=5, column=1, sticky="w", pady=(4, 0))
        self.lbl_estado = ttk.Label(marco, text="", foreground="#dc2626", wraplength=380)
        self.lbl_estado.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0))
        self.btn = ttk.Button(marco, text="Conectar", command=self._entrar)
        self.btn.grid(row=7, column=1, sticky="e", pady=(10, 0))

        (e2 if cuenta else e1).focus_set()
        self.bind("<Return>", lambda e: self._entrar())
        self.protocol("WM_DELETE_WINDOW", padre.destroy)
        self.grab_set()

    def _entrar(self):
        cuenta = self.var_cuenta.get().strip()
        contrasena = self.var_pass.get().replace(" ", "")
        if not cuenta or not contrasena:
            self.lbl_estado.config(text="Escribe el correo y la contraseña de aplicación.")
            return
        self.btn.config(state="disabled")
        self.lbl_estado.config(text="Conectando…", foreground="#6b7280")
        resultado = queue.Queue()

        def probar():
            cliente = ClienteGmail(cuenta, contrasena)
            try:
                cliente.conectar()
                resultado.put((True, cliente))
            except Exception as e:  # noqa: BLE001
                resultado.put((False, e))

        threading.Thread(target=probar, daemon=True).start()

        def comprobar():
            try:
                ok, valor = resultado.get_nowait()
            except queue.Empty:
                self.after(100, comprobar)
                return
            if ok:
                self.grab_release()
                self.destroy()
                self.al_entrar(valor, self.var_recordar.get())
            else:
                self.btn.config(state="normal")
                self.lbl_estado.config(foreground="#dc2626", text=(
                    "No se pudo conectar. Revisa el correo y la contraseña de "
                    "aplicación, y que IMAP esté activado en Gmail "
                    "(Configuración → Reenvío y correo POP/IMAP).\n\nDetalle: {}".format(valor)))

        comprobar()


# ------------------------------------------------------------ app principal
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NOMBRE)
        self.geometry("1150x700")
        self.minsize(820, 480)

        self.cliente = None
        self.bloqueo = threading.Lock()
        self.correos = []
        self.por_id = {}
        self.descartados = set(leer_json(ARCHIVO_DESCARTADOS, []))
        self.reglas = leer_json(ARCHIVO_REGLAS, {})
        self.categorias = clasificador.cargar_categorias()
        self.nombres_cat = list(self.categorias.keys())
        if clasificador.OTROS not in self.nombres_cat:
            self.nombres_cat.append(clasificador.OTROS)
        self.vista = TODOS
        self.cargando = False
        self.trabajos = queue.Queue()

        self._estilos()
        self._construir()
        self.after(100, self._procesar_trabajos)
        self.after(50, self._inicio)

    # ---------------------------------------------------------- interfaz
    def _estilos(self):
        st = ttk.Style(self)
        if "vista" in st.theme_names():
            st.theme_use("vista")
        elif "clam" in st.theme_names():
            st.theme_use("clam")
        st.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        st.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        st.configure("Titulo.TLabel", font=("Segoe UI", 15, "bold"))

    def _construir(self):
        # Barra superior
        barra = ttk.Frame(self, padding=(12, 10))
        barra.pack(fill="x")
        ttk.Label(barra, text="✉ " + APP_NOMBRE, style="Titulo.TLabel").pack(side="left")
        self.btn_actualizar = ttk.Button(barra, text="⟳ Actualizar", command=self.actualizar)
        self.btn_actualizar.pack(side="left", padx=(16, 0))
        ttk.Button(barra, text="Abrir Gmail",
                   command=lambda: webbrowser.open(self._url_bandeja())).pack(side="left", padx=6)
        ttk.Button(barra, text="Cerrar sesión", command=self._cerrar_sesion).pack(side="right")
        self.lbl_cuenta = ttk.Label(barra, text="", foreground="#6b7280")
        self.lbl_cuenta.pack(side="right", padx=10)
        self.var_buscar = tk.StringVar()
        self.var_buscar.trace_add("write", lambda *a: self._refrescar_lista())
        buscar = ttk.Entry(barra, textvariable=self.var_buscar, width=28)
        buscar.pack(side="right", padx=6)
        ttk.Label(barra, text="🔍").pack(side="right")

        cuerpo = ttk.PanedWindow(self, orient="horizontal")
        cuerpo.pack(fill="both", expand=True, padx=12, pady=(0, 6))

        # Panel de categorías
        izq = ttk.Frame(cuerpo, padding=(0, 0, 8, 0))
        ttk.Label(izq, text="TEMAS", foreground="#6b7280",
                  font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))
        self.lista_cat = tk.Listbox(izq, activestyle="none", font=("Segoe UI", 11),
                                    borderwidth=0, highlightthickness=0, width=27,
                                    selectbackground="#dbeafe", selectforeground="#111827")
        self.lista_cat.pack(fill="both", expand=True)
        self.lista_cat.bind("<<ListboxSelect>>", self._cambiar_vista)
        cuerpo.add(izq, weight=0)

        # Lista de correos + vista previa
        der = ttk.PanedWindow(cuerpo, orient="vertical")
        marco_lista = ttk.Frame(der)
        columnas = ("fecha", "de", "asunto", "tema")
        self.tabla = ttk.Treeview(marco_lista, columns=columnas, show="headings",
                                  selectmode="extended")
        for col, titulo, ancho in (("fecha", "Fecha", 135), ("de", "De", 220),
                                   ("asunto", "Asunto", 380), ("tema", "Tema", 100)):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=ancho, anchor="w", stretch=(col == "asunto"))
        barra_v = ttk.Scrollbar(marco_lista, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra_v.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra_v.pack(side="right", fill="y")
        self.tabla.tag_configure("noleido", font=("Segoe UI", 10, "bold"))
        for nombre, color in COLORES.items():
            self.tabla.tag_configure("cat_" + nombre, foreground=color)
        der.add(marco_lista, weight=3)

        marco_prev = ttk.Frame(der, padding=(0, 6, 0, 0))
        acciones = ttk.Frame(marco_prev)
        acciones.pack(fill="x")
        self.lbl_prev = ttk.Label(acciones, text="", font=("Segoe UI", 11, "bold"))
        self.lbl_prev.pack(side="left")
        ttk.Button(acciones, text="🗑 Descartar", command=self.descartar).pack(side="right")
        ttk.Button(acciones, text="↗ Abrir en Gmail", command=self.abrir_en_gmail).pack(side="right", padx=6)
        self.prev = tk.Text(marco_prev, wrap="word", height=8, font=("Segoe UI", 10),
                            borderwidth=1, relief="solid", padx=8, pady=6)
        self.prev.pack(fill="both", expand=True, pady=(4, 0))
        self.prev.config(state="disabled")
        der.add(marco_prev, weight=1)
        cuerpo.add(der, weight=1)

        # Barra de estado
        self.lbl_estado = ttk.Label(self, padding=(12, 4), foreground="#6b7280", text=(
            "Doble clic: abrir en Gmail   ·   Supr: descartar   ·   Clic derecho: más opciones"))
        self.lbl_estado.pack(fill="x")

        # Eventos de la tabla
        self.tabla.bind("<Double-1>", lambda e: self.abrir_en_gmail())
        self.tabla.bind("<Return>", lambda e: self.abrir_en_gmail())
        self.tabla.bind("<Delete>", lambda e: self.descartar())
        self.tabla.bind("<BackSpace>", lambda e: self.descartar())
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self._mostrar_previa())
        self.tabla.bind("<Button-3>", self._menu_contextual)
        self.tabla.bind("<Button-2>", self._menu_contextual)  # macOS
        self.tabla.bind("<Control-Button-1>", self._menu_contextual)
        self.bind("<F5>", lambda e: self.actualizar())

        self._refrescar_categorias()

    # ---------------------------------------------------------- inicio / login
    def _inicio(self):
        config = leer_json(ARCHIVO_CONFIG, {})
        if config.get("cuenta") and config.get("contrasena"):
            self.lbl_estado.config(text="Conectando con Gmail…")
            cliente = ClienteGmail(config["cuenta"], config["contrasena"])

            def conectar():
                cliente.conectar()
                return cliente

            def ok(c):
                self._conectado(c, recordar=True)

            def error(e):
                self._pedir_login(config.get("cuenta", ""))

            self._en_segundo_plano(conectar, ok, error)
        else:
            self._pedir_login(config.get("cuenta", ""))

    def _pedir_login(self, cuenta=""):
        VentanaLogin(self, cuenta, al_entrar=self._conectado)

    def _conectado(self, cliente, recordar):
        self.cliente = cliente
        datos = {"cuenta": cliente.cuenta}
        if recordar:
            datos["contrasena"] = cliente.contrasena
        guardar_json(ARCHIVO_CONFIG, datos)
        self.lbl_cuenta.config(text=cliente.cuenta)
        self.actualizar()
        self.after(ACTUALIZAR_CADA_MS, self._auto_actualizar)

    def _cerrar_sesion(self):
        if not messagebox.askyesno(APP_NOMBRE, "¿Cerrar sesión y olvidar la contraseña guardada?"):
            return
        cuenta = self.cliente.cuenta if self.cliente else ""
        if self.cliente:
            self.cliente.cerrar()
        self.cliente = None
        guardar_json(ARCHIVO_CONFIG, {"cuenta": cuenta})
        self.correos, self.por_id = [], {}
        self.lbl_cuenta.config(text="")
        self._refrescar_categorias()
        self._refrescar_lista()
        self._pedir_login(cuenta)

    # ---------------------------------------------------------- trabajo en segundo plano
    def _en_segundo_plano(self, funcion, al_terminar, al_fallar=None):
        def ejecutar():
            try:
                with self.bloqueo:
                    r = funcion()
                self.trabajos.put((al_terminar, r))
            except Exception as e:  # noqa: BLE001
                self.trabajos.put((al_fallar or self._error, e))
        threading.Thread(target=ejecutar, daemon=True).start()

    def _procesar_trabajos(self):
        try:
            while True:
                funcion, valor = self.trabajos.get_nowait()
                funcion(valor)
        except queue.Empty:
            pass
        self.after(100, self._procesar_trabajos)

    def _error(self, e):
        self.config(cursor="")
        self.cargando = False
        self.btn_actualizar.config(state="normal")
        self.lbl_estado.config(text="Error: {}".format(e))
        messagebox.showerror(APP_NOMBRE, "Ha ocurrido un error:\n\n{}".format(e))

    # ---------------------------------------------------------- carga de correos
    def actualizar(self):
        if not self.cliente or self.cargando:
            return
        self.cargando = True
        self.btn_actualizar.config(state="disabled")
        self.config(cursor="watch")
        self.lbl_estado.config(text="Leyendo correos de Gmail…")
        self._en_segundo_plano(self.cliente.leer, self._correos_leidos)

    def _auto_actualizar(self):
        if self.cliente:
            self.actualizar()
            self.after(ACTUALIZAR_CADA_MS, self._auto_actualizar)

    def _correos_leidos(self, correos):
        self.cargando = False
        self.config(cursor="")
        self.btn_actualizar.config(state="normal")
        self.correos = correos
        self.por_id = {c.msgid: c for c in correos}
        self._reclasificar()
        self.lbl_estado.config(text=(
            "{} correos leídos.   Doble clic: abrir en Gmail   ·   Supr: descartar   ·   "
            "Clic derecho: más opciones".format(len(correos))))

    def _reclasificar(self):
        for c in self.correos:
            c.categoria = clasificador.clasificar(
                c.remitente, c.asunto, c.texto, self.categorias,
                en_carpeta_spam=c.es_spam, reglas_usuario=self.reglas)
        self._refrescar_categorias()
        self._refrescar_lista()

    # ---------------------------------------------------------- pintar
    def _visibles(self, vista):
        if vista == DESCARTADOS:
            return [c for c in self.correos if c.msgid in self.descartados]
        activos = [c for c in self.correos if c.msgid not in self.descartados]
        if vista == TODOS:
            return activos
        return [c for c in activos if c.categoria == vista]

    def _refrescar_categorias(self):
        self.vistas = [TODOS] + self.nombres_cat + [DESCARTADOS]
        self.lista_cat.delete(0, "end")
        for v in self.vistas:
            n = len(self._visibles(v))
            sin_leer = sum(1 for c in self._visibles(v) if not c.leido)
            texto = "  {} {}  ({})".format(ICONOS.get(v, "•"), v, n)
            if sin_leer and v != DESCARTADOS:
                texto += " · {} nuevos".format(sin_leer)
            self.lista_cat.insert("end", texto)
        indice = self.vistas.index(self.vista) if self.vista in self.vistas else 0
        self.lista_cat.selection_set(indice)

    def _refrescar_lista(self):
        seleccion = set(self.tabla.selection())
        self.tabla.delete(*self.tabla.get_children())
        filtro = clasificador.normalizar(self.var_buscar.get().strip())
        for c in self._visibles(self.vista):
            if filtro and filtro not in clasificador.normalizar(
                    c.asunto + " " + c.remitente + " " + c.texto[:3000]):
                continue
            fecha = c.fecha.strftime("%d/%m/%Y %H:%M") if c.fecha else ""
            etiquetas = ["cat_" + (c.categoria or "")]
            if not c.leido:
                etiquetas.append("noleido")
            self.tabla.insert("", "end", iid=c.msgid, tags=etiquetas,
                              values=(fecha, c.remitente, c.asunto, c.categoria))
        restantes = [i for i in seleccion if self.tabla.exists(i)]
        if restantes:
            self.tabla.selection_set(restantes)
        self._mostrar_previa()

    def _cambiar_vista(self, _evento=None):
        sel = self.lista_cat.curselection()
        if not sel:
            return
        self.vista = self.vistas[sel[0]]
        self._refrescar_lista()

    def _mostrar_previa(self):
        sel = self._seleccionados()
        self.prev.config(state="normal")
        self.prev.delete("1.0", "end")
        if len(sel) == 1:
            c = sel[0]
            self.lbl_prev.config(text=c.asunto[:90])
            texto = "De: {}\nTema: {}\n\n{}".format(
                c.remitente, c.categoria, " ".join(c.texto.split())[:3000])
            self.prev.insert("1.0", texto)
        elif sel:
            self.lbl_prev.config(text="{} correos seleccionados".format(len(sel)))
        else:
            self.lbl_prev.config(text="")
        self.prev.config(state="disabled")

    # ---------------------------------------------------------- acciones
    def _seleccionados(self):
        return [self.por_id[i] for i in self.tabla.selection() if i in self.por_id]

    def _url_bandeja(self):
        if self.cliente:
            return "https://mail.google.com/mail/?authuser={}#inbox".format(self.cliente.cuenta)
        return "https://mail.google.com/"

    def abrir_en_gmail(self):
        for c in self._seleccionados()[:5]:
            webbrowser.open(c.url_gmail(self.cliente.cuenta))

    def descartar(self):
        sel = self._seleccionados()
        if not sel:
            return
        siguiente = self._fila_siguiente()
        for c in sel:
            self.descartados.add(c.msgid)
        self._guardar_descartados()
        self._refrescar_categorias()
        self._refrescar_lista()
        if siguiente and self.tabla.exists(siguiente):
            self.tabla.selection_set(siguiente)
            self.tabla.focus(siguiente)
        self.lbl_estado.config(text="{} correo(s) descartado(s). Puedes recuperarlos en «Descartados».".format(len(sel)))

    def restaurar(self):
        sel = self._seleccionados()
        for c in sel:
            self.descartados.discard(c.msgid)
        self._guardar_descartados()
        self._refrescar_categorias()
        self._refrescar_lista()

    def _fila_siguiente(self):
        filas = self.tabla.get_children()
        sel = set(self.tabla.selection())
        if not sel:
            return None
        ultimo = max(filas.index(i) for i in sel)
        for i in filas[ultimo + 1:]:
            if i not in sel:
                return i
        for i in reversed(filas[:ultimo]):
            if i not in sel:
                return i
        return None

    def _guardar_descartados(self):
        # Solo se guardan los que siguen existiendo para que el archivo no crezca sin fin.
        if self.correos:
            existentes = {c.msgid for c in self.correos}
            self.descartados &= existentes
        guardar_json(ARCHIVO_DESCARTADOS, sorted(self.descartados))

    def cambiar_tema(self, categoria):
        sel = self._seleccionados()
        if not sel:
            return
        for c in sel:
            self.reglas[clasificador.normalizar(direccion_de(c.remitente))] = categoria
        guardar_json(ARCHIVO_REGLAS, self.reglas)
        self._reclasificar()
        self.lbl_estado.config(text="A partir de ahora los correos de ese remitente irán a «{}».".format(categoria))

    def olvidar_regla(self):
        cambios = 0
        for c in self._seleccionados():
            if self.reglas.pop(clasificador.normalizar(direccion_de(c.remitente)), None):
                cambios += 1
        if cambios:
            guardar_json(ARCHIVO_REGLAS, self.reglas)
            self._reclasificar()

    def _accion_gmail(self, metodo, texto):
        sel = self._seleccionados()
        if not sel:
            return
        if not messagebox.askyesno(APP_NOMBRE, "¿{} {} correo(s) en Gmail?".format(texto, len(sel))):
            return
        self.lbl_estado.config(text="Aplicando cambios en Gmail…")

        def hacer():
            for c in sel:
                metodo(c)
            return sel

        def hecho(_):
            self.lbl_estado.config(text="Hecho.")
            self.actualizar()

        self._en_segundo_plano(hacer, hecho)

    def _menu_contextual(self, evento):
        fila = self.tabla.identify_row(evento.y)
        if not fila:
            return
        if fila not in self.tabla.selection():
            self.tabla.selection_set(fila)
            self.tabla.focus(fila)
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="↗  Abrir en Gmail", command=self.abrir_en_gmail)
        if self.vista == DESCARTADOS:
            menu.add_command(label="↩  Restaurar", command=self.restaurar)
        else:
            menu.add_command(label="🗑  Descartar (ocultar aquí)", command=self.descartar)
        sub = tk.Menu(menu, tearoff=0)
        for nombre in self.nombres_cat:
            sub.add_command(label="{} {}".format(ICONOS.get(nombre, "•"), nombre),
                            command=lambda n=nombre: self.cambiar_tema(n))
        sub.add_separator()
        sub.add_command(label="Volver a clasificar automáticamente", command=self.olvidar_regla)
        menu.add_cascade(label="🏷  Cambiar tema (este remitente)", menu=sub)
        menu.add_separator()
        menu.add_command(label="Mover a la papelera de Gmail",
                         command=lambda: self._accion_gmail(self.cliente.mover_a_papelera,
                                                            "Mover a la papelera"))
        menu.add_command(label="Marcar como spam en Gmail",
                         command=lambda: self._accion_gmail(self.cliente.marcar_como_spam,
                                                            "Marcar como spam"))
        try:
            menu.tk_popup(evento.x_root, evento.y_root)
        finally:
            menu.grab_release()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
