# Trady's — página web

Página informativa de una sola pieza (`index.html`) sobre el supermercado
**Trady's** de Carrer Pau Casals, 14, 08430 Santa Agnès de Malanyanes (Barcelona).

## Contenido

- Cabecera con nombre, categoría, valoración (4,4 sobre 11 reseñas) y estado de apertura.
- Accesos rápidos: cómo llegar, llamar, horarios, reseñas y locales cercanos.
- Ficha de información: dirección, teléfono, Plus Code y horario.
- Tabla de horarios.
- Gráfico de horas de mayor afluencia (martes).
- Resumen de valoraciones y tres reseñas.
- Bloque «la gente también busca».

## Uso

Abre `index.html` en cualquier navegador. No tiene dependencias externas: todo el
CSS, los iconos SVG y el JavaScript están dentro del propio archivo. El diseño es
responsive y se adapta al tema claro u oscuro del sistema.

## Nota sobre los datos

Los datos provienen de una ficha pública de Google Maps y no están verificados.
Solo se conoce con certeza el horario de cierre del día en curso; el resto de días
aparecen como «Consultar». La distribución por estrellas y las horas de afluencia
son estimaciones. La página no es oficial ni está asociada al negocio.

---

# El Trabuc — web de reserves

A `el-trabuc/index.html` hi ha una segona web, independent de l'anterior: la
pàgina d'un restaurant de brasa amb **reserva de taula en línia**, pensada per
publicar-la i entregar-la a un client.

- Un sol fitxer, sense dependències ni build ni servidor.
- Tot el que canvia d'un restaurant a un altre és al bloc `CONFIG` del final del
  fitxer: dades de contacte, horaris (que generen sols la taula d'horaris, l'estat
  «obert ara» i els torns disponibles) i la carta.
- Les reserves s'envien per WhatsApp o correu sense servidor, o a un `endpoint`
  (Formspree, Google Apps Script, un webhook…) si se'n configura un.
- Dades estructurades per a Google, mode fosc, disseny responsiu i accessible.

**Manual de personalització, publicació i traspàs al comprador:
[`el-trabuc/ENTREGA.md`](el-trabuc/ENTREGA.md).**

## Publicació

El flux de treball `.github/workflows/pages.yml` publica el repositori a GitHub
Pages a cada `push` a la branca principal. Cal activar-ho un cop a
`Settings → Pages → Source: GitHub Actions`. Un cop actiu:

- `https://<usuari>.github.io/<repositori>/` → Trady's
- `https://<usuari>.github.io/<repositori>/el-trabuc/` → El Trabuc

Les dades de contacte, horaris i carta d'El Trabuc són **d'exemple**: cal
substituir-les per les reals abans de publicar-la com a web d'un negoci.
