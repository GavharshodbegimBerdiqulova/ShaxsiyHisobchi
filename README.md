# ShaxsiyHisobchi

Shaxsiy kirim-chiqimlarni nazorat qiluvchi dastur (backend: API va admin panel).

## Loyiha nima uchun kerak?

Foydalanuvchi o'z pullarining qayerdan kelayotganini (kirim) va qayerga ketayotganini (chiqim) yozib boradi. Dastur kunlik, haftalik va oylik hisobot beradi. Shunda foydalanuvchi oyda qancha topgani, qancha sarflagani va qancha qolganini ko'radi.

## Asosiy qoidalar

- **Hammasi dinamik.** Chiqim turlari, kirim turlari, hisoblar va valyutalar kodga yozib qo'yilmagan. Ularni dasturning o'zidan qo'shish, o'zgartirish va o'chirish mumkin.
- **Har kim o'zinikini ko'radi.** Foydalanuvchi faqat o'z hisoblari, turlari, kirimlari va chiqimlarini ko'radi va o'zgartiradi. Boshqa odamning ma'lumotini ko'ra olmaydi.
- **Superadmin hamma narsani ko'radi.** Superadmin barcha foydalanuvchilarning ma'lumotiga kira oladi va valyutalarni boshqaradi.
- **3 tilda ishlaydi:** o'zbekcha (asosiy), ruscha va inglizcha. Dastur matnlari va xabarlari foydalanuvchi tanlagan tilda chiqadi.
- **Kirish tizimi:** foydalanuvchi login qiladi va token oladi. Token bilan API'dan foydalanadi.

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

## Ishlash rejasi va holati

| № | Bosqich | Holati |
|---|---|---|
| 1 | Loyiha skeleti va sozlamalar | Tayyor |
| 2 | Modellar (jadvallar) | Tayyor |
| 3 | Serializer'lar (ma'lumotni tekshirish va API formatiga o'tkazish) | Tayyor |
| 4 | View'lar (API amallari va hisobotlar) | Kutilmoqda |
| 5 | Admin panel va URL manzillar | Kutilmoqda |
| 6 | 3 tilga tarjima | Kutilmoqda |
| 7 | Tekshirish va sinov | Kutilmoqda |
| 8 | Himoyaga tayyorgarlik | Kutilmoqda |

Frontend (ko'rinish qismi) hozircha qilinmaydi, oxirida qo'shiladi.

Har bosqich alohida tasdiqlanadi va tasdiqlangandan keyingina keyingisiga o'tiladi.

## Texnologiyalar

- Python 3.14
- Django 6.1 (asosiy freymvork)
- Django REST Framework (API uchun)
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

## Papkalar

- `config/` : loyihaning umumiy sozlamalari (`settings.py`, asosiy `urls.py`)
- `finance/` : asosiy ilova (modellar, serializer'lar, view'lar, admin)
- `locale/` : tarjima fayllari (uz, ru, en)
- `requirements.txt` : kerakli paketlar ro'yxati
