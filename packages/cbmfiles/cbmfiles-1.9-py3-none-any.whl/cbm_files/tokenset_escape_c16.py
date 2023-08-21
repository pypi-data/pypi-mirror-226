from .tokensets import _token_set_register
from .tokenset_escape_vic20 import TokenSet_EscapeVIC20


_escape_c16_tokens = (
    ("{orng}", 0x81),
    ("{flon}", 0x82),
    ("{flof}", 0x84),
    ("{help}", 0x8C),
    ("{brn}", 0x95),
    ("{ylgn}", 0x96),
    ("{pink}", 0x97),
    ("{blgr}", 0x98),
    ("{lblu}", 0x99),
    ("{dblu}", 0x9A),
    ("{lgrn}", 0x9B)
    )


class TokenSet_EscapeC16(TokenSet_EscapeVIC20):
    def __init__(self):
        super().__init__()
        self.add_tokens(_escape_c16_tokens)


_token_set_register['escape-c16'] = TokenSet_EscapeC16()
