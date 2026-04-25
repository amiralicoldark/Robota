
import sys
import time
from robota import RubikaBot, RubikaHelpers, ChatKeypadTypeEnum, FileTypeEnum, MetadataTypeEnum

# ========== تنظیمات اولیه ==========
TOKEN = input("🔑 توکن بات را وارد کنید: ").strip()
CHAT_ID = input("💬 شناسه چت (chat_id) را وارد کنید: ").strip()

if not TOKEN or not CHAT_ID:
    print("❌ توکن و chat_id الزامی هستند.")
    sys.exit(1)

bot = RubikaBot(TOKEN)
helpers = RubikaHelpers()

print("\n" + "="*60)
print("🚀 شروع تست کتابخانه robota")
print("="*60)

# ========== توابع تست ==========
def print_result(name: str, success: bool, detail: str = ""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status:8} - {name:<30} : {detail}")

def test_get_me():
    try:
        me = bot.get_me()
        print_result("get_me", True, f"{me.bot_title} (@{me.username})")
        return True
    except Exception as e:
        print_result("get_me", False, str(e))
        return False

def test_send_message():
    try:
        res = bot.send_message(CHAT_ID, "سلام! این پیام تست از کتابخانه robota است.")
        msg_id = res.get("message_id")
        print_result("send_message (متن ساده)", bool(msg_id), f"message_id: {msg_id}")
        return msg_id
    except Exception as e:
        print_result("send_message (متن ساده)", False, str(e))
        return None

def test_send_inline_keypad():
    try:
        btn1 = helpers.simple_button("yes", "✅ بله")
        btn2 = helpers.simple_button("no", "❌ خیر")
        row = helpers.row(btn1, btn2)
        keypad = helpers.keypad([row])
        res = bot.send_message(CHAT_ID, "آیا کتابخانه را کامل می‌دانید؟", inline_keypad=keypad)
        print_result("send_message با InlineKeypad", bool(res.get("message_id")), f"msg_id: {res.get('message_id')}")
        return True
    except Exception as e:
        print_result("send_message با InlineKeypad", False, str(e))
        return False

def test_send_poll():
    try:
        res = bot.send_poll(CHAT_ID, "نظر شما درباره کتابخانه؟", ["عالی", "خوب", "متوسط", "ضعیف"])
        print_result("send_poll", bool(res.get("message_id")), f"msg_id: {res.get('message_id')}")
        return True
    except Exception as e:
        print_result("send_poll", False, str(e))
        return False

def test_send_location():
    try:
        res = bot.send_location(CHAT_ID, 35.699739, 51.338097)  # تهران
        print_result("send_location", bool(res.get("message_id")), f"msg_id: {res.get('message_id')}")
        return True
    except Exception as e:
        print_result("send_location", False, str(e))
        return False

def test_send_contact():
    try:
        res = bot.send_contact(CHAT_ID, "علی", "محمدی", "09123456789")
        print_result("send_contact", bool(res.get("message_id")), f"msg_id: {res.get('message_id')}")
        return True
    except Exception as e:
        print_result("send_contact", False, str(e))
        return False

def test_get_chat():
    try:
        chat = bot.get_chat(CHAT_ID)
        print_result("get_chat", True, f"نوع: {chat.chat_type.value}, نام: {chat.title or chat.first_name or chat.username}")
        return True
    except Exception as e:
        print_result("get_chat", False, str(e))
        return False

def test_set_commands():
    try:
        commands = [
            {"command": "start", "description": "شروع ربات"},
            {"command": "help", "description": "راهنما"},
            {"command": "about", "description": "درباره ربات"}
        ]
        bot.set_commands(commands)
        print_result("set_commands", True, "دستورات با موفقیت ثبت شد")
        return True
    except Exception as e:
        print_result("set_commands", False, str(e))
        return False

def test_edit_and_delete_message():
    try:
        res = bot.send_message(CHAT_ID, "پیام موقت برای ویرایش و حذف")
        msg_id = res.get("message_id")
        if not msg_id:
            raise Exception("message_id دریافت نشد")
        bot.edit_message_text(CHAT_ID, msg_id, "✏️ متن ویرایش شده")
        print_result("edit_message_text", True, f"msg {msg_id} ویرایش شد")
        confirm = input("🔄 آیا می‌خواهید پیام تست را حذف کنید؟ (y/n): ").strip().lower()
        if confirm == 'y':
            bot.delete_message(CHAT_ID, msg_id)
            print_result("delete_message", True, f"msg {msg_id} حذف شد")
        else:
            print_result("delete_message", True, "حذف انجام نشد (اختیاری)")
        return True
    except Exception as e:
        print_result("edit_and_delete", False, str(e))
        return False

def test_chat_keypad():
    try:
        btn = helpers.simple_button("test_key", "دکمه تست")
        row = helpers.row(btn)
        keypad = helpers.keypad([row], resize_keyboard=True, one_time_keyboard=True)
        bot.edit_chat_keypad(CHAT_ID, chat_keypad=keypad, chat_keypad_type=ChatKeypadTypeEnum.NEW)
        print_result("edit_chat_keypad (اضافه)", True, "کیپد پایین اضافه شد")
        confirm = input("🗑️ آیا می‌خواهید کیپد را حذف کنید؟ (y/n): ").strip().lower()
        if confirm == 'y':
            bot.edit_chat_keypad(CHAT_ID, chat_keypad_type=ChatKeypadTypeEnum.REMOVE)
            print_result("edit_chat_keypad (حذف)", True, "کیپد حذف شد")
        else:
            print_result("edit_chat_keypad (حذف)", True, "حذف نشد (اختیاری)")
        return True
    except Exception as e:
        print_result("chat_keypad", False, str(e))
        return False

def test_get_updates():
    try:
        updates, next_offset = bot.get_updates(limit=3, auto_offset=False)
        print_result("get_updates (بدون offset خودکار)", True, f"تعداد: {len(updates)}")
        if updates:
            print(f"   آخرین آپدیت: {updates[0].type.value} از {updates[0].chat_id}")
        return True
    except Exception as e:
        print_result("get_updates", False, str(e))
        return False

def test_forward_message():
    try:
        res = bot.send_message(CHAT_ID, "پیام مبدأ برای فوروارد")
        msg_id = res.get("message_id")
        if not msg_id:
            raise Exception("message_id برای فوروارد دریافت نشد")
        time.sleep(1)
        fwd = bot.forward_message(CHAT_ID, msg_id, CHAT_ID)
        new_id = fwd.get("new_message_id")
        print_result("forward_message", bool(new_id), f"new_message_id: {new_id}")
        # پاک کردن پیام اصلی (اختیاری)
        bot.delete_message(CHAT_ID, msg_id)
        return True
    except Exception as e:
        print_result("forward_message", False, str(e))
        return False

def test_metadata():
    try:
        text = "سلام کاربر گرامی! لطفاً به سایت مراجعه کنید."
        parts = [
            helpers.metadata_part(MetadataTypeEnum.BOLD, 0, 4),          # "سلام" پررنگ
            helpers.metadata_part(MetadataTypeEnum.LINK, 16, 8, link_url="https://rubika.ir")
        ]
        meta = helpers.metadata(parts)
        res = bot.send_message(CHAT_ID, text, metadata=meta)
        print_result("send_message با Metadata", bool(res.get("message_id")), f"msg_id: {res.get('message_id')}")
        return True
    except Exception as e:
        print_result("metadata", False, str(e))
        return False

def test_upload_and_send_file():
    import os
    file_path = input("📁 برای تست آپلود فایل، مسیر یک عکس کوچک را وارد کنید (یا Enter برای رد شدن): ").strip()
    if not file_path or not os.path.isfile(file_path):
        print("⏭️ تست آپلود فایل رد شد.")
        return True
    try:
        res = bot.upload_and_send_file(CHAT_ID, file_path, FileTypeEnum.IMAGE, caption="عکس آپلودی از تست")
        print_result("upload_and_send_file", bool(res.get("message_id")), f"msg_id: {res.get('message_id')}")
        return True
    except Exception as e:
        print_result("upload_and_send_file", False, str(e))
        return False

def test_ban_unban():
    print("\n⚠️ تست مسدود کردن کاربر نیاز به user_id دارد (اختیاری)")
    user_id = input("شناسه کاربر (user_id) برای تست ban/unban (یا Enter برای رد شدن): ").strip()
    if not user_id:
        print("⏭️ تست ban/unban رد شد.")
        return True
    try:
        bot.ban_chat_member(CHAT_ID, user_id)
        print_result("ban_chat_member", True, f"user {user_id} مسدود شد")
        confirm = input("رفع مسدودیت؟ (y/n): ").strip().lower()
        if confirm == 'y':
            bot.unban_chat_member(CHAT_ID, user_id)
            print_result("unban_chat_member", True, f"user {user_id} آزاد شد")
        else:
            print_result("unban_chat_member", True, "اختیاری، انجام نشد")
        return True
    except Exception as e:
        print_result("ban/unban", False, str(e))
        return False

# ========== اجرای تست‌ها ==========
if __name__ == "__main__":
    tests = [
        ("get_me", test_get_me),
        ("send_message", test_send_message),
        ("send_inline_keypad", test_send_inline_keypad),
        ("send_poll", test_send_poll),
        ("send_location", test_send_location),
        ("send_contact", test_send_contact),
        ("get_chat", test_get_chat),
        ("set_commands", test_set_commands),
        ("edit_and_delete", test_edit_and_delete_message),
        ("chat_keypad", test_chat_keypad),
        ("get_updates", test_get_updates),
        ("forward_message", test_forward_message),
        ("metadata", test_metadata),
        ("upload_and_send_file", test_upload_and_send_file),
        ("ban_unban", test_ban_unban),
    ]

    results = []
    for name, func in tests:
        print(f"\n--- تست {name} ---")
        res = func()
        results.append((name, res))
        time.sleep(0.5)

    print("\n" + "="*60)
    print("📊 خلاصه نتایج تست:")
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")

    total = len(results)
    passed = sum(1 for _, s in results if s)
    print(f"\n🎯 موفقیت: {passed}/{total} تست با موفقیت انجام شد.")
    print("="*60)
