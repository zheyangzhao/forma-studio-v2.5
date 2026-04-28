/* Forma Studio · Service Worker (離線快取)
   僅快取主 HTML 和 manifest，CDN 資源由瀏覽器預設行為處理 */

const CACHE_NAME = 'forma-studio-v1.0';
const PRECACHE_URLS = [
  './forma-studio.html',
  './manifest.json',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(names =>
      Promise.all(
        names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const { request } = event;
  // 只處理 GET 同源請求
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  // OpenAI API 絕對不快取
  if (url.hostname.includes('openai.com')) return;

  // 主 HTML / manifest：network-first，失敗時用快取
  if (PRECACHE_URLS.some(u => request.url.endsWith(u.replace('./', '')))) {
    event.respondWith(
      fetch(request)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // CDN 資源（Tailwind / React / Babel）：cache-first，一次下載長期用
  if (url.hostname.includes('cdn.') || url.hostname.includes('cdnjs.')) {
    event.respondWith(
      caches.match(request).then(cached => {
        if (cached) return cached;
        return fetch(request).then(response => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
          }
          return response;
        });
      })
    );
  }
});
