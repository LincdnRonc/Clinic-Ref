// Google Apps Script for the site's access log. Paste into a Google Sheet (Extensions → Apps Script),
// then Deploy → New deployment → Web app: Execute as "Me", Who has access "Anyone".
// Copy the web app URL into the GitHub secret ACCESS_LOG_URL. Each login adds a row to the first sheet.
function doPost(e) {
  var d = {};
  try { d = JSON.parse(e.postData.contents); } catch (err) { return ContentService.createTextOutput("bad"); }
  var clip = function (v) { return String(v || "").slice(0, 80); };
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sheet.getLastRow() === 0) sheet.appendRow(["Date and time", "Name", "Type", "Page", "Device"]);
  sheet.appendRow([new Date(), clip(d.name) || "(blank)", clip(d.type), clip(d.page), clip(d.device)]);
  return ContentService.createTextOutput("ok");
}
