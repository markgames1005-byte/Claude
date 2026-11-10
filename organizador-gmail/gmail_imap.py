"""Acceso a Gmail por IMAP (solo librería estándar de Python).

Se usa una "contraseña de aplicación" de Google, no la contraseña normal.
"""
import email
import email.policy
import imaplib
import re
from email.header import decode_header, make_header
from email.utils import parseaddr, parsedate_to_datetime

SERVIDOR = "imap.gmail.com"
BYTES_POR_CORREO = 30000  # suficiente para asunto, remitente y el inicio del texto


class Correo:
    def __init__(self, uid, carpeta, msgid, thrid, remitente, asunto, fecha,
                 texto, leido, es_spam):
        self.uid = uid              # identificador dentro de la carpeta
        self.carpeta = carpeta      # nombre IMAP de la carpeta
        self.msgid = msgid          # id único de Gmail (no cambia)
        self.thrid = thrid          # id de la conversación en Gmail
        self.remitente = remitente
        self.asunto = asunto
        self.fecha = fecha
        self.texto = texto
        self.leido = leido
        self.es_spam = es_spam
        self.categoria = None

    def url_gmail(self, cuenta):
        vista = "spam" if self.es_spam else "all"
        return "https://mail.google.com/mail/?authuser={}#{}/{:x}".format(
            cuenta, vista, int(self.thrid))


def _decodificar(valor):
    if not valor:
        return ""
    try:
        return str(make_header(decode_header(valor)))
    except Exception:
        return str(valor)


def _texto_plano(msg):
    partes_html = []
    for parte in msg.walk():
        if parte.is_multipart():
            continue
        tipo = parte.get_content_type()
        if tipo not in ("text/plain", "text/html"):
            continue
        try:
            carga = parte.get_payload(decode=True) or b""
            charset = parte.get_content_charset() or "utf-8"
            texto = carga.decode(charset, errors="replace")
        except Exception:
            continue
        if tipo == "text/plain":
            return texto
        partes_html.append(texto)
    if partes_html:
        html = re.sub(r"(?is)<(script|style).*?</\1>", " ", partes_html[0])
        html = re.sub(r"(?s)<[^>]+>", " ", html)
        html = re.sub(r"&nbsp;", " ", html)
        return re.sub(r"[ \t\r\f\v]+", " ", html)
    return ""


class ClienteGmail:
    def __init__(self, cuenta, contrasena):
        self.cuenta = cuenta
        self.contrasena = contrasena
        self.conn = None
        self.carpetas = {}

    # ---- conexión -------------------------------------------------------
    def conectar(self):
        self.conn = imaplib.IMAP4_SSL(SERVIDOR)
        self.conn.login(self.cuenta, self.contrasena)
        self._buscar_carpetas()

    def cerrar(self):
        if self.conn is not None:
            try:
                self.conn.logout()
            except Exception:
                pass
            self.conn = None

    def _asegurar(self):
        try:
            if self.conn is not None:
                self.conn.noop()
                return
        except Exception:
            pass
        self.conectar()

    def _buscar_carpetas(self):
        """Encuentra las carpetas especiales (sus nombres cambian según idioma)."""
        typ, lineas = self.conn.list()
        self.carpetas = {"inbox": "INBOX"}
        for linea in lineas or []:
            if not linea:
                continue
            texto = linea.decode("utf-8", errors="replace")
            m = re.match(r'\((?P<flags>[^)]*)\) "(?P<sep>[^"]*)" (?P<nombre>.+)$', texto)
            if not m:
                continue
            flags = m.group("flags")
            nombre = m.group("nombre").strip()
            for flag, clave in (("\\Junk", "spam"), ("\\Trash", "papelera")):
                if flag in flags:
                    self.carpetas[clave] = nombre

    # ---- lectura --------------------------------------------------------
    def leer(self, max_bandeja=150, max_spam=50):
        self._asegurar()
        correos = self._leer_carpeta(self.carpetas["inbox"], max_bandeja, False)
        if "spam" in self.carpetas and max_spam > 0:
            correos += self._leer_carpeta(self.carpetas["spam"], max_spam, True)
        correos.sort(key=lambda c: c.fecha.timestamp() if c.fecha else 0,
                     reverse=True)
        return correos

    def _leer_carpeta(self, carpeta, maximo, es_spam):
        typ, _ = self.conn.select(carpeta, readonly=True)
        if typ != "OK":
            return []
        typ, datos = self.conn.uid("SEARCH", None, "ALL")
        uids = (datos[0] or b"").split()
        uids = uids[-maximo:]
        if not uids:
            return []
        consulta = "(X-GM-MSGID X-GM-THRID FLAGS BODY.PEEK[]<0.{}>)".format(
            BYTES_POR_CORREO)
        typ, respuesta = self.conn.uid("FETCH", b",".join(uids).decode(), consulta)
        correos = []
        cabecera, cuerpo = b"", None
        for item in respuesta or []:
            if isinstance(item, tuple):
                if cuerpo is not None:
                    c = self._crear(cabecera, cuerpo, carpeta, es_spam)
                    if c:
                        correos.append(c)
                cabecera, cuerpo = item[0], item[1]
            elif isinstance(item, bytes) and cuerpo is not None:
                cabecera += b" " + item  # a veces FLAGS llega después del cuerpo
        if cuerpo is not None:
            c = self._crear(cabecera, cuerpo, carpeta, es_spam)
            if c:
                correos.append(c)
        return correos

    def _crear(self, cabecera, cuerpo, carpeta, es_spam):
        cab = cabecera.decode("utf-8", errors="replace")
        uid = re.search(r"UID (\d+)", cab)
        msgid = re.search(r"X-GM-MSGID (\d+)", cab)
        thrid = re.search(r"X-GM-THRID (\d+)", cab)
        if not (uid and msgid and thrid):
            return None
        flags = re.search(r"FLAGS \(([^)]*)\)", cab)
        leido = bool(flags and "\\Seen" in flags.group(1))
        msg = email.message_from_bytes(cuerpo, policy=email.policy.compat32)
        nombre, direccion = parseaddr(_decodificar(msg.get("From")))
        remitente = "{} <{}>".format(nombre, direccion) if nombre else direccion
        try:
            fecha = parsedate_to_datetime(msg.get("Date"))
            if fecha is not None and fecha.tzinfo is not None:
                fecha = fecha.astimezone()
        except Exception:
            fecha = None
        return Correo(uid.group(1), carpeta, msgid.group(1), thrid.group(1),
                      remitente, _decodificar(msg.get("Subject")) or "(sin asunto)",
                      fecha, _texto_plano(msg), leido, es_spam)

    # ---- acciones en Gmail ----------------------------------------------
    def _mover(self, correo, destino):
        self._asegurar()
        typ, _ = self.conn.select(correo.carpeta, readonly=False)
        if typ != "OK":
            raise RuntimeError("No se pudo abrir la carpeta " + correo.carpeta)
        typ, datos = self.conn.uid("MOVE", correo.uid, destino)
        if typ != "OK":
            raise RuntimeError("Gmail rechazó la operación: {}".format(datos))

    def mover_a_papelera(self, correo):
        if "papelera" not in self.carpetas:
            raise RuntimeError("No se encontró la papelera de Gmail")
        self._mover(correo, self.carpetas["papelera"])

    def marcar_como_spam(self, correo):
        if "spam" not in self.carpetas:
            raise RuntimeError("No se encontró la carpeta de spam de Gmail")
        self._mover(correo, self.carpetas["spam"])
