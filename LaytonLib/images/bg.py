from LaytonLib.binary import BinaryReader, BinaryWriter
from LaytonLib.compression import decompress, compress, LZ10
from .color import Color
import LaytonLib.filesystem
import PIL.Image as imgl

# Defines
MAX_COLORS = 200

class Bg:
    def __init__(self):
        self.start_word = 2
        self.img = imgl.new("RGB", (256, 192))

    def import_data(self, data: bytes):
        compressed_rdr = BinaryReader(data)
        self.start_word = compressed_rdr.readU32()

        rdr = BinaryReader(decompress(compressed_rdr.readFinal()))

        # Read colors
        colors = []  # reset
        n_colors = rdr.readU32()
        for i in range(n_colors):
            colors.append(Color(bgr555sum=rdr.readU16()))
        # Image Data
        n_tiles = rdr.readU32()
        tiles = rdr.readU8List(n_tiles * 0x40)

        # Map Info
        width = rdr.readU16() * 8
        height = rdr.readU16() * 8
        map = []
        map_len = int(width * height / 0x40)
        for i in range(map_len):
            map.append(rdr.readU16())

        # Generate Image
        self.img = imgl.new("RGB", (width, height))
        pix = self.img.load()

        map_index = 0
        for y in range(int(height / 8)):
            for x in range(int(width / 8)):
                tile = map[map_index]
                map_index += 1
                tile_index = tile * 0x40
                for yt in range(8):
                    for xt in range(8):
                        pix[x * 8 + xt, y * 8 + yt] = colors[tiles[tile_index]].rgb
                        tile_index += 1
        # self.img.show()

    def export_data(self):
        img = self.img.quantize(MAX_COLORS).convert("RGB")
        pix = img.load()
        wtr = BinaryWriter()

        # Write Colors
        colors_T = img.getcolors()
        colors_T = [Color(rgb=x[1]) for x in colors_T]
        colors = [Color((224, 0, 120)), Color((224, 224, 224))]
        for c in colors_T:
            if not c.rgb in [x.rgb for x in colors]:
                colors.append(c)

        wtr.writeU32(len(colors))
        for c in colors:
            wtr.writeU16(c.bgr555int)

        # Generate tiles and map
        all_tiles = []
        width, height = img.size
        for y in range(int(height / 8)):
            for x in range(int(width / 8)):
                tile = []
                for yt in range(8):
                    for xt in range(8):
                        c = Color(rgb=pix[x * 8 + xt, y * 8 + yt])
                        c_index = 0
                        i = 0
                        for test_color in colors:
                            if c.rgb == test_color.rgb:
                                c_index = i
                                break
                            i += 1
                        tile.append(c_index)
                all_tiles.append(tile)
        map = list(range(int(width/8)*int(height/8)))

        # Reduce
        reduced_tiles = []
        index = 0
        for tile in all_tiles:
            if not tile in reduced_tiles:
                reduced_tiles.append(tile)
            map[index] = reduced_tiles.index(tile)
            index += 1

        # Make one dimensional
        index = 0
        tiles = []
        for tile in reduced_tiles:
            tiles += tile

        # Write
        wtr.writeU32(int(len(tiles)/0x40))
        wtr.writeU8List(tiles)

        # Write map
        wtr.writeU16(int(width/8))
        wtr.writeU16(int(height/8))
        wtr.writeU16List(map)

        compressed = compress(wtr.data, LZ10)
        compressed_wtr = BinaryWriter()
        compressed_wtr.writeU32(self.start_word)
        compressed_wtr.write(compressed)

        return compressed_wtr.data

class BgFile(Bg, LaytonLib.filesystem.File):
    def __init__(self, rom: LaytonLib.filesystem.NintendoDSRom, id):
        Bg.__init__(self)
        LaytonLib.filesystem.File.__init__(self, rom, id)
        self.reload()

    def save(self):
        self.write(self.export_data())

    def reload(self):
        self.import_data(self.read())