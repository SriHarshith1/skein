// Serves the static Pages build (out/) under /skein, the way GitHub Pages will.
// Usage: npm run build:static && npm run preview:static
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";

const root = path.resolve("out");
const base = "/skein";
const port = Number(process.env.PORT ?? 4180);
const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".svg": "image/svg+xml", ".ico": "image/x-icon", ".woff2": "font/woff2", ".txt": "text/plain" };

createServer(async (req, res) => {
  const url = decodeURIComponent(new URL(req.url ?? "/", "http://x").pathname);
  if (!url.startsWith(base)) return res.writeHead(302, { location: `${base}/` }).end();
  let file = path.join(root, url.slice(base.length));
  if (!file.startsWith(root)) return res.writeHead(403).end();
  try {
    if ((await stat(file)).isDirectory()) file = path.join(file, "index.html");
    res.writeHead(200, { "content-type": types[path.extname(file)] ?? "application/octet-stream" });
    res.end(await readFile(file));
  } catch {
    res.writeHead(404, { "content-type": "text/html" }).end(await readFile(path.join(root, "404.html")).catch(() => "not found"));
  }
}).listen(port, () => console.log(`static preview on http://localhost:${port}${base}/`));
