"""
Tokenize a stream into s-expression atoms
"""
import re


class SexTokens(object):
    """that is- S-Expresion Tokens ;)"""
    def __init__(self, stream, parens='()', strict=False):
        self.stream = stream
        if len(parens) != 2:
            raise ValueError("parens must be exactly 2 chars long")
        self._open_paren = parens[0]
        self._close_paran = parens[1]
        self._paren_re = re.compile(u'{open}|{close}'.format(
            open=re.escape(self._open_paren),
            close=re.escape(self._close_paran)))

    def read(self):
        pass

    def next(self):
        pass

    def sex_eater(self, token_type, token_string, start_pas, end_pos, line_no):
        pass
