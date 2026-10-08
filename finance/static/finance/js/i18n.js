

const LANGS = ["uz", "ru", "en"];

const TEXTS = {
  uz: {
    "nav.home": "🏠 Bosh sahifa", "nav.incomes": "💰 Kirimlar", "nav.expenses": "🛍️ Chiqimlar",
    "nav.accounts": "👛 Hisoblar", "nav.types": "🏷️ Turlar", "nav.profile": "🌷 Profil",
    "nav.superadmin": "Superadmin 👑", "nav.currencies": "💱 Valyutalar", "nav.admin": "⚙️ Admin panel",
    "nav.logout": "Chiqish", "role.user": "Foydalanuvchi", "role.admin": "Superadmin 👑",

    "page.login": "Kirish", "page.dashboard": "Bosh sahifa 🌷", "page.incomes": "Kirimlar 💰",
    "page.expenses": "Chiqimlar 🛍️", "page.accounts": "Hisoblar 👛", "page.types": "Turlar 🏷️",
    "page.currencies": "Valyutalar 💱", "page.profile": "Profil 🌷",

    "common.save": "Saqlash 💖", "common.cancel": "Bekor qilish", "common.saved": "Saqlandi 🌸",
    "common.deleted": "O'chirildi 🌸", "common.select": "Tanlang...", "common.all": "Hammasi",
    "common.edit": "O'zgartirish", "common.delete": "O'chirish", "common.add": "+ Qo'shish",
    "common.error": "Xatolik yuz berdi. Qaytadan urinib ko'ring.",
    "common.date": "Sana", "common.type": "Tur", "common.account": "Hisob", "common.amount": "Summa",
    "common.owner": "Egasi", "common.name": "Nomi", "common.currency": "Valyuta",
    "common.no_records": "Hali yozuv yo'q 🌸",

    "login.subtitle": "Kirim-chiqimlaringiz bir joyda 💖", "login.tab_login": "Kirish",
    "login.tab_register": "Ro'yxatdan o'tish", "login.login": "Username yoki email",
    "login.password": "Parol", "login.btn_login": "Kirish 🌷", "login.username": "Username",
    "login.email": "Email", "login.password2": "Parolni takrorlang",
    "login.btn_register": "Ro'yxatdan o'tish 🌺",

    "dash.report": "Hisobot", "dash.day": "Kun", "dash.week": "Hafta", "dash.month": "Oy",
    "dash.accounts": "Hisoblarim 👛", "dash.last_incomes": "Oxirgi kirimlar 💰",
    "dash.last_expenses": "Oxirgi chiqimlar 🛍️", "dash.income": "Kirim", "dash.expense": "Chiqim",
    "dash.diff": "Farq", "dash.no_period": "Bu davrda yozuv yo'q 🌸",
    "dash.no_accounts": "Hali hisob yo'q. Hisoblar bo'limidan qo'shing 🌸",

    "tx.from": "Sanadan", "tx.to": "Sanagacha", "tx.reset": "Tozalash",
    "tx.new_income": "Yangi kirim 💰", "tx.new_expense": "Yangi chiqim 🛍️",
    "tx.edit": "Yozuvni o'zgartirish", "tx.need_account_type": "Avval hisob va tur qo'shing 🌸",
    "tx.confirm_delete": "Bu yozuvni o'chirasizmi?",

    "acc.add": "+ Hisob qo'shish", "acc.initial": "Boshlang'ich summa", "acc.balance": "Joriy qoldiq",
    "acc.empty": "Hali hisob yo'q. Birinchi hisobingizni qo'shing 🌸", "acc.new": "Yangi hisob 👛",
    "acc.edit": "Hisobni o'zgartirish", "acc.name_hint": "Nomi (masalan: Naqd pul, Karta)",
    "acc.no_currency": "Valyuta yo'q. Superadmin valyuta qo'shishi kerak 🌸",
    "acc.confirm_delete": "Hisobni o'chirasizmi?",

    "type.income_title": "Kirim turlari 💰", "type.expense_title": "Chiqim turlari 🛍️",
    "type.empty": "Hali tur yo'q 🌸", "type.new": "Yangi tur 🏷️", "type.edit": "Turni o'zgartirish",
    "type.confirm_delete": "Turni o'chirasizmi?",

    "cur.add": "+ Valyuta qo'shish",
    "cur.info": "Valyutalarni faqat superadmin boshqaradi. Foydalanuvchilar hisob ochganda shu ro'yxatdan tanlaydi.",
    "cur.code": "Kodi", "cur.code_hint": "Kodi (masalan: UZS)", "cur.name_hint": "Nomi (masalan: So'm)",
    "cur.empty": "Hali valyuta yo'q. Masalan UZS ni qo'shing 🌸", "cur.new": "Yangi valyuta 💱",
    "cur.edit": "Valyutani o'zgartirish", "cur.confirm_delete": "Valyutani o'chirasizmi?",

    "prof.first": "Ism", "prof.last": "Familiya",

    "nav.users": "👥 Foydalanuvchilar", "page.users": "Foydalanuvchilar 👥", "page.user_detail": "Foydalanuvchi 👤",
    "users.fullname": "F.I.Sh.", "users.joined": "Ro'yxatdan o'tgan", "users.last_login": "Oxirgi kirish",
    "users.accounts": "Hisoblar", "users.incomes": "Kirimlar", "users.expenses": "Chiqimlar",
    "users.view": "Ko'rish", "users.back": "← Foydalanuvchilar", "users.never": "kirmagan",
    "users.admin_badge": "Superadmin 👑", "users.info": "Superadmin barcha foydalanuvchilarning ma'lumotini ko'ra oladi.",
    "ud.accounts": "Hisoblar 👛", "ud.incomes": "Kirimlar 💰", "ud.expenses": "Chiqimlar 🛍️",
    "ud.total_balance": "Jami qoldiq",
  },

  ru: {
    "nav.home": "🏠 Главная", "nav.incomes": "💰 Доходы", "nav.expenses": "🛍️ Расходы",
    "nav.accounts": "👛 Счета", "nav.types": "🏷️ Категории", "nav.profile": "🌷 Профиль",
    "nav.superadmin": "Суперадмин 👑", "nav.currencies": "💱 Валюты", "nav.admin": "⚙️ Админ-панель",
    "nav.logout": "Выйти", "role.user": "Пользователь", "role.admin": "Суперадмин 👑",

    "page.login": "Вход", "page.dashboard": "Главная 🌷", "page.incomes": "Доходы 💰",
    "page.expenses": "Расходы 🛍️", "page.accounts": "Счета 👛", "page.types": "Категории 🏷️",
    "page.currencies": "Валюты 💱", "page.profile": "Профиль 🌷",

    "common.save": "Сохранить 💖", "common.cancel": "Отмена", "common.saved": "Сохранено 🌸",
    "common.deleted": "Удалено 🌸", "common.select": "Выберите...", "common.all": "Все",
    "common.edit": "Изменить", "common.delete": "Удалить", "common.add": "+ Добавить",
    "common.error": "Произошла ошибка. Попробуйте ещё раз.",
    "common.date": "Дата", "common.type": "Категория", "common.account": "Счёт", "common.amount": "Сумма",
    "common.owner": "Владелец", "common.name": "Название", "common.currency": "Валюта",
    "common.no_records": "Записей пока нет 🌸",

    "login.subtitle": "Ваши доходы и расходы в одном месте 💖", "login.tab_login": "Вход",
    "login.tab_register": "Регистрация", "login.login": "Имя пользователя или email",
    "login.password": "Пароль", "login.btn_login": "Войти 🌷", "login.username": "Имя пользователя",
    "login.email": "Email", "login.password2": "Повторите пароль",
    "login.btn_register": "Зарегистрироваться 🌺",

    "dash.report": "Отчёт", "dash.day": "День", "dash.week": "Неделя", "dash.month": "Месяц",
    "dash.accounts": "Мои счета 👛", "dash.last_incomes": "Последние доходы 💰",
    "dash.last_expenses": "Последние расходы 🛍️", "dash.income": "Доход", "dash.expense": "Расход",
    "dash.diff": "Разница", "dash.no_period": "За этот период записей нет 🌸",
    "dash.no_accounts": "Счетов пока нет. Добавьте их в разделе «Счета» 🌸",

    "tx.from": "С даты", "tx.to": "По дату", "tx.reset": "Сбросить",
    "tx.new_income": "Новый доход 💰", "tx.new_expense": "Новый расход 🛍️",
    "tx.edit": "Изменить запись", "tx.need_account_type": "Сначала добавьте счёт и категорию 🌸",
    "tx.confirm_delete": "Удалить эту запись?",

    "acc.add": "+ Добавить счёт", "acc.initial": "Начальная сумма", "acc.balance": "Текущий остаток",
    "acc.empty": "Счетов пока нет. Добавьте первый счёт 🌸", "acc.new": "Новый счёт 👛",
    "acc.edit": "Изменить счёт", "acc.name_hint": "Название (например: Наличные, Карта)",
    "acc.no_currency": "Нет валют. Суперадмин должен добавить валюту 🌸",
    "acc.confirm_delete": "Удалить счёт?",

    "type.income_title": "Категории доходов 💰", "type.expense_title": "Категории расходов 🛍️",
    "type.empty": "Категорий пока нет 🌸", "type.new": "Новая категория 🏷️", "type.edit": "Изменить категорию",
    "type.confirm_delete": "Удалить категорию?",

    "cur.add": "+ Добавить валюту",
    "cur.info": "Валютами управляет только суперадмин. Пользователи выбирают их из этого списка при создании счёта.",
    "cur.code": "Код", "cur.code_hint": "Код (например: UZS)", "cur.name_hint": "Название (например: Сум)",
    "cur.empty": "Валют пока нет. Например, добавьте UZS 🌸", "cur.new": "Новая валюта 💱",
    "cur.edit": "Изменить валюту", "cur.confirm_delete": "Удалить валюту?",

    "prof.first": "Имя", "prof.last": "Фамилия",

    "nav.users": "👥 Пользователи", "page.users": "Пользователи 👥", "page.user_detail": "Пользователь 👤",
    "users.fullname": "Имя", "users.joined": "Зарегистрирован", "users.last_login": "Последний вход",
    "users.accounts": "Счета", "users.incomes": "Доходы", "users.expenses": "Расходы",
    "users.view": "Открыть", "users.back": "← Пользователи", "users.never": "не входил",
    "users.admin_badge": "Суперадмин 👑", "users.info": "Суперадмин видит данные всех пользователей.",
    "ud.accounts": "Счета 👛", "ud.incomes": "Доходы 💰", "ud.expenses": "Расходы 🛍️",
    "ud.total_balance": "Общий остаток",
  },

  en: {
    "nav.home": "🏠 Home", "nav.incomes": "💰 Income", "nav.expenses": "🛍️ Expenses",
    "nav.accounts": "👛 Accounts", "nav.types": "🏷️ Categories", "nav.profile": "🌷 Profile",
    "nav.superadmin": "Superadmin 👑", "nav.currencies": "💱 Currencies", "nav.admin": "⚙️ Admin panel",
    "nav.logout": "Log out", "role.user": "User", "role.admin": "Superadmin 👑",

    "page.login": "Sign in", "page.dashboard": "Home 🌷", "page.incomes": "Income 💰",
    "page.expenses": "Expenses 🛍️", "page.accounts": "Accounts 👛", "page.types": "Categories 🏷️",
    "page.currencies": "Currencies 💱", "page.profile": "Profile 🌷",

    "common.save": "Save 💖", "common.cancel": "Cancel", "common.saved": "Saved 🌸",
    "common.deleted": "Deleted 🌸", "common.select": "Select...", "common.all": "All",
    "common.edit": "Edit", "common.delete": "Delete", "common.add": "+ Add",
    "common.error": "Something went wrong. Please try again.",
    "common.date": "Date", "common.type": "Category", "common.account": "Account", "common.amount": "Amount",
    "common.owner": "Owner", "common.name": "Name", "common.currency": "Currency",
    "common.no_records": "No records yet 🌸",

    "login.subtitle": "Your income and expenses in one place 💖", "login.tab_login": "Sign in",
    "login.tab_register": "Sign up", "login.login": "Username or email",
    "login.password": "Password", "login.btn_login": "Sign in 🌷", "login.username": "Username",
    "login.email": "Email", "login.password2": "Repeat password",
    "login.btn_register": "Sign up 🌺",

    "dash.report": "Report", "dash.day": "Day", "dash.week": "Week", "dash.month": "Month",
    "dash.accounts": "My accounts 👛", "dash.last_incomes": "Latest income 💰",
    "dash.last_expenses": "Latest expenses 🛍️", "dash.income": "Income", "dash.expense": "Expense",
    "dash.diff": "Difference", "dash.no_period": "No records for this period 🌸",
    "dash.no_accounts": "No accounts yet. Add one in the Accounts section 🌸",

    "tx.from": "From", "tx.to": "To", "tx.reset": "Reset",
    "tx.new_income": "New income 💰", "tx.new_expense": "New expense 🛍️",
    "tx.edit": "Edit record", "tx.need_account_type": "Add an account and a category first 🌸",
    "tx.confirm_delete": "Delete this record?",

    "acc.add": "+ Add account", "acc.initial": "Initial amount", "acc.balance": "Current balance",
    "acc.empty": "No accounts yet. Add your first account 🌸", "acc.new": "New account 👛",
    "acc.edit": "Edit account", "acc.name_hint": "Name (for example: Cash, Card)",
    "acc.no_currency": "No currencies. A superadmin has to add a currency 🌸",
    "acc.confirm_delete": "Delete this account?",

    "type.income_title": "Income categories 💰", "type.expense_title": "Expense categories 🛍️",
    "type.empty": "No categories yet 🌸", "type.new": "New category 🏷️", "type.edit": "Edit category",
    "type.confirm_delete": "Delete this category?",

    "cur.add": "+ Add currency",
    "cur.info": "Only a superadmin manages currencies. Users pick from this list when they create an account.",
    "cur.code": "Code", "cur.code_hint": "Code (for example: UZS)", "cur.name_hint": "Name (for example: Som)",
    "cur.empty": "No currencies yet. For example, add UZS 🌸", "cur.new": "New currency 💱",
    "cur.edit": "Edit currency", "cur.confirm_delete": "Delete this currency?",

    "prof.first": "First name", "prof.last": "Last name",

    "nav.users": "👥 Users", "page.users": "Users 👥", "page.user_detail": "User 👤",
    "users.fullname": "Full name", "users.joined": "Joined", "users.last_login": "Last login",
    "users.accounts": "Accounts", "users.incomes": "Income", "users.expenses": "Expenses",
    "users.view": "View", "users.back": "← Users", "users.never": "never",
    "users.admin_badge": "Superadmin 👑", "users.info": "A superadmin can see the data of all users.",
    "ud.accounts": "Accounts 👛", "ud.incomes": "Income 💰", "ud.expenses": "Expenses 🛍️",
    "ud.total_balance": "Total balance",
  },
};

function getLang() {
  let lang = null;
  try { lang = localStorage.getItem("lang"); } catch (e) {  }
  return LANGS.includes(lang) ? lang : "uz";
}


function setLang(lang) {
  localStorage.setItem("lang", lang);
  window.location.reload();
}


function t(key) {
  const texts = TEXTS[getLang()];
  return texts[key] !== undefined ? texts[key] : TEXTS.uz[key] !== undefined ? TEXTS.uz[key] : key;
}


function translatePage() {
  document.documentElement.lang = getLang();

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });

  const page = document.body.dataset.page;
  if (page) document.title = t(page) + " | ShaxsiyHisobchi";


  document.querySelectorAll(".lang-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === getLang());
    button.addEventListener("click", () => setLang(button.dataset.lang));
  });
}

document.addEventListener("DOMContentLoaded", translatePage);
