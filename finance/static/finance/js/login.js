// Login va ro'yxatdan o'tish sahifasi

if (isLoggedIn()) {
  window.location.href = "/";
}

const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

// Tablarni almashtirish
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");

    const isLogin = tab.dataset.tab === "login";
    loginForm.hidden = !isLogin;
    registerForm.hidden = isLogin;
  });
});

// Formani yuborish: muvaffaqiyatli bo'lsa tokenlarni saqlab, bosh sahifaga o'tadi
async function submitForm(form, url) {
  const errorBox = form.querySelector(".form-error");
  errorBox.hidden = true;

  const body = Object.fromEntries(new FormData(form));
  const result = await api(url, "POST", body);

  if (result.ok) {
    saveTokens(result.data);
    window.location.href = "/";
  } else {
    errorBox.textContent = errorText(result.data);
    errorBox.hidden = false;
  }
}

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  submitForm(loginForm, "/api/auth/login/");
});

registerForm.addEventListener("submit", (event) => {
  event.preventDefault();
  submitForm(registerForm, "/api/auth/register/");
});
