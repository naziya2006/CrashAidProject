const CACHE_NAME = 'hospital-dashboard-cache-v1';
const urlsToCache = [
    '/',
    '/hospitalapp/dashboard/',
    '/static/hospitalapp/manifest.json'
];

// Install service worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(cache => cache.addAll(urlsToCache))
    );
});

// Fetch cached content
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
        .then(response => response || fetch(event.request))
    );
});
