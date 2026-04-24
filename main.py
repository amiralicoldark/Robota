

نصب: pip install requests
استفاده:
    from robota import Robota

    bot = Robota("YOUR_TOKEN")
    bot.send_text("chat_id", "سلام!")
"""

from __future__ import annotations
import requests
import time
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Callable


# ----------------------------- Enums -----------------------------
class ChatTypeEnum(str, Enum):
    USER = "User"
    BOT = "Bot"
    GROUP = "Group"
    CHANNEL = "Channel"


class FileTypeEnum(str, Enum):
    FILE = "File"
    IMAGE = "Image"
    VOICE = "Voice"
    VIDEO = "Video"
    MUSIC = "Music"
    GIF = "Gif"


class ForwardedFromEnum(str, Enum):
    USER = "User"
    CHANNEL = "Channel"
    BOT = "Bot"


class PollStatusEnum(str, Enum):
    CLOSED = "Closed"
    OPEN = "Open"


class ButtonSelectionTypeEnum(str, Enum):
    TEXT = "Text"
    IMAGE = "Image"
    TEXT_IMAGE = "TextImage"


class ButtonSelectionSearchEnum(str, Enum):
    NONE = "None"
    SERVER = "Server"
    CLIENT = "Client"


class ButtonSelectionGetEnum(str, Enum):
    OFFLINE = "Offline"
    SERVER = "Server"


class ButtonCalendarTypeEnum(str, Enum):
    PERSIAN = "Persian"
    GREGORIAN = "Gregorian"


class ButtonTextboxTypeKeypadEnum(str, Enum):
    STRING = "String"
    NUMBER = "Number"


class ButtonTextboxTypeLineEnum(str, Enum):
    SINGLE = "Single"
    MULTI = "Multi"


class ButtonLocationTypeEnum(str, Enum):
    SELECT = "Select"
    VIEW = "View"


class MessageSenderEnum(str, Enum):
    USER = "User"
    BOT = "Bot"


class UpdateTypeEnum(str, Enum):
    NEW_MESSAGE = "NewMessage"
    EDITED_MESSAGE = "EditedMessage"
    REMOVED_MESSAGE = "RemovedMessage"


class ChatKeypadTypeEnum(str, Enum):
    NEW = "New"
    REMOVE = "Remove"


class UpdateEndpointTypeEnum(str, Enum):
    GET_SELECTION_ITEM = "GetSelectionItem"
    GET_CALENDAR = "GetCalendar"
    GET_NUMBER_PICKER = "GetNumberPicker"
    GET_STRING_PICKER = "GetStringPicker"
    GET_LOCATION = "GetLocation"
    GET_TEXTBOX = "GetTextbox"
    GET_FILE = "GetFile"
    GET_AUDIO = "GetAudio"
    GET_VIDEO = "GetVideo"
    GET_IMAGE = "GetImage"
    GET_GIF = "GetGif"
    GET_VOICE = "GetVoice"
    GET_MUSIC = "GetMusic"


class MetadataTypeEnum(str, Enum):
    BOLD = "Bold"
    ITALIC = "Italic"
    UNDERLINE = "Underline"
    STRIKE = "Strike"
    LINK = "Link"
    MENTION_TEXT = "MentionText"


class ButtonTypeEnum(str, Enum):
    SIMPLE = "Simple"
    SELECTION = "Selection"
    CALENDAR = "Calendar"
    NUMBER_PICKER = "NumberPicker"
    STRING_PICKER = "StringPicker"
    LOCATION = "Location"
    CAMERA_IMAGE = "CameraImage"
    CAMERA_VIDEO = "CameraVideo"
    GALLERY_IMAGE = "GalleryImage"
    GALLERY_VIDEO = "GalleryVideo"
    FILE = "File"
    AUDIO = "Audio"
    RECORD_AUDIO = "RecordAudio"
    TEXTBOX = "Textbox"
    LINK = "Link"
    ASK_MY_PHONE_NUMBER = "AskMyPhoneNumber"
    ASK_MY_LOCATION = "AskMyLocation"
    BARCODE = "Barcode"


# ------------------------ Data Models ---------------------------
@dataclass
class File:
    file_id: str
    file_name: Optional[str] = None
    size: Optional[str] = None  # bytes


@dataclass
class ForwardedFrom:
    type_from: ForwardedFromEnum
    message_id: Optional[str] = None
    from_chat_id: Optional[str] = None
    from_sender_id: Optional[str] = None


@dataclass
class Bot:
    bot_id: str
    bot_title: Optional[str] = None
    avatar: Optional[File] = None
    description: Optional[str] = None
    username: Optional[str] = None
    start_message: Optional[str] = None
    share_url: Optional[str] = None


@dataclass
class BotCommand:
    command: str
    description: str


@dataclass
class Sticker:
    sticker_id: str
    file: Optional[File] = None
    emoji_character: Optional[str] = None


@dataclass
class ContactMessage:
    phone_number: str
    first_name: str
    last_name: Optional[str] = None


@dataclass
class PollStatus:
    state: PollStatusEnum
    selection_index: int = -1
    percent_vote_options: List[int] = field(default_factory=list)
    total_vote: int = 0
    show_total_votes: bool = False


@dataclass
class Poll:
    question: str
    options: List[str] = field(default_factory=list)
    poll_status: Optional[PollStatus] = None


@dataclass
class Location:
    longitude: str
    latitude: str


@dataclass
class ButtonSelectionItem:
    text: str
    image_url: Optional[str] = None
    type: ButtonSelectionTypeEnum = ButtonSelectionTypeEnum.TEXT


@dataclass
class ButtonSelection:
    selection_id: str
    search_type: ButtonSelectionSearchEnum = ButtonSelectionSearchEnum.NONE
    get_type: ButtonSelectionGetEnum = ButtonSelectionGetEnum.OFFLINE
    items: List[ButtonSelectionItem] = field(default_factory=list)
    is_multi_selection: bool = False
    columns_count: str = "1"
    title: Optional[str] = None


@dataclass
class ButtonCalendar:
    type: ButtonCalendarTypeEnum
    min_year: str
    max_year: str
    default_value: Optional[str] = None
    title: Optional[str] = None


@dataclass
class ButtonNumberPicker:
    min_value: str
    max_value: str
    default_value: Optional[str] = None
    title: Optional[str] = None


@dataclass
class ButtonStringPicker:
    items: List[str] = field(default_factory=list)
    default_value: Optional[str] = None
    title: Optional[str] = None


@dataclass
class ButtonTextbox:
    type_line: ButtonTextboxTypeLineEnum
    type_keypad: ButtonTextboxTypeKeypadEnum
    place_holder: Optional[str] = None
    title: Optional[str] = None
    default_value: Optional[str] = None


@dataclass
class ButtonLocation:
    default_pointer_location: Location
    default_map_location: Location
    type: ButtonLocationTypeEnum
    title: Optional[str] = None


@dataclass
class AuxData:
    start_id: Optional[str] = None
    button_id: Optional[str] = None


@dataclass
class Button:
    id: str
    type: ButtonTypeEnum
    button_text: Optional[str] = None
    button_selection: Optional[ButtonSelection] = None
    button_calendar: Optional[ButtonCalendar] = None
    button_number_picker: Optional[ButtonNumberPicker] = None
    button_string_picker: Optional[ButtonStringPicker] = None
    button_location: Optional[ButtonLocation] = None
    button_textbox: Optional[ButtonTextbox] = None


@dataclass
class KeypadRow:
    buttons: List[Button] = field(default_factory=list)


@dataclass
class Keypad:
    rows: List[KeypadRow] = field(default_factory=list)
    resize_keyboard: bool = False
    one_time_keyboard: bool = False


@dataclass
class MessageKeypadUpdate:
    message_id: str
    inline_keypad: Keypad


@dataclass
class Message:
    message_id: str
    text: Optional[str] = None
    time: Optional[int] = None
    is_edited: bool = False
    sender_type: Optional[MessageSenderEnum] = None
    sender_id: Optional[str] = None
    aux_data: Optional[AuxData] = None
    file: Optional[File] = None
    reply_to_message_id: Optional[str] = None
    forwarded_from: Optional[ForwardedFrom] = None
    forwarded_no_link: Optional[str] = None
    location: Optional[Location] = None
    sticker: Optional[Sticker] = None
    contact_message: Optional[ContactMessage] = None
    poll: Optional[Poll] = None


@dataclass
class Update:
    type: UpdateTypeEnum
    chat_id: str
    new_message: Optional[Message] = None
    updated_message: Optional[Message] = None
    removed_message_id: Optional[str] = None


@dataclass
class InlineMessage:
    sender_id: str
    message_id: str
    chat_id: str
    text: Optional[str] = None
    file: Optional[File] = None
    location: Optional[Location] = None
    aux_data: Optional[AuxData] = None


@dataclass
class MetadataPart:
    type: MetadataTypeEnum
    from_index: int
    length: int
    link_url: Optional[str] = None
    mention_text_user_id: Optional[str] = None


@dataclass
class Metadata:
    meta_data_parts: List[MetadataPart] = field(default_factory=list)


@dataclass
class Chat:
    chat_id: str
    chat_type: ChatTypeEnum
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None


@dataclass
class MessageTextUpdate:
    message_id: str
    text: str


# ------------------------ Main Bot Class ------------------------
class Robota:
    """رباتی ساده و کامل برای تعامل با API روبیکا"""

    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://botapi.rubika.ir/v3/{self.token}"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _post(self, method: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{method}"
        resp = self.session.post(url, json=data or {})
        resp.raise_for_status()
        return resp.json()

    # ---------- اطلاعات بات ----------
    def get_me(self) -> Dict[str, Any]:
        """دریافت اطلاعات بات (نام، شناسه و ...)"""
        return self._post("getMe")

    # ---------- ارسال پیام ----------
    def send_message(
        self,
        chat_id: str,
        text: str,
        *,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "disable_notification": disable_notification,
        }
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if inline_keypad:
            payload["inline_keypad"] = inline_keypad
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad
            payload["chat_keypad_type"] = chat_keypad_type or ChatKeypadTypeEnum.NEW
        if metadata:
            payload["metadata"] = metadata
        return self._post("sendMessage", payload)

    def send_text(self, chat_id: str, text: str, **kwargs) -> Dict[str, Any]:
        return self.send_message(chat_id, text, **kwargs)

    # ---------- ارسال نظرسنجی ----------
    def send_poll(self, chat_id: str, question: str, options: List[str]) -> Dict[str, Any]:
        return self._post("sendPoll", {
            "chat_id": chat_id,
            "question": question,
            "options": options,
        })

    # ---------- ارسال موقعیت مکانی ----------
    def send_location(
        self,
        chat_id: str,
        latitude: str,
        longitude: str,
        *,
        inline_keypad: Optional[Dict] = None,
        chat_keypad: Optional[Dict] = None,
        chat_keypad_type: Optional[str] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "disable_notification": disable_notification,
        }
        self._attach_keypad(payload, inline_keypad, chat_keypad, chat_keypad_type, reply_to_message_id)
        return self._post("sendLocation", payload)

    # ---------- ارسال مخاطب ----------
    def send_contact(
        self,
        chat_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        *,
        inline_keypad: Optional[Dict] = None,
        chat_keypad: Optional[Dict] = None,
        chat_keypad_type: Optional[str] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "disable_notification": disable_notification,
        }
        self._attach_keypad(payload, inline_keypad, chat_keypad, chat_keypad_type, reply_to_message_id)
        return self._post("sendContact", payload)

    def _attach_keypad(
        self,
        payload: Dict,
        inline: Optional[Dict],
        chat: Optional[Dict],
        chat_type: Optional[str],
        reply_id: Optional[str],
    ):
        if inline:
            payload["inline_keypad"] = inline
        if chat:
            payload["chat_keypad"] = chat
            payload["chat_keypad_type"] = chat_type or ChatKeypadTypeEnum.NEW
        if reply_id:
            payload["reply_to_message_id"] = reply_id

    # ---------- اطلاعات چت ----------
    def get_chat(self, chat_id: str) -> Dict[str, Any]:
        return self._post("getChat", {"chat_id": chat_id})

    # ---------- دریافت به‌روزرسانی‌ها ----------
    def get_updates(self, limit: int = 10, offset_id: Optional[str] = None) -> Dict[str, Any]:
        data = {"limit": limit}
        if offset_id:
            data["offset_id"] = offset_id
        return self._post("getUpdates", data)

    # ---------- فوروارد پیام ----------
    def forward_message(
        self,
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        disable_notification: bool = False,
    ) -> Dict[str, Any]:
        return self._post("forwardMessage", {
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "to_chat_id": to_chat_id,
            "disable_notification": disable_notification,
        })

    # ---------- ویرایش پیام ----------
    def edit_message_text(self, chat_id: str, message_id: str, text: str) -> Dict[str, Any]:
        return self._post("editMessageText", {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
        })

    def edit_message_keypad(
        self, chat_id: str, message_id: str, inline_keypad: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self._post("editMessageKeypad", {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_keypad": inline_keypad,
        })

    # ---------- حذف پیام ----------
    def delete_message(self, chat_id: str, message_id: str) -> Dict[str, Any]:
        return self._post("deleteMessage", {
            "chat_id": chat_id,
            "message_id": message_id,
        })

    # ---------- دستورات بات ----------
    def set_commands(self, commands: List[Dict[str, str]]) -> Dict[str, Any]:
        return self._post("setCommands", {"bot_commands": commands})

    # ---------- مدیریت Endpoint ----------
    def update_bot_endpoints(self, url: str, endpoint_type: str) -> Dict[str, Any]:
        return self._post("updateBotEndpoints", {
            "url": url,
            "type": endpoint_type,
        })

    # ---------- مدیریت Chat Keypad ----------
    def edit_chat_keypad(
        self,
        chat_id: str,
        keypad_type: str,
        keypad: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {"chat_id": chat_id, "chat_keypad_type": keypad_type}
        if keypad_type == ChatKeypadTypeEnum.NEW and keypad:
            payload["chat_keypad"] = keypad
        return self._post("editChatKeypad", payload)

    # ---------- مدیریت فایل ----------
    def get_file(self, file_id: str) -> Dict[str, Any]:
        return self._post("getFile", {"file_id": file_id})

    def send_file(
        self,
        chat_id: str,
        file_id: str,
        text: str = "",
        *,
        inline_keypad: Optional[Dict] = None,
        chat_keypad: Optional[Dict] = None,
        chat_keypad_type: Optional[str] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "chat_id": chat_id,
            "file_id": file_id,
            "text": text,
            "disable_notification": disable_notification,
        }
        self._attach_keypad(payload, inline_keypad, chat_keypad, chat_keypad_type, reply_to_message_id)
        return self._post("sendFile", payload)

    def request_send_file(self, file_type: str) -> Dict[str, Any]:
        return self._post("requestSendFile", {"type": file_type})

    def upload_file(self, upload_url: str, file_path: str) -> Dict[str, Any]:
        with open(file_path, "rb") as f:
            resp = requests.post(upload_url, files={"file": f})
        resp.raise_for_status()
        return resp.json()

    # ---------- مدیریت کاربران در گروه/کانال ----------
    def ban_chat_member(self, chat_id: str, user_id: str) -> Dict[str, Any]:
        return self._post("banChatMember", {
            "chat_id": chat_id,
            "user_id": user_id,
        })

    def unban_chat_member(self, chat_id: str, user_id: str) -> Dict[str, Any]:
        return self._post("unbanChatMember", {
            "chat_id": chat_id,
            "user_id": user_id,
        })

    # =================================================================
    #                    ابزارهای کمکی (Helpers)
    # =================================================================

    # ---------- ساخت دکمه و کیبورد ----------
    @staticmethod
    def create_button_simple(button_id: str, text: str) -> Dict[str, Any]:
        """ساخت یک دکمه ساده"""
        return {"id": button_id, "type": "Simple", "button_text": text}

    @staticmethod
    def create_button_link(button_id: str, text: str, url: str) -> Dict[str, Any]:
        """ساخت دکمه لینک (برای inline keypad)"""
        return {
            "id": button_id,
            "type": "Link",
            "button_text": text,
            "link_url": url,
        }

    @staticmethod
    def create_inline_keypad(rows: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        ساخت inline keypad از لیست ردیف‌ها.
        rows: [[btn1, btn2], [btn3]]
        """
        return {"rows": [{"buttons": row} for row in rows]}

    @staticmethod
    def create_chat_keypad(
        rows: List[List[Dict[str, Any]]],
        resize: bool = True,
        one_time: bool = False,
    ) -> Dict[str, Any]:
        """
        ساخت chat keypad (دکمه‌های پایین صفحه)
        """
        return {
            "rows": [{"buttons": row} for row in rows],
            "resize_keyboard": resize,
            "one_time_keyboard": one_time,
        }

    # ---------- متادیتا ----------
    @staticmethod
    def create_metadata_parts(parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"meta_data_parts": parts}

    @staticmethod
    def bold(from_index: int, length: int) -> Dict[str, Any]:
        return {"type": "Bold", "from_index": from_index, "length": length}

    @staticmethod
    def italic(from_index: int, length: int) -> Dict[str, Any]:
        return {"type": "Italic", "from_index": from_index, "length": length}

    @staticmethod
    def link(from_index: int, length: int, url: str) -> Dict[str, Any]:
        return {
            "type": "Link",
            "from_index": from_index,
            "length": length,
            "link_url": url,
        }

    @staticmethod
    def mention(from_index: int, length: int, user_id: str) -> Dict[str, Any]:
        return {
            "type": "MentionText",
            "from_index": from_index,
            "length": length,
            "mention_text_user_id": user_id,
        }

    # ---------- میانبرهای ارسال رسانه (آپلود + ارسال) ----------
    def send_image(
        self, chat_id: str, image_path: str, caption: str = "", **kwargs
    ) -> Dict[str, Any]:
        """آپلود و ارسال تصویر در یک مرحله"""
        upload_resp = self.request_send_file("Image")
        return self._upload_and_send(chat_id, upload_resp, image_path, caption, **kwargs)

    def send_video(
        self, chat_id: str, video_path: str, caption: str = "", **kwargs
    ) -> Dict[str, Any]:
        """آپلود و ارسال ویدیو"""
        upload_resp = self.request_send_file("Video")
        return self._upload_and_send(chat_id, upload_resp, video_path, caption, **kwargs)

    def send_voice(self, chat_id: str, voice_path: str, **kwargs) -> Dict[str, Any]:
        """آپلود و ارسال ویس"""
        upload_resp = self.request_send_file("Voice")
        return self._upload_and_send(chat_id, upload_resp, voice_path, "", **kwargs)

    def send_document(self, chat_id: str, file_path: str, caption: str = "", **kwargs) -> Dict[str, Any]:
        """آپلود و ارسال فایل (سند)"""
        upload_resp = self.request_send_file("File")
        return self._upload_and_send(chat_id, upload_resp, file_path, caption, **kwargs)

    def _upload_and_send(
        self, chat_id: str, upload_resp: Dict, file_path: str, text: str, **kwargs
    ) -> Dict[str, Any]:
        upload_url = upload_resp.get("upload_url")
        if not upload_url:
            raise Exception("upload_url not found in response")
        file_resp = self.upload_file(upload_url, file_path)
        file_id = file_resp.get("file_id")
        if not file_id:
            raise Exception("file_id not received after upload")
        return self.send_file(chat_id, file_id, text=text, **kwargs)

    # ---------- Long Polling (دریافت خودکار پیام‌ها) ----------
    def start_polling(
        self,
        callback: Callable[[Update], None],
        interval: int = 3,
        limit: int = 10,
    ):
        """
        اجرای مداوم دریافت رویدادها (Long Polling)
        callback: تابعی که یک شیء Update دریافت می‌کند.
        """
        offset_id: Optional[str] = None
        print("🤖 Robota polling started ...")
        while True:
            try:
                data = self.get_updates(limit=limit, offset_id=offset_id)
                updates = data.get("updates", [])
                for upd in updates:
                    callback(Update(**upd))
                offset_id = data.get("next_offset_id")
                time.sleep(interval)
            except KeyboardInterrupt:
                print("Polling stopped.")
                break
            except Exception as e:
                print(f"Error in polling: {e}")
                time.sleep(5)

    # ---------- Webhook ساده (نیازمند http.server) ----------
    def start_webhook(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        path: str = "/webhook",
        callback: Callable[[Dict[str, Any]], None] = None,
    ):
        """
        اجرای یک سرور ساده برای دریافت وب‌هوک.
        callback: تابعی که دیکشنری داده‌های دریافتی را دریافت می‌کند.
        """
        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
        except ImportError:
            raise ImportError("http.server not available")

        bot = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.path == path:
                    content_length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(content_length)
                    data = json.loads(body)
                    if callback:
                        callback(data)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"ok")
                else:
                    self.send_response(404)
                    self.end_headers()

        server = HTTPServer((host, port), Handler)
        print(f"🌐 Webhook server running on http://{host}:{port}{path}")
        server.serve_forever()
