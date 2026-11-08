// Service worker: abre la app sin conexión y envía los recordatorios.
// Estrategia de red: red primero (para recibir actualizaciones) y caché como respaldo.
const CACHE = '66days-v5';
const CFG_CACHE = '66days-cfg'; // configuración de recordatorios que escribe la app
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE && k !== CFG_CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});

/* ---------- Recordatorios con la app cerrada ----------
   Android (Chrome, app instalada) despierta al service worker de vez en cuando
   con "periodicsync". Aquí se comprueba si toca algún recordatorio. */
const pad = n => String(n).padStart(2, '0');
const todayKey = () => { const d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); };

async function checkReminders() {
  const c = await caches.open(CFG_CACHE);
  const res = await c.match('cfg');
  if (!res) return;
  const cfg = await res.json();
  if (!cfg.on || !cfg.list) return;
  const now = new Date(), wd = now.getDay(), mins = now.getHours() * 60 + now.getMinutes(), tk = todayKey();
  cfg.fired = cfg.fired || {};
  let changed = false;
  for (const r of cfg.list) {
    const [h, m] = r.t.split(':').map(Number), at = h * 60 + m;
    if (!r.days.includes(wd) || mins < at || mins - at > 180 || cfg.fired[r.id] === tk) continue;
    cfg.fired[r.id] = tk; changed = true;
    const s = cfg.summary || {};
    const body = s.date === tk && s.text ? s.text : '¡Hora de tus hábitos! No pierdas tu racha 🔥 y abre tu cofre diario 🎁';
    await self.registration.showNotification('66 Days', {
      body, icon: 'icons/icon-192.png', badge: 'icons/icon-192.png', tag: '66days-' + r.id, data: { url: './' }
    });
  }
  if (changed) await c.put('cfg', new Response(JSON.stringify(cfg)));
}

self.addEventListener('periodicsync', e => {
  if (e.tag === 'reminders') e.waitUntil(checkReminders());
});

// Al tocar la notificación se abre (o se enfoca) la app
self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      for (const w of list) if ('focus' in w) return w.focus();
      return self.clients.openWindow((e.notification.data && e.notification.data.url) || './');
    })
  );
});
