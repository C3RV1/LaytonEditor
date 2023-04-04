from gui.ui.sound_bank.SampleEditWidget import SampleEditWidgetUI
from formats.sound.sound_types import Sample
import numpy as np
import pygame as pg
from formats.sound import sample_transform


class SampleEditor(SampleEditWidgetUI):
    def __init__(self):
        super(SampleEditor, self).__init__()
        self.sample: [Sample] = None

    def set_sample(self, sample: Sample):
        self.sample = sample
        self.play_button.setEnabled(not sample.empty())
        # self.import_button.setEnabled(not sample.empty())
        self.import_button.setEnabled(False)
        # self.export_button.setEnabled(not sample.empty())
        self.export_button.setEnabled(False)

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

    def play_click(self):
        sample = self.sample.pcm16
        sample_pcm = np.reshape(sample, (1, sample.shape[0]))
        target_rate = pg.mixer.get_init()[0]
        target_channels = pg.mixer.get_init()[2]
        sample_pcm = sample_transform.change_sample_rate(sample_pcm, self.sample.sample_rate, target_rate)
        sample_pcm = sample_transform.change_channels(sample_pcm, target_channels)
        sample_pcm = sample_pcm.swapaxes(0, 1)
        sample_pcm = np.ascontiguousarray(sample_pcm)
        sound = pg.sndarray.make_sound(sample_pcm)
        sound.set_volume(0.5)
        sound.play()
