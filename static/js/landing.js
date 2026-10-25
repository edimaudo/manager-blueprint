
// Theme and Scale Logic
const r=document.documentElement,t=document.getElementById("theme"),b=document.querySelectorAll("[data-size]");
function theme(v){r.dataset.theme=v;t.textContent=v==="dark"?"Light mode":"Dark mode";t.setAttribute("aria-pressed",v==="dark");localStorage.setItem("mb-theme",v)}
function size(v){r.style.setProperty("--scale",{small:.875,medium:1,large:1.125}[v]);b.forEach(x=>x.setAttribute("aria-pressed",x.dataset.size===v));localStorage.setItem("mb-size",v)}
theme(localStorage.getItem("mb-theme")||"light");size(localStorage.getItem("mb-size")||"medium");
t.onclick=()=>theme(r.dataset.theme==="dark"?"light":"dark");b.forEach(x=>x.onclick=()=>size(x.dataset.size));

// Landing-page CTAs navigate to the app. Preferences are shared with the application.
