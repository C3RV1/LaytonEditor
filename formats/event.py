# Ported from shortbrim
import io
import re

import formats.binary as binary
import formats.gds
import formats.filesystem as fs
from typing import Optional, Union

from formats import conf
from formats.dlz import EventLchDlz, EventInf2Dlz


class Event:
    """
    A representation of an Event, which handles its loading and saving from a Layton2 rom.
    """
    def __init__(self, rom: fs.NintendoDSRom = None):
        """
        Parameters
        ----------
        rom : NintendoDSROM
            Rom which will be used when loading and saving the event.
        """
        self.rom = rom
        """The rom from which the event is loaded and where it is saved."""
        self.event_id = 0
        """The id of the event. Each event id is composed of 5 numbers (10030 for example)."""

        self.gds: formats.gds.GDS = formats.gds.GDS()
        """
        The script of the event as a GDS script.
        
        For information on the commands, look at formats_parsed.gds_parsers.EventGDSParser
        """
        self.texts = {}
        """
        The texts of the dialogues as a pair of dialogue id and GDS script.

        Each GDS script contains the dialogue data as GDS script parameters.
        The parameters are:
        
        - Character ID (int)
        - Starting animation (str)
        - End animation (str)
        - Voice sound pitch (int) (1 - Chelmey, 2 - Layton, 3 - Luke...)
        - Character text (str)
        """

        self.map_top_id = 0
        """ID of the image at the top screen. Corresponds to data_lt2/bg/event/sub<id>.arc"""
        self.map_bottom_id = 0
        """ID of the image at the bottom screen. Corresponds to data_lt2/bg/map/main<id>.arc"""
        self.unk0 = 0
        self.characters = [0, 0, 0, 0, 0, 0, 0, 0]
        """List of the IDs of the characters present in the event."""
        self.characters_pos = [0, 0, 0, 0, 0, 0, 0, 0]
        """List of the position of the characters when the event starts."""
        self.characters_shown = [False, False, False, False, False, False, False, False]
        """List of booleans representing whether the characters are shown or not when the event starts."""
        self.characters_anim_index = [0, 0, 0, 0, 0, 0, 0, 0]
        """List of the animation indexes of the characters when the event starts."""

        self.sound_profile = 0
        """Sound profile in snd_fix.dlz"""

        self.name = ""
        """Event name in ev_lch.dlz"""

    def _resolve_event_id(self):
        """
        Resolves the event id into its prefix, postfix and complete values.

        The prefix value corresponds to the first two digits of the event id.
        The postfix value corresponds to the last three digits of the event id.
        The complete value corresponds to the termination of the packed file containing the event.

        Returns
        -------
        Tuple[str]
            A tuple as (prefix, postfix, complete).

        Examples
        --------
        For the event 10030, the prefix would be "10", the postfix "030" and the complete "10",
        as that event is contained within "ev_d10.plz".

        For the event 24300, the prefix would be "24", the postfix "300" and the complete "24b",
        as that event is contained within "ev_d24b.plz".
        """
        prefix = self.event_id // 1000
        postfix = self.event_id % 1000
        complete = str(prefix)
        if prefix == 24:
            if postfix < 300:
                complete += "a"
            elif postfix < 600:
                complete += "b"
            else:
                complete += "c"
        return str(prefix), str(postfix).zfill(3), complete

    def load_from_rom(self):
        """
        Loads the event data from the ROM.
        """
        if self.rom is None:
            return
        prefix, postfix, complete = self._resolve_event_id()
        events_packed = self.rom.get_archive(f"/data_lt2/event/ev_d{complete}.plz")
        file = events_packed.open(f"d{prefix}_{postfix}.dat", "rb")
        self.read_stream(file)
        file.close()
        self._load_gds()
        self._load_texts()
        self._load_dlz()

    def save_to_rom(self):
        """
        Saves the event data to the ROM.
        """
        if self.rom is None:
            return
        prefix, postfix, complete = self._resolve_event_id()
        events_packed = self.rom.get_archive(f"/data_lt2/event/ev_d{complete}.plz")
        file = events_packed.open(f"d{prefix}_{postfix}.dat", "wb")
        self.write_stream(file)
        file.close()
        self._sort_and_remove_unused_texts()
        self._save_gds()
        self._clear_event_texts()
        self._save_texts()
        self._save_dlz()

    def read_stream(self, reader: Union[binary.BinaryReader, io.BytesIO]):
        """
        Reads the event data from a stream.

        Parameters
        ----------
        reader : binary.BinaryReader | io.BytesIO
            The stream from which to read the data.
        """
        if not isinstance(reader, binary.BinaryReader):
            reader = binary.BinaryReader(reader)
        self.map_bottom_id = reader.read_uint16()
        self.map_top_id = reader.read_uint16()
        self.unk0 = reader.read_uint16()

        self.characters = []
        for _indexChar in range(8):
            self.characters.append(reader.read_uint8())
        self.characters_pos = []
        for _indexChar in range(8):
            self.characters_pos.append(reader.read_uint8())
        self.characters_shown = []
        for _indexChar in range(8):
            self.characters_shown.append(reader.read_bool())
        self.characters_anim_index = []
        for _indexChar in range(8):
            self.characters_anim_index.append(reader.read_uint8())

        self.sound_profile = reader.read_uint16()

    def write_stream(self, wtr: Union[binary.BinaryWriter, io.BytesIO]):
        """
        Write the event data into the supplied stream.
        Parameters
        ----------
        wtr : binary.BinaryWriter | io.BytesIO
            The stream to which the data should be written.
        """
        if not isinstance(wtr, binary.BinaryWriter):
            wtr = binary.BinaryWriter(wtr)
        wtr.write_uint16(self.map_bottom_id)
        wtr.write_uint16(self.map_top_id)
        wtr.write_uint16(self.unk0)

        for char in self.characters:
            wtr.write_uint8(char)
        for char_pos in self.characters_pos:
            wtr.write_uint8(char_pos)
        for char_show in self.characters_shown:
            wtr.write_bool(char_show)
        for char_anim in self.characters_anim_index:
            wtr.write_uint8(char_anim)

        wtr.write_uint16(self.sound_profile)

        return wtr.data

    def _load_dlz(self):
        event_lch = EventLchDlz(rom=self.rom, filename=f"/data_lt2/rc/{conf.LANG}/ev_lch.dlz")
        self.name = event_lch.get(self.event_id, "")

        event_inf2 = EventInf2Dlz(rom=self.rom, filename=f"/data_lt2/rc/{conf.LANG}/ev_inf2.dlz")
        self.sound_profile = event_inf2[self.event_id]

    def _save_dlz(self):
        event_lch = EventLchDlz(rom=self.rom, filename=f"/data_lt2/rc/{conf.LANG}/ev_lch.dlz")
        if self.name != "":
            event_lch[self.event_id] = self.name
        else:
            event_lch.pop(self.event_id)
        event_lch.save()

        event_inf2 = EventInf2Dlz(rom=self.rom, filename=f"/data_lt2/rc/{conf.LANG}/ev_inf2.dlz")
        event_inf2[self.event_id] = self.sound_profile
        event_inf2.save()

    def _load_gds(self):
        if self.rom is None:
            return
        prefix, postfix, complete = self._resolve_event_id()
        events_packed = self.rom.get_archive(f"/data_lt2/event/ev_d{complete}.plz")
        self.gds = formats.gds.GDS(f"e{prefix}_{postfix}.gds", rom=events_packed)

    def _save_gds(self):
        if self.rom is None:
            return
        prefix, postfix, complete = self._resolve_event_id()
        events_packed = self.rom.get_archive(f"/data_lt2/event/ev_d{complete}.plz")
        self.gds.save(filename=f"e{prefix}_{postfix}.gds", rom=events_packed)

    @property
    def _texts_archive(self):
        prefix, postfix, complete = self._resolve_event_id()
        return self.rom.get_archive(f"/data_lt2/event/?/ev_t{complete}.plz".replace("?", conf.LANG))

    def _load_texts(self):
        if self.rom is None:
            return
        self.texts = {}
        event_texts = self._list_event_texts()
        for dial_id, filename in event_texts.items():
            self.texts[dial_id] = formats.gds.GDS(filename=filename, rom=self._texts_archive)

    def _sort_and_remove_unused_texts(self):
        text_order = []
        # sort in order of appearance
        for command in self.gds.commands:
            if command.command == 0x4:
                text_order.append(command.params[0])
                command.params[0] = len(text_order) * 100

        # replace in texts, while dropping the ones not present
        old_texts = self.texts
        self.texts = {}
        for text_key in old_texts.keys():
            if text_key in text_order:
                text = old_texts[text_key]
                self.texts[(text_order.index(text_key) + 1) * 100] = text

    def _save_texts(self):
        prefix, postfix, complete = self._resolve_event_id()
        for dial_id, text in self.texts.items():
            text: formats.gds.GDS
            text.save(filename=f"t{prefix}_{postfix}_{dial_id}.gds", rom=self._texts_archive)

    def get_text(self, text_num) -> formats.gds.GDS:
        """
        Gets the dialogue GDS from the dialogue ID.

        The dialogue data GDS has the following parameters:

        - Character ID (int)
        - Starting animation (str)
        - End animation (str)
        - Voice sound pitch (int) (1 - Chelmey, 2 - Layton, 3 - Luke...)
        - Character text (str)

        Parameters
        ----------
        text_num : int
            The dialogue ID for which to get the text GDS.

        Returns
        -------
        GDS
            The dialogue data GDS.
        """
        default_gds = formats.gds.GDS()
        default_gds.params = [0, "", "", 3, ""]
        if self.rom is None:
            return default_gds
        return self.texts.get(text_num, default_gds)

    def _list_event_texts(self):
        if self.rom is None:
            return
        text_lst = {}
        dial_files = self._texts_archive.filenames
        prefix, postfix, complete = self._resolve_event_id()
        for filename in dial_files:
            if match := re.match(f"t{prefix}_{postfix}_([0-9]+).gds", filename):
                text_lst[int(match.group(1))] = filename
        return text_lst

    def _clear_event_texts(self):
        if self.rom is None:
            return
        dial_files = self._list_event_texts()
        for filename in dial_files.values():
            self._texts_archive.remove_file(filename)
