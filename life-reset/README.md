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

- **Cuestionario inicial** (edad, peso, altura, objetivos, hábitos actuales) y **gráfico de telaraña**
  con 8 habilidades: Fuerza, Resistencia, Nutrición, Sueño, Mente, Intelecto, Social y Finanzas.
- **Hábitos adaptados a tu perfil**: cada hábito tiene versión normal, fácil y mínima. Si una habilidad
  está baja (o por edad/IMC en las físicas) empiezas con la fácil. Tras completarlo 10 veces puedes
  **subirlo de nivel** (+30 % XP). Se empieza con solo 4 hábitos buenos y 2 malos.
- **Versión mínima («nunca cero»)**: botón 🌱½ para los días difíciles; da media XP y mantiene la racha.
- **Recompensas diarias**: cofre diario con premio variable (XP, jackpot o escudo de racha),
  3 misiones diarias fáciles, día perfecto (+50 XP), hitos en los días 7, 14, 21, 33, 50 y 66, y 17 logros.
- **Racha**: un día cuenta si completas al menos la mitad de tus hábitos. Multiplicador hasta x1,5.
  Los **escudos** 🛡️ protegen la racha si fallas un día.
- **Castigo — la maldición 💀**: se activa si fallas 2 días seguidos, marcas 3 hábitos malos en un día
  o caes en hábitos malos 3 días seguidos. Pierdes XP, tus hábitos dan la mitad de XP y tienes 48 h para
  una **misión de redención adaptada a tu nivel físico, edad e IMC** y a tu habilidad más débil.
  Si la completas, recuperas la mitad de lo perdido; si no, pierdes más y el plazo se reinicia.
  Cada día sin ningún hábito también resta 15 XP.
- **9 rangos** con 3 divisiones (III → II → I), con sonido, vibración y confeti al subir:

  | Rango | XP |
  |---|---|
  | 🪵 Madera | 0 |
  | 🥉 Bronce | 150 |
  | 🥈 Plata | 400 |
  | 🥇 Oro | 800 |
  | 💠 Platino | 1.400 |
  | ♦️ Rubí | 2.200 |
  | 🏆 Campeón | 3.200 |
  | 👑 Gran Campeón | 4.500 |
  | 🌟 Dios | 6.500 |

- **Liga** contra 11 rivales simulados.
- **Personaje personalizable** con accesorios que se desbloquean por rango.

## Nota

El coach funciona con reglas, no con una IA real, y los rivales son simulados. Para tener un
coach con IA o competir con amigos reales haría falta un servidor (y, para la IA, una clave de API).
