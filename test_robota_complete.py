
import sys
import time
import os
from robota import (
    RubikaBot, RubikaHelpers,
    ChatTypeEnum, FileTypeEnum, UpdateTypeEnum,
    Keypad, KeypadRow, Button, ButtonTypeEnum,
    BotCommand, Metadata, MetadataTypeEnum
)


# ========== دریافت اطلاعات اولیه ==========
def get_input(prompt, default=None):
    val = input(prompt).strip()
    return val if val else default


print("🤖 Robota - تست کامل کتابخانه")
print("=" * 50)

TOKEN = get_input("🔑 توکن بات خود را وارد کنید: ")
CHAT_ID = get_input("💬 شناسه چت (chat_id) را وارد کنید: ")

if not TOKEN or not CHAT_ID:
    print("❌ توکن و chat_id الزامی هستند.")
    sys.exit(1)

bot = RubikaBot(TOKEN)
helpers = RubikaHelpers()


# ========== توابع تست ==========
def print_result(name, success, detail=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status:8} - {name:<35} : {detail}")


def test_get_me():
    try:
        me = bot.get_me()
        print_result("get_me", True, f"{me.bot_title} (@{me.username})")
        return True
    except Exception as e:
        print_result("get_me", False, str(e))
        return False


def test_send_simple_message():
    try:
        res = bot.send_message(CHAT_ID, "سلام! این پیام تست از کتابخانه Robota است.")
        msg_id = res.get("message_id")
        print_result("send_message (ساده)", bool(msg_id), f"msg_id: {msg_id}")
        return msg_id
    except Exception as e:
        print_result("send_message (ساده)", False, str(e))
        return None


def test_send_inline_keypad():
    try:
        btn1 = helpers.simple_button("yes", "✅ بله")
        btn2 = helpers.simple_button("no", "❌ خیر")
        row = helpers.row(btn1, btn2)
        keypad = helpers.keypad([row])
        res = bot.send_message(CHAT_ID, "آیا کتابخانه را کامل می‌دانید؟", inline_keypad=keypad)
        print_result("send_message + InlineKeypad", bool(res.get("message_id")), "ارسال شد")
        return True
    except Exception as e:
        print_result("send_message + InlineKeypad", False, str(e))
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
        print_result("get_chat", True,
                     f"نوع: {chat.chat_type.value}, نام: {chat.title or chat.first_name or chat.username}")
        return True
    except Exception as e:
        print_result("get_chat", False, str(e))
        return False


def test_set_commands():
    try:
        commands = [
            BotCommand(command="start", description="شروع ربات"),
            BotCommand(command="help", description="راهنما"),
            BotCommand(command="about", description="درباره ربات")
        ]
        bot.set_commands(commands)
        print_result("set_commands", True, "دستورات ثبت شد")
        return True
    except Exception as e:
        print_result("set_commands", False, str(e))
        return False


def test_edit_and_delete():
    try:
        res = bot.send_message(CHAT_ID, "پیام موقت برای تست ویرایش و حذف")
        msg_id = res.get("message_id")
        if not msg_id:
            raise Exception("message_id دریافت نشد")
        bot.edit_message_text(CHAT_ID, msg_id, "✏️ متن ویرایش شده")
        print_result("edit_message_text", True, f"پیام {msg_id} ویرایش شد")
        confirm = input("🗑️  آیا می‌خواهید پیام تست را حذف کنید؟ (y/n): ").strip().lower()
        if confirm == 'y':
            bot.delete_message(CHAT_ID, msg_id)
            print_result("delete_message", True, "پیام حذف شد")
        else:
            print_result("delete_message", True, "حذف نشد (اختیاری)")
        return True
    except Exception as e:
        print_result("edit_and_delete", False, str(e))
        return False


def test_chat_keypad():
    try:
        btn = helpers.simple_button("test_key", "دکمه تست کیپد")
        row = helpers.row(btn)
        keypad = helpers.keypad([row], resize_keyboard=True, one_time_keyboard=True)
        bot.set_chat_keypad(CHAT_ID, keypad)
        print_result("set_chat_keypad", True, "کیپد پایین اضافه شد")
        confirm = input("🗑️  آیا می‌خواهید کیپد را حذف کنید؟ (y/n): ").strip().lower()
        if confirm == 'y':
            bot.remove_chat_keypad(CHAT_ID)
            print_result("remove_chat_keypad", True, "کیپد حذف شد")
        else:
            print_result("remove_chat_keypad", True, "حذف نشد (اختیاری)")
        return True
    except Exception as e:
        print_result("chat_keypad", False, str(e))
        return False


def test_get_updates():
    try:
        updates, _ = bot.get_updates(limit=3, auto_offset=False)
        print_result("get_updates", True, f"تعداد: {len(updates)}")
        if updates:
            print(f"   نمونه آپدیت: {updates[0].type.value} - chat_id: {updates[0].chat_id}")
        return True
    except Exception as e:
        print_result("get_updates", False, str(e))
        return False


def test_forward_message():
    try:
        # ارسال یک پیام موقت برای فوروارد
        res = bot.send_message(CHAT_ID, "پیام مبدأ برای فوروارد")
        msg_id = res.get("message_id")
        if not msg_id:
            raise Exception("نمی‌توان پیام مبدأ ایجاد کرد")
        time.sleep(1)
        fwd = bot.forward_message(CHAT_ID, msg_id, CHAT_ID)
        new_id = fwd.get("new_message_id")
        print_result("forward_message", bool(new_id), f"new_msg_id: {new_id}")
        # پاک کردن پیام مبدأ
        bot.delete_message(CHAT_ID, msg_id)
        return True
    except Exception as e:
        print_result("forward_message", False, str(e))
        return False


def test_metadata():
    try:
        text = "سلام کاربر گرامی! لطفاً به سایت مراجعه کنید."
        parts = [
            helpers.metadata_part(MetadataTypeEnum.BOLD, 0, 4),  # "سلام" پررنگ
            helpers.metadata_part(MetadataTypeEnum.LINK, 16, 8, link_url="https://rubika.ir")
        ]
        meta = helpers.metadata(parts)
        res = bot.send_message(CHAT_ID, text, metadata=meta)
        print_result("metadata", bool(res.get("message_id")), f"msg_id: {res.get('message_id')}")
        return True
    except Exception as e:
        print_result("metadata", False, str(e))
        return False


def test_upload_and_send_file():
    file_path = input("📁  مسیر یک فایل (عکس/فیلم) را برای آپلود وارد کنید (یا Enter برای رد شدن): ").strip()
    if not file_path or not os.path.isfile(file_path):
        print("⏭️  تست آپلود فایل رد شد.")
        return True
    try:
        res = bot.upload_and_send_file(CHAT_ID, file_path, FileTypeEnum.IMAGE, caption="آپلود از تست")
        print_result("upload_and_send_file", bool(res.get("message_id")), f"msg_id: {res.get('message_id')}")
        return True
    except Exception as e:
        print_result("upload_and_send_file", False, str(e))
        return False


def test_ban_unban():
    print("\n⚠️  تست بن/آنبن نیاز به user_id دارد (اختیاری)")
    user_id = input("شناسه کاربر (user_id) را وارد کنید (یا Enter برای رد شدن): ").strip()
    if not user_id:
        print("⏭️  تست بن/آنبن رد شد.")
        return True
    try:
        bot.ban_chat_member(CHAT_ID, user_id)
        print_result("ban_chat_member", True, f"کاربر {user_id} مسدود شد")
        confirm = input("رفع مسدودیت؟ (y/n): ").strip().lower()
        if confirm == 'y':
            bot.unban_chat_member(CHAT_ID, user_id)
            print_result("unban_chat_member", True, "رفع مسدودیت انجام شد")
        else:
            print_result("unban_chat_member", True, "اختیاری، انجام نشد")
        return True
    except Exception as e:
        print_result("ban/unban", False, str(e))
        return False


def test_edit_message_keypad():
    try:
        # ابتدا یک پیام با inline_keypad ارسال می‌کنیم
        btn = helpers.simple_button("old_btn", "دکمه قدیمی")
        row = helpers.row(btn)
        old_kp = helpers.keypad([row])
        res = bot.send_message(CHAT_ID, "پیام با کیپد اولیه", inline_keypad=old_kp)
        msg_id = res.get("message_id")
        if not msg_id:
            raise Exception("نمی‌توان پیام اولیه ایجاد کرد")
        # ساخت کیپد جدید
        new_btn = helpers.simple_button("new_btn", "دکمه جدید")
        new_row = helpers.row(new_btn)
        new_kp = helpers.keypad([new_row])
        bot.edit_message_keypad(CHAT_ID, msg_id, new_kp)
        print_result("edit_message_keypad", True, f"کیپد پیام {msg_id} ویرایش شد")
        # پاک کردن پیام تست (اختیاری)
        confirm = input("آیا می‌خواهید پیام تست را حذف کنید؟ (y/n): ").strip().lower()
        if confirm == 'y':
            bot.delete_message(CHAT_ID, msg_id)
        return True
    except Exception as e:
        print_result("edit_message_keypad", False, str(e))
        return False


# ========== اجرای تست‌ها ==========
def main():
    tests = [
        ("get_me", test_get_me),
        ("send_simple_message", test_send_simple_message),
        ("send_inline_keypad", test_send_inline_keypad),
        ("send_poll", test_send_poll),
        ("send_location", test_send_location),
        ("send_contact", test_send_contact),
        ("get_chat", test_get_chat),
        ("set_commands", test_set_commands),
        ("edit_and_delete", test_edit_and_delete),
        ("chat_keypad", test_chat_keypad),
        ("get_updates", test_get_updates),
        ("forward_message", test_forward_message),
        ("metadata", test_metadata),
        ("edit_message_keypad", test_edit_message_keypad),
        ("upload_and_send_file", test_upload_and_send_file),
        ("ban_unban", test_ban_unban),
    ]

    results = []
    for name, func in tests:
        print(f"\n--- تست {name} ---")
        res = func()
        results.append((name, res))
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("📊 خلاصه نتایج تست:")
    passed = 0
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
        if success:
            passed += 1
    total = len(results)
    print(f"\n🎯 موفقیت: {passed}/{total} تست با موفقیت انجام شد.")
    print("=" * 60)


if __name__ == "__main__":
    main()
