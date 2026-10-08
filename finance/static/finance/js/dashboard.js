// Bosh sahifa: hisobot, hisoblar va oxirgi kirim-chiqimlar

function statCard(label, value, code, className) {
  return el(
    "div", { class: "stat " + className },
    el("div", { class: "stat-label", text: label }),
    el("div", { class: "stat-value", text: money(value) + " " + code }),
  );
}

async function loadReport(period) {
  const result = await api("/api/reports/?period=" + period);
  const box = $("report");
  box.replaceChildren();
  if (!result.ok) return;

  if (result.data.length === 0) {
    box.append(el("p", { class: "empty", text: t("dash.no_period") }));
    $("report-range").textContent = "";
    return;
  }

  const first = result.data[0];
  $("report-range").textContent = first.start_date + "  —  " + first.end_date;

  result.data.forEach((row) => {
    box.append(el(
      "div", { class: "stats" },
      statCard(t("dash.income"), row.total_income, row.currency, "stat-income"),
      statCard(t("dash.expense"), row.total_expense, row.currency, "stat-expense"),
      statCard(t("dash.diff"), row.balance, row.currency, "stat-balance"),
    ));
  });
}

async function loadAccounts() {
  const result = await api("/api/accounts/");
  const box = $("accounts");
  box.replaceChildren();
  if (!result.ok) return;

  if (result.data.length === 0) {
    box.append(el("p", { class: "empty", text: t("dash.no_accounts") }));
    return;
  }
  result.data.forEach((account) => {
    let title = account.name;
    if (currentUser.is_superuser) title += " (" + account.owner_name + ")";
    box.append(el(
      "div", { class: "account-card" },
      el("div", { class: "account-name", text: title }),
      el("div", { class: "account-balance", text: money(account.balance) + " " + account.currency_code }),
    ));
  });
}

async function loadLast(url, listId) {
  const result = await api(url);
  const list = $(listId);
  list.replaceChildren();
  if (!result.ok) return;

  if (result.data.length === 0) {
    list.append(el("li", { class: "empty", text: t("common.no_records") }));
    return;
  }
  result.data.slice(0, 5).forEach((item) => {
    list.append(el(
      "li", {},
      el("div", {}, el("strong", { text: item.type_name }), el("div", { class: "muted small", text: item.date + " · " + item.account_name })),
      el("div", { class: "amount", text: money(item.amount) }),
    ));
  });
}

initApp().then((user) => {
  if (!user) return;
  loadReport("day");
  loadAccounts();
  loadLast("/api/incomes/", "last-incomes");
  loadLast("/api/expenses/", "last-expenses");

  // Kun, hafta, oy tugmalari
  document.querySelectorAll("#period-tabs .tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll("#period-tabs .tab").forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      loadReport(tab.dataset.period);
    });
  });
});
