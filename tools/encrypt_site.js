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

// 1b. Access log (optional): if the ACCESS_LOG_URL secret is set, every page gets a small script,
//     inside the encryption so the URL stays private, that sends the visitor's name to a Google Sheet.
const LOG_URL = (process.env.ACCESS_LOG_URL || "").trim();
if (LOG_URL) {
  const logJs = fs.readFileSync(path.join(__dirname, "access_log.js"), "utf8").replace("__LOG_URL__", LOG_URL);
  let n = 0;
  (function walk(d) {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) { walk(p); continue; }
      if (!e.name.endsWith(".html")) continue;
      const t = fs.readFileSync(p, "utf8");
      const i = t.lastIndexOf("</body>");
      if (i < 0) continue;
      fs.writeFileSync(p, t.slice(0, i) + "<script>" + logJs + "</script>\n" + t.slice(i));
      n++;
    }
  })(OUT);
  console.log("Access log added to " + n + " pages");
} else {
  console.log("ACCESS_LOG_URL not set: no access log");
}

// 2. Encrypt every page. "Remember me" is ticked by default so people log in once per device.
const tplSrc = require.resolve("staticrypt/lib/password_template.html");
const tpl = path.join(ROOT, "node_modules", ".clinicref_template.html");
let html = fs.readFileSync(tplSrc, "utf8").replace('name="remember" />', 'name="remember" checked />');
if (!html.includes('name="remember" checked')) throw new Error("StatiCrypt template changed: remember-me default not set");
html = html.replace("<head>", '<head>\n        <meta name="robots" content="noindex, nofollow" />');
if (LOG_URL) {
  // Name box above the password; remembered on this device and logged after a successful login.
  const nameBox = '<input id="qr-name" type="text" name="qrname" placeholder="Your name" autocomplete="name" required maxlength="80" '
    + 'style="width:100%;box-sizing:border-box;padding:15px;margin-bottom:15px;font-size:14px;border:0;outline:0;background:#f3f5f6" />';
  const before = '<div class="staticrypt-password-container">';
  if (!html.includes(before)) throw new Error("StatiCrypt template changed: name box not added");
  html = html.replace(before, nameBox + "\n" + before);
  const note = '<p style="font-size:12px;color:#5b6675;margin:10px 0 0">Your name is recorded each time you open the site.</p>';
  html = html.replace("</form>", note + "\n</form>");
  const hook = 'const { isSuccessful } = await staticrypt.handleDecryptionOfPage(password, isRememberChecked);';
  if (!html.includes(hook)) throw new Error("StatiCrypt template changed: name not saved on login");
  html = html.replace(hook,
    'try { localStorage.setItem("qr_user", document.getElementById("qr-name").value.trim()); sessionStorage.setItem("qr_login", "1"); } catch (_) {}\n                ' + hook);
  html = html.replace("</body>",
    '<script>try{var qn=document.getElementById("qr-name"),qv=localStorage.getItem("qr_user");if(qv)qn.value=qv;'
    + 'window.addEventListener("load",function(){setTimeout(function(){if(!qn.value)qn.focus();},0);});}catch(_){}</script>\n</body>');
}
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

  // 4. Tie the offline cache to the password: after a password change, every device drops
  //    its cached pages (locked with the old password) instead of mixing old and new.
  const swPath = path.join(OUT, "sw.js");
  const tag = require("crypto").createHash("sha256").update(hashed).digest("hex").slice(0, 8);
  const sw = fs.readFileSync(swPath, "utf8");
  if (!/const V='[^']+'/.test(sw)) throw new Error("Unexpected sw.js format");
  fs.writeFileSync(swPath, sw.replace(/const V='([^']+)'/, (_, v) => "const V='" + v + "-" + tag + "'"));
  console.log("Encrypted " + pages.length + " pages and the search index into _site/");
})().catch(e => { console.error(e); process.exit(1); });
