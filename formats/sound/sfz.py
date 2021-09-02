from .soundtypes import *

def sfz_write_preset(stream: TextIO, preset: Preset, sample_location=r"..\samples\sample_%04i.wav"):
    for split in preset.split_entries:
        stream.writelines([
            f"<region>\n",
            f"sample={sample_location % split.sample_info.sample_index}\n"
            f"lokey={split.lowkey} hikey={split.highkey}\n"
            f"pitch_keycenter={split.rootkey}\n"
            f"loop_mode={'loop_continuous' if split.sample_info.loop_enabled else 'no_loop'}\n",
            f"tune={split.tuning}\n",
            f"loop_start={split.sample_info.loop}\n",
            f"\n"
        ])

