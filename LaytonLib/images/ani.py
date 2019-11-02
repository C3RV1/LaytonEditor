import LaytonLib.binary
import LaytonLib.compression
from LaytonLib.images.color import Color
import numpy as np
import PIL.Image as imgl
from math import log, sqrt


# Special Reader to have extra values
class AniReader(LaytonLib.binary.BinaryReader):
    def __init__(self, data, filetype="arc", colordepth=None):
        self.colordepth = colordepth
        self.filetype = filetype
        super().__init__(data)


class AniWriter(LaytonLib.binary.BinaryWriter):
    def __init__(self, colordepth, filetype):
        self.colordepth = colordepth
        self.filetype = filetype
        super().__init__()

class Animation():
    def __init__(self):
        self.name = ""
        self.frameIDs = []
        self.imageIndexes = []
        self.frameDurations = []

    def name_from_reader(self, rdr):
        self.name = rdr.readChars(0x1E).split("\0")[0]

    def framedata_from_reader(self, rdr):
        n_frames = rdr.readU32()
        for i in range(n_frames):
            self.frameIDs.append(rdr.readU32())
        for i in range(n_frames):
            self.frameDurations.append(rdr.readU32())
        for i in range(n_frames):
            self.imageIndexes.append(rdr.readU32())

    def name_to_writer(self, wtr: AniWriter):
        name = self.name
        while len(name) < 0x1E:
            name += "\0"
        wtr.write(name)

    def framedata_to_writer(self, wtr: AniWriter):
        wtr.writeU32(len(self.imageIndexes))
        for i in range(len(self.frameIDs)):
            wtr.writeU32(self.frameIDs[i])
        for i in range(len(self.frameIDs)):
            wtr.writeU32(self.frameDurations[i])
        for i in range(len(self.frameIDs)):
            wtr.writeU32(self.imageIndexes[i])


class Palette():
    def __init__(self):
        self.colors = []

    def from_reader(self, rdr: AniReader, size=0):
        if rdr.filetype == "arj":
            n_colors = size
        else:
            n_colors = rdr.readU32()
        for i in range(n_colors):
            self.colors.append(Color(bgr555sum=rdr.readU16()))

    def to_writer(self, wtr: AniWriter):
        if wtr.filetype == "arc":
            wtr.writeU32(len(self.colors))
        for c in self.colors:
            c: Color
            wtr.writeU16(c.bgr555int)

    def to_rgb_list(self):
        return [c.rgb for c in self.colors]

    def clear(self):
        self.colors = []

    def get_closest_color(self, rgb):
        if rgb == self.colors[0].rgb:
            return 0
        best_dist = 10000.
        best = 1
        for i in range(1, len(self.colors)):
            color = self.colors[i].rgb
            r = color[0] - rgb[0]
            g = color[1] - rgb[1]
            b = color[2] - rgb[2]
            dist = sqrt(sum((r ** 2, g ** 2, b ** 2)))
            if dist < best_dist:
                best_dist = dist
                best = i
        return best

class Part:
    def __init__(self, palette, isarj=False):
        self.x = 0  # placeholder
        self.y = 0  # placeholder
        self.palette = palette  # placeholder
        self.data = np.zeros((8, 8), np.uint8)
        self.glbX = 0
        self.glbY = 0

    @property
    def w(self):
        return self.data.shape[1]

    @property
    def h(self):
        return self.data.shape[0]

    @w.setter
    def w(self, value):
        self.data.resize((self.h, value))

    @h.setter
    def h(self, value):
        self.data.resize((value, self.w))

    def from_reader(self, rdr: AniReader):
        if rdr.filetype == "arj":
            self.glbX = rdr.readU16()
            self.glbY = rdr.readU16()
        self.x = rdr.readU16()
        self.y = rdr.readU16()
        wr = rdr.readU16()
        hr = rdr.readU16()
        w = 2 ** (3 + wr)
        h = 2 ** (3 + hr)
        self.w, self.h = w, h
        if rdr.colordepth == 8:
            len = w * h
            raw = np.asarray(rdr.readU8List(len))

        else:
            len = int(w * h / 2)
            raw = np.asarray(rdr.readU4List(len))

        if rdr.filetype == "arj":
            self.data = np.zeros((h, w), np.uint8)
            offset = 0
            for yt in range(int(h/8)):
                for xt in range(int(w/8)):
                    for y in range(8):
                        for x in range(8):
                            self.data[y + yt*8, x+xt*8] = raw[offset]
                            offset += 1
        else:
            self.data = raw.reshape((h, w))

    def to_writer(self, wtr: AniWriter):
        if wtr.filetype == "arj":
            wtr.writeU16(self.glbX)
            wtr.writeU16(self.glbY)
        wtr.writeU16(self.x)
        wtr.writeU16(self.y)
        wtr.writeU16(int(log(self.w, 2))-3)
        wtr.writeU16(int(log(self.h, 2))-3)
        raw = []
        if wtr.filetype == "arc":
            raw = list(self.data.flatten().tolist())
        elif wtr.filetype == "arj":
            for yt in range(int(self.h/8)):
                for xt in range(int(self.w/8)):
                    for y in range(8):
                        for x in range(8):
                            raw.append(self.data[y + yt*8, x+xt*8])

        if wtr.colordepth == 8:
            wtr.writeU8List(raw)
        else:
            wtr.writeU4List(raw)

    def to_RGB_array(self):
        pal = np.asarray(self.palette.to_rgb_list(), np.uint8)
        return pal[self.data]

    def to_PIL(self):
        arr = self.to_RGB_array()
        img = imgl.new("RGB", (self.w, self.h))
        pix = img.load()
        for x in range(self.w):
            for y in range(self.h):
                a = tuple(arr[y, x].tolist())
                pix[x, y] = a
        return img

    def from_PIL(self, bbox, image: imgl.Image):
        self.x, self.y, self.w, self.h = bbox
        pix = image.load()
        for x in range(self.w):
            for y in range(self.h):
                self.data[y, x] = self.palette.get_closest_color(pix[x+self.x, y+self.y])

class Image:
    def __init__(self, palette):
        self.w = 8  # placeholder
        self.h = 8  # placeholder
        self.palette = palette
        self.parts = []

    def from_reader(self, rdr):
        self.w = rdr.readU16()
        self.h = rdr.readU16()
        n_parts = rdr.readU16()
        rdr.c += 2
        for i in range(n_parts):
            part = Part(self.palette)
            part.from_reader(rdr)
            self.parts.append(part)

    def to_writer(self, wtr: AniWriter):
        wtr.writeU16(self.w)
        wtr.writeU16(self.h)
        wtr.writeU16(len(self.parts))
        wtr.writeZeros(2)
        for part in self.parts:
            part: Part
            part.to_writer(wtr)

    def to_PIL(self):
        img = imgl.new("RGB", (self.w, self.h))
        for part in self.parts:
            img.paste(part.to_PIL(),(part.x, part.y))
        return img

    def from_PIL(self, image: imgl.Image):
        self.parts = [] # Start with no parts
        w, h = self.w, self.h = image.size

        # Align width and height to 8
        w = (w >> 3) << 3
        h = (h >> 3) << 3
        if w < self.w: w += 8
        if h < self.h: h += 8

        # Make a new image with the size of the original.
        fimage = imgl.new("RGB", (w, h), self.palette.colors[0].rgb)
        fimage.paste(image)

        # Some code to get the width and height of every part
        parts_w = []
        while w > 0:
            a = 8
            while a * 2 <= w:
                a *= 2
            w -= a
            parts_w.append(a)
        parts_h = []
        while h > 0:
            a = 8
            while a * 2 <= h:
                a *= 2
            h -= a
            parts_h.append(a)

        # Make the parts and import from the image
        x, y = 0, 0
        for part_w in parts_w:
            y = 0
            for part_h in parts_h:
                part = Part(self.palette)
                part.from_PIL((x, y, part_w, part_h), fimage)
                self.parts.append(part)
                y += part_h
            x += part_w



class Ani():
    def __init__(self, filetype="arc"):
        self.filetype = filetype
        self.colordepth = 8
        self.images = []
        self.animations = []
        self.vars = []
        self.palette = Palette()
        self.startbyte = 0x02

    def import_data(self, data: bytes):
        # Work with the image in compressed format
        compressed_rdr = LaytonLib.binary.BinaryReader(data)
        del data
        self.startbyte = compressed_rdr.readU32()
        rdr = AniReader(
            LaytonLib.compression.decompress(
                compressed_rdr.readFinal()),
            self.filetype)
        del compressed_rdr

        # Now work with the uncompressed one, starting with the images
        n_images = rdr.readU16()
        rdr.colordepth = self.colordepth = 4 if rdr.readU16() == 3 else 8

        palettesize = 0
        if self.filetype == "arj":
            palettesize = rdr.readU32()

        for i in range(n_images):
            new_image = Image(self.palette)
            self.images.append(new_image)
            new_image.from_reader(rdr)

        # Get the used palette
        self.palette.clear()
        self.palette.from_reader(rdr, palettesize)

        # Work trough each of the animations
        rdr.c += 0x1E
        n_animations = rdr.readU32()
        for i in range(n_animations):
            animation = Animation()
            self.animations.append(animation)
            animation.name_from_reader(rdr)
        for a in self.animations:
            a.framedata_from_reader(rdr)

        # Now read variable data
        self.vars = rdr.readFinal()
        # TODO: Figure out how variables work

    def export_data(self):
        wtr = AniWriter(self.colordepth, self.filetype)
        wtr.writeU16(len(self.images))
        wtr.writeU16(3 if self.colordepth == 4 else 4)
        if self.filetype == "arj":
            wtr.writeU32(len(self.palette.colors))

        for image in self.images:
            image: Image
            image.to_writer(wtr)

        self.palette.to_writer(wtr)

        wtr.writeZeros(0x1E)

        wtr.writeU32(len(self.animations))
        for animation in self.animations:
            animation: Animation
            animation.name_to_writer(wtr)
        for animation in self.animations:
            animation.framedata_to_writer(wtr)

        wtr.write(self.vars)

        compressed = LaytonLib.binary.BinaryWriter()
        compressed.writeU32(self.startbyte)
        compressed.write(LaytonLib.compression.compress(wtr.data, LaytonLib.compression.LZ10))
        return compressed.data

    def frame_to_PIL(self, frameindex):
        return self.images[frameindex].to_PIL()

    def frame_from_PIL_nopalswap(self, frameindex, image):
        self.images[frameindex].from_PIL(image)

    def frame_from_PIL_addpal(self, frameindex, image: imgl.Image):
        ## First we need to get a new palette
        # Combine all current images
        all_except_new = self.images[0:frameindex] + self.images[frameindex:]
        total_w = 0
        max_h = 0
        for img in all_except_new:
            total_w += img.w
            max_h = max(max_h, img.h)
        combination = imgl.new("RGB", (total_w, max_h), self.palette.colors[0].rgb)
        x = 0
        for img in all_except_new:
            combination.paste(img.to_PIL(), (x, 0))
            x += img.w

        # Combine previous combination with new
        combination_with_new = imgl.new("RGB", (total_w+image.size[0], max(max_h, image.size[1])),
                                        self.palette.colors[0].rgb)
        combination_with_new.paste(combination)
        combination_with_new.paste(image, (total_w, 0))

        # Now quantize it
        combination_with_new = combination_with_new.quantize(2**self.colordepth-1).convert("RGB")

        # Get the new colors, set green to the first one and convert to the Color class
        newcolors = combination_with_new.getcolors(2 ** self.colordepth - 1)
        del combination_with_new
        newcolors = [x[1] for x in newcolors]
        if (0, 248, 0) in newcolors:
            newcolors.remove((0, 248, 0))
        newcolors = [(0, 248, 0),] + newcolors
        newcolors = [LaytonLib.images.color.Color(x) for x in newcolors]

        # Get all the images for later
        images = []
        for img in self.images:
            images.append(img.to_PIL())

        # Swap with new image
        images[frameindex] = image

        # Replace colors in palette
        self.palette.colors = newcolors

        # And now update all images with the new palette
        for i in range(len(self.images)):
            self.images[i].from_PIL(images[i])

class AniFile(Ani, LaytonLib.filesystem.File):
    def __init__(self, rom: LaytonLib.filesystem.NintendoDSRom, id):
        filename = rom.filenames[id]
        if filename.endswith("arc"):
            filetype = "arc"
        elif filename.endswith("arj"):
            filetype = "arj"
        else:
            raise NotImplementedError("Unsupported File Type")
        Ani.__init__(self, filetype=filetype)
        LaytonLib.filesystem.File.__init__(self, rom, id)
        self.reload()

    def save(self):
        self.write(self.export_data())

    def reload(self):
        self.import_data(self.read())