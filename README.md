# Kirim-Chiqim Ilovasi (Income-Expense Tracker)

Django REST Framework asosida qurilgan kirim va chiqimlarni hisobga olish tizimi. Loyiha JWT autentifikatsiya, email orqali tasdiqlash, ko'p valyutali hisoblar, CBU valyuta kurslari va operatsiyalar tarixini taqdim etadi.

## Mundarija

1. [Imkoniyatlar](#imkoniyatlar)
2. [Texnologiyalar](#texnologiyalar)
3. [Loyiha tuzilishi](#loyiha-tuzilishi)
4. [Muhit o'zgaruvchilari (.env)](#muhit-ozgaruvchilari-env)
5. [Ishga tushirish](#ishga-tushirish)
6. [API umumiy qoidalari](#api-umumiy-qoidalari)
7. [API endpointlari](#api-endpointlari)
8. [To'liq ishlash oqimi (misol)](#toliq-ishlash-oqimi-misol)
9. [Valyuta konvertatsiyasi va cache](#valyuta-konvertatsiyasi-va-cache)
10. [Ma'lumotlar modeli](#malumotlar-modeli)
11. [Testlar](#testlar)
12. [Ma'lum cheklovlar](#malum-cheklovlar)
13. [Muallif](#muallif)

## Imkoniyatlar

### Autentifikatsiya va profil
- Email orqali ro'yxatdan o'tish: 6 xonali tasdiqlash kodi emailga yuboriladi.
- Kodni tasdiqlash va bir martalik ro'yxatdan o'tish tokenini olish.
- Hisob yaratishda username, ism, familiya, til va parolni tekshirish.
- Ro'yxatdan muvaffaqiyatli o'tgach tabrik xati yuboriladi.
- JWT login, logout (refresh token blacklist), token yangilash.
- Profilni ko'rish va tahrirlash (ism, familiya, username, til).
- Parolni almashtirish (joriy parolni tekshirish bilan).
- Parol talablari: kamida 1 katta harf, 1 kichik harf, 1 raqam, 1 maxsus belgi.

### Hisoblar (Accounts)
- Foydalanuvchi o'z hisoblarini yaratadi va ro'yxatini ko'radi.
- Hisob turi (masalan, Naqd, Karta) nomi bo'yicha aniqlanadi; mavjud bo'lmasa global `AccountBase` yaratiladi.
- Bir foydalanuvchida bir xil turdagi hisob ikki marta bo'lmaydi.
- Valyutalar: `USD`, `UZS`, `RUB`, `EUR`.
- Hisobni tahrirlash (PATCH) va o'chirish (DELETE).
- Balans `Transaction` lar asosida yangilanadi.

### Kirim/chiqim turlari
- Foydalanuvchi shaxsiy operatsiya turlarini yaratadi va ro'yxatini ko'radi.
- Tur nomi + yo'nalishi (`INCOME` / `EXPENCE`) bo'yicha `TransactionTypeBase` qayta ishlatiladi.
- Bir xil tur foydalanuvchida takrorlanmaydi.
- Turini o'chirish (DELETE).

### Transaksiyalar
- Kirim va chiqimlar uchun yagona `Transaction` modeli.
- Tranzaksiya yaratilganda hisob balansi atomar (`transaction.atomic`) yangilanadi.
- Chiqimda balans yetarliligi tekshiriladi.
- Tranzaksiya yaratilgandan keyingi balans (`changed_balance`) saqlanadi.
- Foydalanuvchining barcha tranzaksiyalari ro'yxati.
- Hisoblar o'rtasida ichki o'tkazma (`transaction/tome`) — bitta foydalanuvchining ikki hisobi o'rtasida.
- Tarixni filtrlash: davr, summa oralig'i, tur, kirim/chiqim, hisob.
- Tarix uchun pagination (`page`, `page_size`).

### Valyuta kurslari
- CBU (cbu.uz) API'sidan kurslar olinadi.
- Kurslar Redis cache'da 1 soat saqlanadi.
- Hisob balansi va tranzaksiya balansi javoblarda hisob valyutasiga o'girilgan holda qaytariladi.

### Qo'shimcha
- Django admin paneli.
- Swagger (drf-spectacular) va ReDoc orqali API hujjatlari.
- Docker / Docker Compose orqali ishga tushirish (web + Redis).

## Texnologiyalar

- Python 3.13+
- Django 6.1
- Django REST Framework
- djangorestframework-simplejwt (JWT + token blacklist)
- drf-spectacular (OpenAPI / Swagger / ReDoc)
- Redis (cache)
- requests (CBU API)
- python-dotenv (.env)
- SQLite (standart ma'lumotlar bazasi)
- uv (paket va virtual muhit menejeri)
- Docker / Docker Compose

## Loyiha tuzilishi

```
Final-Exam/
├── accounting/          # Hisoblar, hisob turlari, kirim/chiqim turlari
├── authentication/      # CustomUser, OTP, JWT, profil, email yuborish
│   └── email.py         # Tasdiqlash kodi va tabrik xatlari
├── transactions/        # Tranzaksiyalar, o'tkazma, tarix, pagination
├── config/              # settings, urls, wsgi/asgi
├── templates/           # code.html, greeting.html (email shablonlari)
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

## Muhit o'zgaruvchilari (.env)

`.env` fayli repoga qo'shilmaydi (`.gitignore` da). Uni loyiha ildizida o'zingiz yaratishingiz shart, aks holda dastur ishga tushmaydi.

| O'zgaruvchi | Majburiy | Tavsif |
|---|---|---|
| `DJANGO_SECRET_KEY` | Ha | Django `SECRET_KEY` qiymati |
| `EMAIL_HOST_USER` | Ha | SMTP (Gmail) foydalanuvchisi |
| `EMAIL_HOST_PASSWORD` | Ha | SMTP (Gmail) app-parol |
| `DEBUG` | Yo'q | Hozircha `.env` dan o'qilmaydi (settingsda `True`) |

`.env` namunasi:

```env
DJANGO_SECRET_KEY=change-me-to-a-long-random-string
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_google_app_password
DEBUG=True
```

> Gmail uchun oddiy parol emas, **App Password** ishlatiladi (Google Account → Security → 2-Step Verification → App passwords).

## Ishga tushirish

### Talablar

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (tavsiya etiladi)
- Docker + Docker Compose (Docker varianti uchun)
- Redis (lokal variantda valyuta konvertatsiyasi uchun)

### Variant A — Docker Compose (tavsiya etiladi)

Bu variantda web va Redis birga ko'tariladi, `redis://redis:6379/1` manzili to'g'ri ishlaydi.

1. **`.env` faylini yaratish** (yuqoridagi namunadan).
2. **Konteynerlarni ko'tarish:**

   ```bash
   docker compose up --build -d
   ```

3. **Migratsiyalarni qo'llash:**

   ```bash
   docker compose exec web python manage.py migrate
   ```

4. **Superuser yaratish (ixtiyoriy):**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

5. **Tekshirish:**

   - API: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`
   - Swagger: `http://127.0.0.1:8000/api/docs/`
   - ReDoc: `http://127.0.0.1:8000/api/redoc/`

6. **To'xtatish:**

   ```bash
   docker compose down
   ```

### Variant B — Lokal muhit (uv)

1. **Bog'liqliklarni o'rnatish:**

   ```bash
   uv sync
   ```

   `pip` bilan:

   ```bash
   pip install -e .
   ```

2. **`.env` faylini yaratish** (yuqoridagi namunadan).

3. **Redis'ni ishga tushirish.**

   > Muhim: `config/settings.py` dagi cache manzili Docker uchun
   > `redis://redis:6379/1`. Lokal `runserver` uchun Redis `redis`
   > hostida topilmaydi. Ikki yo'l bor:
   > - Docker Compose'dan foydalanish (Variant A), yoki
   > - lokal Redis ishga tushirib, `CACHES["default"]["LOCATION"]` ni
   >   `redis://127.0.0.1:6379/1` ga o'zgartirish.
   >
   > Redis mavjud bo'lmasa, valyuta konvertatsiyasi ishlatiladigan
   > endpointlar xato qaytaradi.

4. **Migratsiyalar:**

   ```bash
   python manage.py migrate
   ```

5. **Superuser (ixtiyoriy):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Serverni ishga tushirish:**

   ```bash
   python manage.py runserver
   ```

   Server: `http://127.0.0.1:8000/`

### Boshlang'ich ma'lumotlar

- Hisob turlari (`AccountBase`) va operatsiya turlari (`TransactionTypeBase`) foydalanuvchi tomonidan yaratiladi.
- Admin panelda `TransactionTypeBase` va `AccountBase` yozuvlarini qo'lda qo'shish mumkin.
- `transaction/tome` (ichki o'tkazma) endpointi `TransactionTypeBase` dagi **ID 5** va **ID 6** yozuvlariga tayanadi. Toza bazada bu IDlar bo'lmasa o'tkazma xato beradi — ularni oldindan yaratib qo'ying.

## API umumiy qoidalari

- Base URL: `http://127.0.0.1:8000`
- URL'lar oxirida slash **yo'q** (masalan `/api/auth/login`).
- Himoyalangan endpointlar uchun header:

  ```
  Authorization: Bearer <access_token>
  ```

- Muvaffaqiyatli javob formati:

  ```json
  {
    "success": true,
    "message": "Transaction created",
    "data": {}
  }
  ```

- Xatolik javobi (biznes xatolari):

  ```json
  {
    "success": false,
    "message": "Account not found",
    "data": null
  }
  ```

- Validatsiya xatolari DRF standart formatida qaytadi (HTTP 400):

  ```json
  {
    "email": ["A user with this email already exists"]
  }
  ```

- Sana/vaqt: `TIME_ZONE=Asia/Tashkent`, `USE_TZ=True`.
- Pul summalari `decimal` (string) sifatida yuboriladi.

## API endpointlari

### Autentifikatsiya — `/api/auth/`

| Metod | URL | Auth | Tavsif |
|---|---|---|---|
| POST | `/api/auth/signup` | Yo'q | Emailga tasdiqlash kodi yuborish |
| POST | `/api/auth/verify-code` | Yo'q | Kodni tasdiqlash, token olish |
| POST | `/api/auth/create-account` | Yo'q | Token bilan hisob yaratish |
| POST | `/api/auth/login` | Yo'q | JWT access/refresh olish |
| POST | `/api/auth/logout` | Ha | Refresh tokenni blacklist qilish |
| POST | `/api/auth/token/refresh` | Yo'q | Access tokenni yangilash |
| GET | `/api/auth/profile` | Ha | Profilni ko'rish |
| PATCH | `/api/auth/profile` | Ha | Profilni tahrirlash |
| POST | `/api/auth/password/change` | Ha | Parolni almashtirish |

#### Ro'yxatdan o'tish oqimi

1) **Kod so'rash**

```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com"
}
```

Javob (201): `data` ichida `id` va `email`. Kod emailga yuboriladi.

2) **Kodni tasdiqlash**

```http
POST /api/auth/verify-code
Content-Type: application/json

{
  "email": "user@example.com",
  "code": 123456
}
```

Javob (201): `data` ichida `id`, `email`, `code` va `token`. `token` keyingi qadam uchun kerak.

3) **Hisob yaratish**

```http
POST /api/auth/create-account
Content-Type: application/json

{
  "token": "<verify-code dan olingan token>",
  "username": "maqsudbek",
  "first_name": "Maqsudbek",
  "last_name": "Dehqonov",
  "language": "UZ",
  "password": "Strong1!",
  "conf_password": "Strong1!"
}
```

Javob (201): foydalanuvchi ma'lumotlari (parol va token qaytarilmaydi). Tabrik xati yuboriladi.

#### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "maqsudbek",
  "password": "Strong1!"
}
```

Javob (200):

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "1",
      "username": "maqsudbek",
      "email": "user@example.com",
      "first_name": "Maqsudbek",
      "last_name": "Dehqonov"
    },
    "tokens": {
      "access": "<access_token>",
      "refresh": "<refresh_token>"
    }
  }
}
```

#### Logout

```http
POST /api/auth/logout
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

#### Token yangilash

```http
POST /api/auth/token/refresh
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

Javob SimpleJWT formatida: `access` (va rotation yoqilgani uchun yangi `refresh`).

#### Profil

```http
GET /api/auth/profile
Authorization: Bearer <access_token>
```

```http
PATCH /api/auth/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Maqsud",
  "last_name": "Dehqonov",
  "language": "EN"
}
```

`language` qiymatlari: `UZ`, `EN`, `RU`.

#### Parolni almashtirish

```http
POST /api/auth/password/change
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "Strong1!",
  "new_password": "NewStrong2@",
  "conf_password": "NewStrong2@"
}
```

### Hisoblar — `/api/accounting/`

| Metod | URL | Auth | Tavsif |
|---|---|---|---|
| GET | `/api/accounting/account` | Ha | Foydalanuvchi hisoblari ro'yxati |
| POST | `/api/accounting/account` | Ha | Yangi hisob yaratish |
| PATCH | `/api/accounting/account/<id>` | Ha | Hisobni tahrirlash |
| DELETE | `/api/accounting/account/<id>` | Ha | Hisobni o'chirish |

#### Hisob yaratish

```http
POST /api/accounting/account
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "account_name": "Naqd",
  "currency": "UZS"
}
```

Javob (200):

```json
{
  "success": true,
  "message": "Account created",
  "data": {
    "id": 1,
    "name": "Naqd",
    "currency": "UZS",
    "balance": "0.00"
  }
}
```

`currency` qiymatlari: `USD`, `UZS`, `RUB`, `EUR`. `balance` faqat o'qish uchun.

#### Hisobni tahrirlash / o'chirish

```http
PATCH /api/accounting/account/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "currency": "USD"
}
```

```http
DELETE /api/accounting/account/1
Authorization: Bearer <access_token>
```

### Kirim/chiqim turlari — `/api/accounting/`

| Metod | URL | Auth | Tavsif |
|---|---|---|---|
| GET | `/api/accounting/transaction-type` | Ha | Foydalanuvchi turlari ro'yxati |
| POST | `/api/accounting/transaction-type` | Ha | Yangi tur yaratish |
| DELETE | `/api/accounting/transaction-type/<id>` | Ha | Turini o'chirish |

#### Tur yaratish

```http
POST /api/accounting/transaction-type
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "transaction_name": "Oylik",
  "transaction_type": "INCOME"
}
```

`transaction_type`: `INCOME` yoki `EXPENCE` (kodda shu imlo ishlatiladi).

Javob:

```json
{
  "success": true,
  "message": "New transaction type created",
  "data": {
    "id": 3,
    "transaction_name": "Oylik",
    "transaction_type": "INCOME"
  }
}
```

> Eslatma: bu ro'yxatdagi `id` — shaxsiy tur (`TransactionTypePrivate`) IDsi. Tranzaksiya yaratishda esa `TransactionTypeBase` IDsi kutiladi (quyida).

### Transaksiyalar — `/api/transactions/`

| Metod | URL | Auth | Tavsif |
|---|---|---|---|
| GET | `/api/transactions/transaction` | Ha | Barcha tranzaksiyalar |
| POST | `/api/transactions/transaction` | Ha | Yangi tranzaksiya |
| POST | `/api/transactions/transaction/tome` | Ha | Ichki o'tkazma |
| GET | `/api/transactions/transaction/history` | Ha | Filtrlangan tarix + pagination |

#### Tranzaksiya yaratish

```http
POST /api/transactions/transaction
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "amount": "150000.00",
  "transaction_type": 2,
  "account": 1
}
```

- `transaction_type` — `TransactionTypeBase` jadvalidagi ID.
- `account` — foydalanuvchiga tegishli hisob IDsi.
- Chiqim (`EXPENCE`) uchun balans yetarli bo'lishi shart.

Javob (200): tranzaksiya + `transaction_type` obyekti va `account` ichida yangilangan balans.

#### Ichki o'tkazma

```http
POST /api/transactions/transaction/tome
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "amount": "50000.00",
  "account": 1,
  "recipient": 2
}
```

- `account` — jo'natuvchi hisob, `recipient` — qabul qiluvchi hisob.
- Ikkala hisob ham shu foydalanuvchiga tegishli bo'lishi kerak.
- Hisoblar har xil bo'lishi va jo'natuvchida mablag' yetarli bo'lishi kerak.

#### Tarix va filtrlash

```http
GET /api/transactions/transaction/history?interval=monthly&inout=EXPENCE&account=1&page=1&page_size=20
Authorization: Bearer <access_token>
```

| Parametr | Qiymatlar | Tavsif |
|---|---|---|
| `interval` | `daily`, `weekly`, `monthly` | Vaqt oralig'i |
| `min_amount` | decimal | Minimal summa |
| `max_amount` | decimal | Maksimal summa |
| `transaction_type` | ID | `TransactionTypeBase` IDsi |
| `inout` | `INCOME`, `EXPENCE` | Kirim yoki chiqim |
| `account` | ID | Hisob bo'yicha |
| `page` | raqam | Sahifa raqami |
| `page_size` | 1–100 | Sahifa hajmi (default 50) |

Javob:

```json
{
  "success": true,
  "message": "Transaction history",
  "data": {
    "count": 42,
    "applied_filters": {
      "interval": "monthly",
      "inout": "EXPENCE"
    },
    "transactions": []
  }
}
```

### Hujjatlar

| URL | Tavsif |
|---|---|
| `/api/schema/` | OpenAPI sxema (YAML) |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |
| `/admin/` | Django admin |

## To'liq ishlash oqimi (misol)

```bash
BASE=http://127.0.0.1:8000

# 1. Kod so'rash
curl -X POST $BASE/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'

# 2. Emaildan kodni olib tasdiqlash
curl -X POST $BASE/api/auth/verify-code \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","code":123456}'

# 3. Token bilan hisob yaratish
curl -X POST $BASE/api/auth/create-account \
  -H "Content-Type: application/json" \
  -d '{"token":"<TOKEN>","username":"maqsudbek","first_name":"Maqsudbek","last_name":"Dehqonov","language":"UZ","password":"Strong1!","conf_password":"Strong1!"}'

# 4. Login
curl -X POST $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"maqsudbek","password":"Strong1!"}'

# 5. Hisob yaratish
curl -X POST $BASE/api/accounting/account \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"account_name":"Naqd","currency":"UZS"}'

# 6. Operatsiya turi yaratish
curl -X POST $BASE/api/accounting/transaction-type \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"transaction_name":"Oylik","transaction_type":"INCOME"}'

# 7. Tranzaksiya yaratish
curl -X POST $BASE/api/transactions/transaction \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"amount":"150000.00","transaction_type":1,"account":1}'

# 8. Tarix
curl "$BASE/api/transactions/transaction/history?interval=monthly&page=1&page_size=20" \
  -H "Authorization: Bearer $ACCESS"
```

## Valyuta konvertatsiyasi va cache

- Kurslar `https://cbu.uz/en/arkhiv-kursov-valyut/json/` dan olinadi.
- Faqat loyihada ishlatiladigan valyutalar (`USD`, `UZS`, `RUB`, `EUR`) ajratib olinadi.
- Natija `cbu_rates` kaliti bilan Redis'da **1 soat** keshlanadi.
- Javoblarda hisob balansi hisob valyutasiga o'giriladi (UZS uchun o'zgarishsiz).
- Redis yoki CBU API ishlamasa, konvertatsiya talab qiladigan endpointlar xato qaytaradi.

## Ma'lumotlar modeli

| Model | Tavsif |
|---|---|
| `CustomUser` | `AbstractUser` + `language` (`UZ`/`EN`/`RU`) |
| `TempUser` | Ro'yxatdan o'tishgacha vaqtinchalik email + tasdiqlash kodi + muddat |
| `MyToken` | Kod tasdiqlangandan keyingi bir martalik token |
| `AccountBase` | Global hisob turlari (Naqd, Karta, ...) |
| `Account` | Foydalanuvchi hisobi: tur, balans, valyuta |
| `TransactionTypeBase` | Global kirim/chiqim turlari (`INCOME`/`EXPENCE`) |
| `TransactionTypePrivate` | Foydalanuvchiga bog'langan tur |
| `Transaction` | Kirim/chiqim yozuvi: summa, tur, hisob, yaratilgan vaqt, keyingi balans |

## Testlar

Hozircha avtomatlashtirilgan testlar yozilmagan (`tests.py` fayllari bo'sh). Django testlarini ishga tushirish buyrug'i:

```bash
python manage.py test
```

## Ma'lum cheklovlar

- `DEBUG` va `ALLOWED_HOSTS` hozircha development uchun sozlangan (`DEBUG=True`, bo'sh ro'yxat).
- `DEBUG` `.env` da mavjud bo'lsa ham, settingsda hali o'qilmaydi.
- Cache manzili Docker uchun qat'iy yozilgan (`redis://redis:6379/1`); lokal ishga tushirishda yuqoridagi ko'rsatmaga qarang.
- `transaction/tome` `TransactionTypeBase` ID 5 va 6 ga tayanadi; toza bazada ularni yaratish kerak.
- Valyutalari har xil hisoblar o'rtasidagi o'tkazmada konvertatsiya qilinmaydi.
- `GET /api/transactions/transaction` hali pagination qo'llamaydi (tarix endpointi qo'llaydi).
- Rate limiting (throttling) va ko'p tilli javoblar (gettext/locale) hali joriy qilinmagan.
- Email yuborish sinxron bajariladi; SMTP sekin yoki ishlamasa so'rov kechikishi/xatosi mumkin.
- `DEFAULT_FROM_EMAIL` sozlanmagan; Gmail SMTP ba'zi holatlarda jo'natuvchi manzilini rad etishi mumkin — uni `.env`/settings orqali qo'shish tavsiya etiladi.

## Muallif

**Maqsudbek** — dehkanaliev@gmail.com
