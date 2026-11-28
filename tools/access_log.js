// Access log: runs inside every page after the password unlocks it (added at deploy by encrypt_site.js
// only when the ACCESS_LOG_URL secret is set). Sends name, page and device to the Google Sheet behind
// tools/access_log.gs. One row per login, plus one per return visit after 30 minutes away.
(function () {
  var URL = "__LOG_URL__", GAP = 30 * 60 * 1000;
  function device() {
    var u = navigator.userAgent;
    if (/iPad|Macintosh.*Mobile/.test(u) || (/Macintosh/.test(u) && navigator.maxTouchPoints > 1)) return "iPad";
    if (/iPhone/.test(u)) return "iPhone";
    if (/Android/.test(u)) return "Android";
    if (/Windows/.test(u)) return "Windows";
    if (/Macintosh/.test(u)) return "Mac";
    return "Other";
  }
  function send(name, type) {
    var body = JSON.stringify({ name: name, type: type, page: location.pathname.split("/").pop() || "index.html", device: device() });
    try { if (navigator.sendBeacon && navigator.sendBeacon(URL, body)) return; } catch (_) {}
    try { fetch(URL, { method: "POST", mode: "no-cors", body: body, keepalive: true }); } catch (_) {}
  }
  function log(name) {
    var now = Date.now(), fresh = false, last = 0;
    try { fresh = sessionStorage.getItem("qr_login") === "1"; sessionStorage.removeItem("qr_login"); } catch (_) {}
    try { last = +localStorage.getItem("qr_last_log") || 0; } catch (_) {}
    if (!fresh && now - last < GAP) { try { localStorage.setItem("qr_last_log", now); } catch (_) {} return; }
    try { localStorage.setItem("qr_last_log", now); } catch (_) {}
    send(name, fresh ? "Login" : "Return visit");
  }
  // Devices that were already remembered before the name box existed: ask once.
  function ask() {
    var d = document.createElement("div");
    d.setAttribute("style", "position:fixed;inset:0;background:rgba(16,36,63,.55);z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px");
    d.innerHTML = '<form style="background:#fff;border-radius:10px;padding:20px;max-width:340px;width:100%;font:15px system-ui,sans-serif;color:#10243f">'
      + '<p style="margin:0 0 10px;font-weight:600">Your name</p>'
      + '<input required maxlength="80" autocomplete="name" placeholder="Your name" style="width:100%;box-sizing:border-box;padding:10px 12px;font-size:16px;border:1px solid #ccd;border-radius:6px">'
      + '<p style="font-size:12px;color:#5b6675;margin:8px 0 12px">Your name is recorded each time you open the site.</p>'
      + '<button style="width:100%;padding:10px;border:0;border-radius:6px;background:#10243f;color:#fff;font-size:15px">Continue</button></form>';
    document.body.appendChild(d);
    var f = d.querySelector("form"), i = d.querySelector("input");
    setTimeout(function () { i.focus(); }, 50);
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var n = i.value.trim(); if (!n) return;
      try { localStorage.setItem("qr_user", n); sessionStorage.setItem("qr_login", "1"); } catch (_) {}
      d.remove(); log(n);
    });
  }
  var name = "";
  try { name = (localStorage.getItem("qr_user") || "").trim(); } catch (_) {}
  if (name) log(name);
  else if (document.body) ask();
  else document.addEventListener("DOMContentLoaded", ask);
})();
