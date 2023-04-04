import logging
import re

import formats.filesystem
import formats.gds
import formats.sound.sadl


class Movie:
    def __init__(self, rom: formats.filesystem.NintendoDSRom, id_):
        self.rom: formats.filesystem.NintendoDSRom = rom
        self.movie_id = id_
        self.subtitles = {}
        self.gds: formats.gds.GDS = None

    def load_from_rom(self):
        self._load_gds()
        self._load_subtitles()

    def save_to_rom(self):
        self._sort_and_remove_unused_subtitles()
        self._save_subtitles()
        self._save_gds()

    def _load_gds(self):
        movie_plz_file = self.rom.get_archive(f"/data_lt2/script/movie/{self.rom.lang}/movie.plz")
        gds_filename = f"m{self.movie_id}.gds"

        if gds_filename not in movie_plz_file.filenames:
            logging.error(f"GDS for movie {self.movie_id} not found")
            return

        self.gds = formats.gds.GDS(gds_filename, rom=movie_plz_file)

    def _save_gds(self):
        movie_plz_file = self.rom.get_archive(f"/data_lt2/script/movie/{self.rom.lang}/movie.plz")
        gds_filename = f"m{self.movie_id}.gds"
        self.gds.save(gds_filename, rom=movie_plz_file)

    def _load_subtitles(self):
        subtitle_plz = self.rom.get_archive(f"/data_lt2/txt/{self.rom.lang}/txt.plz")
        self.subtitles = {}
        for filename in subtitle_plz.filenames:
            if match := re.match(f"m{self.movie_id}_([0-9]+)\\.txt", filename):
                subtitle_id = int(match.group(1))
                with subtitle_plz.open(filename, "rb") as subtitle_file:
                    self.subtitles[subtitle_id] = subtitle_file.read().decode("cp1252")

    def _save_subtitles(self):
        subtitle_plz = self.rom.get_archive(f"/data_lt2/txt/{self.rom.lang}/txt.plz")

        for filename in subtitle_plz.filenames.copy():
            if re.match(f"m{self.movie_id}_[0-9]+\\.txt", filename):
                subtitle_plz.remove_file(filename)

        keys = list(self.subtitles.keys())
        keys.sort()
        for subtitle_id in keys:
            subtitle_text = self.subtitles[subtitle_id]
            print(f"Saving {subtitle_text} to m{self.movie_id}_{subtitle_id}.txt")
            with subtitle_plz.open(f"m{self.movie_id}_{subtitle_id}.txt", "wb+") as subtitle_file:
                subtitle_file.write(subtitle_text.encode("cp1252"))

    def _sort_and_remove_unused_subtitles(self):
        subtitle_order = []
        for command in self.gds.commands:
            if command.command == 0xa2:
                subtitle_order.append(command.params[0])
                command.params[0] = len(subtitle_order) - 1
        print(subtitle_order)

        old_subtitles = self.subtitles
        self.subtitles = {}
        for subtitle_id in old_subtitles:
            if subtitle_id in subtitle_order:
                subtitle_text = old_subtitles[subtitle_id]
                self.subtitles[subtitle_order.index(subtitle_id)] = subtitle_text
        print(self.subtitles)

    def get_sad(self):
        return formats.sound.sadl.SADL(f"/data_lt2/stream/movie/{self.rom.lang}/M{self.movie_id}.SAD", rom=self.rom)


if __name__ == '__main__':
    rom = formats.filesystem.NintendoDSRom.fromFile("../rom.nds")
    movie = Movie(rom, 1)
    movie.load_from_rom()
    movie.save_to_rom()
    print(movie.subtitles)
    print(movie.gds)
