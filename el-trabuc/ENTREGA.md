# El Trabuc · web de reserves — manual d'entrega

Web d'una sola pàgina (`index.html`) per a un restaurant amb reserva en línia.
**Un únic fitxer, sense dependències, sense build i sense servidor**: es pot
publicar a qualsevol allotjament estàtic amb cost zero, i s'entrega al client
copiant un fitxer.

---

## 1. Què hi ha a dins

| Bloc | Detall |
|---|---|
| Portada | Reclam, estat «obert / tancat ara» calculat en directe i accessos a reserva i carta |
| Reserves | Formulari amb dia, torns generats a partir de l'horari real, comensals, contacte, ocasió, al·lèrgies i consentiment RGPD |
| Carta | Pestanyes per categories, preus i etiquetes (vegetarià, sense gluten, de temporada) |
| La casa / Espais | Text de marca i tres espais amb marcs de fotografia |
| Horaris i contacte | Taula d'horaris amb el dia d'avui destacat, telèfon, WhatsApp, correu i Google Maps |
| Extres tècnics | Dades estructurades `schema.org/Restaurant` (SEO), etiquetes Open Graph, icona en línia, mode fosc automàtic, disseny responsiu, accessible amb teclat, versió imprimible |

La reserva enviada genera una **referència**, un **resum** i un enllaç per
**afegir-la a Google Calendar**.

---

## 2. Personalitzar-la per a un client (10 minuts)

Tot el que canvia d'un restaurant a un altre és al bloc `CONFIG`, al final de
`index.html`, dins de `<script>`:

```js
const CONFIG = {
  nom: 'El Trabuc',
  telefon: '+34 900 000 000',
  telefonRaw: '+34900000000',      // enllaços tel:
  whatsapp: '34900000000',         // sense + ni espais
  email: 'reserves@eltrabuc.example',
  adreca: 'Camí del Trabuc, s/n · 08000 Població',
  mapsQuery: 'El Trabuc restaurant',
  reserva: { maxComensals: 12, intervalMinuts: 30, ultimaEntradaMin: 90, ... },
  horaris: { 0:[['13:00','16:30']], 1:[], 2:[['13:00','16:00']], ... },
  carta:   [ { id:'entrants', nom:'Per compartir', plats:[ ... ] }, ... ]
};
```

- **`horaris`** — clau `0` = diumenge … `6` = dissabte. Cada torn és
  `['obertura','tancament']`; `[]` vol dir tancat. D'aquí surten alhora la taula
  d'horaris, l'indicador d'obert/tancat i **les hores que ofereix el formulari**.
- **`carta`** — afegeix, treu o reordena categories i plats; les pestanyes es
  generen soles. `t:` és una etiqueta opcional.
- **Colors i tipografies** — variables `:root` a dalt del `<style>`
  (`--ember` és el color de marca). El mode fosc en deriva sol.
- **Fotografies** — cada marc porta un comentari `<!-- FOTO n -->`. Substitueix
  `<div class="ph">…</div>` per `<img src="img/portada.jpg" alt="…">`. Fes servir
  JPG/WebP d'uns 1600 px d'ample i menys de 300 kB.
- **Textos legals i SEO** — actualitza també el bloc `application/ld+json` del
  `<head>` (adreça, telèfon, horaris) i les etiquetes `og:` i `canonical`.

---

## 3. Connectar les reserves

Per defecte `CONFIG.reserva.endpoint` és buit: en enviar el formulari s'obre
**WhatsApp** (o el correu, si poses `canalAlternatiu: 'email'`) amb la reserva
ja redactada. Funciona a tot arreu, no costa res i molts restaurants petits en
tenen prou.

Perquè la reserva arribi sola a la bústia del restaurant, posa un `endpoint`:

```js
reserva: { endpoint: 'https://formspree.io/f/xxxxxxx', canalAlternatiu: 'whatsapp' }
```

Serveix qualsevol servei que accepti un `POST` amb JSON: **Formspree**,
**FormSubmit**, **Getform**, **Basin**, un **Google Apps Script** publicat com a
aplicació web (guarda les reserves en un full de càlcul) o un webhook propi
(**Make**, **Zapier**, n8n). El cos que s'envia és:

```json
{
  "ref": "TRB-K3L9AB",
  "data": "2026-09-12",
  "dataLlarga": "divendres, 12 de setembre de 2026",
  "hora": "21:00",
  "comensals": "4",
  "nom": "…", "telefon": "…", "email": "…",
  "ocasio": "Aniversari",
  "comentaris": "…",
  "restaurant": "El Trabuc",
  "origen": "https://…"
}
```

Si el servei falla o cau, el formulari **no perd la reserva**: torna
automàticament al canal alternatiu (WhatsApp o correu).

> Per a gestió de taules, pagaments o antelació amb prepagament, el pas següent
> és una plataforma de reserves (CoverManager, TheFork, Resengo). Aquesta web
> està pensada per substituir el telèfon, no una plataforma completa.

---

## 4. Publicar-la

**GitHub Pages** (inclòs en aquest repositori)
1. `Settings → Pages → Build and deployment → Source: GitHub Actions`.
2. En fusionar a la branca principal, el flux de treball `.github/workflows/pages.yml`
   publica el repositori sencer. La web queda a
   `https://<usuari>.github.io/<repositori>/el-trabuc/`.

**Netlify o Vercel** — arrossega la carpeta `el-trabuc/` a
[app.netlify.com/drop](https://app.netlify.com/drop). Publicat en segons, amb HTTPS.

**Allotjament clàssic** — puja `index.html` (i la carpeta `img/`) per FTP a
`public_html/`. No cal PHP, ni base de dades, ni Node.

**Domini propi** — a Pages, `Settings → Pages → Custom domain`; al proveïdor del
domini, un registre `CNAME` cap a `<usuari>.github.io` (o els registres `A` de
GitHub per al domini nu). Activa «Enforce HTTPS» quan el certificat estigui llest.

---

## 5. Abans d'entregar-la o vendre-la

- [ ] Dades reals: nom, adreça, telèfon, WhatsApp, correu i horaris (ara són **d'exemple**).
- [ ] Carta i preus revisats i signats pel client.
- [ ] Fotografies pròpies amb `alt` descriptiu (les del client o de banc d'imatges amb llicència).
- [ ] Canal de reserves provat de punta a punta amb un enviament real.
- [ ] Avís legal, política de privacitat i responsable del tractament RGPD reals
      (el peu hi enllaça: substitueix el text pels documents del client).
- [ ] `canonical`, `og:` i JSON-LD amb el domini definitiu.
- [ ] Imatge social (`og:image`, 1200×630) i comprovació a
      [opengraph.xyz](https://www.opengraph.xyz).
- [ ] Prova en mòbil, en mode fosc i amb teclat; passa
      [PageSpeed Insights](https://pagespeed.web.dev/).
- [ ] Fitxa de Google Business Profile del client enllaçada a la web nova.

## 6. Traspàs al comprador

Quan es tanca la venda, tot el que existeix cap en quatre coses:

1. **El codi** — transferència del repositori (`Settings → Transfer ownership`)
   o simplement el fitxer `index.html`; no depèn de cap compte teu.
2. **El domini** — traspàs al registrador del client, o codi d'autorització.
3. **L'allotjament** — el compte de Pages, Netlify o l'FTP del client.
4. **El canal de reserves** — el compte de Formspree o el full de càlcul, creats
   amb el correu del client.

Deixa per escrit què inclou el manteniment (canvis de carta, horaris de
temporada, còpies) i què no. Aquest document serveix de manual d'usuari: entrega'l
amb la web.
