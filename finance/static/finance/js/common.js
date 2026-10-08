

requireLogin();

let currentUser = null;

function $(id) {
  return document.getElementById(id);
}


function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const key in props) {
    if (key === "class") node.className = props[key];
    else if (key === "text") node.textContent = props[key];
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), props[key]);
    else node.setAttribute(key, props[key]);
  }
  children.forEach((child) => node.append(child));
  return node;
}


function money(value) {
  return Number(value).toLocaleString("ru-RU", { maximumFractionDigits: 2 });
}

function today() {
  const d = new Date();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return d.getFullYear() + "-" + month + "-" + day;
}


async function initApp() {
  const result = await api("/api/auth/profile/");
  if (!result.ok) return null;
  currentUser = result.data;

  $("side-username").textContent = currentUser.username;
  $("side-role").textContent = currentUser.is_superuser ? t("role.admin") : t("role.user");


  if (currentUser.is_superuser) {
    document.querySelectorAll("[data-admin-only]").forEach((item) => { item.hidden = false; });
  }


  document.querySelectorAll(".side-links a").forEach((link) => {
    if (link.getAttribute("href") === window.location.pathname) link.classList.add("active");
  });


  const sidebar = $("sidebar");
  const backdrop = $("backdrop");
  function toggleMenu(open) {
    sidebar.classList.toggle("open", open);
    backdrop.hidden = !open;
  }
  $("menu-btn").addEventListener("click", () => toggleMenu(true));
  backdrop.addEventListener("click", () => toggleMenu(false));

  return currentUser;
}


function closeModal() {
  $("modal").hidden = true;
}


function openModal({ title, fields, values = {}, onSubmit }) {
  const form = $("modal-form");
  $("modal-title").textContent = title;
  form.replaceChildren();

  fields.forEach((field) => {
    let input;
    if (field.type === "select") {
      input = el("select", { name: field.name });
      input.append(el("option", { value: "", text: t("common.select") }));
      field.options.forEach((option) => {
        input.append(el("option", { value: option.value, text: option.label }));
      });
    } else {
      input = el("input", { name: field.name, type: field.type || "text" });
      if (field.step) input.step = field.step;
      if (field.min !== undefined) input.min = field.min;
    }
    input.required = field.required !== false;

    const value = values[field.name];
    if (value !== undefined && value !== null) input.value = value;

    form.append(el("label", {}, field.label, input));
  });

  const errorBox = el("p", { class: "form-error", hidden: "" });
  const saveBtn = el("button", { type: "submit", class: "btn", text: t("common.save") });
  const cancelBtn = el("button", {
    type: "button", class: "btn btn-light", text: t("common.cancel"), onclick: closeModal,
  });
  form.append(errorBox, el("div", { class: "modal-buttons" }, saveBtn, cancelBtn));

  form.onsubmit = async (event) => {
    event.preventDefault();
    errorBox.hidden = true;
    const result = await onSubmit(Object.fromEntries(new FormData(form)));
    if (result.ok) {
      closeModal();
    } else {
      errorBox.textContent = errorText(result.data);
      errorBox.hidden = false;
    }
  };

  $("modal").hidden = false;
}


document.addEventListener("click", (event) => {
  if (event.target === $("modal")) closeModal();
});


function nameFields() {
  return ["uz", "ru", "en"].map((lang) => ({
    name: "name_" + lang,
    label: t("common.name") + " (" + lang.toUpperCase() + ")",
  }));
}


async function deleteItem(url, question, reload) {
  if (!confirm(question)) return;
  const result = await api(url, "DELETE");
  if (result.ok) {
    showToast(t("common.deleted"));
    reload();
  } else {
    showToast(errorText(result.data));
  }
}


function actionButtons(onEdit, onDelete) {
  return el(
    "div", { class: "actions" },
    el("button", { type: "button", class: "icon-btn", title: t("common.edit"), text: "✏️", onclick: onEdit }),
    el("button", { type: "button", class: "icon-btn", title: t("common.delete"), text: "🗑️", onclick: onDelete }),
  );
}
