// API bilan ishlash uchun umumiy funksiyalar

const ACCESS_KEY = "access";
const REFRESH_KEY = "refresh";

function saveTokens(data) {
  localStorage.setItem(ACCESS_KEY, data.access);
  if (data.refresh) {
    localStorage.setItem(REFRESH_KEY, data.refresh);
  }
}

function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

function isLoggedIn() {
  return !!localStorage.getItem(ACCESS_KEY);
}

// Kirmagan foydalanuvchini login sahifasiga yuboradi
function requireLogin() {
  if (!isLoggedIn()) {
    window.location.href = "/login/";
  }
}

// access tokenning muddati tugasa, refresh orqali yangisini oladi
async function refreshAccess() {
  const refresh = localStorage.getItem(REFRESH_KEY);
  if (!refresh) return false;

  const response = await fetch("/api/auth/token/refresh/", {
    method: "POST",
    headers: { "Content-Type": "application/json", "Accept-Language": getLang() },
    body: JSON.stringify({ refresh: refresh }),
  });
  if (!response.ok) return false;

  saveTokens(await response.json());
  return true;
}

// Token bilan so'rov yuboradi. Natija: { ok, status, data }
async function api(url, method = "GET", body = null) {
  async function send() {
    // Accept-Language: server xabarlari tanlangan tilda qaytadi
    const headers = { "Content-Type": "application/json", "Accept-Language": getLang() };
    const access = localStorage.getItem(ACCESS_KEY);
    if (access) headers["Authorization"] = "Bearer " + access;

    return fetch(url, {
      method: method,
      headers: headers,
      body: body ? JSON.stringify(body) : null,
    });
  }

  let response = await send();

  if (response.status === 401 && (await refreshAccess())) {
    response = await send();
  }
  if (response.status === 401) {
    clearTokens();
    window.location.href = "/login/";
  }

  let data = null;
  if (response.status !== 204) {
    data = await response.json().catch(() => null);
  }
  return { ok: response.ok, status: response.status, data: data };
}

// API xatolarini bitta matnga aylantiradi
function errorText(data) {
  if (!data) return t("common.error");
  if (typeof data === "string") return data;
  if (data.detail) return data.detail;

  const parts = [];
  for (const key in data) {
    const value = Array.isArray(data[key]) ? data[key].join(" ") : data[key];
    parts.push(value);
  }
  return parts.join(" ");
}

// Pastda chiqadigan kichik xabar
function showToast(text) {
  const toast = document.getElementById("toast");
  toast.textContent = text;
  toast.hidden = false;
  setTimeout(() => { toast.hidden = true; }, 3000);
}

// Tizimdan chiqish tugmasi (agar sahifada bo'lsa)
document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("logout-btn");
  if (!button) return;

  button.addEventListener("click", async () => {
    await api("/api/auth/logout/", "POST", { refresh: localStorage.getItem(REFRESH_KEY) });
    clearTokens();
    window.location.href = "/login/";
  });
});
