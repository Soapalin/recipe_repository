const installButton = document.getElementById("install-btn");
const lastUrl = document.getElementById("last-url");
const lastTitle = document.getElementById("last-title");

let deferredPrompt = null;

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredPrompt = event;
  if (installButton) installButton.hidden = false;
});

installButton?.addEventListener("click", async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  await deferredPrompt.userChoice;
  deferredPrompt = null;
  if (installButton) installButton.hidden = true;
});

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js");
}

const storedShare = JSON.parse(localStorage.getItem("lastShare") || "null");
if (storedShare?.url) {
  lastUrl.textContent = storedShare.url;
  lastTitle.textContent = storedShare.title ? `Title: ${storedShare.title}` : "";
}
