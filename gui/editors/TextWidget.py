from ..ui.TextWidget import TextWidgetUI

from ..editor_categories.Filesystem import AssetNode

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..MainEditor import MainEditor


class TextEditor(TextWidgetUI):
    def __init__(self, main_editor):
        super(TextEditor, self).__init__()
        self.main_editor: MainEditor = main_editor
        self.text_asset: AssetNode = None

    def set_text(self, text: AssetNode):
        self.text_asset = text
        f = text.rom.open(text.path, "rb")
        data = f.read()
        try:
            self.text_editor.setPlainText(data.decode("cp1252"))
            self.save_btn.setEnabled(True)
        except UnicodeDecodeError:
            self.text_editor.setPlainText(data.decode("shift-jis"))
            self.save_btn.setEnabled(False)
        finally:
            f.close()

    def save_btn_click(self):
        f = self.text_asset.rom.open(self.text_asset.path, "w")
        f.write(self.text_editor.toPlainText())
        f.close()
