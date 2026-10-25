<h1 style="color: green">Kirim chiqim ilovasi</h1>

# Umumiy loyiha haqida
    - Loyiha 3 tilda (O'zbek, Ingliz va Rus)
    - Chiqimlar va kirimlarni hisoblab, qayd etib borish
    - Django RestFrameworkdan foydalangan holda quriladi
    - Docker orqali ishga tushirilishi kerak
    - Default SQLite bazasidan foydalanish kerak

# Hisoblar
    1. Naqd pul, karta (Default mavjud bo'lgan hisoblar)
    2. Foydalanuvchilar 5 tagacha hisob qo'shishlari mumkin (Masalan: visa, hamkor bank-Humo)
    3. Eslatmalar (Hisoblardagi mablag' belgilangan miqdordan kamayganida, foydalanuvchilarga bildirishnoma berish)

# Kirim turlari
    1. Oylik, avans, bonus
    2. Kirim turlari ham 5 tagacha foydalanuvchi tomonidan kiritib qo'yilishi mumkin

# Chiqim turlari
    1. Yo'l haqi, Tushlik, Salomatlik uchun
    2. Bu qism ham foydalanuvchi tomonidan qo'shilishi va o'chirilishi mumkin bo'ladi
    3. Ko'p ishlatiladigan chiqim turlari, foydalanuvchi yaratilganda uning chiqim turlari jadvaliga avtomatik yozib qo'yiladi

# Kirim va Chiqim transaksiyalari
    1. Chiqimlar va kirimlar ma'lumotlar bazasiga jadval ko'rinishida yozib boriladi
    2. Chiqimlar:
        - summa
        - sana
        - hisob
        - chiqim turi
       
       Kirimlar:
        - summa
        - sana
        - hisob
        - kirim turi
    3. Kirim va chiqimlar bitta modelda yaratiladi

# Hisobotlar
    - Kirim va chiqim ma'lumotlaridan foydalangan xolda oylik haftalik va kunlik hisobotlar statistika ko'rinishida qaytariladi
    