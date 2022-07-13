from typing import TextIO

from .swd import ProgramInfoEntry


def sfz_write_preset(stream: TextIO, preset: ProgramInfoEntry, sample_location=r"..\samples\sample_%04i.wav"):
    for split in preset.splits_table:
        stream.writelines([
            f"<region>\n",
            f"sample={sample_location % split.sample_info.id_}\n"
            f"lokey={split.low_key} hikey={split.hi_key}\n"
            f"pitch_keycenter={split.root_key}\n"
            f"loop_mode={'loop_continuous' if split.sample_info.loop_enabled else 'no_loop'}\n",
            f"tune={split.fine_tune}\n",
            f"loop_start={split.sample_info.loop_beginning}\n",
            f"\n"
        ])
