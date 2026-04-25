# rubika_bot.py
import requests
from typing import Optional, List, Dict, Any, Union

class RubikaBot:
    """
    کتابخانه رسمی بات روبیکا
    تمام متدهای مستند شده پشتیبانی می‌شوند.
    """

    def __init__(self, token: str, base_url: str = "https://botapi.rubika.ir/v3"):
        self.token = token
        self.base_url = base_url

    def _request(self, method: str, params: Dict[str, Any] = None) -> Dict:
        """ارسال درخواست به سرور روبیکا"""
        if params is None:
            params = {}
        url = f"{self.base_url}/{self.token}/{method}"
        resp = requests.post(url, json=params)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") and data["status"] != "OK":
            raise Exception(f"API Error: {data}")
        return data

    # ----------------------------------------------
    # متدهای اصلی (بر اساس مستندات)
    # ----------------------------------------------
    def get_me(self) -> Dict:
        """اطلاعات پایه‌ای بات (getMe)"""
        return self._request("getMe")

    def send_message(
        self,
        chat_id: str,
        text: str,
        chat_keypad: Dict = None,
        inline_keypad: Dict = None,
        disable_notification: bool = False,
        reply_to_message_id: str = None,
        chat_keypad_type: str = None,   # "New" یا "Remove"
        metadata: Dict = None
    ) -> Dict:
        """
        ارسال پیام متنی + دکمه‌های شیشه‌ای (InlineKeypad) یا صفحه‌کلید پایین (ChatKeypad)
        """
        params = {"chat_id": chat_id, "text": text}
        if chat_keypad:
            params["chat_keypad"] = chat_keypad
        if inline_keypad:
            params["inline_keypad"] = inline_keypad
        if disable_notification:
            params["disable_notification"] = disable_notification
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if chat_keypad_type:
            params["chat_keypad_type"] = chat_keypad_type
        if metadata:
            params["metadata"] = metadata
        return self._request("sendMessage", params)

    def send_poll(self, chat_id: str, question: str, options: List[str]) -> Dict:
        """ارسال نظرسنجی (sendPoll)"""
        return self._request("sendPoll", {
            "chat_id": chat_id,
            "question": question,
            "options": options
        })

    def send_location(
        self,
        chat_id: str,
        latitude: Union[str, float],
        longitude: Union[str, float],
        chat_keypad: Dict = None,
        disable_notification: bool = False,
        inline_keypad: Dict = None,
        reply_to_message_id: str = None,
        chat_keypad_type: str = None
    ) -> Dict:
        """ارسال موقعیت مکانی (sendLocation)"""
        params = {"chat_id": chat_id, "latitude": str(latitude), "longitude": str(longitude)}
        if chat_keypad:
            params["chat_keypad"] = chat_keypad
        if disable_notification:
            params["disable_notification"] = disable_notification
        if inline_keypad:
            params["inline_keypad"] = inline_keypad
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if chat_keypad_type:
            params["chat_keypad_type"] = chat_keypad_type
        return self._request("sendLocation", params)

    def send_contact(
        self,
        chat_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        chat_keypad: Dict = None,
        disable_notification: bool = False,
        inline_keypad: Dict = None,
        reply_to_message_id: str = None,
        chat_keypad_type: str = None
    ) -> Dict:
        """ارسال مخاطب (sendContact)"""
        params = {
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number
        }
        if chat_keypad:
            params["chat_keypad"] = chat_keypad
        if disable_notification:
            params["disable_notification"] = disable_notification
        if inline_keypad:
            params["inline_keypad"] = inline_keypad
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if chat_keypad_type:
            params["chat_keypad_type"] = chat_keypad_type
        return self._request("sendContact", params)

    def get_chat(self, chat_id: str) -> Dict:
        """دریافت اطلاعات یک چت (getChat)"""
        return self._request("getChat", {"chat_id": chat_id})

    def get_updates(self, offset_id: str = None, limit: int = None) -> Dict:
        """دریافت آخرین آپدیت‌ها (Long Polling) - getUpdates"""
        params = {}
        if offset_id:
            params["offset_id"] = offset_id
        if limit:
            params["limit"] = limit
        return self._request("getUpdates", params)

    def forward_message(
        self,
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        disable_notification: bool = False
    ) -> Dict:
        """فوروارد کردن پیام (forwardMessage)"""
        return self._request("forwardMessage", {
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "to_chat_id": to_chat_id,
            "disable_notification": disable_notification
        })

    def edit_message_text(self, chat_id: str, message_id: str, text: str) -> Dict:
        """ویرایش متن پیام (فقط پیام‌های خود بات) - editMessageText"""
        return self._request("editMessageText", {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        })

    def edit_message_keypad(self, chat_id: str, message_id: str, inline_keypad: Dict) -> Dict:
        """ویرایش دکمه‌های شیشه‌ای یک پیام (editMessageKeypad)"""
        return self._request("editMessageKeypad", {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_keypad": inline_keypad
        })

    def delete_message(self, chat_id: str, message_id: str) -> Dict:
        """حذف پیام (deleteMessage)"""
        return self._request("deleteMessage", {
            "chat_id": chat_id,
            "message_id": message_id
        })

    def set_commands(self, bot_commands: List[Dict[str, str]]) -> Dict:
        """
        تنظیم دستورات بات (setCommands)
        مثال: [{"command": "start", "description": "شروع"}, ...]
        """
        return self._request("setCommands", {"bot_commands": bot_commands})

    def update_bot_endpoints(self, url: str, type_: str) -> Dict:
        """تنظیم Webhook (updateBotEndpoints) - type: ReceiveUpdate, GetSelectionItem, ..."""
        return self._request("updateBotEndpoints", {"url": url, "type": type_})

    def edit_chat_keypad(self, chat_id: str, chat_keypad: Dict = None, chat_keypad_type: str = "Remove") -> Dict:
        """
        حذف یا ویرایش صفحه‌کلید پایین چت (editChatKeypad)
        - برای حذف: chat_keypad_type="Remove"
        - برای افزودن/ویرایش: chat_keypad_type="New" و chat_keypad را پر کنید.
        """
        params = {"chat_id": chat_id, "chat_keypad_type": chat_keypad_type}
        if chat_keypad:
            params["chat_keypad"] = chat_keypad
        return self._request("editChatKeypad", params)

    def get_file(self, file_id: str) -> Dict:
        """دریافت آدرس دانلود فایل (getFile)"""
        return self._request("getFile", {"file_id": file_id})

    def send_file(
        self,
        chat_id: str,
        file_id: str,
        text: str = None,
        reply_to_message_id: str = None,
        disable_notification: bool = False,
        chat_keypad: Dict = None,
        inline_keypad: Dict = None,
        chat_keypad_type: str = None
    ) -> Dict:
        """ارسال فایل با استفاده از file_id (sendFile)"""
        params = {"chat_id": chat_id, "file_id": file_id}
        if text:
            params["text"] = text
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if disable_notification:
            params["disable_notification"] = disable_notification
        if chat_keypad:
            params["chat_keypad"] = chat_keypad
        if inline_keypad:
            params["inline_keypad"] = inline_keypad
        if chat_keypad_type:
            params["chat_keypad_type"] = chat_keypad_type
        return self._request("sendFile", params)

    def request_send_file(self, type_: str) -> Dict:
        """
        دریافت آدرس آپلود فایل (requestSendFile)
        type_ = "Image", "Video", "File", "Voice", "Music", "Gif"
        """
        return self._request("requestSendFile", {"type": type_})

    def upload_file_to_url(self, upload_url: str, file_path: str) -> Dict:
        """آپلود فایل به آدرسی که request_send_file برگردانده است"""
        with open(file_path, "rb") as f:
            files = {"file": f}
            resp = requests.post(upload_url, files=files)
            resp.raise_for_status()
            return resp.json()

    def upload_and_send_file(
        self,
        chat_id: str,
        file_path: str,
        file_type: str,
        caption: str = None,
        **kwargs
    ) -> Dict:
        """
        یک مرحله‌ای: درخواست آدرس آپلود -> آپلود فایل -> ارسال فایل با file_id به دست آمده
        """
        # 1. درخواست آدرس آپلود
        res = self.request_send_file(file_type)
        upload_url = res.get("upload_url")
        if not upload_url:
            raise Exception("upload_url not found in response")
        # 2. آپلود فایل
        upload_result = self.upload_file_to_url(upload_url, file_path)
        file_id = upload_result.get("file_id")
        if not file_id:
            raise Exception("file_id not found in upload response")
        # 3. ارسال فایل
        return self.send_file(chat_id=chat_id, file_id=file_id, text=caption, **kwargs)

    def ban_chat_member(self, chat_id: str, user_id: str) -> Dict:
        """مسدود کردن کاربر در گروه/کانال (banChatMember)"""
        return self._request("banChatMember", {"chat_id": chat_id, "user_id": user_id})

    def unban_chat_member(self, chat_id: str, user_id: str) -> Dict:
        """رفع مسدودیت کاربر (unbanChatMember)"""
        return self._request("unbanChatMember", {"chat_id": chat_id, "user_id": user_id})


# ------------------------------------------------------------
# ابزارهای کمکی برای ساخت Keypad ، InlineKeypad ، Metadata
# ------------------------------------------------------------
class RubikaHelpers:
    """توابع کمکی برای ساخت دکمه‌ها، صفحه‌کلیدها و متادیتا"""

    @staticmethod
    def simple_button(button_id: str, button_text: str) -> Dict:
        """دکمه ساده (Simple)"""
        return {"id": button_id, "type": "Simple", "button_text": button_text}

    @staticmethod
    def link_button(button_id: str, button_text: str, link_url: str) -> Dict:
        """دکمه لینک (Link)"""
        return {"id": button_id, "type": "Link", "button_text": button_text, "link_url": link_url}

    @staticmethod
    def selection_button(button_id: str, button_text: str, selection_data: Dict) -> Dict:
        """دکمه لیست انتخابی (Selection) - selection_data مطابق مدل ButtonSelection"""
        return {"id": button_id, "type": "Selection", "button_text": button_text, "button_selection": selection_data}

    @staticmethod
    def number_picker_button(button_id: str, button_text: str, min_val: int, max_val: int, default_val: int = None, title: str = None) -> Dict:
        """دکمه انتخاب عدد"""
        picker = {"min_value": str(min_val), "max_value": str(max_val)}
        if default_val is not None:
            picker["default_value"] = str(default_val)
        if title:
            picker["title"] = title
        return {"id": button_id, "type": "NumberPicker", "button_text": button_text, "button_number_picker": picker}

    @staticmethod
    def location_button(button_id: str, button_text: str, type_: str = "Picker", title: str = None) -> Dict:
        """دکمه موقعیت مکانی (Picker یا View)"""
        loc = {"type": type_}
        if title:
            loc["title"] = title
        return {"id": button_id, "type": "Location", "button_text": button_text, "button_location": loc}

    @staticmethod
    def textbox_button(button_id: str, button_text: str, type_line: str = "Single", type_keypad: str = "String", placeholder: str = None, title: str = None) -> Dict:
        """دکمه ورودی متن"""
        tb = {"type_line": type_line, "type_keypad": type_keypad}
        if placeholder:
            tb["place_holder"] = placeholder
        if title:
            tb["title"] = title
        return {"id": button_id, "type": "Textbox", "button_text": button_text, "button_textbox": tb}

    @staticmethod
    def row(*buttons) -> Dict:
        """ساخت یک ردیف از دکمه‌ها"""
        return {"buttons": list(buttons)}

    @staticmethod
    def keypad(rows: List[Dict], resize_keyboard: bool = False, one_time_keyboard: bool = False) -> Dict:
        """ساخت صفحه‌کلید (Keypad) - قابل استفاده در send_message (chat_keypad یا inline_keypad)"""
        return {
            "rows": rows,
            "resize_keyboard": resize_keyboard,
            "one_time_keyboard": one_time_keyboard
        }

    @staticmethod
    def metadata_part(type_: str, from_index: int, length: int, link_url: str = None, mention_user_id: str = None) -> Dict:
        """
        ساخت یک قسمت متادیتا
        type_ : Bold, Italic, Underline, Strike, Link, MentionText, Pre, Quote, Spoiler, Mono
        """
        part = {"type": type_, "from_index": from_index, "length": length}
        if type_ == "Link" and link_url:
            part["link_url"] = link_url
        if type_ == "MentionText" and mention_user_id:
            part["mention_text_user_id"] = mention_user_id
        return part

    @staticmethod
    def metadata(parts: List[Dict]) -> Dict:
        """ساخت Metadata کامل برای ارسال با send_message"""
        return {"meta_data_parts": parts}
