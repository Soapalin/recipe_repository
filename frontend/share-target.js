const params = new URLSearchParams(location.search);
const title = params.get("title") || "";
const text = params.get("text") || "";
const url = params.get("url") || "";
const webhookUrl = "http://localhost:9999/recipe/share";
const receivedAt = new Date().toISOString();
const hasSharedData = Boolean(title || text || url);

const titleEl = document.getElementById("shared-title");
const textEl = document.getElementById("shared-text");
const urlEl = document.getElementById("shared-url");
const openLink = document.getElementById("open-url");
const sendButton = document.getElementById("send-webhook");
const statusEl = document.getElementById("webhook-status");

if (titleEl) titleEl.textContent = title || "(none)";
if (textEl) textEl.textContent = text || "(none)";
if (urlEl) urlEl.textContent = url || "(none)";

if (url && openLink) {
  openLink.href = url;
  openLink.hidden = false;
}

if (url) {
  localStorage.setItem(
    "lastShare",
    JSON.stringify({ title, text, url, receivedAt })
  );
}

const payload = new URLSearchParams({ title, text, url, receivedAt });
const payloadString = payload.toString();

function sendToWebhook() {
  if (!hasSharedData) return;
  if (statusEl) statusEl.textContent = "Sending to webhook...";

  const sent =
    "sendBeacon" in navigator &&
    navigator.sendBeacon(
      webhookUrl,
      new Blob([payloadString], {
        type: "application/x-www-form-urlencoded;charset=UTF-8",
      })
    );

  if (sent) {
    if (statusEl) statusEl.textContent = "Webhook sent.";
    return;
  }

  fetch(webhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: payloadString,
    keepalive: true,
  })
    .then(() => {
      if (statusEl) statusEl.textContent = "Webhook sent.";
    })
    .catch(() => {
      if (statusEl) statusEl.textContent = "Webhook failed to send.";
    });
}

if (sendButton) {
  sendButton.addEventListener("click", sendToWebhook);
  sendButton.disabled = !hasSharedData;
}

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js");
}
