import pathlib
from gmail_api.utils import read_txt_file_from_zip_buffer
from display_configs import PREVIEW_DISPLAY_LENGTH


class WhatsAppChatDisplayHandler(object):

    def __init__(self, whatsapp_chat_text):
        self.whatsapp_chat_text = whatsapp_chat_text

    def get_short_version(self, preview_display_length):
        return self.whatsapp_chat_text[:preview_display_length]
