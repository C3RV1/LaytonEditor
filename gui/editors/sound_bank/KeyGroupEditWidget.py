from gui.ui.sound_bank.KeyGroupEditWidget import KeyGroupEditWidgetUI
from formats.sound.sound_types import KeyGroup


class KeyGroupEditor(KeyGroupEditWidgetUI):
    def __init__(self):
        super(KeyGroupEditor, self).__init__()
        self.key_group: [KeyGroup] = None

    def set_key_group(self, key_group: KeyGroup):
        self.key_group = key_group

        self.polyphony.setValue(self.key_group.polyphony)
        self.priority.setValue(self.key_group.priority)
        self.voice_channel_low.setValue(self.key_group.voice_channel_low)
        self.voice_channel_high.setValue(self.key_group.voice_channel_high)
