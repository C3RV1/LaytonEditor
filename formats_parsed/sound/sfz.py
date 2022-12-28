from typing import TextIO

from formats.sound.sound_types import Program


def sfz_write_preset(stream: TextIO, preset: Program, sample_location=r"..\samples\sample_%04i.wav"):
    for split in preset.splits:
        stream.writelines([
            f"<region>\n",
            f"sample={sample_location % split.sample.id_}\n"
            f"lokey={split.low_key} hikey={split.high_key}\n"
            f"pitch_keycenter={split.root_key}\n"
            f"loop_mode={'loop_continuous' if split.sample.loop_enabled else 'no_loop'}\n",
            f"tune={split.fine_tune}\n",
            f"loop_start={split.sample.loop_beginning}\n",
            f"\n"
        ])
