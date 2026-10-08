# ShaxsiyHisobchi

## Bu loyiha nima haqida?

**ShaxsiyHisobchi** shaxsiy kirim-chiqimlarni nazorat qiluvchi dastur (hozircha backend: API va admin panel).

Foydalanuvchi o'z pullarining qayerdan kelayotganini (kirim) va qayerga ketayotganini (chiqim) yozib boradi. Pul turgan joylar (naqd pul, karta, valyuta hisobi) alohida hisoblar sifatida yuritiladi. Dastur kunlik, haftalik va oylik hisobot beradi. Shunda foydalanuvchi oyda qancha topgani, qancha sarflagani va qancha qolganini ko'radi.

Misol: foydalanuvchi "Karta" hisobini 1 000 000 so'm bilan ochadi, "Avans" nomli kirim turi bilan 500 000 so'm kirim va "Tushlik" nomli chiqim turi bilan 30 000 so'm chiqim yozadi. Hisobdagi qoldiq 1 470 000 so'm bo'lib ko'rinadi.

## Loyihani qanday ishga tushirish mumkin?

Kerak bo'ladi: Python 3.12 yoki undan yangisi (loyiha 3.14 da yozilgan). Barcha buyruqlar loyiha papkasida (`manage.py` turgan joyda) yoziladi.

```bash
# 1. Virtual muhit yaratish (faqat birinchi marta)
python3 -m venv venv

# 2. Virtual muhitni yoqish
source venv/bin/activate          # Windows'da: venv\Scripts\activate

# 3. Kerakli paketlarni o'rnatish (faqat birinchi marta)
pip install -r requirements.txt

# 4. Bazani tayyorlash
python manage.py migrate

# 5. Superadmin yaratish (faqat birinchi marta)
python manage.py createsuperuser

# 6. Serverni yurgizish
python manage.py runserver
```

Server yurgandan keyin brauzerda oching:

- http://127.0.0.1:8000/ : dastur sahifalari (pushti-gulli ko'rinish; kirish sahifasi `/login/`). Chap tomonda sidebar menyu bor.
- http://127.0.0.1:8000/api/docs/ : Swagger. API'ni shu yerdan sinab ko'rish mumkin.
- http://127.0.0.1:8000/admin/ : admin panel (superadmin login va paroli bilan kiriladi).

Boshlash uchun: Swagger'da `register` orqali ro'yxatdan o'ting, `login` qiling, javobdagi `access` tokenni **Authorize** tugmasiga joylang. Shundan keyin hisob, tur, kirim va chiqim qo'shishingiz mumkin. Hisob ochishdan oldin valyuta kerak. Valyutani (masalan UZS) faqat superadmin qo'sha oladi: admin panelda **Valyutalar** bo'limidan yoki superadmin sifatida `login` qilib `POST /api/currencies/` orqali qo'shing.

Testlarni yurgizish: `python manage.py test`

## Asosiy qoidalar

- **Hammasi dinamik.** Chiqim turlari, kirim turlari, hisoblar va valyutalar kodga yozib qo'yilmagan. Ularni dasturning o'zidan qo'shish, o'zgartirish va o'chirish mumkin.
- **Har kim o'zinikini ko'radi.** Foydalanuvchi faqat o'z hisoblari, turlari, kirimlari va chiqimlarini ko'radi va o'zgartiradi. Boshqa odamning ma'lumotini ko'ra olmaydi.
- **Superadmin hamma narsani ko'radi.** Superadmin barcha foydalanuvchilarning ma'lumotiga kira oladi va valyutalarni boshqaradi.
- **3 tilda ishlaydi:** o'zbekcha (asosiy), ruscha va inglizcha. Sahifalar tepasidagi navbar'da **UZ / RU / EN** tugmalari bor (kirish sahifasida ham). Tanlangan til brauzerda eslab qolinadi. Sahifa matnlari ham, API xabarlari (xato va ogohlantirishlar) ham shu tilda chiqadi. **Valyuta, hisob, kirim turi va chiqim turi nomlari ham 3 tilda saqlanadi** (`name_uz`, `name_ru`, `name_en`). Ularni qo'shganda uchala tilda yozish kerak. Dastur tanlangan tilga mos nomni ko'rsatadi, masalan hisob: "Naqd pul" / "Наличные" / "Cash".
- **Kirish tizimi:** foydalanuvchi login qiladi va JWT token oladi: `access` (30 daqiqa) va `refresh` (7 kun). `access` bilan API'dan foydalanadi, muddati tugasa `refresh` orqali yangisini oladi.

## Ma'lumotlar tuzilishi (jadvallar)

| Jadval | Nima uchun | Misol |
|---|---|---|
| **Valyuta** | Pul birliklari. Hamma uchun umumiy, faqat superadmin qo'shadi. Nomi 3 tilda. | UZS (So'm / Сум / Som) |
| **Hisob** | Pul turgan joy. Har bir hisobda bitta valyuta va boshlang'ich summa bor. | Naqd pul, Karta |
| **Chiqim turi** | Pul nimaga sarflangani. | Yo'lkira, Tushlik, Salomatlik |
| **Kirim turi** | Pul qayerdan kelgani. | Oylik, Avans, Kunlik ish haqi |
| **Chiqim** | Bitta sarf: summa, sana, tur va hisob. | 15 000 so'm, bugun, Tushlik, Naqd pul |
| **Kirim** | Bitta daromad: summa, sana, tur va hisob. | 3 000 000 so'm, 5-oktabr, Avans, Karta |

**Nomlar 3 tilda.** Valyuta, hisob, chiqim turi va kirim turining nomi uchta tilda saqlanadi. API javobida `name` maydoni so'rov tilidagi nomni beradi (`Accept-Language` bo'yicha; til bo'sh bo'lsa o'zbekcha). Tahrirlash uchun `name_uz`, `name_ru`, `name_en` ham qaytadi. Yaratish va o'zgartirishda uchala nom majburiy (PATCH da faqat o'zgargan nomni yuborish mumkin). Bir foydalanuvchida har bir tilda nom takrorlanmaydi.

**Hisobning joriy qoldig'i** bazada saqlanmaydi, har safar hisoblanadi: boshlang'ich summa + shu hisobdagi kirimlar − shu hisobdagi chiqimlar. Shuning uchun kirim yoki chiqim o'zgarsa, qoldiq o'zi to'g'ri chiqadi.

**Hisobotlar** (kunlik, haftalik, oylik) alohida jadval emas. Dastur ularni kirim va chiqimlardan o'zi hisoblab beradi: jami kirim, jami chiqim va ularning farqi.

### Jadvallar o'rtasidagi bog'lanish

- Har bir kirim va chiqim bitta turga va bitta hisobga bog'langan.
- Har bir hisob bitta valyutaga bog'langan.
- Hisob, tur, kirim va chiqim bitta foydalanuvchiga tegishli.
- Ishlatilayotgan tur yoki hisobni o'chirib bo'lmaydi. Shunda eski yozuvlar yo'qolmaydi.
- Bir foydalanuvchida bir xil nomli hisob yoki tur ikki marta bo'lmaydi.

## Kirish (autentifikatsiya) API'lari

| Manzil | Usul | Vazifasi |
|---|---|---|
| `/api/auth/register/` | POST | Ro'yxatdan o'tish (`username`, `email`, `password`, `password2`). Username va email takrorlanmaydi. `access` va `refresh` token qaytaradi. |
| `/api/auth/login/` | POST | `login` (username yoki email) va `password` bilan kirish. `access` va `refresh` token qaytaradi. |
| `/api/auth/token/refresh/` | POST | `refresh` bersa, yangi `access` (va yangi `refresh`) qaytaradi. |
| `/api/auth/logout/` | POST | Tizimdan chiqish: `refresh` token bekor qilinadi (blacklist). |
| `/api/auth/profile/` | GET, PATCH | O'z ma'lumotini ko'rish va o'zgartirish. |

`access` token so'rovga `Authorization: Bearer <access>` sarlavhasi bilan yuboriladi.

**Ruxsatlar:** oddiy foydalanuvchi faqat o'z yozuvlarini o'zgartira oladi, superadmin hammasini. Valyutalarni hamma ko'ra oladi, o'zgartirishni faqat superadmin qiladi.

## Asosiy API'lar

Hammasi `Authorization: Bearer <access>` talab qiladi. Har bir manzil uchun ro'yxat (GET), bitta yozuv (GET `/<id>/`), qo'shish (POST), o'zgartirish (PUT, PATCH) va o'chirish (DELETE) ishlaydi.

| Manzil | Nima uchun | Kim o'zgartira oladi |
|---|---|---|
| `/api/currencies/` | Valyutalar | Faqat superadmin (hamma ko'ra oladi) |
| `/api/accounts/` | Hisoblar (nomi 3 tilda, valyuta, boshlang'ich summa, joriy qoldiq) | Egasi yoki superadmin |
| `/api/expense-types/` | Chiqim turlari | Egasi yoki superadmin |
| `/api/income-types/` | Kirim turlari | Egasi yoki superadmin |
| `/api/expenses/` | Chiqimlar | Egasi yoki superadmin |
| `/api/incomes/` | Kirimlar | Egasi yoki superadmin |
| `/api/reports/` | Hisobot (faqat o'qish) | Hamma o'zinikini ko'radi |
| `/api/users/` | Foydalanuvchilar ro'yxati va bitta foydalanuvchi (faqat o'qish) | **Faqat superadmin** (boshqalarga 403) |

**Superadmin uchun qo'shimcha:** hisob, tur, kirim va chiqim ro'yxatiga `?owner=<foydalanuvchi id>` qo'shsa, faqat shu foydalanuvchining yozuvlari chiqadi. Hisobotga `?user=<id>` qo'shsa, shu foydalanuvchining hisoboti chiqadi. Oddiy foydalanuvchida bu parametrlar boshqaning ma'lumotini ochmaydi.

**Kirim va chiqimni filtrlash:** `?date_from=2026-10-01&date_to=2026-10-31&account=<id>&type=<id>`

**Hisobot:** `/api/reports/?period=day|week|month&date=YYYY-MM-DD`
- `period`: kun, hafta (dushanbadan yakshanbagacha) yoki oy. Bo'sh qoldirilsa `day`.
- `date`: shu sana qaysi davrga tushsa, o'sha davr olinadi. Bo'sh qoldirilsa bugun.
- Natijada jami kirim, jami chiqim va farqi (`balance`) bor. Valyutalar aralashib ketmasligi uchun har bir valyuta alohida qator bo'ladi.

**Qoidalar:**
- Summa 0 dan katta bo'lishi kerak.
- Kirim yoki chiqimga faqat o'zingizning hisobingiz va turingizni tanlay olasiz.
- Kirim yoki chiqimda ishlatilgan tur yoki hisobni, hisobda ishlatilgan valyutani o'chirib bo'lmaydi (xabar bilan 400 qaytadi).

## Dastur sahifalari (frontend)

Chap tomonda sidebar menyu, tepada navbar (til almashtirgich, foydalanuvchi nomi, chiqish tugmasi) bor. Har kimga faqat o'ziga tegishli bo'limlar ko'rinadi.

| Sahifa | Manzil | Kimga | Nima qiladi |
|---|---|---|---|
| Kirish / ro'yxatdan o'tish | `/login/` | Hammaga | Username yoki email bilan kirish, yangi akkaunt ochish |
| Bosh sahifa | `/` | Kirganlarga | Kun, hafta va oy hisoboti, hisob qoldiqlari, oxirgi kirim va chiqimlar |
| Kirimlar | `/incomes/` | Kirganlarga | Ro'yxat, sana, hisob va tur bo'yicha filtr, qo'shish, o'zgartirish, o'chirish |
| Chiqimlar | `/expenses/` | Kirganlarga | Kirimlar bilan bir xil |
| Hisoblar | `/accounts/` | Kirganlarga | Hisob qo'shish (valyuta va boshlang'ich summa bilan), qoldiqni ko'rish |
| Turlar | `/types/` | Kirganlarga | Kirim va chiqim turlari |
| Profil | `/profile/` | Kirganlarga | Ism, familiya va emailni o'zgartirish |
| **Foydalanuvchilar** | `/users/` | **Faqat superadmin** | Hamma foydalanuvchilar ro'yxati: hisoblar, kirimlar va chiqimlar soni |
| **Foydalanuvchi sahifasi** | `/users/<id>/` | **Faqat superadmin** | Bitta foydalanuvchining hammasi: kun, hafta, oy hisoboti, hisoblari va pullari, kirim va chiqimlari, kirim va chiqim turlari |
| **Valyutalar** | `/currencies/` | **Faqat superadmin** | Valyuta qo'shish, o'zgartirish, o'chirish |
| **Admin panel** | `/admin/` | **Faqat superadmin** | Django admin paneliga o'tish |

- Oddiy foydalanuvchi faqat o'zining hisoblari, turlari, kirim va chiqimlarini ko'radi.
- Superadmin hammaning yozuvini ko'radi (jadvalda "Egasi" ustuni chiqadi) va qo'shimcha bo'limlarni ko'radi.
- Oddiy foydalanuvchi `/currencies/` ga kirsa, bosh sahifaga qaytariladi.
- Telefonda sidebar tugma (☰) bilan ochiladi.

### Tillar qanday ishlaydi

- Frontend matnlari `finance/static/finance/js/i18n.js` faylidagi lug'atda turadi (uz, ru, en). Yangi matn qo'shish uchun uchala tilga bir xil kalit yoziladi.
- API xabarlari `locale/ru/` va `locale/en/` fayllarida. Frontend har so'rovga `Accept-Language` sarlavhasini qo'shadi. Tarjimani o'zgartirgandan keyin `python manage.py compilemessages --ignore venv` yurgiziladi (kompyuterda `gettext` o'rnatilgan bo'lishi kerak).

## Admin panel

Manzil: http://127.0.0.1:8000/admin/ (superadmin bilan kiriladi).

- Foydalanuvchilar, valyutalar, hisoblar, chiqim va kirim turlari, chiqimlar va kirimlarni ko'rish, qo'shish, o'zgartirish va o'chirish mumkin.
- Ro'yxatlarda kerakli ustunlar ko'rinadi, qidiruv va filtrlar bor. Kirim va chiqimda sana bo'yicha tezkor filtr ham bor.
- Foydalanuvchi qo'shish yoki o'zgartirishda email takrorlanishi tekshiriladi (API'dagi kabi).

## API hujjati (Swagger)

Serverni yurgizgandan keyin brauzerda oching:

- http://127.0.0.1:8000/api/docs/ : Swagger. Endpoint'larni shu yerdan sinab ko'rish mumkin.
- http://127.0.0.1:8000/api/schema/ : API sxemasi (fayl ko'rinishida).

Himoyalangan endpoint'larni sinash uchun: avval `login` ni ishga tushiring, javobdagi `access` ni nusxalang, sahifa tepasidagi **Authorize** tugmasini bosib, `jwtAuth` maydoniga joylang.

## Ishlash rejasi va holati

| № | Bosqich | Holati |
|---|---|---|
| 1 | Loyiha skeleti va sozlamalar | Tayyor |
| 2 | Modellar (jadvallar) | Tayyor |
| 3 | Serializer'lar (ma'lumotni tekshirish va API formatiga o'tkazish) | Tayyor |
| 3.5 | Kirish tizimi (JWT: register, login, token yangilash, logout, profil, ruxsatlar) | Tayyor |
| 3.6 | Swagger (API hujjati) | Tayyor |
| 4 | View'lar (API amallari va hisobotlar) | Tayyor |
| 5 | Admin panel va URL manzillar | Tayyor |
| 5.5 | Frontend (sidebar, barcha sahifalar, pushti-gulli uslub) | Tayyor |
| 6 | 3 tilga tarjima (API xabarlari va frontend, til almashtirgich) | Tayyor |
| 6.5 | Superadmin uchun foydalanuvchilar bo'limi | Tayyor |
| 7 | Tekshirish va sinov | Avtomatik testlar tayyor (38 ta), qo'lda sinash qoldi |
| 8 | Himoyaga tayyorgarlik | Kutilmoqda |

Frontend (Django template, CSS va JS; pushti-gulli uslub) 5-bosqichdan keyin, tarjimadan oldin qilinmoqda: barcha sahifalar tayyor (kirish, bosh sahifa, kirimlar, chiqimlar, hisoblar, turlar, valyutalar, profil).

Har bosqich alohida tasdiqlanadi va tasdiqlangandan keyingina keyingisiga o'tiladi.

## Texnologiyalar

- Python 3.14
- Django 6.1 (asosiy freymvork)
- Django REST Framework (API uchun)
- Simple JWT (kirish tokenlari uchun)
- drf-spectacular (Swagger hujjati uchun)
- SQLite (ma'lumotlar bazasi, hozircha)

## Papkalar

- `config/` : loyihaning umumiy sozlamalari (`settings.py`: JWT va Swagger sozlamalari ham shu yerda, asosiy `urls.py`)
- `finance/` : asosiy ilova (modellar, serializer'lar, view'lar, ruxsatlar, testlar, admin)
- `finance/templates/`, `finance/static/` : frontend (HTML shablonlar, CSS, JS)
- `locale/` : API xabarlarining tarjimasi (ru, en; o'zbekcha asosiy til)
- `requirements.txt` : kerakli paketlar ro'yxati
