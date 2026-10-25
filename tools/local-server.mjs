import http from "node:http";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import worker from "../_worker.js";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PORT = process.env.PORT || 8787;

const env = {};
try {
  const txt = await readFile(path.join(ROOT, ".dev.vars"), "utf8");
  for (const line of txt.split(/\r?\n/)) {
    const m = line.match(/^([A-Za-z0-9_]+)=(.*)$/);
    if (m && !m[2].trim().startsWith("PLEASE_FILL")) env[m[1]] = m[2].trim();
  }
} catch (e) {
  // no .dev.vars - Alipay API returns "not configured"
}

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".json": "application/json; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".ico": "image/x-icon"
};

const IGNORED = ["/tools/", "/data/", "/functions/", "/eura/", "/keywords.txt", "/.git", "/.assetsignore", "/_worker.js", "/.dev.vars", "/wrangler", "/robots.txt.curl"];

async function serveAsset(pathname) {
  if (IGNORED.some(function (p) { return pathname === p || pathname.startsWith(p); })) return null;
  let filePath = path.join(ROOT, pathname === "/" ? "index.html" : decodeURIComponent(pathname));
  try {
    const s = await stat(filePath);
    if (s.isDirectory()) filePath = path.join(filePath, "index.html");
    const data = await readFile(filePath);
    return new Response(data, {
      headers: { "Content-Type": MIME[path.extname(filePath).toLowerCase()] || "application/octet-stream" }
    });
  } catch (e) {
    return null;
  }
}

const ASSETS = {
  fetch: async function (r) {
    const u = new URL(r.url);
    const asset = await serveAsset(u.pathname);
    return asset || new Response("Not Found", { status: 404 });
  }
};

const server = http.createServer(async function (req, res) {
  try {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    const body = chunks.length ? Buffer.concat(chunks) : undefined;
    const headers = { ...req.headers };
    delete headers["host"];
    const request = new Request("http://127.0.0.1:" + PORT + req.url, {
      method: req.method,
      headers: headers,
      body: body,
      redirect: "manual"
    });
    const response = await worker.fetch(request, Object.assign({ ASSETS: ASSETS }, env));
    const outHeaders = {};
    response.headers.forEach(function (v, k) { outHeaders[k] = v; });
    res.writeHead(response.status, outHeaders);
    const buf = Buffer.from(await response.arrayBuffer());
    res.end(buf);
  } catch (e) {
    res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("local-server error: " + (e && e.stack ? e.stack : e));
  }
});

server.listen(PORT, "127.0.0.1", function () {
  console.log("FarFlight local preview (static + Alipay API): http://127.0.0.1:" + PORT);
  console.log("Env vars loaded from .dev.vars:", Object.keys(env).join(", ") || "(none)");
});
