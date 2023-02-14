from gui.ui.sound_bank.SplitEditWidget import SplitEditWidgetUI
from formats.sound.sound_types import Split


class SplitEditor(SplitEditWidgetUI):
    def __init__(self):
        super(SplitEditor, self).__init__()
        self.split: [Split] = None

    def set_split(self, split: Split):
        self.split = split

        self.low_key.setValue(self.split.low_key)
        self.high_key.setValue(self.split.high_key)
        self.low_vel.setValue(self.split.low_vel)
        self.high_vel.setValue(self.split.high_vel)
        self.sample_id.setValue(self.split.sample.id_)
        self.fine_tune.setValue(self.split.fine_tune)
        self.coarse_tune.setValue(self.split.coarse_tune)
        self.root_key.setValue(self.split.root_key)
        self.volume.setValue(self.split.volume)
        self.pan.setValue(self.split.pan)
        self.key_group_id.setValue(self.split.key_group.id_)
        self.envelope_enabled.setChecked(self.split.envelope_on)
        self.attack_volume.setValue(self.split.attack_volume)
        self.attack.setValue(self.split.attack)
        self.decay.setValue(self.split.decay)
        self.decay2.setValue(self.split.decay2)
        self.sustain.setValue(self.split.sustain)
        self.hold.setValue(self.split.hold)
        self.release.setValue(self.split.release)
