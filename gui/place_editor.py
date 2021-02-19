import re
from typing import *

import wx.propgrid

import gui.generated
from formats.filesystem import NintendoDSRom, PlzArchive
from formats.place import *


class PlaceEditor(gui.generated.PlaceEditor):
    _rom: NintendoDSRom
    _places: Dict[int, Place]
    _place_archive: PlzArchive
    _place_index: int
    _place_subindex: int

    def load_place(self, rom, place_index, place_subindex=0):
        self._rom = rom
        self._place_archive = PlzArchive(f"data_lt2/place/plc_data" +
                                         f"{1 if place_index < 40 else 2}.plz", rom=rom)
        self._place_index = place_index
        self._place_subindex = place_subindex
        self._places = {}
        for filename in self._place_archive.filenames:
            if finds := re.findall(r"n_place([0-9]+)_([0-9]+)\.dat", filename):
                index, subindex = int(finds[0][0]), int(finds[0][1])
                if index == place_index:
                    # TODO: Clean with intializer
                    self._places[subindex] = Place()
                    self._places[subindex].read_stream(self._place_archive.open(filename))

        # Load placeviewer for place
        self.plc_preview.load_place(self._places[place_subindex], self._rom)

        # List tree items for all subplaces
        self.plc_items.DeleteAllItems()
        root = self.plc_items.AddRoot("Places")
        for subindex in self._places:
            place = self._places[subindex]
            place_root = self.plc_items.AppendItem(root, f"Version {subindex}", data=place)
            hintcoin_node = self.plc_items.AppendItem(place_root, "Hintcoins")
            for i, hintcoin in enumerate(place.hintcoins):
                self.plc_items.AppendItem(hintcoin_node, f"Hintcoin {i}", data=hintcoin)
            # TODO: Other place items

        self.load_place_properties(self._places[self._place_subindex])

    def load_place_properties(self, place: Place):
        self.plc_item_data.Clear()
        self.plc_item_data.Append(wx.propgrid.IntProperty("Background Image", "Background Image",
                                                          place.background_image_index))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Map Image", "Map Image",
                                                          place.map_image_index))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Map X", "Map X",
                                                          place.map_x))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Map Y", "Map Y",
                                                          place.map_y))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Background Music", "Background Music",
                                                          place.background_music_index))

    def load_hintcoin_properties(self, hintcoin: PlaceHintcoin):
        self.plc_item_data.Clear()
        self.plc_item_data.Append(wx.propgrid.IntProperty("Hintcoin ID", "Hintcoin ID",
                                                          hintcoin.index))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Hintcoin X", "Hintcoin X",
                                                          hintcoin.x))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Hintcoin Y", "Hintcoin Y",
                                                          hintcoin.y))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Hintcoin UNK", "Hintcoin UNK",
                                                          hintcoin.unk))

    def plc_items_selchanged(self, event):
        selection = self.plc_items.GetSelection()
        name = self.plc_items.GetItemText(selection)
        data = self.plc_items.GetItemData(selection)
        print(data)
        if data is None:
            return
        elif isinstance(data, Place):
            self._place_subindex = int(name[8:])
            self.plc_preview.load_place(data, self._rom)
            self.load_place_properties(data)
        else:
            # TODO: Load the place the item is in in the viewer, if that place is not loaded already.
            if isinstance(data, PlaceHintcoin):
                # TODO: Load the place the hintcoin is in in the viewer, if that place is not loaded already.
                self.load_hintcoin_properties(data)




    def enter(self):
        pass

    def exit(self):
        pass
