// Builds the password-protected copy of the site in _site/ for GitHub Pages.
// Run by .github/workflows/deploy.yml on every push to main; not needed for local editing.
//
//   npm install --no-save staticrypt@3.5.4
//   SITE_PASSWORD=... node tools/encrypt_site.js
//
// Every published .html page is encrypted with StatiCrypt (AES, password never stored in the repo).
// The site-wide search index is encrypted with the same key, and assets/extras.js decrypts it
// using the key StatiCrypt remembers in the browser after login.

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { webcrypto: crypto } = require("crypto");
const engine = require("staticrypt/lib/cryptoEngine.js");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "_site");
// Not secret: fixed so a remembered login stays valid across deploys.
const SALT = "c1a7e5b0d4f24e6a9b3c8d2e1f0a7b6c";
const REMEMBER_DAYS = "365";
const PASSWORD = process.env.SITE_PASSWORD || "";
if (!PASSWORD) { console.error("SITE_PASSWORD is not set"); process.exit(1); }

// 1. Copy only what the live site needs (no src/, tools/, build scripts or README).
const SKIP = new Set([".git", ".github", "src", "tools", "node_modules", "_site", "__pycache__", "notes"]);
fs.rmSync(OUT, { recursive: true, force: true });
function copy(dir, rel = "") {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(e.name) && rel === "") continue;
    if (e.name === "__pycache__") continue;
    const from = path.join(dir, e.name), r = path.join(rel, e.name), to = path.join(OUT, r);
    if (e.isDirectory()) { copy(from, r); continue; }
    if (rel === "" && /\.(py|md)$|^package(-lock)?\.json$|^\.gitignore$/.test(e.name)) continue;
    fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.copyFileSync(from, to);
  }
}
copy(ROOT);
fs.writeFileSync(path.join(OUT, "robots.txt"), "User-agent: *\nDisallow: /\n");

// 2. Encrypt every page. "Remember me" is ticked by default so people log in once per device.
const tplSrc = require.resolve("staticrypt/lib/password_template.html");
const tpl = path.join(ROOT, "node_modules", ".clinicref_template.html");
let html = fs.readFileSync(tplSrc, "utf8").replace('name="remember" />', 'name="remember" checked />');
if (!html.includes('name="remember" checked')) throw new Error("StatiCrypt template changed: remember-me default not set");
html = html.replace("<head>", '<head>\n        <meta name="robots" content="noindex, nofollow" />');
fs.writeFileSync(tpl, html);

const pages = [];
(function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p); else if (e.name.endsWith(".html")) pages.push(p);
  }
})(OUT);

const cli = require.resolve("staticrypt/cli/index.js");
for (const dir of [...new Set(pages.map(p => path.dirname(p)))]) {
  const files = pages.filter(p => path.dirname(p) === dir);
  execFileSync(process.execPath, [cli, ...files,
    "-d", dir, "-c", "false", "-s", SALT, "--short",
    "--remember", REMEMBER_DAYS, "-t", tpl,
    "--template-title", "Radiation Oncology Quick Reference",
    "--template-instructions", "Personal clinical reference. Enter the password to continue.",
    "--template-button", "Open",
    "--template-remember", "Remember me on this device",
    "--template-color-primary", "#10243f",
    "--template-color-secondary", "#f3f5f6",
  ], { stdio: ["ignore", "ignore", "inherit"], env: { ...process.env, STATICRYPT_PASSWORD: PASSWORD } });
}
for (const p of pages) {
  if (!fs.readFileSync(p, "utf8").includes("staticrypt")) throw new Error("Not encrypted: " + p);
}

// 3. Encrypt the search index with the same key StatiCrypt stores after login.
(async () => {
  const idxPath = path.join(OUT, "assets", "search-index.js");
  const src = fs.readFileSync(idxPath, "utf8");
  const m = src.match(/^window\.QR_INDEX=([\s\S]*);\s*$/);
  if (!m) throw new Error("Unexpected search-index.js format");
  const hashed = await engine.hashPassword(PASSWORD, SALT);
  const keyBytes = Uint8Array.from(hashed.match(/../g).map(h => parseInt(h, 16)));
  const key = await crypto.subtle.importKey("raw", keyBytes, "AES-CBC", false, ["encrypt"]);
  const iv = crypto.getRandomValues(new Uint8Array(16));
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-CBC", iv }, key, new TextEncoder().encode(m[1])));
  const b64 = Buffer.concat([Buffer.from(iv), Buffer.from(ct)]).toString("base64");
  fs.writeFileSync(idxPath, 'window.QR_INDEX_ENC="' + b64 + '";');
  console.log("Encrypted " + pages.length + " pages and the search index into _site/");
})().catch(e => { console.error(e); process.exit(1); });
