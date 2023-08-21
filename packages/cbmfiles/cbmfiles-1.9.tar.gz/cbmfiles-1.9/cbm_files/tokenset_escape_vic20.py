from .tokensets import _token_set_register
from .tokenset_escape_pet2001 import TokenSet_EscapePet2001


_escape_vic20_tokens = (
    ("{wht}", 0x05),
    ("{dish}", 0x08),
    ("{ensh}", 0x09),
    ("{red}", 0x1C),
    ("{grn}", 0x1E),
    ("{blu}", 0x1F),
    ("{f1}", 0x85),
    ("{f3}", 0x86),
    ("{f5}", 0x87),
    ("{f7}", 0x88),
    ("{f2}", 0x89),
    ("{f4}", 0x8A),
    ("{f6}", 0x8B),
    ("{f8}", 0x8C),
    ("{blk}", 0x90),
    ("{pur}", 0x9C),
    ("{yel}", 0x9E),
    ("{cyn}", 0x9F)
    )


class TokenSet_EscapeVIC20(TokenSet_EscapePet2001):
    def __init__(self):
        super().__init__()
        self.add_tokens(_escape_vic20_tokens)


_token_set_register['escape-vic20'] = TokenSet_EscapeVIC20()
_token_set_register['escape-vic1001'] = TokenSet_EscapeVIC20()
