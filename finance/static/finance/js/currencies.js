

async function loadRows() {
  const result = await api("/api/currencies/");
  const body = $("rows");
  body.replaceChildren();
  if (!result.ok) return;

  $("empty").hidden = result.data.length > 0;

  result.data.forEach((currency) => {
    body.append(el(
      "tr", {},
      el("td", {}, el("strong", { text: currency.code })),
      el("td", { text: currency.name_uz }),
      el("td", { text: currency.name_ru }),
      el("td", { text: currency.name_en }),
      el("td", {}, actionButtons(
        () => openForm(currency),
        () => deleteItem("/api/currencies/" + currency.id + "/", t("cur.confirm_delete"), loadRows),
      )),
    ));
  });
}

function openForm(currency = null) {
  openModal({
    title: currency ? t("cur.edit") : t("cur.new"),
    fields: [
      { name: "code", label: t("cur.code") },
      ...nameFields(),
    ],
    values: currency || {},
    onSubmit: async (data) => {
      const result = currency
        ? await api("/api/currencies/" + currency.id + "/", "PATCH", data)
        : await api("/api/currencies/", "POST", data);
      if (result.ok) {
        showToast(t("common.saved"));
        loadRows();
      }
      return result;
    },
  });
}

initApp().then((user) => {
  if (!user) return;


  if (!user.is_superuser) {
    window.location.href = "/";
    return;
  }
  $("add-btn").addEventListener("click", () => openForm());
  loadRows();
});
