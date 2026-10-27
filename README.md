# Kirim-Chiqim Ilovasi (Income-Expense Tracker)

Django REST Framework asosida qurilgan kirim va chiqimlarni hisobga olish va kuzatib borish tizimi.

## Loyiha haqida

- **Ko'p tillilik**: O'zbek, Ingliz va Rus tillarini qo'llab-quvvatlaydi
- **Kirim va chiqimlarni hisobga olish**: Barcha kirim va chiqim operatsiyalarini saqlash va kuzatish
- **Django REST Framework**: RESTful API orqali ishlaydi
- **JWT autentifikatsiya**: `djangorestframework-simplejwt` yordamida xavfsiz autentifikatsiya
- **SQLite**: Standart ma'lumotlar bazasi sifatida ishlatiladi
- **Docker**: Konteyner orqali ishga tushirish imkoniyati

## Texnologiyalar

- Python 3.13+
- Django
- Django REST Framework
- djangorestframework-simplejwt
- matplotlib (hisobotlar va grafiklar uchun)

## Asosiy funksiyalar

### 1. Hisoblar (Accounts)
- **Asosiy hisob turlari**: Naqd pul, karta va boshqa standart hisob turlari
- **Shaxsiy hisoblar**: Har bir foydalanuvchi o'z hisoblarini yaratishi mumkin (maksimal 5 ta)
- **Valyuta qo'llab-quvvatlash**: USD, SUM, RUBL, EURO kabi valyutalar
- **Balans hisoblash**: Har bir hisob bo'yicha joriy balansni kuzatish

### 2. Kirim va Chiqim turlari
- **Umumiy turlari**: Ma'mur tomonidan belgilangan kirim/chiqim turlari
- **Shaxsiy turlari**: Foydalanuvchilar o'zlariga kerakli kirim va chiqim turlarini qo'shishlari mumkin (maksimal 5 tagacha)
- **Avtomatik yaratish**: Yangi foydalanuvchi ro'yxatdan o'tganda, ko'p ishlatiladigan chiqim turlari avtomatik ravishda shaxsiy turlar ro'yxatiga qo'shiladi
- **Turlar tahlili**: Har bir operatsiya turi `INCOME` yoki `OUTCOME` sifatida tasniflanadi

### 3. Transaksiyalar
- **Birlashtirilgan model**: Kirim va chiqim operatsiyalari bitta `Transaction` modeli orqali saqlanadi
- **To'liq ma'lumot**: Har bir transaksiyada summa, sana, hisob va operatsiya turi saqlanadi
- **O'tkazmalar**: Kartadan naqdga yoki naqd puldan kartaga o'tkazmalar ham kirim/chiqim sifatida hisobga olinadi
- **Tarixiy kuzatuv**: Barcha operatsiyalar vaqt bo'yicha saqlanib boriladi

### 4. Eslatmalar (Notifications)
- Hisobdagi mablag' belgilangan minimal miqdordan pastga tushganda foydalanuvchiga eslatma beriladi

### 5. Valyuta kurslari
- Foydalanuvchilar har bir hisob uchun o'zlariga qulay valyutani tanlashlari mumkin
- Valyuta kurslarini aniqlash uchun Jahon bankining API'sidan foydalaniladi
- Turli valyutalarda ko'rsatish imkoniyati mavjud

### 6. Hisobotlar
- Kunlik, haftalik va oylik hisobotlar
- Statistik ma'lumotlar ko'rinishida taqdim etiladi
- Grafiklar va vizualizatsiya (`matplotlib` yordamida)

## Loyiha tuzilishi

```
Final-Exam/
├── accounting/      # Hisoblar, operatsiya turlari va asosiy biznes mantiqi
├── authentication/  # Autentifikatsiya va JWT tokenlar
├── transactions/    # Transaksiyalar moduli
├── config/          # Loyiha sozlamalari (settings, urls, wsgi/asgi)
└── manage.py        # Django boshqaruv skripti
```

## O'rnatish va ishga tushirish

### Talablar
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (tavsiya etiladi) yoki pip

### Lokal muhitda ishga tushirish

1. **Loyihani klonlash**
```bash
git clone <repository-url>
cd Final-Exam
```

2. **Virtual muhit yaratish va bog'liqliklarni o'rnatish**
```bash
# uv orqali
uv sync

# yoki pip orqali
pip install -e .
```

3. **Ma'lumotlar bazasini migratsiya qilish**
```bash
python manage.py migrate
```

4. **Superuser yaratish (ixtiyoriy)**
```bash
python manage.py createsuperuser
```

5. **Serverni ishga tushirish**
```bash
python manage.py runserver
```

Server `http://127.0.0.1:8000/` manzilida ishga tushadi.

### Docker orqali ishga tushirish

```bash
docker build -t kirim-chiqim .
docker run -p 8000:8000 kirim-chiqim
```

## API Endpoints

Asosiy URL manzillari:

- `/admin/` - Django admin paneli
- `/api/auth/` - Autentifikatsiya endpointlari
- `/api/accounting/` - Hisoblar va operatsiya turlari
- `/api/transactions/` - Transaksiyalar

Batafsil API dokumentatsiyasi uchun admin panel yoki kodni ko'rib chiqishingiz mumkin.

## Ma'lumotlar modeli

### Asosiy modellar

| Model | Tavsif |
|---|---|
| `AccountBase` | Umumiy hisob turlari (Naqd, Karta va boshqalar) |
| `Account` | Foydalanuvchining shaxsiy hisoblari (balans, valyuta bilan) |
| `TransactionTypeBase` | Umumiy kirim/chiqim turlari |
| `TransactionTypePrivate` | Foydalanuvchiga tegishli shaxsiy operatsiya turlari |
| `Transaction` | Barcha kirim va chiqim operatsiyalari |

## Muallif

**Maqsudbek** - dehkanaliev@gmail.com
