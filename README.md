```markdown
# 🤖 Robota – کتابخانه رسمی بات روبیکا

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/docs-online-brightgreen)](https://amiralicoldark.github.io/Robota)
[![GitHub Stars](https://img.shields.io/github/stars/amiralicoldark/Robota)](https://github.com/amiralicoldark/Robota)

**Robota** یک کتابخانه قدرتمند، کامل و آسان برای تعامل با **API رسمی بات روبیکا** است. با این کتابخانه می‌توانید تمام قابلیت‌های روبیکا را در ربات خود پیاده کنید: ارسال پیام‌های متنی، دکمه‌های شیشه‌ای و کیپد، نظرسنجی، موقعیت مکانی، مخاطب، فایل (عکس، ویدئو، صدا، سند)، مدیریت گروه و کانال (بن، آنبن، حذف پیام، ویرایش)، و دریافت رویدادها با لانگ پولینگ یا وب‌هوک.

✨ **ویژگی‌های برجسته**:
- پشتیبانی از **همه متدهای رسمی** روبیکا (بیش از ۲۵ متد)
- **۱۸ نوع دکمه تعاملی** (ساده، لینک، انتخاب عدد، تقویم، دوربین، گالری، درخواست شماره و موقعیت، بارکد و...)
- صفحه‌کلید شیشه‌ای (`InlineKeypad`) و صفحه‌کلید پایین چت (`ChatKeypad`)
- متادیتا برای **فرمت‌بندی متن** (پررنگ، کج، لینک، منشن، نقل‌قول، کد و...)
- آپلود و ارسال فایل در **یک خط کد**
- **Long Polling خودکار** با مدیریت `offset`
- پشتیبانی از **Webhook** (با متد `parse_update`)
- **تایپ‌هینتینگ کامل** و خطاگیری حرفه‌ای
- **بدون وابستگی اضافی** (فقط `requests`)

---

## 📦 نصب

### نصب از GitHub (نسخه پایدار و به‌روز)

```bash
pip install git+https://github.com/amiralicoldark/Robota.git
```

### نصب دستی

```bash
git clone https://github.com/amiralicoldark/Robota.git
cd Robota
python setup.py install
```

---

## 🚀 شروع سریع

```python
from robota import RubikaBot

bot = RubikaBot("YOUR_TOKEN")
CHAT_ID = "c123456789"   # از @UserInfoRobot روبیکا بگیرید

# ارسال پیام ساده
bot.send_message(CHAT_ID, "سلام! من ربات Robota هستم 🤖")

# دریافت اطلاعات بات
me = bot.get_me()
print(f"نام بات: {me.bot_title}")
print(f"یوزرنیم: @{me.username}")
```

---

## 📚 مستندات متدها

| متد | توضیح |
|------|--------|
| `get_me()` | دریافت اطلاعات بات (نام، یوزرنیم، آواتار) |
| `send_message(chat_id, text, ...)` | ارسال پیام متنی + کیپد/اینلاین/متادیتا |
| `send_poll(chat_id, question, options)` | ارسال نظرسنجی |
| `send_location(chat_id, lat, lon)` | ارسال موقعیت مکانی |
| `send_contact(chat_id, first_name, last_name, phone)` | ارسال مخاطب |
| `get_chat(chat_id)` | دریافت اطلاعات چت (نوع، عنوان، نام کاربری) |
| `get_updates(limit, auto_offset)` | دریافت آپدیت‌ها (لانگ پولینگ) |
| `forward_message(from_chat, msg_id, to_chat)` | فوروارد پیام |
| `edit_message_text(chat_id, msg_id, new_text)` | ویرایش متن پیام خود بات |
| `edit_message_keypad(chat_id, msg_id, new_keypad)` | ویرایش Inline Keypad |
| `delete_message(chat_id, msg_id)` | حذف پیام |
| `set_commands(list_of_commands)` | تنظیم دستورات منوی بات |
| `update_bot_endpoints(url, type_)` | تنظیم وب‌هوک |
| `set_chat_keypad(chat_id, keypad)` | افزودن صفحه کلید پایین چت |
| `remove_chat_keypad(chat_id)` | حذف صفحه کلید پایین چت |
| `get_file(file_id)` | دریافت آدرس دانلود فایل |
| `send_file(chat_id, file_id, caption)` | ارسال فایل با `file_id` |
| `request_send_file(file_type)` | درخواست آدرس آپلود فایل |
| `upload_and_send_file(chat_id, file_path, file_type, caption)` | آپلود و ارسال یک‌مرحله‌ای فایل |
| `ban_chat_member(chat_id, user_id)` | مسدود کردن کاربر در گروه/کانال |
| `unban_chat_member(chat_id, user_id)` | رفع مسدودیت |
| `parse_update(request_body)` | تبدیل Webhook به شیء Update |
| `parse_inline_message(request_body)` | تبدیل Webhook Inline به شیء InlineMessage |
| `start_polling(callback, interval)` | شروع حلقه‌ی Long Polling خودکار |

> 💡 تمام متدها دارای پارامترهای اضافی (مانند `disable_notification`, `reply_to_message_id`, `chat_keypad`, `inline_keypad`, `metadata`) هستند. برای دیدن جزئیات به [مستندات آنلاین](https://amiralicoldark.github.io/Robota) مراجعه کنید.

---

## 🧩 ساخت دکمه‌ها و کیپد (RubikaHelpers)

کلاس `RubikaHelpers` تمام نوع دکمه‌های مجاز در روبیکا را می‌سازد.

### دکمه‌های پایه

```python
from robota import RubikaHelpers

# دکمه ساده
btn1 = RubikaHelpers.simple_button("id1", "دکمه ساده")

# دکمه لینک
btn2 = RubikaHelpers.link_button("id2", "وب‌سایت", "https://rubika.ir")

# دکمه انتخاب عدد
btn3 = RubikaHelpers.number_picker_button("id3", "انتخاب سن", 1, 100, default=25)

# دکمه ورودی متن
btn4 = RubikaHelpers.textbox_button("id4", "نظر خود را بنویسید", type_line="MultiLine")

# دکمه دوربین عکس
btn5 = RubikaHelpers.camera_image_button("id5", "📸 گرفتن عکس")

# دکمه درخواست شماره تلفن
btn6 = RubikaHelpers.ask_phone_button("id6", "ارسال شماره من")

# دکمه موقعیت
btn7 = RubikaHelpers.ask_location_button("id7", "ارسال موقعیت من")

# دکمه تقویم
btn8 = RubikaHelpers.calendar_button("id8", "انتخاب تاریخ", cal_type="DatePersian")
```

### ساخت ردیف و صفحه‌کلید

```python
# یک ردیف شامل سه دکمه
row = RubikaHelpers.row(btn1, btn2, btn3)

# ساخت کیپد (برای inline_keypad یا chat_keypad)
my_keypad = RubikaHelpers.keypad([row], resize_keyboard=True, one_time_keyboard=False)

# ارسال با inline_keypad
bot.send_message(chat_id, "لطفاً انتخاب کنید:", inline_keypad=my_keypad)
```

---

## 🎨 متادیتا (فرمت‌بندی متن)

```python
from robota import RubikaHelpers, MetadataTypeEnum

text = "سلام کاربر گرامی! لطفاً به سایت مراجعه کنید."

parts = [
    RubikaHelpers.metadata_part(MetadataTypeEnum.BOLD, 0, 4),
    RubikaHelpers.metadata_part(MetadataTypeEnum.LINK, 16, 8, link_url="https://rubika.ir")
]
metadata = RubikaHelpers.metadata(parts)

bot.send_message(chat_id, text, metadata=metadata)
```

انواع `MetadataTypeEnum`: `BOLD`, `ITALIC`, `UNDERLINE`, `STRIKE`, `SPOILER`, `LINK`, `MENTION_TEXT`, `PRE`, `QUOTE`, `MONO`

---

## 🔄 دریافت رویدادها

### روش ۱: Long Polling خودکار (ساده)

```python
from robota import UpdateTypeEnum

def handle(update):
    if update.type == UpdateTypeEnum.NEW_MESSAGE:
        print(f"پیام جدید: {update.new_message.text}")

bot.start_polling(handle, interval=1)
```

### روش ۲: وب‌هوک (Webhook)

```python
# تنظیم آدرس
bot.update_bot_endpoints("https://yourdomain.com/webhook", "ReceiveUpdate")

# در سرور (مثلاً با Flask)
from flask import Flask, request
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = RubikaBot.parse_update(request.get_data())
    # پردازش update
    return "OK"
```

---

## 📂 آپلود و ارسال فایل

### روش یک‌مرحله‌ای (پیشنهادی)

```python
bot.upload_and_send_file(chat_id, "photo.jpg", "Image", caption="عکس من")
```

انواع `file_type`: `"File"`, `"Image"`, `"Voice"`, `"Video"`, `"Music"`, `"Gif"`

### روش دو مرحله‌ای (دسترسی بیشتر)

```python
upload_url = bot.request_send_file("Image")
file_id = bot.upload_file_to_url(upload_url, "photo.jpg")
bot.send_file(chat_id, file_id, text="توضیح")
```

---

## 👥 مدیریت گروه و کانال

برای استفاده از متدهای مدیریتی، بات باید **ادمین** گروه یا کانال باشد.

```python
# مسدود کردن کاربر
bot.ban_chat_member(group_id, user_id)

# رفع مسدودیت
bot.unban_chat_member(group_id, user_id)

# حذف پیام
bot.delete_message(group_id, message_id)
```

---

## 🧪 تست کامل (اسکریپت آماده)

```bash
git clone https://github.com/amiralicoldark/Robota.git
cd Robota
python test_robota_complete.py
```

اسکریپت تست تمام متدها را به صورت تعاملی اجرا کرده و نتیجه را نمایش می‌دهد.

---

## 📄 مستندات آنلاین

برای مشاهده مستندات تعاملی با React و مثال‌های بیشتر، به آدرس زیر مراجعه کنید:

🔗 **[https://amiralicoldark.github.io/Robota](https://amiralicoldark.github.io/Robota)**

---

## 🤝 مشارکت در توسعه

1. مخزن را **فورک** کنید
2. یک برنچ جدید بسازید (`git checkout -b feature/awesome`)
3. تغییرات را کامیت کنید (`git commit -m 'Add awesome feature'`)
4. پوش کنید (`git push origin feature/awesome`)
5. یک **Pull Request** باز کنید

---

## 📜 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است.

---

## 👤 درباره توسعه‌دهنده

**امیرعلی مومنی** (AmirAli Momeni)  
توسعه‌دهنده ارشد پایتون، عاشق متن‌باز و جامعه روبیکا.

- GitHub: [@amiralicoldark](https://github.com/amiralicoldark)
- Rubika: [@am1ralimo](https://rubika.ir/am1ralimo)
- Email: amir.darkli80@gmail.com

---

**ساخته شده با ❤️ برای جامعه روبیکا**
```
