from .tokensets import TokenSet, _token_set_register


_basic_v2_tokens = (
    ("END", 0x80),
    ("FOR", 0x81),
    ("NEXT", 0x82),
    ("DATA", 0x83),
    ("INPUT#", 0x84),
    ("INPUT", 0x85),
    ("DIM", 0x86),
    ("READ", 0x87),
    ("LET", 0x88),
    ("GOTO", 0x89),
    ("RUN", 0x8A),
    ("IF", 0x8B),
    ("RESTORE", 0x8C),
    ("GOSUB", 0x8D),
    ("RETURN", 0x8E),
    ("REM", 0x8F),
    ("STOP", 0x90),
    ("ON", 0x91),
    ("WAIT", 0x92),
    ("LOAD", 0x93),
    ("SAVE", 0x94),
    ("VERIFY", 0x95),
    ("DEF", 0x96),
    ("POKE", 0x97),
    ("PRINT#", 0x98),
    ("PRINT", 0x99),
    ("CONT", 0x9A),
    ("LIST", 0x9B),
    ("CLR", 0x9C),
    ("CMD", 0x9D),
    ("SYS", 0x9E),
    ("OPEN", 0x9F),
    ("CLOSE", 0xA0),
    ("GET", 0xA1),
    ("NEW", 0xA2),
    ("TAB(", 0xA3),
    ("TO", 0xA4),
    ("FN", 0xA5),
    ("SPC(", 0xA6),
    ("THEN", 0xA7),
    ("NOT", 0xA8),
    ("STEP", 0xA9),
    ("+", 0xAA),
    ("-", 0xAB),
    ("*", 0xAC),
    ("/", 0xAD),
    ("↑", 0xAE),
    ("^", 0xAE),
    ("AND", 0xAF),
    ("OR", 0xB0),
    (">", 0xB1),
    ("=", 0xB2),
    ("<", 0xB3),
    ("SGN", 0xB4),
    ("INT", 0xB5),
    ("ABS", 0xB6),
    ("USR", 0xB7),
    ("FRE", 0xB8),
    ("POS", 0xB9),
    ("SQR", 0xBA),
    ("RND", 0xBB),
    ("LOG", 0xBC),
    ("EXP", 0xBD),
    ("COS", 0xBE),
    ("SIN", 0xBF),
    ("TAN", 0xC0),
    ("ATN", 0xC1),
    ("PEEK", 0xC2),
    ("LEN", 0xC3),
    ("STR$", 0xC4),
    ("VAL", 0xC5),
    ("ASC", 0xC6),
    ("CHR$", 0xC7),
    ("LEFT$", 0xC8),
    ("RIGHT$", 0xC9),
    ("MID$", 0xCA),
    ("GO", 0xCB),
    ("~", 0xFF)
    )


class TokenSet_BASICv2(TokenSet):
    def __init__(self):
        super().__init__()
        self.add_tokens(_basic_v2_tokens)
        self.skip_tokenize_next_statement = 0x83
        self.skip_tokenize_eol = 0x8F
        self.ren_tokens = (0x89, 0x8A, 0x8D, 0x9B, 0XA7)

    def renumber_split(self, line_encoded):
        """Yield a sequence of substrings and integer line numbers."""
        next_part = bytearray()
        in_quote = False
        last_token = None
        val = None

        for b in line_encoded:
            if val is not None:
                # processing a line number
                if b >= ord('0') and b <= ord('9'):
                    val = val*10+(b-ord('0'))
                    continue
                else:
                    # line number complete
                    yield val
                    val = None

            if not in_quote:
                if b >= ord('0') and b <= ord('9') and last_token in self.ren_tokens:
                    # new line number
                    yield next_part
                    next_part = bytearray()
                    val = b-ord('0')
                    continue

                if b >= 0x80:
                    if last_token == 0xCB and b == 0xA4:
                        # convert 'GO TO' into 'GOTO'
                        last_token = 0x89
                    # ignore '-' token to handle 'LIST#-#' correctly
                    elif last_token != 0x9B or b != 0xAB:
                        last_token = b
                elif b == ord(':'):
                    # next statement
                    last_token = None

            if b == ord('"'):
                in_quote = not in_quote

            next_part.append(b)

        if val is None:
            if next_part:
                yield next_part
        else:
            yield val


_token_set_register['basic-v2'] = TokenSet_BASICv2()
