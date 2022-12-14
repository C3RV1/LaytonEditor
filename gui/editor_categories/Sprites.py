from .Filesystem import FolderNode, AssetNodeBasename, FilesystemCategory
from formats.graphics.ani import AniSprite, AniSubSprite
from typing import Union


class SpriteAsset(AssetNodeBasename):
    def get_sprite(self) -> Union[AniSprite, AniSubSprite]:
        if self.path.endswith(".arc"):
            return AniSprite(self.path, rom=self.rom)
        return AniSubSprite(self.path, rom=self.rom)


class SpriteCategory(FilesystemCategory):
    def __init__(self):
        super(SpriteCategory, self).__init__()
        self.name = "Sprites"

    def reset_file_system(self):
        self._root = FolderNode(self, "/data_lt2/ani", self.rom.filenames["/data_lt2/ani"], None,
                                asset_class=SpriteAsset)
