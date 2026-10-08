// Kirimlar va chiqimlar sahifasi (ikkalasi uchun bitta kod)

const kind = $("page-data").dataset.kind; // "income" yoki "expense"
const URL_ITEMS = kind === "income" ? "/api/incomes/" : "/api/expenses/";
const URL_TYPES = kind === "income" ? "/api/income-types/" : "/api/expense-types/";

let accounts = [];
let types = [];

function ownerSuffix(item) {
  return currentUser.is_superuser ? " – " + item.owner_name : "";
}

function accountOptions() {
  return accounts.map((a) => ({
    value: a.id, label: a.name + " (" + a.currency_code + ")" + ownerSuffix(a),
  }));
}

function typeOptions() {
  return types.map((t) => ({ value: t.id, label: t.name + ownerSuffix(t) }));
}

function fillSelect(select, options) {
  const first = select.options[0]; // "Hammasi"
  select.replaceChildren(first);
  options.forEach((o) => select.append(el("option", { value: o.value, text: o.label })));
}

async function loadRows() {
  const params = new URLSearchParams();
  new FormData($("filters")).forEach((value, key) => {
    if (value) params.set(key, value);
  });

  const result = await api(URL_ITEMS + "?" + params.toString());
  const body = $("rows");
  body.replaceChildren();
  if (!result.ok) return;

  $("empty").hidden = result.data.length > 0;

  result.data.forEach((item) => {
    const row = el(
      "tr", {},
      el("td", { text: item.date }),
      el("td", { text: item.type_name }),
      el("td", { text: item.account_name }),
      el("td", { class: "right amount amount-" + kind, text: money(item.amount) }),
    );
    if (currentUser.is_superuser) row.append(el("td", { text: item.owner_name }));
    row.append(el("td", {}, actionButtons(
      () => openForm(item),
      () => deleteItem(URL_ITEMS + item.id + "/", t("tx.confirm_delete"), loadRows),
    )));
    body.append(row);
  });
}

// item bo'lsa o'zgartirish, bo'lmasa yangi qo'shish
function openForm(item = null) {
  openModal({
    title: item ? t("tx.edit") : (kind === "income" ? t("tx.new_income") : t("tx.new_expense")),
    fields: [
      { name: "type", label: t("common.type"), type: "select", options: typeOptions() },
      { name: "account", label: t("common.account"), type: "select", options: accountOptions() },
      { name: "amount", label: t("common.amount"), type: "number", step: "0.01", min: "0.01" },
      { name: "date", label: t("common.date"), type: "date" },
    ],
    values: item || { date: today() },
    onSubmit: async (data) => {
      const result = item
        ? await api(URL_ITEMS + item.id + "/", "PATCH", data)
        : await api(URL_ITEMS, "POST", data);
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

  const [accountResult, typeResult] = await Promise.all([api("/api/accounts/"), api(URL_TYPES)]);
  accounts = accountResult.ok ? accountResult.data : [];
  types = typeResult.ok ? typeResult.data : [];

  fillSelect($("filters").elements["account"], accountOptions());
  fillSelect($("filters").elements["type"], typeOptions());

  $("filters").addEventListener("change", loadRows);
  $("reset-btn").addEventListener("click", () => {
    $("filters").reset();
    loadRows();
  });
  $("add-btn").addEventListener("click", () => {
    if (accounts.length === 0 || types.length === 0) {
      showToast(t("tx.need_account_type"));
      return;
    }
    openForm();
  });

  loadRows();
});
