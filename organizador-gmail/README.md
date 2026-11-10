# Organizador de Gmail

Aplicación de escritorio que lee tus correos de Gmail y los ordena por temas:

- 🎓 **Universidad**
- 💊 **Farmacia**
- 🧠 **Psicología**
- 🚫 **Spam**
- 📁 **Otros** (lo que no encaja en ninguno)

## Qué puedes hacer

| Acción | Cómo |
|---|---|
| Ver los correos de un tema | Pulsa el tema en la columna de la izquierda |
| **Abrir el correo en Gmail de verdad** | **Doble clic** sobre el correo (o el botón «Abrir en Gmail», o Enter) |
| Descartar un correo (quitarlo de la lista) | Tecla **Supr**, o el botón «Descartar» |
| Recuperar un descartado | Tema «Descartados» → clic derecho → Restaurar |
| Menú con más opciones | **Clic derecho** sobre el correo |
| Corregir el tema de un remitente | Clic derecho → «Cambiar tema». Desde ese momento todos sus correos irán a ese tema |
| Enviarlo a la papelera o a spam en Gmail | Clic derecho → «Mover a la papelera de Gmail» / «Marcar como spam en Gmail» |
| Buscar | Escribe en la caja 🔍 de arriba |
| Actualizar | Botón «Actualizar» o F5 (también se actualiza sola cada 5 minutos) |

«Descartar» solo oculta el correo en esta aplicación; en Gmail no se borra nada.
Solo la papelera y el spam (con confirmación) cambian algo en tu Gmail.

## Instalación (una sola vez)

### 1. Instala Python
Descárgalo de <https://www.python.org/downloads/>. En Windows, durante la
instalación, **marca la casilla «Add Python to PATH»**. No hace falta instalar nada más.

### 2. Activa IMAP en Gmail
Gmail → ⚙️ Configuración → Ver todos los ajustes → «Reenvío y correo POP/IMAP» →
**Habilitar IMAP** → Guardar cambios. (En muchas cuentas ya viene activado).

### 3. Crea una «contraseña de aplicación»
Por seguridad, la app no usa tu contraseña normal de Google.

1. Activa la **verificación en dos pasos** en tu cuenta de Google si no la tienes.
2. Entra en <https://myaccount.google.com/apppasswords>.
3. Ponle un nombre (por ejemplo «Organizador») y pulsa Crear.
4. Copia las 16 letras que te da. Las pegarás en la app la primera vez.

### 4. Ponla en el escritorio
- **Windows:** haz doble clic en `Crear acceso directo en el escritorio (Windows).bat`.
  Te aparecerá el icono «Organizador de Gmail» en el escritorio.
  (También puedes abrirla directamente con `Abrir Organizador (Windows).bat`).
- **Mac:** abre `Abrir Organizador (Mac).command` (la primera vez puede que tengas
  que hacer clic derecho → Abrir). Puedes arrastrarlo al Dock o al escritorio.

La primera vez te pedirá tu correo y la contraseña de aplicación.

## Personalizar los temas

Abre `categorias.json` con el Bloc de notas. Cada tema tiene:

- `palabras`: palabras que, si aparecen en el asunto o el texto, llevan el correo a ese tema.
  No hace falta poner tildes ni mayúsculas, y una palabra encaja con todas las que
  empiezan igual (`farmac` → farmacia, farmacéutico, farmacología…).
- `remitentes`: trozos de direcciones de correo. **Te recomiendo añadir el dominio de tu
  universidad** (por ejemplo `"@ub.edu"`, `"@ucm.es"`, `"@alumnes.ub.edu"`).

Puedes añadir temas nuevos copiando uno de los bloques. Cierra y vuelve a abrir la app
para aplicar los cambios.

También aprende de ti: si con clic derecho cambias el tema de un correo, todos los
correos de ese remitente irán a ese tema.

## Privacidad

- La app se conecta directamente de tu ordenador a Gmail; no pasa por ningún otro servidor.
- Si marcas «Recordar en este ordenador», la contraseña de aplicación se guarda en
  `~/.organizador_gmail/config.json` (en tu carpeta de usuario). Con «Cerrar sesión» se borra.
  Puedes revocar la contraseña de aplicación en cualquier momento desde tu cuenta de Google.
- Lee los últimos 150 correos de la bandeja de entrada y los últimos 50 de spam.
