from laytonlib.images import rgb_to_bgr555, bgr555_to_rgb
from laytonlib import decompress, compress
from laytonlib.binfunctions import BinaryReader, BinaryWriter
from math import log, sqrt
import PIL.Image
from os import remove

class Palette:
    def __init__(self, rbg_colors=[], bgr555_colors=[]):
        self.colours = []
        self.offset = 0
        self.lenght = 0

    def add_rgb(self, rgb):
        self.colours.append(rgb)

    def add_bgr555_sum(self, bgr555_sum):
        self.colours.append(bgr555_to_rgb(bgr555_sum))

    def import_raw(self, rdr: BinaryReader):
        self.offset = rdr.c
        self.lenght = rdr.readU32() * 2
        n_colors = int(self.lenght / 2)
        for i in range(n_colors):
            bgr = rdr.readU16()
            self.add_bgr555_sum(bgr)

    def export_raw(self, rdw: BinaryWriter):
        rdw.writeU32(len(self.colours))
        for color in self.colours:
            rdw.writeU16(rgb_to_bgr555(*color))


class Part:
    def __init__(self, colordepth):
        self.colordepth = colordepth
        self.offset = 0
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.lenght = 0
        self.data = []

    def import_raw(self, rdr: BinaryReader):
        self.offset = rdr.c
        self.x = rdr.readU16()
        self.y = rdr.readU16()
        self.w = 2 ** (3 + rdr.readU16())
        self.h = 2 ** (3 + rdr.readU16())
        if self.colordepth == 8:
            self.lenght = self.w * self.h
            self.data = rdr.readU8List(self.lenght)

        else:
            self.lenght = int(self.w * self.h / 2)
            self.data = rdr.readU4List(self.lenght)

    def export_raw(self, rdw: BinaryWriter):
        rdw.writeU16(self.x)
        rdw.writeU16(self.y)
        rdw.writeU16(int(log(self.w, 2)) - 3)
        rdw.writeU16(int(log(self.h, 2)) - 3)
        if self.colordepth == 4:
            rdw.writeU4List(self.data)
        else:
            rdw.writeU8List(self.data)

    def import_image(self, bbox, palette, image: PIL.Image.Image):
        pix = image.load()
        self.x = bbox[0]
        self.y = bbox[1]
        self.w = bbox[2]
        self.h = bbox[3]
        self.data = [0 for i in range(self.w*self.h)]
        for x in range(self.w):
            for y in range(self.h):
                values = pix[x+self.x, y+self.y]
                self.data[y*self.w+x] = self.get_closest_index(palette, values)

    def get_closest_index(self, palette, pixelvalue):
        if pixelvalue == palette.colours[0]:
            return 0
        best_dist = 10000.
        best = 1
        for i in range(1, len(palette.colours)):
            color = palette.colours[i]
            r = color[0] - pixelvalue[0]
            g = color[1] - pixelvalue[1]
            b = color[2] - pixelvalue[2]
            dist = sqrt(sum((r**2, g**2, b**2)))
            if dist < best_dist:
                best_dist = dist
                best = i
        return best


class Animation:
    def __init__(self):
        self.name = ""
        self.n_frames = 0
        self.framesIDs = []
        self.framesUNK = []
        self.imageIndexes = []


class Image:
    def __init__(self, colordepth):
        self.colordepth = colordepth
        self.w = 0
        self.h = 0
        self.parts = []
        # ...

    def import_raw(self, rdr):
        self.w = rdr.readU16()
        self.h = rdr.readU16()
        n_parts = rdr.readU16()
        lenght = self.w * self.h
        rdr.c += 2
        for i in range(n_parts):
            part = Part(self.colordepth)
            part.import_raw(rdr)
            self.parts.append(part)

    def export_raw(self, rdw: BinaryWriter):
        rdw.writeU16(self.w)
        rdw.writeU16(self.h)
        rdw.writeU16(len(self.parts))
        rdw.writeZeros(2)
        for part in self.parts:
            part.export_raw(rdw)

    def export_image(self, palette):
        w, h = self.__get_original_size()
        final = PIL.Image.new("RGB", (w, h), palette.colours[0])
        pix = final.load()
        for part in self.parts:
            for y in range(part.h):
                for x in range(part.w):
                    pix[x+part.x, y+part.y] = palette.colours[part.data[y*part.w+x]]

        final = final.crop((0, 0, self.w, self.h))
        return final

    def import_image(self, palette: Palette, image: PIL.Image.Image):
        self.parts = []
        self.w, self.h = image.size
        w, h = self.w, self.h
        w = (w >> 3) << 3
        if w < self.w: w+=8
        if h < self.h: h+=8
        h = (h >> 3) << 3
        rimage = PIL.Image.new("RGB", (w, h), palette.colours[0])
        rimage.paste(image)
        parts_w = []
        while w > 0:
            a = 8
            while a*2 <= w:
                a *= 2
            w -= a
            parts_w.append(a)
        parts_h = []
        while h > 0:
            a = 8
            while a*2 <= h:
                a *= 2
            h -= a
            parts_h.append(a)
        x, y = 0, 0
        for part_w in parts_w:
            y = 0
            for part_h in parts_h:
                part = Part(self.colordepth)
                part.import_image((x, y, part_w, part_h), palette, rimage)
                self.parts.append(part)
                y += part_h
            x += part_w



    def __get_original_size(self):
        h, w = self.h, self.w
        for part in self.parts:
            h = max(part.y + part.h, h)
            w = max(part.x + part.w, w)
        return w, h

class Arc:
    def __init__(self):
        self.colordepth = 8
        self.images = []
        self.anims = []
        self.vars = []
        self.palette = Palette()
        self.filedata = {"startbyte": 2}

    def import_arc(self, b_read: bytes):
        C = 0
        self.filedata["startbyte"] = int(b_read[C])
        C = 4
        uncompressed = decompress(b_read[C:])
        del b_read, C
        self.import_data(uncompressed)

    def export_arc(self):
        rdw = BinaryWriter()
        rdw.writeU32(self.filedata["startbyte"])
        rdw.write(compress(self.export_data(), 0x10))
        return rdw.data

    def import_data(self, data):
        self.images = []
        self.anims = []
        self.vars = []
        self.palette = Palette()
        # Load Images
        rdr = BinaryReader(data)
        n_images = rdr.readU16()
        self.colordepth = 4 if rdr.readU16() == 3 else 8
        for i in range(n_images):
            new = Image(self.colordepth)
            self.images.append(new)
            new.import_raw(rdr)
        # Get Palette
        self.palette.import_raw(rdr)
        # Read Animations
        rdr.c += 0x1E
        n_animations = rdr.readU32()
        for i in range(n_animations):
            anim = Animation()
            anim.name = rdr.readChars(0x1E).split("\0")[0]
            self.anims.append(anim)
        for i in range(n_animations):
            anim: Animation = self.anims[i]
            anim.n_frames = rdr.readU32()
            for j in range(anim.n_frames):
                anim.framesIDs.append(rdr.readU32())
                anim.framesUNK.append(rdr.readU32())
                anim.imageIndexes.append(rdr.readU32())

        # Read Variables
        self.vars = rdr.data[rdr.c:]
        del rdr

    def export_data(self):
        # Images
        rdw = BinaryWriter()
        rdw.writeU16(len(self.images))
        c = 3 if self.colordepth == 4 else 4
        rdw.writeU16(c)
        del c
        for im in self.images:
            im: Image = im
            im.export_raw(rdw)
        # Palette
        self.palette.export_raw(rdw)
        # Animations
        rdw.writeZeros(0x1E)
        rdw.writeU32(len(self.anims))
        for anim in self.anims:
            anim: Animation = anim
            name: str = anim.name
            while len(name) < 0x1E:
                name += "\0"
            rdw.write(name)
        for anim in self.anims:
            anim: Animation = anim
            rdw.writeU32(anim.n_frames)
            for j in range(anim.n_frames):
                rdw.writeU32(anim.framesIDs[j])
                rdw.writeU32(anim.framesUNK[j])
                rdw.writeU32(anim.imageIndexes[j])

        # Uninplemented Variables
        rdw.write(self.vars)

        return rdw.data

    def export_frame_to_image(self, frame_i):
        image: Image = self.images[frame_i]
        data = image.export_image(self.palette)
        return data

    def import_frame_to_image_nopal(self, frame_i, image):
        self.images[frame_i] = Image(self.colordepth)
        self.images[frame_i].import_image(self.palette, image)

    def import_frame_to_image(self, frame_i, image: PIL.Image.Image):
        all = self.get_all_images()

        all_list = [img.export_image(self.palette) for img in self.images]
        all_list[frame_i] = image

        total_width = image.width+all.width
        total_height = max(image.height, all.height)
        forpalette = PIL.Image.new("RGB", (total_width, total_height), self.palette.colours[0])
        forpalette.paste(image)
        forpalette.paste(all, (image.width, 0))
        forpalette = forpalette.quantize(2**self.colordepth).convert("RGB")
        newcolors = forpalette.getcolors(2**self.colordepth)
        newcolors = [x[1] for x in newcolors]
        if (0, 248, 0) in newcolors:
            newcolors.remove((0, 248, 0))
        newcolors = [(0, 248, 0),] + newcolors
        self.palette.colours = newcolors

        for i in range(len(self.images)):
            self.images[i].import_image(self.palette, all_list[i])



    def get_all_images(self):
        total_w = 0
        max_h = 0
        for image in self.images:
            total_w += image.w
            max_h = max(max_h, image.h)
        final = PIL.Image.new("RGB", (total_w, max_h), self.palette.colours[0])
        x = 0
        for image in self.images:
            final.paste(image.export_image(self.palette), (x, 0))
            x += image.w
        return final

    def add_frame(self, image):
        return len(self.images) - 1

    def remove_frame(self, frame_i):
        pass

    ...  # More functions


if __name__ == "__main__":
    a = Arc()
    a.import_arc(open("../recources/a.arc", "rb").read())
    b = a.export_frame_to_image(0)
    b.show("hi")
    c: PIL.Image.Image = PIL.Image.open("../recources/huh.png")
    a.palette.colours = [x[1] for x in c.getcolors(2**a.colordepth)]
    a.import_frame_from_image(0, c)

    open("../recources/e.arc", "wb+").write(a.export_arc())
