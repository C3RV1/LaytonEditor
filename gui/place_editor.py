import re

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
    _loaded_place: Place

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
                    place_file = self._place_archive.open(filename)
                    self._places[subindex].read_stream(place_file)
                    place_file.close()

        # Load placeviewer for place
        self.plc_preview.load_place(self._places[place_subindex], self._rom)

        # List tree items for all subplaces
        self.plc_items.DeleteAllItems()
        root = self.plc_items.AddRoot("Places")
        for subindex in self._places:
            place = self._places[subindex]
            place_root = self.plc_items.AppendItem(root, f"Version {subindex}", data=place)
            hintcoin_node = self.plc_items.AppendItem(place_root, "Hintcoins")
            object_node = self.plc_items.AppendItem(place_root, "Objects")
            spr_node = self.plc_items.AppendItem(place_root, "Sprites")
            comment_node = self.plc_items.AppendItem(place_root, "Comments")
            exit_node = self.plc_items.AppendItem(place_root, "Exits")
            for i, hintcoin in enumerate(place.hintcoins):
                self.plc_items.AppendItem(hintcoin_node, f"Hintcoin {i}", data=hintcoin)
            for i, obj in enumerate(place.objects):
                self.plc_items.AppendItem(object_node, f"Object {i}", data=obj)
            for i, spr in enumerate(place.sprites):
                self.plc_items.AppendItem(spr_node, f"Sprite {i}", data=spr)
            for i, comment in enumerate(place.comments):
                self.plc_items.AppendItem(comment_node, f"Comment {i}", data=comment)
            for i, exit_obj in enumerate(place.exits):
                self.plc_items.AppendItem(exit_node, f"Exit {i}", data=exit_obj)

        self.load_place_properties(self._places[self._place_subindex])

    def load_place_properties(self, place: Place):
        self._loaded_place = place
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

    def load_object_properties(self, obj: PlaceObject):
        self.plc_item_data.Clear()
        self.plc_item_data.Append(wx.propgrid.IntProperty("Object Character Index", "Object Character Index",
                                                          obj.character_index))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Object Event Index", "Object Event Index",
                                                          obj.event_index))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Objecy X", "Object X",
                                                          obj.x))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Objecy Y", "Object Y",
                                                          obj.y))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Object Width", "Object Width",
                                                          obj.width))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Object Height", "Object Height",
                                                          obj.height))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Object UNK", "Object UNK",
                                                          obj.unk))

    def load_sprite_properties(self, spr: PlaceSprite):
        self.plc_item_data.Clear()
        self.plc_item_data.Append(wx.propgrid.IntProperty("Sprite X", "Sprite X",
                                                          spr.x))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Sprite Y", "Sprite Y",
                                                          spr.y))
        self.plc_item_data.Append(wx.propgrid.StringProperty("Sprite Filename", "Sprite Filename",
                                                             spr.filename))

    def load_comment_properties(self, comment: PlaceComment):
        self.plc_item_data.Clear()
        self.plc_item_data.Append(wx.propgrid.IntProperty("Comment X", "Comment X",
                                                          comment.x))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Comment Y", "Comment Y",
                                                          comment.y))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Comment Width", "Comment Width",
                                                          comment.width))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Comment Height", "Comment Height",
                                                          comment.height))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Comment Character Index", "Comment Character Index",
                                                          comment.character_index))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Comment Text Index", "Comment Text Index",
                                                          comment.text_index))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Comment UNK", "Comment UNK",
                                                          comment.unk))

    def load_exit_properties(self, exit_obj: PlaceExit):
        self.plc_item_data.Clear()
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit X", "Exit X",
                                                          exit_obj.x))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit Y", "Exit Y",
                                                          exit_obj.y))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit Width", "Exit Width",
                                                          exit_obj.width))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit Height", "Exit Height",
                                                          exit_obj.height))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit Image Index", "Exit Image Index",
                                                          exit_obj.image_index))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit Action", "Exit Action",
                                                          exit_obj.action))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit UNK0", "Exit UNK0",
                                                          exit_obj.unk0))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit UNK1", "Exit UNK1",
                                                          exit_obj.unk1))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit UNK2", "Exit UNK2",
                                                          exit_obj.unk2))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit UNK3", "Exit UNK3",
                                                          exit_obj.unk3))
        self.plc_item_data.Append(wx.propgrid.IntProperty("Exit Event or Place ID", "Exit Event or Place ID",
                                                          exit_obj.event_or_place_index))

    def plc_items_selchanged(self, event):
        try:
            if not self.plc_items.GetSelections():
                return
        except RuntimeError:
            # wrapped c/c++ object of type TreeCtrl has been deleted
            return
        selection = self.plc_items.GetSelection()
        name = self.plc_items.GetItemText(selection)
        data = self.plc_items.GetItemData(selection)
        if data is None:
            return
        elif isinstance(data, Place):
            self._place_subindex = int(name[8:])
            self.plc_preview.load_place(data, self._rom)
            self.load_place_properties(data)
        else:
            # Load the place the object is in if it is not loaded
            place_parent = self.plc_items.GetItemParent(selection)
            place_parent = self.plc_items.GetItemParent(place_parent)
            place_name = self.plc_items.GetItemText(place_parent)
            place_parent = self.plc_items.GetItemData(place_parent)
            if isinstance(place_parent, Place) and self._loaded_place is not place_parent:
                self._place_subindex = int(place_name[8:])
                self.plc_preview.load_place(place_parent, self._rom)
                self.load_place_properties(place_parent)

            if isinstance(data, PlaceHintcoin):
                self.load_hintcoin_properties(data)
            elif isinstance(data, PlaceObject):
                self.load_object_properties(data)
            elif isinstance(data, PlaceSprite):
                self.load_sprite_properties(data)
            elif isinstance(data, PlaceComment):
                self.load_comment_properties(data)
            elif isinstance(data, PlaceExit):
                self.load_exit_properties(data)

    def enter(self):
        pass

    def exit(self):
        pass

    def close(self):
        return True
