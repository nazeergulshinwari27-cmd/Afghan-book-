# د افغان ډیجیټل کتابتون — FastAPI Backend

دا یوازې Backend/API پروژه ده؛ `index.html` او Frontend پکې نشته.

## د فایلونو جوړښت

```text
Afghan_Library_FastAPI_Backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── books.py
│       └── admin.py
├── requirements.txt
└── render.yaml
```

## API برخې

- `POST /api/auth/register` — حساب جوړول
- `POST /api/auth/login` — ننوتل او Token ترلاسه کول
- `GET /api/auth/me` — د اوسني کارن معلومات
- `GET /api/books/` — د تایید شویو کتابونو لست او لټون
- `POST /api/books/` — PDF کتاب پورته کول (د ننوتلي کارن لپاره)
- `GET /api/books/mine` — د خپل کتابونو لست
- `GET /api/books/{id}/pdf` — د تایید شوي PDF لوستل
- `GET /api/admin/books` — د ټولو کتابونو لست (یوازې اډمین)
- `POST /api/admin/books/{id}/approve` — کتاب تاییدول
- `DELETE /api/admin/books/{id}` — کتاب حذفول
- `GET /api/admin/users` — د کاروونکو لست

## د GitHub/Render له لارې نشر

1. په GitHub کې نوی Repository جوړ کړئ او د دې فولډر دننه فایلونه پورته کړئ؛ ZIP فایل پخپله مه پورته کوئ.
2. په Render کې د PostgreSQL ډیټابېس جوړ کړئ.
3. د Render Web Service د جوړولو پر مهال خپل GitHub Repository ونښلوئ. د Blueprint کارولای شئ، ځکه `render.yaml` چمتو دی.
4. په Web Service کې Environment Variables جوړ کړئ:
   - `DATABASE_URL` = د PostgreSQL Internal Database URL
   - `ADMIN_EMAIL` = ستا د اډمین ایمیل
   - `ADMIN_PASSWORD` = قوي، ځانګړی پټ نوم (لږ تر لږه ۱۲ توري)
   - `SECRET_KEY` = Render یې د `render.yaml` له لارې جوړوي.
5. Deploy بشپړ شي؛ د API اسناد په `https://ستاسو-سایټ.onrender.com/docs` کې ښکاري.

## مهمې تخنیکي یادونې

- د PostgreSQL اتصال لپاره `DATABASE_URL` باید د Render د PostgreSQL داخلي URL وي.
- PDF فایلونه په PostgreSQL کې د `BYTEA` په بڼه ساتل کېږي؛ دا د لومړنۍ کوچنۍ نسخې لپاره دی. د لوی کتابتون لپاره Object Storage غوره دی.
- د PDF فایل حد ۲۰ MB دی.
- د کاروونکو کتابونه په لومړي سر کې `pending` وي؛ اډمین یې تاییدوي.
- یوازې د شریکولو د اجازې لرونکي کتابونه پورته کړئ.
- د دې MVP له پراخې عامه کارونې مخکې د بیک‌اپ، د فایلونو د ویروس سکین، د API rate limiting، او د لا پیاوړي فایل‌ذخیرې سیستم زیاتول مهم دي.
- د `SECRET_KEY`، `ADMIN_PASSWORD` او `DATABASE_URL` ارزښتونه په GitHub کې مه لیکئ.
