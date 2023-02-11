from gui.ui.sound_bank.SampleEditWidget import SampleEditWidgetUI
from formats.sound.sound_types import Sample


class SampleEditor(SampleEditWidgetUI):
    def __init__(self):
        super(SampleEditor, self).__init__()
        self.sample: [Sample] = None

    def set_sample(self, sample: Sample):
        self.sample = sample
        self.play_button.setEnabled(sample.has_data())
        self.import_button.setEnabled(sample.has_data())
        self.export_button.setEnabled(sample.has_data())

        self.fine_tune.setValue(self.sample.fine_tune)
        self.coarse_tune.setValue(self.sample.coarse_tune)
        self.root_key.setValue(self.sample.root_key)
        self.volume.setValue(self.sample.volume)
        self.pan.setValue(self.sample.pan)
        self.loop_enabled.setChecked(self.sample.loop_enabled)
        self.sample_rate.setValue(self.sample.sample_rate)
        self.loop_beginning.setValue(self.sample.loop_beginning)
        self.loop_length.setValue(self.sample.loop_length)
        self.enable_envelope.setChecked(self.sample.envelope_on)
        self.attack_volume.setValue(self.sample.attack_volume)
        self.attack.setValue(self.sample.attack)
        self.decay.setValue(self.sample.decay)
        self.decay2.setValue(self.sample.decay2)
        self.sustain.setValue(self.sample.sustain)
        self.hold.setValue(self.sample.hold)
        self.release.setValue(self.sample.release)
