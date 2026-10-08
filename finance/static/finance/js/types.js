// Kirim va chiqim turlari sahifasi

function urlFor(kind) {
  return kind === "income" ? "/api/income-types/" : "/api/expense-types/";
}

async function loadList(box) {
  const kind = box.dataset.kind;
  const list = box.querySelector(".type-list");
  list.replaceChildren();

  const result = await api(urlFor(kind));
  if (!result.ok) return;

  box.querySelector(".empty").hidden = result.data.length > 0;

  result.data.forEach((type) => {
    let name = type.name;
    if (currentUser.is_superuser) name += " (" + type.owner_name + ")";
    list.append(el(
      "li", {},
      el("span", { text: name }),
      actionButtons(
        () => openForm(box, type),
        () => deleteItem(urlFor(kind) + type.id + "/", t("type.confirm_delete"), () => loadList(box)),
      ),
    ));
  });
}

function openForm(box, type = null) {
  const kind = box.dataset.kind;
  openModal({
    title: type ? t("type.edit") : t("type.new"),
    fields: nameFields(),
    values: type || {},
    onSubmit: async (data) => {
      const result = type
        ? await api(urlFor(kind) + type.id + "/", "PATCH", data)
        : await api(urlFor(kind), "POST", data);
      if (result.ok) {
        showToast(t("common.saved"));
        loadList(box);
      }
      return result;
    },
  });
}

initApp().then((user) => {
  if (!user) return;
  document.querySelectorAll(".type-box").forEach((box) => {
    box.querySelector(".add-type").addEventListener("click", () => openForm(box));
    loadList(box);
  });
});
