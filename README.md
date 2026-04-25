.

```markdown
# 🤖 Robota – کتابخانه  روبیکا

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-online-brightgreen)](https://amiralicoldark.github.io/Robota)
[![GitHub Stars](https://img.shields.io/github/stars/amiralicoldark/Robota)](https://github.com/amiralicoldark/Robota)

**Robota** یک کتابخانه قدرتمند، کامل و آسان برای تعامل با **API بات روبیکا** است. با این کتابخانه میتوانید تمام قابلیتهای رسمی روبیکا را در ربات خود پیاده کنید: ارسال پیامهای متنی، دکمههای شیشهای و کیپد، نظرسنجی، موقعیت مکانی، مخاطب، فایل (عکس، ویدئو، صدا، سند)، مدیریت گروه و کانال (بن، آنبن، حذف پیام، ویرایش)، و دریافت رویدادها با لانگ پولینگ یا وب‌هوک.

✨ **ویژگیها**:
- پشتیبانی از **همه متدهای رسمی** روبیکا (بیش از ۲۰ متد)
- **۱۸ نوع دکمه تعاملی** (ساده، لینک، انتخاب عدد، تقویم، دوربین، گالری، درخواست شماره و موقعیت، بارکد و...)
- صفحهکلید شیشهای (`InlineKeypad`) و صفحهکلید پایین چت (`ChatKeypad`)
- متادیتا برای **فرمت‌بندی متن** (پررنگ، کج، لینک، منشن، نقلقول، کد و...)
- آپلود و ارسال فایل در **یک خط کد**
- **Long Polling خودکار** با مدیریت `offset`
- پشتیبانی از **Webhook** (با متد `parse_update`)
- **تایپ‌هینتینگ کامل** و خطاگیری حرفهای
- **بدون وابستگی اضافی** (فقط `requests`)

---

## 📦 نصب

### نصب از GitHub (نسخه پایدار و بهروز)

```bash
pip install git+https://github.com/amiralicoldark/Robota.git
```

### نصب از PyPI (به‌زودی)

```bash
pip install robota
```

### نصب دستی

```bash
pip install git+https://github.com/amiralicoldark/Robota.git
```

---

## 🚀 قدم اول: ساخت بات و گرفتن توکن

1. در روبیکا، ربات **BotFather** را پیدا کنید (`@BotFather`).
2. به آن پیام `/newbot` بدهید.
3. یک نام و سپس یک **یوزرنیم** برای بات انتخاب کنید (باید به `bot` ختم شود).
4. پس از اتمام، یک **توکن** دریافت میکنید (رشته‌ای مثل `a1b2c3d4...`).
5. توکن را ذخیره کنید. **هیچکس جز شما نباید به آن دسترسی داشته باشد**.

> [!نکته]
> برای پیدا کردن `chat_id` خود، میتوانید به بات `@UserInfoRobot` در روبیکا پیام دهید یا از متد `get_updates` کتابخانه استفاده کنید.

---

## 🧪 اولین ربات: سلام دنیا

```python
from robota import RubikaBot

# توکن واقعی خود را جایگزین کنید
TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "c123456789"   # شناسه چت خودتان

bot = RubikaBot(TOKEN)

# ارسال پیام ساده
result = bot.send_message(CHAT_ID, "سلام! من ربات Robota هستم 🤖")
print(f"پیام ارسال شد. message_id: {result.get('message_id')}")

# دریافت اطلاعات بات
me = bot.get_me()
print(f"نام بات: {me.bot_title}")
print(f"یوزرنیم: @{me.username}")
```

---

## 📚 مستندات کامل متدها

| متد | توضیح | مثال کوتاه |
|------|--------|-------------|
| `get_me()` | دریافت اطلاعات بات (نام، یوزرنیم، آواتار و ...) | `bot.get_me()` |
| `send_message(chat_id, text, ...)` | ارسال پیام متنی + کیپد/اینلاین/متادیتا | `bot.send_message(chat_id, "متن")` |
| `send_poll(chat_id, question, options)` | ارسال نظرسنجی | `bot.send_poll(chat_id, "سوال؟", ["گزینه1","گزینه2"])` |
| `send_location(chat_id, lat, lon)` | ارسال موقعیت مکانی | `bot.send_location(chat_id, 35.6997, 51.3381)` |
| `send_contact(chat_id, first, last, phone)` | ارسال مخاطب | `bot.send_contact(chat_id, "علی", "رضایی", "09123456789")` |
| `get_chat(chat_id)` | دریافت اطلاعات چت (نوع، عنوان، اعضا و...) | `chat = bot.get_chat(chat_id)` |
| `get_updates(limit, auto_offset)` | دریافت آپدیت‌ها (لانگ پولینگ) | `updates, next_id = bot.get_updates(10)` |
| `forward_message(from_chat, msg_id, to_chat)` | فوروارد پیام | `bot.forward_message(chat_id, msg_id, chat_id)` |
| `edit_message_text(chat_id, msg_id, new_text)` | ویرایش متن پیام | `bot.edit_message_text(chat_id, msg_id, "متن جدید")` |
| `edit_message_keypad(chat_id, msg_id, new_keypad)` | ویرایش کیپد شیشه‌ای | `bot.edit_message_keypad(chat_id, msg_id, keypad)` |
| `delete_message(chat_id, msg_id)` | حذف پیام | `bot.delete_message(chat_id, msg_id)` |
| `set_commands(list_of_dicts)` | تنظیم دستورات بات (منوی /start و ...) | `bot.set_commands([{"command":"start","description":"شروع"}])` |
| `update_bot_endpoints(url, type_)` | تنظیم وب‌هوک | `bot.update_bot_endpoints("https://...", "ReceiveUpdate")` |
| `edit_chat_keypad(chat_id, keypad, type_)` | اضافه/حذف صفحهکلید پایین | `bot.edit_chat_keypad(chat_id, chat_keypad=keypad, chat_keypad_type="New")` |
| `get_file(file_id)` | دریافت آدرس دانلود فایل | `url = bot.get_file(file_id)` |
| `send_file(chat_id, file_id, caption, ...)` | ارسال فایل با file_id | `bot.send_file(chat_id, file_id, text="توضیح")` |
| `request_send_file(file_type)` | درخواست آدرس آپلود | `upload_url = bot.request_send_file("Image")` |
| `upload_file_to_url(upload_url, file_path)` | آپلود فایل به آدرس | `file_id = bot.upload_file_to_url(upload_url, "photo.jpg")` |
| `upload_and_send_file(chat_id, file_path, file_type, caption)` | آپلود و ارسال یکمرحله‌ای | `bot.upload_and_send_file(chat_id, "photo.jpg", "Image", "عکس")` |
| `ban_chat_member(chat_id, user_id)` | مسدود کردن کاربر در گروه/کانال | `bot.ban_chat_member(group_id, user_id)` |
| `unban_chat_member(chat_id, user_id)` | رفع مسدودیت | `bot.unban_chat_member(group_id, user_id)` |

---

## 🧩 ساخت دکمه‌ها و صفحهکلید (RubikaHelpers)

کلاس `RubikaHelpers` تمام نوع دکمه‌های مجاز در روبیکا را می‌سازد.

### دکمه‌های پایه

```python
from robota import RubikaHelpers

# دکمه ساده
btn1 = RubikaHelpers.simple_button("id1", "دکمه ساده")

# دکمه لینک
btn2 = RubikaHelpers.link_button("id2", "وب‌سایت", "https://rubika.ir")

# دکمه انتخاب عدد
btn3 = RubikaHelpers.number_picker_button("id3", "انتخاب سن", 1, 100, default=25, title="سن خود را وارد کنید")

# دکمه ورودی متن
btn4 = RubikaHelpers.textbox_button("id4", "نظر خود را بنویسید", type_line="MultiLine", placeholder="...")

# دکمه دوربین عکس
btn5 = RubikaHelpers.camera_image_button("id5", "📸 گرفتن عکس")

# دکمه گالری ویدئو
btn6 = RubikaHelpers.gallery_video_button("id6", "🎥 انتخاب ویدئو")

# دکمه درخواست شماره تلفن
btn7 = RubikaHelpers.ask_phone_button("id7", "ارسال شماره من")

# دکمه درخواست موقعیت
btn8 = RubikaHelpers.ask_location_button("id8", "ارسال موقعیت من")

# دکمه بارکدخوان
btn9 = RubikaHelpers.barcode_button("id9", "📱 اسکن بارکد")

# دکمه تقویم
btn10 = RubikaHelpers.calendar_button("id10", "انتخاب تاریخ", calendar_type="DatePersian", min_year="1400", max_year="1450")

# دکمه انتخاب از لیست رشته‌ها
btn11 = RubikaHelpers.string_picker_button("id11", "انتخاب شهر", ["تهران", "اصفهان", "شیراز"], title="شهر خود را انتخاب کنید")
```

### ساخت ردیف و صفحهکلید

```python
# یک ردیف شامل سه دکمه (حداکثر ۳ دکمه در هر ردیف)
row1 = RubikaHelpers.row(btn1, btn2, btn3)
row2 = RubikaHelpers.row(btn4, btn5)

# ساخت کیپد (برای inline_keypad یا chat_keypad)
my_keypad = RubikaHelpers.keypad(
    rows=[row1, row2],
    resize_keyboard=True,      # اندازه دکمه‌ها متناسب با محتوا
    one_time_keyboard=False    # کیپد بعد از کلیک بسته نشود
)

# ارسال با inline_keypad
bot.send_message(chat_id, "لطفاً انتخاب کنید:", inline_keypad=my_keypad)
```

---

## 🎨 متادیتا: فرمت‌بندی متن پیام

با `metadata` میتوانید بخش‌هایی از متن را پررنگ، کج، لینک، منشن، نقلقول و ... کنید.

```python
from robota import RubikaHelpers, MetadataTypeEnum

text = "سلام علی جان! لطفاً به سایت ما مراجعه کن. کد: print('hello')"

# ساخت قطعات متادیتا
parts = [
    # پررنگ کردن کلمه "سلام" (از اندیس 0 تا 4)
    RubikaHelpers.metadata_part(MetadataTypeEnum.BOLD, 0, 4),
    # لینک کردن "سایت ما" (از اندیس 15 تا 23) به آدرس https://example.com
    RubikaHelpers.metadata_part(MetadataTypeEnum.LINK, 15, 8, link_url="https://example.com"),
    # منشن کردن کاربر با user_id (فقط در گروه)
    RubikaHelpers.metadata_part(MetadataTypeEnum.MENTION_TEXT, 5, 9, mention_user_id="u0HspK0e53c9c5bc874ec6c4673bf868"),
    # کد بلاک (مونواسپیس) برای عبارت print('hello')
    RubikaHelpers.metadata_part(MetadataTypeEnum.PRE, 35, 17)
]

metadata = RubikaHelpers.metadata(parts)

bot.send_message(chat_id, text, metadata=metadata)
```

انواع `MetadataTypeEnum`: `BOLD`, `ITALIC`, `UNDERLINE`, `STRIKE`, `SPOILER`, `LINK`, `MENTION_TEXT`, `PRE`, `QUOTE`, `MONO`

---

## 🔄 دریافت پیام‌ها و رویدادها

### روش ۱: Long Polling خودکار (ساده‌ترین)

```python
from robota import UpdateTypeEnum

def handle(update):
    if update.type == UpdateTypeEnum.NEW_MESSAGE:
        msg = update.new_message
        print(f"پیام جدید از {msg.sender_id}: {msg.text}")
        # پاسخ به کاربر
        bot.send_message(update.chat_id, f"پیام شما دریافت شد: {msg.text}")
    elif update.type == UpdateTypeEnum.EDITED_MESSAGE:
        print(f"پیام ویرایش شد: {update.updated_message.text}")

# شروع حلقه بی‌نهایت
bot.start_polling(handle, interval=1, limit=100)
```

### روش ۲: دریافت دستی آپدیت‌ها

```python
updates, next_offset = bot.get_updates(limit=5, auto_offset=False)
for update in updates:
    if update.type == UpdateTypeEnum.NEW_MESSAGE:
        print(update.new_message.text)

# اگر میخواهید offset خودکار باشد:
updates, _ = bot.get_updates(auto_offset=True)  # next_offset درون bot ذخیره میشود
```

---

## 🌐 تنظیم وب‌هوک (Webhook)

اگر سرور دارید (مثلاً با Flask)، میتوانید رویدادها را به سرور خود بفرستید.

### گام ۱: تنظیم آدرس endpoint در روبیکا

```python
bot.update_bot_endpoints("https://your-domain.com/webhook", "ReceiveUpdate")
```

### گام ۲: کد سرور (مثال با Flask)

```python
from flask import Flask, request
from robota import RubikaBot

app = Flask(__name__)
bot = RubikaBot("YOUR_TOKEN")  # فقط برای parse_update استفاده میشود

@app.route("/webhook", methods=["POST"])
def webhook():
    update = RubikaBot.parse_update(request.get_data())
    # پردازش update (مثل همان handle)
    if update.type == UpdateTypeEnum.NEW_MESSAGE:
        print(update.new_message.text)
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
```

> [!توجه]
> سرور شما باید **HTTPS** داشته باشد و آدرس آن **عمومی** باشد. برای تست لوکال از ngrok یا تونل‌های مشابه استفاده کنید.

---

## 📁 آپلود و ارسال فایل

### روش یک مرحله‌ای (پیشنهادی)

```python
# آپلود و ارسال عکس
bot.upload_and_send_file(chat_id, "my_photo.jpg", "Image", caption="عکس من")

# آپلود و ارسال ویدئو
bot.upload_and_send_file(chat_id, "video.mp4", "Video", caption="فیلم")

# آپلود و ارسال فایل صوتی
bot.upload_and_send_file(chat_id, "voice.mp3", "Voice")
```

انواع `file_type`: `"File"`, `"Image"`, `"Voice"`, `"Video"`, `"Music"`, `"Gif"`

### روش دو مرحله‌ای (دسترسی بیشتر)

```python
# 1. درخواست آدرس آپلود
upload_url = bot.request_send_file("Image")
# 2. آپلود فایل و دریافت file_id
file_id = bot.upload_file_to_url(upload_url, "photo.jpg")
# 3. ارسال فایل
bot.send_file(chat_id, file_id, text="توضیح")
```

---

## 👥 مدیریت گروه و کانال

برای استفاده از متدهای مدیریتی، بات باید **ادمین** گروه یا کانال باشد.

```python
# مسدود کردن کاربر
bot.ban_chat_member("g123456789", "u0HspK0e53c9c5bc874ec6c4673bf868")

# رفع مسدودیت
bot.unban_chat_member("g123456789", "u0HspK0e53c9c5bc874ec6c4673bf868")

# حذف پیام
bot.delete_message("g123456789", "1657017090451768991")

# ویرایش متن پیام خود بات
bot.edit_message_text("g123456789", "1657017090451768991", "متن جدید")
```

---

## 🧪 تست کامل (اسکریپت آماده)

در مخزن Robota یک فایل `test_robota_complete.py` وجود دارد که تمام متدها را به صورت تعاملی تست میکند.

```bash
git clone https://github.com/amiralicoldark/Robota.git
cd Robota
python test_robota_complete.py
```

این اسکریپت از شما توکن و chat_id میخواهد و سپس یکییکی متدها را اجرا کرده و نتیجه را نمایش میدهد.

---

## 📄 مستندات آنلاین

برای مشاهده توضیحات بصری، مثال‌های بیشتر و دموی کیپدها، به صفحه زیر مراجعه کنید:

🔗 **[https://amiralicoldark.github.io/Robota](https://amiralicoldark.github.io/Robota)**

این صفحه با React ساخته شده و تمام متدها، دکمه‌ها و مثال‌ها را به صورت تعاملی نمایش میدهد.

---

## 🤝 مشارکت در توسعه

اگر ایدهای دارید، باگی پیدا کردهاید یا میخواهید متد جدیدی اضافه کنید، خوشحال میشوم.

1. مخزن را **فورک** کنید
2. یک برنچ جدید بسازید (`git checkout -b feature/awesome`)
3. تغییرات را کامیت کنید (`git commit -m 'Add awesome feature'`)
4. پوش کنید (`git push origin feature/awesome`)
5. یک **Pull Request** باز کنید

---

## 📜 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است. برای جزئیات بیشتر فایل `LICENSE` را ببینید.

---

## 🌟 درباره من (توسعه‌دهنده)

سلام! من **امیرعلی مومنی** هستم، برنامه‌نویس پایتون.

- **گیت‌هاب**: [@amiralicoldark](https://github.com/amiralicoldark)
- **روبیکا**: [@am1ralimo](https://rubika.ir/am1ralimo)
- **ایمیل**: amir.darkli80@gmail.com

این کتابخانه را با ❤️ برای جامعه روبیکا و برای اینکه توسعه‌دهندگان ایرانی بتوانند به راحتی ربات‌های حرفه‌ای بسازند، نوشته‌ام. اگر خوشتان آمد، فراموش نکنید به مخزن **ستاره (⭐)** بدهید.

از شما که از Robota استفاده میکنید، سپاسگزارم.

---

**پایان راهنما** 🚀
```

این فایل `README.md` را در ریشه مخزن `Robota` ذخیره کنید. همچنین فایل `index.html` با React را در پوشه `docs/` قرار دهید و GitHub Pages را روی شاخه `/docs` تنظیم کنید تا مستندات آنلاین در آدرس https://amiralicoldark.github.io/Robota در دسترس باشد.

اگر نیاز به تغییر یا افزودن بخش خاصی دارید، بگویید. موفق باشید!
