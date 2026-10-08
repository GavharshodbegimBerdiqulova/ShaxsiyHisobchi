

let currencies = [];

async function loadRows() {
  const result = await api("/api/accounts/");
  const body = $("rows");
  body.replaceChildren();
  if (!result.ok) return;

  $("empty").hidden = result.data.length > 0;

  result.data.forEach((account) => {
    const row = el(
      "tr", {},
      el("td", { text: account.name }),
      el("td", { text: account.currency_code }),
      el("td", { class: "right", text: money(account.initial_balance) }),
      el("td", { class: "right amount", text: money(account.balance) }),
    );
    if (currentUser.is_superuser) row.append(el("td", { text: account.owner_name }));
    row.append(el("td", {}, actionButtons(
      () => openForm(account),
      () => deleteItem("/api/accounts/" + account.id + "/", t("acc.confirm_delete"), loadRows),
    )));
    body.append(row);
  });
}

function openForm(account = null) {
  openModal({
    title: account ? t("acc.edit") : t("acc.new"),
    fields: [
      ...nameFields(),
      {
        name: "currency", label: t("common.currency"), type: "select",
        options: currencies.map((c) => ({ value: c.id, label: c.code + " – " + c.name })),
      },
      { name: "initial_balance", label: t("acc.initial"), type: "number", step: "0.01", min: "0" },
    ],
    values: account || { initial_balance: 0 },
    onSubmit: async (data) => {
      const result = account
        ? await api("/api/accounts/" + account.id + "/", "PATCH", data)
        : await api("/api/accounts/", "POST", data);
      if (result.ok) {
        showToast(t("common.saved"));
        loadRows();
      }
      return result;
    },
  });
}

initApp().then(async (user) => {
  if (!user) return;

  const result = await api("/api/currencies/");
  currencies = result.ok ? result.data : [];

  $("add-btn").addEventListener("click", () => {
    if (currencies.length === 0) {
      showToast(t("acc.no_currency"));
      return;
    }
    openForm();
  });
  loadRows();
});
