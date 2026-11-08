# 66 Days to Live Your Life — tu vida como un videojuego

App web instalable (PWA) para hacer un reto de 66 días como si fuera un juego.

## Instalarla en el móvil

La app tiene que estar publicada en una dirección `https://` para poder instalarse. La forma más fácil
es GitHub Pages (gratis):

1. Une esta rama a `main` en GitHub.
2. En el repositorio: **Settings → Pages → Source: Deploy from a branch → `main` / `(root)` → Save**.
3. Al cabo de un minuto la app estará en `https://<tu-usuario>.github.io/<repo>/life-reset/`.
4. Abre ese enlace en el móvil:
   - **iPhone (Safari):** Compartir ⬆️ → *Añadir a pantalla de inicio*.
   - **Android (Chrome):** menú ⋮ → *Instalar aplicación*.

Desde ese momento tendrás el icono **66 Days** en tu pantalla de inicio: se abre a pantalla completa,
directamente en tu panel, y funciona sin conexión.

## Guardar el progreso

- Se guarda **solo** en el dispositivo cada vez que marcas algo (la app pide al navegador que no borre sus datos).
- En **Personaje → Guardar mi progreso** puedes:
  - **Descargar copia**: un archivo `.json` con tu partida.
  - **Copiar código**: un texto (`D66:...`) con toda tu partida para pegar en tus notas o enviarte por WhatsApp/email.
  - **Restaurar archivo / Pegar código**: recupera la partida en otro móvil o tras borrar el navegador.
    También se puede hacer desde la pantalla de bienvenida.
- La app avisa si llevas más de 7 días sin hacer una copia.

## Qué incluye

- **Cuestionario inicial**: nombre, edad, sexo, peso, altura, objetivos y hábitos actuales
  (sueño, entreno, alimentación, estrés, móvil, lectura, vida social, dinero).
- **Gráfico de telaraña** con 8 habilidades: Fuerza, Resistencia, Nutrición, Sueño, Mente,
  Intelecto, Social y Finanzas. Muestra cómo empezaste y cómo estás ahora.
- **Recomendaciones** para tus 3 habilidades más débiles, con consejos y hábitos que puedes añadir con un toque.
- **Hábitos buenos (+XP)** y **hábitos malos (−XP)**. Cada hábito sube o baja su habilidad.
- **Racha**: multiplicador de XP hasta x1,5. **Día perfecto** (todos los buenos y ningún malo): +50 XP.
- **9 rangos** con 3 divisiones cada uno (III → II → I). Puedes bajar de rango.

  | Rango | XP |
  |---|---|
  | 🪵 Madera | 0 |
  | 🥉 Bronce | 500 |
  | 🥈 Plata | 1.200 |
  | 🥇 Oro | 2.200 |
  | 💠 Platino | 3.500 |
  | ♦️ Rubí | 5.000 |
  | 🏆 Campeón | 7.000 |
  | 👑 Gran Campeón | 9.500 |
  | 🌟 Dios | 13.500 |

- **Liga** contra 11 rivales simulados que avanzan cada día.
- **Personaje personalizable**: piel, peinado, color de pelo, ropa y accesorios que se
  desbloquean al subir de rango (cinta, gorra, cascos, halo, corona). El aura toma el color de tu rango.
- **Calendario de 66 días** con el resultado de cada día.
- **Coach**: mensajes según tu progreso del día, tu racha y tu habilidad más débil.

## Nota

El coach funciona con reglas, no con una IA real, y los rivales son simulados. Para tener un
coach con IA o competir con amigos reales haría falta un servidor (y, para la IA, una clave de API).
