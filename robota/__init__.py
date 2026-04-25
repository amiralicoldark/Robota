# robota/__init__.py
import requests
import json
from typing import Optional, List, Dict, Any, Union, Callable
from enum import Enum
from dataclasses import dataclass

# =========================== Enums ===========================
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
    OPEN = "Open"
    CLOSED = "Closed"

class ButtonSelectionTypeEnum(str, Enum):
    TEXT_ONLY = "TextOnly"
    TEXT_IMG_THU = "TextImgThu"
    TEXT_IMG_BIG = "TextImgBig"

class ButtonSelectionSearchEnum(str, Enum):
    NONE = "None"
    LOCAL = "Local"
    API = "Api"

class ButtonSelectionGetEnum(str, Enum):
    LOCAL = "Local"
    API = "Api"

class ButtonCalendarTypeEnum(str, Enum):
    PERSIAN = "DatePersian"
    GREGORIAN = "DateGregorian"

class ButtonTextboxTypeKeypadEnum(str, Enum):
    STRING = "String"
    NUMBER = "Number"

class ButtonTextboxTypeLineEnum(str, Enum):
    SINGLE = "SingleLine"
    MULTI = "MultiLine"

class ButtonLocationTypeEnum(str, Enum):
    PICKER = "Picker"
    VIEW = "View"

class MessageSenderEnum(str, Enum):
    USER = "User"
    BOT = "Bot"

class UpdateTypeEnum(str, Enum):
    NEW_MESSAGE = "NewMessage"
    EDITED_MESSAGE = "EditedMessage"
    REMOVED_MESSAGE = "RemovedMessage"
    STARTED_BOT = "StartedBot"
    STOPPED_BOT = "StoppedBot"

class ChatKeypadTypeEnum(str, Enum):
    NONE = "None"
    NEW = "New"
    REMOVE = "Remove"

class UpdateEndpointTypeEnum(str, Enum):
    RECEIVE_UPDATE = "ReceiveUpdate"
    RECEIVE_INLINE_MESSAGE = "ReceiveInlineMessage"
    RECEIVE_QUERY = "ReceiveQuery"
    GET_SELECTION_ITEM = "GetSelectionItem"
    SEARCH_SELECTION_ITEMS = "SearchSelectionItems"

class MetadataTypeEnum(str, Enum):
    BOLD = "Bold"
    ITALIC = "Italic"
    MONO = "Mono"
    UNDERLINE = "Underline"
    STRIKE = "Strike"
    SPOILER = "Spoiler"
    LINK = "Link"
    MENTION_TEXT = "MentionText"
    PRE = "Pre"
    QUOTE = "Quote"

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

# =========================== Data Models ===========================
@dataclass
class Location:
    latitude: str
    longitude: str

@dataclass
class File:
    file_id: str
    file_name: str
    size: str

@dataclass
class Bot:
    bot_id: str
    bot_title: str
    avatar: Optional[File] = None
    description: str = ""
    username: str = ""
    start_message: str = ""
    share_url: str = ""

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
class Message:
    message_id: str
    time: int
    is_edited: bool
    sender_type: MessageSenderEnum
    sender_id: str
    text: Optional[str] = None
    file: Optional[File] = None
    location: Optional[Location] = None
    reply_to_message_id: Optional[str] = None
    aux_data: Optional[Dict] = None

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
    aux_data: Optional[Dict] = None

# =========================== Main Bot Class ===========================
class RubikaBot:
    def __init__(self, token: str, base_url: str = "https://botapi.rubika.ir/v3"):
        self.token = token
        self.base_url = base_url
        self._last_update_offset = None

    def _request(self, method: str, params: Dict[str, Any] = None) -> Dict:
        if params is None:
            params = {}
        url = f"{self.base_url}/{self.token}/{method}"
        resp = requests.post(url, json=params)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") and data["status"] != "OK":
            raise Exception(f"API Error: {data}")
        return data

    # ---------- Methods ----------
    def get_me(self) -> Bot:
        data = self._request("getMe")
        bot_data = data.get("bot", {})
        return Bot(
            bot_id=bot_data.get("bot_id", ""),
            bot_title=bot_data.get("bot_title", ""),
            description=bot_data.get("description", ""),
            username=bot_data.get("username", ""),
            start_message=bot_data.get("start_message", ""),
            share_url=bot_data.get("share_url", "")
        )

    def send_message(
        self,
        chat_id: str,
        text: str,
        chat_keypad: Dict = None,
        inline_keypad: Dict = None,
        disable_notification: bool = False,
        reply_to_message_id: str = None,
        chat_keypad_type: Union[str, ChatKeypadTypeEnum] = None,
        metadata: Dict = None
    ) -> Dict:
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
            if isinstance(chat_keypad_type, ChatKeypadTypeEnum):
                params["chat_keypad_type"] = chat_keypad_type.value
            else:
                params["chat_keypad_type"] = chat_keypad_type
        if metadata:
            params["metadata"] = metadata
        return self._request("sendMessage", params)

    def send_poll(self, chat_id: str, question: str, options: List[str]) -> Dict:
        return self._request("sendPoll", {"chat_id": chat_id, "question": question, "options": options})

    def send_location(
        self,
        chat_id: str,
        latitude: Union[str, float],
        longitude: Union[str, float],
        chat_keypad: Dict = None,
        disable_notification: bool = False,
        inline_keypad: Dict = None,
        reply_to_message_id: str = None,
        chat_keypad_type: Union[str, ChatKeypadTypeEnum] = None
    ) -> Dict:
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
            if isinstance(chat_keypad_type, ChatKeypadTypeEnum):
                params["chat_keypad_type"] = chat_keypad_type.value
            else:
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
        chat_keypad_type: Union[str, ChatKeypadTypeEnum] = None
    ) -> Dict:
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
            if isinstance(chat_keypad_type, ChatKeypadTypeEnum):
                params["chat_keypad_type"] = chat_keypad_type.value
            else:
                params["chat_keypad_type"] = chat_keypad_type
        return self._request("sendContact", params)

    def get_chat(self, chat_id: str) -> Chat:
        data = self._request("getChat", {"chat_id": chat_id})
        chat = data.get("chat", {})
        return Chat(
            chat_id=chat.get("chat_id", ""),
            chat_type=ChatTypeEnum(chat.get("chat_type", "User")),
            user_id=chat.get("user_id"),
            first_name=chat.get("first_name"),
            last_name=chat.get("last_name"),
            title=chat.get("title"),
            username=chat.get("username")
        )

    def get_updates(self, limit: int = 100, auto_offset: bool = True) -> List[Update]:
        params = {"limit": limit}
        if self._last_update_offset and auto_offset:
            params["offset_id"] = self._last_update_offset
        data = self._request("getUpdates", params)
        updates = []
        for item in data.get("updates", []):
            upd = Update(
                type=UpdateTypeEnum(item.get("type", "NewMessage")),
                chat_id=item.get("chat_id", ""),
                removed_message_id=item.get("removed_message_id")
            )
            if item.get("new_message"):
                msg = item["new_message"]
                upd.new_message = Message(
                    message_id=msg.get("message_id", ""),
                    time=msg.get("time", 0),
                    is_edited=msg.get("is_edited", False),
                    sender_type=MessageSenderEnum(msg.get("sender_type", "User")),
                    sender_id=msg.get("sender_id", ""),
                    text=msg.get("text"),
                    reply_to_message_id=msg.get("reply_to_message_id")
                )
            if item.get("updated_message"):
                # similar to new_message, omitted for brevity
                pass
            updates.append(upd)
        if auto_offset and data.get("next_offset_id"):
            self._last_update_offset = data["next_offset_id"]
        return updates

    def forward_message(self, from_chat_id: str, message_id: str, to_chat_id: str, disable_notification: bool = False) -> Dict:
        return self._request("forwardMessage", {
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "to_chat_id": to_chat_id,
            "disable_notification": disable_notification
        })

    def edit_message_text(self, chat_id: str, message_id: str, text: str) -> Dict:
        return self._request("editMessageText", {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        })

    def edit_message_keypad(self, chat_id: str, message_id: str, inline_keypad: Dict) -> Dict:
        return self._request("editMessageKeypad", {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_keypad": inline_keypad
        })

    def delete_message(self, chat_id: str, message_id: str) -> Dict:
        return self._request("deleteMessage", {
            "chat_id": chat_id,
            "message_id": message_id
        })

    def set_commands(self, bot_commands: List[Dict[str, str]]) -> Dict:
        return self._request("setCommands", {"bot_commands": bot_commands})

    def update_bot_endpoints(self, url: str, type_: Union[str, UpdateEndpointTypeEnum]) -> Dict:
        typ = type_.value if isinstance(type_, UpdateEndpointTypeEnum) else type_
        return self._request("updateBotEndpoints", {"url": url, "type": typ})

    def edit_chat_keypad(self, chat_id: str, chat_keypad: Dict = None, chat_keypad_type: Union[str, ChatKeypadTypeEnum] = ChatKeypadTypeEnum.REMOVE) -> Dict:
        typ = chat_keypad_type.value if isinstance(chat_keypad_type, ChatKeypadTypeEnum) else chat_keypad_type
        params = {"chat_id": chat_id, "chat_keypad_type": typ}
        if chat_keypad:
            params["chat_keypad"] = chat_keypad
        return self._request("editChatKeypad", params)

    def get_file(self, file_id: str) -> str:
        data = self._request("getFile", {"file_id": file_id})
        return data.get("download_url", "")

    def send_file(
        self,
        chat_id: str,
        file_id: str,
        text: str = None,
        reply_to_message_id: str = None,
        disable_notification: bool = False,
        chat_keypad: Dict = None,
        inline_keypad: Dict = None,
        chat_keypad_type: Union[str, ChatKeypadTypeEnum] = None
    ) -> Dict:
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
            if isinstance(chat_keypad_type, ChatKeypadTypeEnum):
                params["chat_keypad_type"] = chat_keypad_type.value
            else:
                params["chat_keypad_type"] = chat_keypad_type
        return self._request("sendFile", params)

    def request_send_file(self, type_: Union[str, FileTypeEnum]) -> str:
        typ = type_.value if isinstance(type_, FileTypeEnum) else type_
        data = self._request("requestSendFile", {"type": typ})
        return data.get("upload_url", "")

    def upload_file_to_url(self, upload_url: str, file_path: str) -> str:
        with open(file_path, "rb") as f:
            files = {"file": f}
            resp = requests.post(upload_url, files=files)
            resp.raise_for_status()
            result = resp.json()
            return result.get("file_id", "")

    def upload_and_send_file(self, chat_id: str, file_path: str, file_type: Union[str, FileTypeEnum], caption: str = None, **kwargs) -> Dict:
        upload_url = self.request_send_file(file_type)
        file_id = self.upload_file_to_url(upload_url, file_path)
        return self.send_file(chat_id=chat_id, file_id=file_id, text=caption, **kwargs)

    def ban_chat_member(self, chat_id: str, user_id: str) -> Dict:
        return self._request("banChatMember", {"chat_id": chat_id, "user_id": user_id})

    def unban_chat_member(self, chat_id: str, user_id: str) -> Dict:
        return self._request("unbanChatMember", {"chat_id": chat_id, "user_id": user_id})

    @staticmethod
    def parse_update(request_body: Union[str, bytes, Dict]) -> Update:
        if isinstance(request_body, (str, bytes)):
            data = json.loads(request_body)
        else:
            data = request_body
        update_data = data.get("update", {})
        return Update(
            type=UpdateTypeEnum(update_data.get("type", "NewMessage")),
            chat_id=update_data.get("chat_id", ""),
            removed_message_id=update_data.get("removed_message_id")
        )

# =========================== Helpers for keypads and metadata ===========================
class RubikaHelpers:
    @staticmethod
    def simple_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.SIMPLE.value, "button_text": button_text}

    @staticmethod
    def link_button(button_id: str, button_text: str, link_url: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.LINK.value, "button_text": button_text, "link_url": link_url}

    @staticmethod
    def selection_button(button_id: str, button_text: str, selection_data: Dict) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.SELECTION.value, "button_text": button_text, "button_selection": selection_data}

    @staticmethod
    def number_picker_button(button_id: str, button_text: str, min_val: int, max_val: int, default_val: int = None, title: str = None) -> Dict:
        picker = {"min_value": str(min_val), "max_value": str(max_val)}
        if default_val is not None:
            picker["default_value"] = str(default_val)
        if title:
            picker["title"] = title
        return {"id": button_id, "type": ButtonTypeEnum.NUMBER_PICKER.value, "button_text": button_text, "button_number_picker": picker}

    @staticmethod
    def location_button(button_id: str, button_text: str, type_: Union[str, ButtonLocationTypeEnum] = ButtonLocationTypeEnum.PICKER, title: str = None) -> Dict:
        loc = {"type": type_.value if isinstance(type_, ButtonLocationTypeEnum) else type_}
        if title:
            loc["title"] = title
        return {"id": button_id, "type": ButtonTypeEnum.LOCATION.value, "button_text": button_text, "button_location": loc}

    @staticmethod
    def textbox_button(button_id: str, button_text: str, type_line: Union[str, ButtonTextboxTypeLineEnum] = ButtonTextboxTypeLineEnum.SINGLE,
                       type_keypad: Union[str, ButtonTextboxTypeKeypadEnum] = ButtonTextboxTypeKeypadEnum.STRING,
                       placeholder: str = None, title: str = None, default_value: str = None) -> Dict:
        tb = {
            "type_line": type_line.value if isinstance(type_line, ButtonTextboxTypeLineEnum) else type_line,
            "type_keypad": type_keypad.value if isinstance(type_keypad, ButtonTextboxTypeKeypadEnum) else type_keypad
        }
        if placeholder:
            tb["place_holder"] = placeholder
        if title:
            tb["title"] = title
        if default_value:
            tb["default_value"] = default_value
        return {"id": button_id, "type": ButtonTypeEnum.TEXTBOX.value, "button_text": button_text, "button_textbox": tb}

    @staticmethod
    def camera_image_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.CAMERA_IMAGE.value, "button_text": button_text}

    @staticmethod
    def gallery_image_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.GALLERY_IMAGE.value, "button_text": button_text}

    @staticmethod
    def camera_video_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.CAMERA_VIDEO.value, "button_text": button_text}

    @staticmethod
    def gallery_video_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.GALLERY_VIDEO.value, "button_text": button_text}

    @staticmethod
    def file_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.FILE.value, "button_text": button_text}

    @staticmethod
    def audio_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.AUDIO.value, "button_text": button_text}

    @staticmethod
    def record_audio_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.RECORD_AUDIO.value, "button_text": button_text}

    @staticmethod
    def ask_phone_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.ASK_MY_PHONE_NUMBER.value, "button_text": button_text}

    @staticmethod
    def ask_location_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.ASK_MY_LOCATION.value, "button_text": button_text}

    @staticmethod
    def barcode_button(button_id: str, button_text: str) -> Dict:
        return {"id": button_id, "type": ButtonTypeEnum.BARCODE.value, "button_text": button_text}

    @staticmethod
    def calendar_button(button_id: str, button_text: str, calendar_type: Union[str, ButtonCalendarTypeEnum] = ButtonCalendarTypeEnum.PERSIAN,
                        min_year: str = None, max_year: str = None, default_value: str = None, title: str = None) -> Dict:
        cal = {"type": calendar_type.value if isinstance(calendar_type, ButtonCalendarTypeEnum) else calendar_type}
        if min_year:
            cal["min_year"] = min_year
        if max_year:
            cal["max_year"] = max_year
        if default_value:
            cal["default_value"] = default_value
        if title:
            cal["title"] = title
        return {"id": button_id, "type": ButtonTypeEnum.CALENDAR.value, "button_text": button_text, "button_calendar": cal}

    @staticmethod
    def string_picker_button(button_id: str, button_text: str, items: List[str], default_value: str = None, title: str = None) -> Dict:
        picker = {"items": items}
        if default_value:
            picker["default_value"] = default_value
        if title:
            picker["title"] = title
        return {"id": button_id, "type": ButtonTypeEnum.STRING_PICKER.value, "button_text": button_text, "button_string_picker": picker}

    @staticmethod
    def row(*buttons) -> Dict:
        return {"buttons": list(buttons)}

    @staticmethod
    def keypad(rows: List[Dict], resize_keyboard: bool = False, one_time_keyboard: bool = False) -> Dict:
        return {"rows": rows, "resize_keyboard": resize_keyboard, "one_time_keyboard": one_time_keyboard}

    @staticmethod
    def metadata_part(type_: Union[str, MetadataTypeEnum], from_index: int, length: int, link_url: str = None, mention_user_id: str = None) -> Dict:
        typ = type_.value if isinstance(type_, MetadataTypeEnum) else type_
        part = {"type": typ, "from_index": from_index, "length": length}
        if typ == "Link" and link_url:
            part["link_url"] = link_url
        if typ == "MentionText" and mention_user_id:
            part["mention_text_user_id"] = mention_user_id
        return part

    @staticmethod
    def metadata(parts: List[Dict]) -> Dict:
        return {"meta_data_parts": parts}
