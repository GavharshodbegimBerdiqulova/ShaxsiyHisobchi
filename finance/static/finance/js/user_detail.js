


const userId = window.location.pathname.split("/").filter(Boolean).pop();

function statCard(label, value, code, className) {
  return el(
    "div", { class: "stat " + className },
    el("div", { class: "stat-label", text: label }),
    el("div", { class: "stat-value", text: money(value) + " " + code }),
  );
}

async function loadReport(period) {
  const result = await api("/api/reports/?period=" + period + "&user=" + userId);
  const box = $("report");
  box.replaceChildren();
  $("report-range").textContent = "";
  if (!result.ok) return;

  if (result.data.length === 0) {
    box.append(el("p", { class: "empty", text: t("dash.no_period") }));
    return;
  }
  $("report-range").textContent = result.data[0].start_date + "  —  " + result.data[0].end_date;

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
  const result = await api("/api/accounts/?owner=" + userId);
  const body = $("accounts-rows");
  if (!result.ok) return;

  $("accounts-empty").hidden = result.data.length > 0;


  const totals = {};
  result.data.forEach((account) => {
    totals[account.currency_code] = (totals[account.currency_code] || 0) + Number(account.balance);
    body.append(el(
      "tr", {},
      el("td", { text: account.name }),
      el("td", { text: account.currency_code }),
      el("td", { class: "right", text: money(account.initial_balance) }),
      el("td", { class: "right amount", text: money(account.balance) }),
    ));
  });

  const box = $("totals");
  for (const code in totals) {
    box.append(el("div", { class: "total-chip", text: t("ud.total_balance") + ": " + money(totals[code]) + " " + code }));
  }
}

async function loadTypes(url, listId) {
  const result = await api(url + "?owner=" + userId);
  const list = $(listId);
  if (!result.ok) return;

  if (result.data.length === 0) {
    list.append(el("li", { class: "empty", text: t("type.empty") }));
    return;
  }
  result.data.forEach((type) => list.append(el("li", {}, el("span", { text: type.name }))));
}

async function loadRows(url, bodyId, emptyId, amountClass) {
  const result = await api(url + "?owner=" + userId);
  const body = $(bodyId);
  if (!result.ok) return;

  $(emptyId).hidden = result.data.length > 0;
  result.data.forEach((item) => {
    body.append(el(
      "tr", {},
      el("td", { text: item.date }),
      el("td", { text: item.type_name }),
      el("td", { text: item.account_name }),
      el("td", { class: "right amount " + amountClass, text: money(item.amount) }),
    ));
  });
}

initApp().then(async (user) => {
  if (!user) return;


  if (!user.is_superuser) {
    window.location.href = "/";
    return;
  }

  const result = await api("/api/users/" + userId + "/");
  if (!result.ok) {
    window.location.href = "/users/";
    return;
  }
  const u = result.data;
  $("u-username").textContent = u.username + (u.is_superuser ? " 👑" : "");

  const lastLogin = u.last_login ? u.last_login.slice(0, 10) : t("users.never");
  const fullName = (u.first_name + " " + u.last_name).trim();
  $("u-info").textContent = [
    fullName, u.email,
    t("users.joined") + ": " + u.date_joined.slice(0, 10),
    t("users.last_login") + ": " + lastLogin,
  ].filter(Boolean).join("  ·  ");

  loadReport("day");
  loadAccounts();
  loadTypes("/api/income-types/", "income-types");
  loadTypes("/api/expense-types/", "expense-types");
  loadRows("/api/incomes/", "income-rows", "income-empty", "amount-income");
  loadRows("/api/expenses/", "expense-rows", "expense-empty", "amount-expense");

  document.querySelectorAll("#period-tabs .tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll("#period-tabs .tab").forEach((x) => x.classList.remove("active"));
      tab.classList.add("active");
      loadReport(tab.dataset.period);
    });
  });
});
