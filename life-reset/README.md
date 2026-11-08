# Life Reset 66 — tu vida como un videojuego

App web de un solo archivo (`index.html`) para hacer un reto de 66 días como si fuera un juego.
Abre `index.html` en el navegador (móvil o PC). No necesita instalación ni internet; todo se guarda
en el propio navegador (localStorage). Puedes exportar/importar tu partida desde «Personaje».

## Qué incluye

- **Cuestionario inicial**: nombre, edad, sexo, peso, altura, objetivos y hábitos actuales
  (sueño, entreno, alimentación, estrés, móvil, lectura, vida social, dinero).
- **Gráfico de telaraña** con 8 habilidades: Fuerza, Resistencia, Nutrición, Sueño, Mente,
  Intelecto, Social y Finanzas. Muestra cómo empezaste y cómo estás ahora.
- **Recomendaciones** para tus 3 habilidades más débiles, con consejos y hábitos que puedes añadir con un toque.
- **Hábitos buenos (+XP)** y **hábitos malos (−XP)**. Cada hábito sube o baja su habilidad.
- **Racha**: multiplicador de XP hasta x1,5. **Día perfecto** (todos los buenos y ningún malo): +50 XP.
- **10 rangos** con 3 divisiones cada uno (III → II → I). Puedes bajar de rango.

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
  | ⚡ Supercampeón | 12.500 |
  | 🌟 Dios | 16.000 |

- **Liga** contra 11 rivales simulados que avanzan cada día.
- **Personaje personalizable**: piel, peinado, color de pelo, ropa y accesorios que se
  desbloquean al subir de rango (cinta, gorra, cascos, halo, corona). El aura toma el color de tu rango.
- **Calendario de 66 días** con el resultado de cada día.
- **Coach**: mensajes según tu progreso del día, tu racha y tu habilidad más débil.

## Nota

El coach funciona con reglas, no con una IA real, y los rivales son simulados. Para tener un
coach con IA o competir con amigos reales haría falta un servidor (y, para la IA, una clave de API).
