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

- http://127.0.0.1:8000/api/docs/ : Swagger. API'ni shu yerdan sinab ko'rish mumkin.
- http://127.0.0.1:8000/admin/ : admin panel (superadmin login va paroli bilan kiriladi).

Boshlash uchun: Swagger'da `register` orqali ro'yxatdan o'ting, `login` qiling, javobdagi `access` tokenni **Authorize** tugmasiga joylang. Shundan keyin hisob, tur, kirim va chiqim qo'shishingiz mumkin. Hisob ochishdan oldin valyuta kerak. Valyutani (masalan UZS) faqat superadmin qo'sha oladi: admin panelda **Valyutalar** bo'limidan yoki superadmin sifatida `login` qilib `POST /api/currencies/` orqali qo'shing.

Testlarni yurgizish: `python manage.py test`

## Asosiy qoidalar

- **Hammasi dinamik.** Chiqim turlari, kirim turlari, hisoblar va valyutalar kodga yozib qo'yilmagan. Ularni dasturning o'zidan qo'shish, o'zgartirish va o'chirish mumkin.
- **Har kim o'zinikini ko'radi.** Foydalanuvchi faqat o'z hisoblari, turlari, kirimlari va chiqimlarini ko'radi va o'zgartiradi. Boshqa odamning ma'lumotini ko'ra olmaydi.
- **Superadmin hamma narsani ko'radi.** Superadmin barcha foydalanuvchilarning ma'lumotiga kira oladi va valyutalarni boshqaradi.
- **3 tilda ishlaydi:** o'zbekcha (asosiy), ruscha va inglizcha. Dastur matnlari va xabarlari foydalanuvchi tanlagan tilda chiqadi.
- **Kirish tizimi:** foydalanuvchi login qiladi va JWT token oladi: `access` (30 daqiqa) va `refresh` (7 kun). `access` bilan API'dan foydalanadi, muddati tugasa `refresh` orqali yangisini oladi.

## Ma'lumotlar tuzilishi (jadvallar)

| Jadval | Nima uchun | Misol |
|---|---|---|
| **Valyuta** | Pul birliklari. Hamma uchun umumiy, faqat superadmin qo'shadi. | UZS, USD |
| **Hisob** | Pul turgan joy. Har bir hisobda bitta valyuta va boshlang'ich summa bor. | Naqd pul, Karta |
| **Chiqim turi** | Pul nimaga sarflangani. | Yo'lkira, Tushlik, Salomatlik |
| **Kirim turi** | Pul qayerdan kelgani. | Oylik, Avans, Kunlik ish haqi |
| **Chiqim** | Bitta sarf: summa, sana, tur va hisob. | 15 000 so'm, bugun, Tushlik, Naqd pul |
| **Kirim** | Bitta daromad: summa, sana, tur va hisob. | 3 000 000 so'm, 5-oktabr, Avans, Karta |

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
| `/api/accounts/` | Hisoblar (nomi, valyuta, boshlang'ich summa, joriy qoldiq) | Egasi yoki superadmin |
| `/api/expense-types/` | Chiqim turlari | Egasi yoki superadmin |
| `/api/income-types/` | Kirim turlari | Egasi yoki superadmin |
| `/api/expenses/` | Chiqimlar | Egasi yoki superadmin |
| `/api/incomes/` | Kirimlar | Egasi yoki superadmin |
| `/api/reports/` | Hisobot (faqat o'qish) | Hamma o'zinikini ko'radi |

**Kirim va chiqimni filtrlash:** `?date_from=2026-10-01&date_to=2026-10-31&account=<id>&type=<id>`

**Hisobot:** `/api/reports/?period=day|week|month&date=YYYY-MM-DD`
- `period`: kun, hafta (dushanbadan yakshanbagacha) yoki oy. Bo'sh qoldirilsa `day`.
- `date`: shu sana qaysi davrga tushsa, o'sha davr olinadi. Bo'sh qoldirilsa bugun.
- Natijada jami kirim, jami chiqim va farqi (`balance`) bor. Valyutalar aralashib ketmasligi uchun har bir valyuta alohida qator bo'ladi.

**Qoidalar:**
- Summa 0 dan katta bo'lishi kerak.
- Kirim yoki chiqimga faqat o'zingizning hisobingiz va turingizni tanlay olasiz.
- Kirim yoki chiqimda ishlatilgan tur yoki hisobni, hisobda ishlatilgan valyutani o'chirib bo'lmaydi (xabar bilan 400 qaytadi).

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
| 6 | 3 tilga tarjima | Kutilmoqda |
| 7 | Tekshirish va sinov | Kutilmoqda |
| 8 | Himoyaga tayyorgarlik | Kutilmoqda |

Frontend (Django template, CSS va JS; pushti-gulli uslub) oxirida qo'shiladi.

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
- `locale/` : tarjima fayllari (uz, ru, en)
- `requirements.txt` : kerakli paketlar ro'yxati
