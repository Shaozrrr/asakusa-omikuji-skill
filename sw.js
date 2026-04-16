const CACHE_NAME = "asakusa-omikuji-pwa-v3";
const ROOT = new URL("./", self.location);

const SHELL_PATHS = [
  "./",
  "./index.html",
  "./app/",
  "./app/index.html",
  "./app/styles.css",
  "./app/app.js?v=20260416-2",
  "./app/manifest.webmanifest",
  "./app/icon.svg",
  "./app/icons/icon-192.png",
  "./app/icons/icon-512.png",
  "./app/icons/icon-maskable-512.png",
  "./app/icons/apple-touch-icon-180.png",
];

const DATA_PATHS = Array.from({ length: 10 }, (_, index) =>
  `./data/asakusa_omikuji_part${String(index + 1).padStart(2, "0")}.json`,
);

const PRECACHE_URLS = [...SHELL_PATHS, ...DATA_PATHS].map((path) =>
  new URL(path, ROOT).toString(),
);

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      cache.addAll(PRECACHE_URLS.map((url) => new Request(url, { cache: "reload" }))),
    ),
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
          return Promise.resolve();
        }),
      ),
    ),
  );
  self.clients.claim();
});

async function networkFirst(request, fallbackUrl = null) {
  const cache = await caches.open(CACHE_NAME);

  try {
    const response = await fetch(request);
    cache.put(request, response.clone());
    return response;
  } catch (error) {
    const cached = await cache.match(request);
    if (cached) {
      return cached;
    }
    if (fallbackUrl) {
      const fallback = await cache.match(fallbackUrl);
      if (fallback) {
        return fallback;
      }
    }
    throw error;
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_NAME);
  const cached = await cache.match(request);

  const networkPromise = fetch(request)
    .then((response) => {
      cache.put(request, response.clone());
      return response;
    })
    .catch(() => cached);

  return cached || networkPromise;
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") {
    return;
  }

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) {
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(networkFirst(request, new URL("./app/index.html", ROOT).toString()));
    return;
  }

  if (url.pathname.includes("/data/")) {
    event.respondWith(networkFirst(request));
    return;
  }

  if (url.pathname.includes("/app/") || url.pathname.endsWith("/sw.js")) {
    event.respondWith(staleWhileRevalidate(request));
  }
});
