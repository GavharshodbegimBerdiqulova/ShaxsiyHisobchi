

initApp().then(async (user) => {
  if (!user) return;


  if (!user.is_superuser) {
    window.location.href = "/";
    return;
  }

  const result = await api("/api/users/");
  if (!result.ok) return;

  const body = $("rows");
  result.data.forEach((u) => {
    const name = el("strong", { text: u.username });
    const nameCell = el("td", {}, name);
    if (u.is_superuser) nameCell.append(" ", el("span", { class: "badge", text: t("users.admin_badge") }));

    body.append(el(
      "tr", {},
      nameCell,
      el("td", { text: (u.first_name + " " + u.last_name).trim() || "—" }),
      el("td", { text: u.email || "—" }),
      el("td", { text: u.date_joined.slice(0, 10) }),
      el("td", { class: "right", text: u.accounts_count }),
      el("td", { class: "right", text: u.incomes_count }),
      el("td", { class: "right", text: u.expenses_count }),
      el("td", { class: "right" }, el("a", { class: "btn btn-small", href: "/users/" + u.id + "/", text: t("users.view") })),
    ));
  });
});
