import wx.stc
from formats.gds import GDS
from utility.gdstextscript import convert_to_textscript


class GdsSTC(wx.stc.StyledTextCtrl):
    (STYLE_NORMAL, STYLE_COMMAND, STYLE_STRING, STYLE_STRINGCODE) = range(4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.StyleSetSpec(self.STYLE_NORMAL, "fore:#000000")
        self.StyleSetSpec(self.STYLE_COMMAND, "fore:#7F0000,bold")
        self.StyleSetSpec(self.STYLE_STRING, "fore:#7F007F,bold")
        self.StyleSetSpec(self.STYLE_STRINGCODE, "fore:#400040,bold")
        self.Bind(wx.stc.EVT_STC_STYLENEEDED, self.on_style)
        self.SetLexer(wx.stc.STC_LEX_CONTAINER)

    def load_gds(self, gds: GDS, index=None, rom=None):
        text = convert_to_textscript(gds, index, rom)
        self.SetReadOnly(False)
        self.ClearAll()
        self.WriteText(text)
        self.SetReadOnly(True)

    def on_style(self, event):
        last_styled_pos = self.GetEndStyled()
        line = self.LineFromPosition(last_styled_pos)
        pos = self.PositionFromLine(line)
        end_pos = event.GetPosition()

        style = self.STYLE_COMMAND
        while pos < end_pos:
            self.StartStyling(pos)
            char = chr(self.GetCharAt(pos))
            if style == self.STYLE_COMMAND:
                if char == " ":
                    style = self.STYLE_NORMAL
            elif style == self.STYLE_NORMAL:
                if char == "\n":
                    style = self.STYLE_COMMAND
                elif char == '"':
                    style = self.STYLE_STRING
            elif style == self.STYLE_STRING:
                if char == '"':
                    self.SetStyling(1, style)
                    pos += 1
                    style = self.STYLE_NORMAL
                    continue
                elif char == "@":
                    style = self.STYLE_STRINGCODE
            elif style == self.STYLE_STRINGCODE:
                self.SetStyling(1, style)
                pos += 1
                style = self.STYLE_STRING
                continue

            self.SetStyling(1, style)
            pos += 1
