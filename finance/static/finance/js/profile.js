// Profil sahifasi

initApp().then((user) => {
  if (!user) return;

  const form = $("profile-form");
  form.elements["username"].value = user.username;
  form.elements["first_name"].value = user.first_name;
  form.elements["last_name"].value = user.last_name;
  form.elements["email"].value = user.email;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const errorBox = form.querySelector(".form-error");
    errorBox.hidden = true;

    const data = {
      first_name: form.elements["first_name"].value,
      last_name: form.elements["last_name"].value,
      email: form.elements["email"].value,
    };
    const result = await api("/api/auth/profile/", "PATCH", data);

    if (result.ok) {
      showToast(t("common.saved"));
    } else {
      errorBox.textContent = errorText(result.data);
      errorBox.hidden = false;
    }
  });
});
