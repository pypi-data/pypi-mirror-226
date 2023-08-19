self.addEventListener('install', (e) => {
     e.waitUntil(
       caches.open('fox-store').then((cache) => cache.addAll([
         'demo.js',
//         '/pwa-examples/a2hs/index.html',
//         '/pwa-examples/a2hs/index.js',
//         '/pwa-examples/a2hs/style.css',
//         '/pwa-examples/a2hs/images/fox1.jpg',
//         '/pwa-examples/a2hs/images/fox2.jpg',
//         '/pwa-examples/a2hs/images/fox3.jpg',
//         '/pwa-examples/a2hs/images/fox4.jpg',
       ])),
     );
   });