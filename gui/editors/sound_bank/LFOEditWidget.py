from gui.ui.sound_bank.LFOEditWidget import LFOEditWidgetUI
from formats.sound.sound_types import LFO


class LFOEditor(LFOEditWidgetUI):
    def __init__(self):
        super(LFOEditor, self).__init__()
        self.lfo: [LFO] = None

    def set_lfo(self, lfo: LFO):
        self.lfo = lfo

        self.destination.setCurrentIndex(self.lfo.destination)
        self.w_shape.setCurrentIndex(self.lfo.wshape)
        self.rate.setValue(self.lfo.rate)
        self.depth.setValue(self.lfo.depth)
        self.delay.setValue(self.lfo.delay)
