

import requests
import json
from typing import Optional, List, Dict, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass, field


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
    UPDATED_MESSAGE = "UpdatedMessage"
    NEW_MESSAGE = "NewMessage"
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
class ForwardedFrom:
    type_from: ForwardedFromEnum
    message_id: str
    from_chat_id: str
    from_sender_id: str

@dataclass
class MessageTextUpdate:
    message_id: str
    text: str

@dataclass
class Bot:
    bot_id: str
    bot_title: str
    username: str
    description: str = ""
    start_message: str = ""
    share_url: str = ""
    avatar: Optional[File] = None

@dataclass
class BotCommand:
    command: str        # بدون /
    description: str

@dataclass
class Sticker:
    sticker_id: str
    emoji_character: str
    file: Optional[File] = None

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
    options: List[str]
    poll_status: Optional[PollStatus] = None

@dataclass
class ButtonSelectionItem:
    text: str
    type: ButtonSelectionTypeEnum
    image_url: Optional[str] = None

@dataclass
class ButtonSelection:
    selection_id: str
    search_type: ButtonSelectionSearchEnum
    get_type: ButtonSelectionGetEnum
    items: List[ButtonSelectionItem]
    is_multi_selection: bool = False
    columns_count: str = "1"
    title: Optional[str] = None

@dataclass
class ButtonCalendar:
    type: ButtonCalendarTypeEnum
    default_value: Optional[str] = None
    min_year: Optional[str] = None
    max_year: Optional[str] = None
    title: Optional[str] = None

@dataclass
class ButtonNumberPicker:
    min_value: str
    max_value: str
    default_value: Optional[str] = None
    title: Optional[str] = None

@dataclass
class ButtonStringPicker:
    items: List[str]
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
    type: ButtonLocationTypeEnum
    default_pointer_location: Optional[Location] = None
    default_map_location: Optional[Location] = None
    title: Optional[str] = None

@dataclass
class AuxData:
    start_id: Optional[str] = None
    button_id: Optional[str] = None

@dataclass
class Button:
    id: str
    type: ButtonTypeEnum
    button_text: str
    button_selection: Optional[ButtonSelection] = None
    button_calendar: Optional[ButtonCalendar] = None
    button_number_picker: Optional[ButtonNumberPicker] = None
    button_string_picker: Optional[ButtonStringPicker] = None
    button_location: Optional[ButtonLocation] = None
    button_textbox: Optional[ButtonTextbox] = None
    link_url: Optional[str] = None   # برای نوع LINK

@dataclass
class KeypadRow:
    buttons: List[Button]

@dataclass
class Keypad:
    rows: List[KeypadRow]
    resize_keyboard: bool = False
    one_time_keyboard: bool = False

@dataclass
class MessageKeypadUpdate:
    message_id: str
    inline_keypad: Keypad

@dataclass
class Message:
    message_id: str
    time: int
    is_edited: bool
    sender_type: MessageSenderEnum
    sender_id: str
    text: Optional[str] = None
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
    meta_data_parts: List[MetadataPart]

@dataclass
class Chat:
    chat_id: str
    chat_type: ChatTypeEnum
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None


class RubikaBot:
    def __init__(self, token: str, base_url: str = "https://botapi.rubika.ir/v3"):
        self.token = token
        self.base_url = base_url
        self._last_update_offset = None   # برای auto_offset در get_updates

    def _request(self, method: str, params: Dict[str, Any] = None) -> Dict:
        if params is None:
            params = {}
        url = f"{self.base_url}/{self.token}/{method}"
        resp = requests.post(url, json=params)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "OK":
            raise Exception(f"API Error: {data}")
        return data.get("data", {})

    def _keypad_to_dict(self, keypad: Keypad) -> Dict:
        rows = []
        for row in keypad.rows:
            buttons = []
            for btn in row.buttons:
                btn_dict = {
                    "id": btn.id,
                    "type": btn.type.value if isinstance(btn.type, ButtonTypeEnum) else btn.type,
                    "button_text": btn.button_text
                }
                if btn.link_url:
                    btn_dict["link_url"] = btn.link_url
                buttons.append(btn_dict)
            rows.append({"buttons": buttons})
        result = {"rows": rows}
        if keypad.resize_keyboard:
            result["resize_keyboard"] = keypad.resize_keyboard
        if keypad.one_time_keyboard:
            result["one_time_keyboard"] = keypad.one_time_keyboard
        return result

    def get_me(self) -> Bot:
        data = self._request("getMe")
        bot_data = data.get("bot", {})
        avatar_data = bot_data.get("avatar")
        avatar = File(**avatar_data) if avatar_data else None
        return Bot(
            bot_id=bot_data.get("bot_id", ""),
            bot_title=bot_data.get("bot_title", ""),
            username=bot_data.get("username", ""),
            description=bot_data.get("description", ""),
            start_message=bot_data.get("start_message", ""),
            share_url=bot_data.get("share_url", ""),
            avatar=avatar
        )

    def send_message(
        self,
        chat_id: str,
        text: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Optional[Union[str, ChatKeypadTypeEnum]] = None,
        metadata: Optional[Metadata] = None
    ) -> Dict:
        params = {"chat_id": chat_id, "text": text}
        if chat_keypad:
            params["chat_keypad"] = self._keypad_to_dict(chat_keypad)
        if inline_keypad:
            params["inline_keypad"] = self._keypad_to_dict(inline_keypad)
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
            parts = []
            for p in metadata.meta_data_parts:
                part = {
                    "type": p.type.value if isinstance(p.type, MetadataTypeEnum) else p.type,
                    "from_index": p.from_index,
                    "length": p.length
                }
                if p.link_url:
                    part["link_url"] = p.link_url
                if p.mention_text_user_id:
                    part["mention_text_user_id"] = p.mention_text_user_id
                parts.append(part)
            params["metadata"] = {"meta_data_parts": parts}
        return self._request("sendMessage", params)

    def send_poll(self, chat_id: str, question: str, options: List[str]) -> Dict:
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
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Optional[Union[str, ChatKeypadTypeEnum]] = None
    ) -> Dict:
        params = {"chat_id": chat_id, "latitude": str(latitude), "longitude": str(longitude)}
        if chat_keypad:
            params["chat_keypad"] = self._keypad_to_dict(chat_keypad)
        if disable_notification:
            params["disable_notification"] = disable_notification
        if inline_keypad:
            params["inline_keypad"] = self._keypad_to_dict(inline_keypad)
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
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Optional[Union[str, ChatKeypadTypeEnum]] = None
    ) -> Dict:
        params = {
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number
        }
        if chat_keypad:
            params["chat_keypad"] = self._keypad_to_dict(chat_keypad)
        if disable_notification:
            params["disable_notification"] = disable_notification
        if inline_keypad:
            params["inline_keypad"] = self._keypad_to_dict(inline_keypad)
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
        chat_data = data.get("chat", {})
        return Chat(
            chat_id=chat_data.get("chat_id", ""),
            chat_type=ChatTypeEnum(chat_data.get("chat_type", "User")),
            user_id=chat_data.get("user_id"),
            first_name=chat_data.get("first_name"),
            last_name=chat_data.get("last_name"),
            title=chat_data.get("title"),
            username=chat_data.get("username")
        )

    def get_updates(self, limit: int = 100, offset_id: Optional[str] = None, auto_offset: bool = True) -> Tuple[List[Update], Optional[str]]:
        params = {"limit": limit}
        if auto_offset and self._last_update_offset:
            params["offset_id"] = self._last_update_offset
        elif offset_id:
            params["offset_id"] = offset_id
        data = self._request("getUpdates", params)
        updates_data = data.get("updates", [])
        updates = []
        for item in updates_data:
            update = Update(
                type=UpdateTypeEnum(item.get("type", "NewMessage")),
                chat_id=item.get("chat_id", ""),
                removed_message_id=item.get("removed_message_id")
            )
            # new_message
            if "new_message" in item:
                msg = item["new_message"]
                aux = None
                if msg.get("aux_data"):
                    aux = AuxData(**msg["aux_data"])
                update.new_message = Message(
                    message_id=msg.get("message_id", ""),
                    time=int(msg.get("time", 0)),
                    is_edited=msg.get("is_edited", False),
                    sender_type=MessageSenderEnum(msg.get("sender_type", "User")),
                    sender_id=msg.get("sender_id", ""),
                    text=msg.get("text"),
                    aux_data=aux,
                    reply_to_message_id=msg.get("reply_to_message_id")
                )
            # updated_message مشابه
            if "updated_message" in item:
                msg = item["updated_message"]
                aux = None
                if msg.get("aux_data"):
                    aux = AuxData(**msg["aux_data"])
                update.updated_message = Message(
                    message_id=msg.get("message_id", ""),
                    time=int(msg.get("time", 0)),
                    is_edited=msg.get("is_edited", False),
                    sender_type=MessageSenderEnum(msg.get("sender_type", "User")),
                    sender_id=msg.get("sender_id", ""),
                    text=msg.get("text"),
                    aux_data=aux,
                    reply_to_message_id=msg.get("reply_to_message_id")
                )
            updates.append(update)
        next_offset = data.get("next_offset_id")
        if auto_offset and next_offset:
            self._last_update_offset = next_offset
        return updates, next_offset

    def forward_message(
        self,
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        disable_notification: bool = False
    ) -> Dict:
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

    def edit_message_keypad(self, chat_id: str, message_id: str, inline_keypad: Optional[Keypad] = None) -> Dict:
        params = {"chat_id": chat_id, "message_id": message_id}
        if inline_keypad:
            params["inline_keypad"] = self._keypad_to_dict(inline_keypad)
        return self._request("editMessageKeypad", params)

    def delete_message(self, chat_id: str, message_id: str) -> Dict:
        return self._request("deleteMessage", {
            "chat_id": chat_id,
            "message_id": message_id
        })

    def set_commands(self, commands: List[BotCommand]) -> Dict:
        bot_commands = [{"command": c.command, "description": c.description} for c in commands]
        return self._request("setCommands", {"bot_commands": bot_commands})

    def update_bot_endpoints(self, url: str, endpoint_type: Union[str, UpdateEndpointTypeEnum]) -> Dict:
        typ = endpoint_type.value if isinstance(endpoint_type, UpdateEndpointTypeEnum) else endpoint_type
        return self._request("updateBotEndpoints", {"url": url, "type": typ})

    def set_chat_keypad(self, chat_id: str, keypad: Keypad) -> Dict:
        return self._request("editChatKeypad", {
            "chat_id": chat_id,
            "chat_keypad_type": "New",
            "chat_keypad": self._keypad_to_dict(keypad)
        })

    def remove_chat_keypad(self, chat_id: str) -> Dict:
        return self._request("editChatKeypad", {
            "chat_id": chat_id,
            "chat_keypad_type": "Remove"
        })

    def get_file(self, file_id: str) -> str:
        data = self._request("getFile", {"file_id": file_id})
        return data.get("download_url", "")

    def send_file(
        self,
        chat_id: str,
        file_id: str,
        text: Optional[str] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        chat_keypad_type: Optional[Union[str, ChatKeypadTypeEnum]] = None
    ) -> Dict:
        params = {"chat_id": chat_id, "file_id": file_id}
        if text:
            params["text"] = text
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if disable_notification:
            params["disable_notification"] = disable_notification
        if chat_keypad:
            params["chat_keypad"] = self._keypad_to_dict(chat_keypad)
        if inline_keypad:
            params["inline_keypad"] = self._keypad_to_dict(inline_keypad)
        if chat_keypad_type:
            if isinstance(chat_keypad_type, ChatKeypadTypeEnum):
                params["chat_keypad_type"] = chat_keypad_type.value
            else:
                params["chat_keypad_type"] = chat_keypad_type
        return self._request("sendFile", params)

    def request_send_file(self, file_type: Union[str, FileTypeEnum]) -> str:
        typ = file_type.value if isinstance(file_type, FileTypeEnum) else file_type
        data = self._request("requestSendFile", {"type": typ})
        return data.get("upload_url", "")

    def upload_file_to_url(self, upload_url: str, file_path: str) -> str:
        with open(file_path, "rb") as f:
            files = {"file": f}
            resp = requests.post(upload_url, files=files)
            resp.raise_for_status()
            result = resp.json()
            return result.get("file_id", "")

    def upload_and_send_file(
        self,
        chat_id: str,
        file_path: str,
        file_type: Union[str, FileTypeEnum],
        caption: Optional[str] = None,
        **kwargs
    ) -> Dict:
        upload_url = self.request_send_file(file_type)
        file_id = self.upload_file_to_url(upload_url, file_path)
        return self.send_file(chat_id=chat_id, file_id=file_id, text=caption, **kwargs)

    def ban_chat_member(self, chat_id: str, user_id: str) -> Dict:
        return self._request("banChatMember", {"chat_id": chat_id, "user_id": user_id})

    def unban_chat_member(self, chat_id: str, user_id: str) -> Dict:
        return self._request("unbanChatMember", {"chat_id": chat_id, "user_id": user_id})

    @staticmethod
    def parse_update(request_body: Union[str, bytes, Dict]) -> Optional[Update]:
        try:
            if isinstance(request_body, (str, bytes)):
                data = json.loads(request_body)
            else:
                data = request_body
            update_data = data.get("update", {})
            upd = Update(
                type=UpdateTypeEnum(update_data.get("type", "NewMessage")),
                chat_id=update_data.get("chat_id", ""),
                removed_message_id=update_data.get("removed_message_id")
            )
            if "new_message" in update_data:
                msg = update_data["new_message"]
                aux = None
                if msg.get("aux_data"):
                    aux = AuxData(**msg["aux_data"])
                upd.new_message = Message(
                    message_id=msg.get("message_id", ""),
                    time=int(msg.get("time", 0)),
                    is_edited=msg.get("is_edited", False),
                    sender_type=MessageSenderEnum(msg.get("sender_type", "User")),
                    sender_id=msg.get("sender_id", ""),
                    text=msg.get("text"),
                    aux_data=aux,
                    reply_to_message_id=msg.get("reply_to_message_id")
                )
            return upd
        except Exception:
            return None

    @staticmethod
    def parse_inline_message(request_body: Union[str, bytes, Dict]) -> Optional[InlineMessage]:
        try:
            if isinstance(request_body, (str, bytes)):
                data = json.loads(request_body)
            else:
                data = request_body
            inline = data.get("inline_message", {})
            aux = None
            if inline.get("aux_data"):
                aux = AuxData(**inline["aux_data"])
            return InlineMessage(
                sender_id=inline.get("sender_id", ""),
                message_id=inline.get("message_id", ""),
                chat_id=inline.get("chat_id", ""),
                text=inline.get("text"),
                file=None,  
                location=None,
                aux_data=aux
            )
        except Exception:
            return None

    def start_polling(self, callback, interval: int = 1, limit: int = 100):
        import time
        while True:
            try:
                updates, _ = self.get_updates(limit=limit, auto_offset=True)
                for update in updates:
                    callback(update)
                time.sleep(interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Polling error: {e}")
                time.sleep(5)



class RubikaHelpers:
    @staticmethod
    def simple_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.SIMPLE, button_text=button_text)

    @staticmethod
    def link_button(button_id: str, button_text: str, link_url: str) -> Button:
        btn = Button(id=button_id, type=ButtonTypeEnum.LINK, button_text=button_text)
        btn.link_url = link_url
        return btn

    @staticmethod
    def selection_button(button_id: str, button_text: str, selection: ButtonSelection) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.SELECTION, button_text=button_text, button_selection=selection)

    @staticmethod
    def number_picker_button(button_id: str, button_text: str, min_val: int, max_val: int, default_val: Optional[int] = None, title: Optional[str] = None) -> Button:
        picker = ButtonNumberPicker(min_value=str(min_val), max_value=str(max_val), default_value=str(default_val) if default_val else None, title=title)
        return Button(id=button_id, type=ButtonTypeEnum.NUMBER_PICKER, button_text=button_text, button_number_picker=picker)

    @staticmethod
    def calendar_button(button_id: str, button_text: str, cal_type: Union[str, ButtonCalendarTypeEnum] = ButtonCalendarTypeEnum.PERSIAN, min_year: Optional[str] = None, max_year: Optional[str] = None, default_value: Optional[str] = None, title: Optional[str] = None) -> Button:
        typ = cal_type.value if isinstance(cal_type, ButtonCalendarTypeEnum) else cal_type
        calendar = ButtonCalendar(type=ButtonCalendarTypeEnum(typ), default_value=default_value, min_year=min_year, max_year=max_year, title=title)
        return Button(id=button_id, type=ButtonTypeEnum.CALENDAR, button_text=button_text, button_calendar=calendar)

    @staticmethod
    def textbox_button(button_id: str, button_text: str, type_line: Union[str, ButtonTextboxTypeLineEnum] = ButtonTextboxTypeLineEnum.SINGLE, type_keypad: Union[str, ButtonTextboxTypeKeypadEnum] = ButtonTextboxTypeKeypadEnum.STRING, placeholder: Optional[str] = None, title: Optional[str] = None, default_value: Optional[str] = None) -> Button:
        line = type_line.value if isinstance(type_line, ButtonTextboxTypeLineEnum) else type_line
        kp = type_keypad.value if isinstance(type_keypad, ButtonTextboxTypeKeypadEnum) else type_keypad
        tb = ButtonTextbox(type_line=ButtonTextboxTypeLineEnum(line), type_keypad=ButtonTextboxTypeKeypadEnum(kp), place_holder=placeholder, title=title, default_value=default_value)
        return Button(id=button_id, type=ButtonTypeEnum.TEXTBOX, button_text=button_text, button_textbox=tb)

    @staticmethod
    def camera_image_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.CAMERA_IMAGE, button_text=button_text)

    @staticmethod
    def gallery_image_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.GALLERY_IMAGE, button_text=button_text)

    @staticmethod
    def camera_video_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.CAMERA_VIDEO, button_text=button_text)

    @staticmethod
    def gallery_video_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.GALLERY_VIDEO, button_text=button_text)

    @staticmethod
    def file_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.FILE, button_text=button_text)

    @staticmethod
    def audio_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.AUDIO, button_text=button_text)

    @staticmethod
    def record_audio_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.RECORD_AUDIO, button_text=button_text)

    @staticmethod
    def ask_phone_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.ASK_MY_PHONE_NUMBER, button_text=button_text)

    @staticmethod
    def ask_location_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.ASK_MY_LOCATION, button_text=button_text)

    @staticmethod
    def barcode_button(button_id: str, button_text: str) -> Button:
        return Button(id=button_id, type=ButtonTypeEnum.BARCODE, button_text=button_text)

    @staticmethod
    def row(*buttons: Button) -> KeypadRow:
        return KeypadRow(buttons=list(buttons))

    @staticmethod
    def keypad(rows: List[KeypadRow], resize_keyboard: bool = False, one_time_keyboard: bool = False) -> Keypad:
        return Keypad(rows=rows, resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)

    @staticmethod
    def metadata_part(meta_type: Union[str, MetadataTypeEnum], from_index: int, length: int, link_url: Optional[str] = None, mention_user_id: Optional[str] = None) -> MetadataPart:
        typ = meta_type.value if isinstance(meta_type, MetadataTypeEnum) else meta_type
        return MetadataPart(type=MetadataTypeEnum(typ), from_index=from_index, length=length, link_url=link_url, mention_text_user_id=mention_user_id)

    @staticmethod
    def metadata(parts: List[MetadataPart]) -> Metadata:
        return Metadata(meta_data_parts=parts)


__all__ = [
    "RubikaBot",
    "RubikaHelpers",
    # Enums
    "ChatTypeEnum", "FileTypeEnum", "ForwardedFromEnum", "PollStatusEnum",
    "ButtonSelectionTypeEnum", "ButtonSelectionSearchEnum", "ButtonSelectionGetEnum",
    "ButtonCalendarTypeEnum", "ButtonTextboxTypeKeypadEnum", "ButtonTextboxTypeLineEnum",
    "ButtonLocationTypeEnum", "MessageSenderEnum", "UpdateTypeEnum",
    "ChatKeypadTypeEnum", "UpdateEndpointTypeEnum", "MetadataTypeEnum", "ButtonTypeEnum",
    # Models
    "Location", "File", "ForwardedFrom", "MessageTextUpdate", "Bot", "BotCommand",
    "Sticker", "ContactMessage", "PollStatus", "Poll", "ButtonSelectionItem",
    "ButtonSelection", "ButtonCalendar", "ButtonNumberPicker", "ButtonStringPicker",
    "ButtonTextbox", "ButtonLocation", "AuxData", "Button", "KeypadRow", "Keypad",
    "MessageKeypadUpdate", "Message", "Update", "InlineMessage", "MetadataPart",
    "Metadata", "Chat"
]
