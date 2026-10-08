# ShaxsiyHisobchi

Shaxsiy kirim-chiqimlarni nazorat qiluvchi dastur (backend: API va admin panel).

## Loyiha nima uchun kerak?

Foydalanuvchi o'z pullarining qayerdan kelayotganini (kirim) va qayerga ketayotganini (chiqim) yozib boradi. Dastur kunlik, haftalik va oylik hisobot beradi. Shunda foydalanuvchi oyda qancha topgani, qancha sarflagani va qancha qolganini ko'radi.

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
| 5 | Admin panel (URL manzillar tayyor) | Kutilmoqda |
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

## Loyihani ishga tushirish

```bash
# 1. Virtual muhitni yoqish
source venv/bin/activate

# 2. Kerakli paketlarni o'rnatish (birinchi marta)
pip install -r requirements.txt

# 3. Bazani tayyorlash
python manage.py migrate

# 4. Superadmin yaratish
python manage.py createsuperuser

# 5. Serverni yurgizish
python manage.py runserver
```

Admin panel: http://127.0.0.1:8000/admin/ (5-bosqichdan keyin ishlaydi)

Swagger: http://127.0.0.1:8000/api/docs/

Testlarni yurgizish: `python manage.py test`

## Papkalar

- `config/` : loyihaning umumiy sozlamalari (`settings.py`: JWT va Swagger sozlamalari ham shu yerda, asosiy `urls.py`)
- `finance/` : asosiy ilova (modellar, serializer'lar, view'lar, ruxsatlar, testlar, admin)
- `locale/` : tarjima fayllari (uz, ru, en)
- `requirements.txt` : kerakli paketlar ro'yxati
