import logging
from dataclasses import dataclass, field
from io import BytesIO
from math import floor, ceil, log
from typing import *
from typing import BinaryIO

import ndspy.color
import numpy as np
from PIL.ImageQt import ImageQt
from PySide6 import QtGui
from PIL import Image

from formats.binary import BinaryReader, BinaryWriter, SEEK_CUR
from formats.filesystem import FileFormat


# Calculate and write the sections
def get_nearest_power_of_2(x: int):
    possible_results = floor(log(x, 2)), ceil(log(x, 2))
    if x - 2 ** possible_results[1] < -7:
        return max(8, int(2 ** possible_results[0]))
    else:
        return max(8, int(2 ** possible_results[1]))


def calculate_power_of_2_steps(x: int):
    ret = 0
    while x > 0:
        ret += 1
        x -= get_nearest_power_of_2(x)
    return ret


@dataclass
class AnimationFrame:
    index: int
    duration: int
    image_index: int


@dataclass
class Animation:
    name: str = "Create an Animation"
    frames: List[AnimationFrame] = field(default_factory=list)
    child_image_x: int = 0
    child_image_y: int = 0
    child_image_animation_index: int = 0


class AniSprite(FileFormat):
    colordepth: int = 8
    images: List[np.ndarray] = []
    animations: List[Animation] = [Animation()]
    variables: dict = {f"Var{i}": [0, ] * 8 for i in range(16)}
    palette: np.ndarray = np.zeros((256, 4), np.uint8)
    child_image: str = ""

    _compressed_default = 2

    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)

        n_images = rdr.read_uint16()
        self.colordepth = 4 if rdr.read_uint16() == 3 else 8

        # import the images
        self.images = []
        for img_i in range(n_images):
            img_w = rdr.read_uint16()
            img_h = rdr.read_uint16()
            n_parts = rdr.read_uint16()

            img = np.zeros((img_h, img_w), np.uint8)

            rdr.seek(2, SEEK_CUR)
            for part_i in range(n_parts):
                part_x = rdr.read_uint16()
                part_y = rdr.read_uint16()
                part_w = 2 ** (3 + rdr.read_uint16())
                part_h = 2 ** (3 + rdr.read_uint16())

                part: np.ndarray
                if self.colordepth == 8:
                    part = np.frombuffer(rdr.read(part_h * part_w), np.uint8)
                    part = part.reshape((part_h, part_w))
                else:
                    bufpart = np.frombuffer(rdr.read(part_h * part_w // 2), np.uint8)
                    part = np.zeros((part_w * part_h), np.uint8)
                    part[0::2] = bufpart & 0xf
                    part[1::2] = bufpart >> 4
                    part = part.reshape((part_h, part_w))

                if (part_x + part_w) > img_w:
                    part_w = img_w - part_x
                if (part_y + part_h) > img_h:
                    part_h = img_h - part_y
                img[part_y:part_y + part_h, part_x:part_x + part_w] = part[:part_h, :part_w]

            self.images.append(img)

        palette_length = rdr.read_uint32()
        self.palette = np.zeros((palette_length, 4), np.uint8)
        for color_i in range(palette_length):
            self.palette[color_i] = ndspy.color.unpack255(rdr.read_uint16())
            if color_i:
                self.palette[color_i, 3] = 255

        rdr.seek(0x1E, SEEK_CUR)
        n_animations = rdr.read_uint32()
        animation_names = rdr.read_string_array(n_animations, 0x1e)
        animation_frame_sets = []
        for i in range(n_animations):
            n_frames = rdr.read_uint32()
            frame_indexes = rdr.read_uint32_array(n_frames)
            frame_durations = rdr.read_uint32_array(n_frames)
            image_indexes = rdr.read_uint32_array(n_frames)
            animation_frame_sets.append([
                AnimationFrame(index=frame_indexes[i], duration=frame_durations[i],
                               image_index=image_indexes[i])
                for i in range(n_frames)])
        self.animations = [Animation(name=animation_names[i], frames=animation_frame_sets[i])
                           for i in range(n_animations)]

        if rdr.read_uint16() != 0x1234:
            return  # We hit end of stream

        variable_labels = rdr.read_string_array(16, 16)
        variable_data = [[] for _ in range(16)]
        for _ in range(8):
            for var_i in range(16):
                variable_data[var_i].append(rdr.read_int16())

        self.variables = {variable_labels[i]: variable_data[i] for i in range(16)}

        for anim in self.animations:
            anim.child_image_x = rdr.read_uint16()
        for anim in self.animations:
            anim.child_image_y = rdr.read_uint16()
        for anim in self.animations:
            anim.child_image_animation_index = rdr.read_uint8()

        self.child_image = rdr.read_string(128)

    def write_stream(self, stream):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        wtr.write_uint16(len(self.images))
        wtr.write_uint16(3 if self.colordepth == 4 else 4)

        for img in self.images:
            img_h, img_w = img.shape
            wtr.write_uint16(img_w)
            wtr.write_uint16(img_h)

            # number of parts
            wtr.write_uint16(calculate_power_of_2_steps(img_w) *
                             calculate_power_of_2_steps(img_h))
            wtr.write_zeros(2)

            w_left, h_left = img_w, img_h
            part_x, part_y = 0, 0
            while h_left > 0:
                part_h = get_nearest_power_of_2(h_left)
                good_h = part_h
                h_left -= part_h
                w_left = img_w
                part_x = 0
                while w_left > 0:
                    part_w = get_nearest_power_of_2(w_left)
                    w_left -= part_w
                    part_h = good_h

                    wtr.write_uint16(part_x)
                    wtr.write_uint16(part_y)
                    wtr.write_uint16(int(log(part_w, 2)) - 3)
                    wtr.write_uint16(int(log(part_h, 2)) - 3)

                    part = np.zeros((part_h, part_w), np.uint8)

                    if part_x + part_w > img_w:
                        part_w = img_w - part_x
                    if part_y + part_h > img_h:
                        part_h = img_h - part_y

                    part[:part_h, :part_w] = img[part_y:part_y + part_h, part_x:part_x + part_w]

                    if self.colordepth == 8:
                        wtr.write(part.tobytes())
                    else:
                        h, w = part.shape
                        bufpart = part.reshape((w * h))
                        part_4bit = np.zeros((h * w // 2), np.uint8)
                        part_4bit[:] = bufpart[0::2] & 0xf | bufpart[1::2] << 4
                        wtr.write(part_4bit.tobytes())

                    part_x += part_w
                part_y += part_h

        wtr.write_uint32(len(self.palette))
        for color_i in range(len(self.palette)):
            self.palette[color_i]: np.ndarray
            self.palette[color_i, 3] = 0
            wtr.write_uint16(ndspy.color.pack255(*self.palette[color_i]))
            self.palette[color_i, 3] = 255

        wtr.write_zeros(0x1e)
        wtr.write_uint32(len(self.animations))

        for anim in self.animations:
            wtr.write_string(anim.name, 0x1e)
        for anim in self.animations:
            wtr.write_uint32(len(anim.frames))
            wtr.write_uint32_array([frame.index for frame in anim.frames])
            wtr.write_uint32_array([frame.duration for frame in anim.frames])
            wtr.write_uint32_array([frame.image_index for frame in anim.frames])

        wtr.write_uint16(0x1234)  # magic number probably

        variable_labels = list(self.variables)
        assert len(variable_labels) == 16
        wtr.write_string_array(variable_labels, 16)
        for dat_i in range(8):
            for var_l in variable_labels:
                wtr.write_int16(self.variables[var_l][dat_i])

        for anim in self.animations:
            wtr.write_uint16(anim.child_image_x)
        for anim in self.animations:
            wtr.write_uint16(anim.child_image_y)
        for anim in self.animations:
            wtr.write_uint8(anim.child_image_animation_index)

        wtr.write_string(self.child_image, 128)

        return stream

    @classmethod
    def fromstream(cls, stream: BinaryIO):
        return cls(file=stream)

    @classmethod
    def frombuffer(cls, buffer: bytes):
        (ret := cls()).read_stream(BytesIO(buffer))
        return ret

    def tobytes(self):
        self.write_stream((stream := BytesIO()))
        return stream.getvalue()

    def extract_image_pil(self, image_index) -> Image.Image:
        return Image.fromarray(self.palette[self.images[image_index]].astype(np.uint8), "RGBA")

    def extract_image_qt(self, image_index) -> QtGui.QPixmap:
        image = self.extract_image_pil(image_index)
        width, height = image.size
        image = image.resize((width * 2, height * 2), resample=Image.Resampling.NEAREST)
        qim = ImageQt(image)
        return QtGui.QPixmap.fromImage(qim)

    def replace_image_pil(self, image_index, image: Optional[Image.Image]):  # also used to recreate palette
        # TODO: Change colordepth
        if image_index is not None:
            logging.info(f"Animation {self._last_filename} replacing image {image_index} to image of size {image.size}")
            if image_index < 0:
                image_index = len(self.images) + image_index
            assert image_index < len(self.images)

            image = image.convert("RGBA")
        else:
            logging.info(f"Animation {self._last_filename} reworking palette")
        # Create the new palette by adding all the images together into 1 pil Image and then quantizing it.
        # TODO: Prioritize inserted image colors in palette
        # TODO: Bulk import images instead?
        comb_w = max([img.shape[1] for img in self.images])
        comb_h = sum([img.shape[0] for img in self.images])
        if image_index is not None:
            comb_w = max(comb_w, image.width)
            comb_h = comb_h + image.height
        comb = Image.new("RGBA", (comb_w, comb_h))
        comb_y = 0
        for i in range(len(self.images)):
            if i == image_index:
                comb.paste(image, (0, comb_y))
                comb_y += image.height
            else:
                comb.paste(self.extract_image_pil(i), (0, comb_y))
                comb_y += self.images[i].shape[0]
        comb = comb.convert("P", colors=(
            255 if self.colordepth == 8 else 15))  # 255 because we need to add the transparent color
        colors = np.frombuffer(comb.palette.palette, np.uint8).reshape((-1, 4))
        indexes = np.asarray(comb, np.uint8)

        # add the regular transparent color
        colors = np.concatenate(([[0, 255, 0, 0]], colors[:(255 if self.colordepth == 8 else 15)]))
        indexes = indexes + 1  # we added our transparent color at the front of the palette
        for i, (*_, a) in enumerate(colors):
            if a < 128:
                indexes[indexes == i] = 0  # transparent color, change to the transparent type

        self.palette = np.zeros((len(colors), 4), np.uint8)
        self.palette[:len(colors)] = colors

        comb_y = 0
        for i in range(len(self.images)):
            h, w, *_ = self.images[i].shape if i != image_index else (image.height, image.width)
            self.images[i] = indexes[comb_y:comb_y + h, :w]
            comb_y += h

    def append_image_pil(self, image: Image.Image):
        logging.info(f"Animation {self._last_filename} appending image of size {image.size}")
        self.images.append(np.ndarray((0, 0), np.uint8))
        self.replace_image_pil(-1, image)

    def insert_image_pil(self, image_index, image: Image.Image):
        logging.info(f"Animation {self._last_filename} inserting image of size {image.size} to idx {image_index}")
        self.images.insert(image_index, np.ndarray((0, 0), np.uint8))
        for anim in self.animations:
            for i, frame in enumerate(anim.frames):
                if frame.image_index >= image_index:
                    anim.frames[i].image_index += 1
        self.replace_image_pil(image_index, image)

    def remove_image(self, image_index):
        logging.info(f"Animation {self._last_filename} removing image of idx {image_index}")
        self.images.pop(image_index)

        for anim in self.animations:
            frames_to_remove = []
            for i, frame in enumerate(anim.frames):
                if frame.image_index == image_index:
                    frames_to_remove.append(frame)
                elif frame.image_index > image_index:
                    anim.frames[i].image_index -= 1
            for frame in frames_to_remove:
                anim.frames.remove(frame)
        self.replace_image_pil(None, None)  # Recreate palette

    def __bytes__(self):
        return self.tobytes()


class AniSubSprite(AniSprite):
    def read_stream(self, stream: BinaryIO):
        rdr = stream if isinstance(stream, BinaryReader) else BinaryReader(stream)

        n_images = rdr.read_uint16()
        self.colordepth = 4 if rdr.read_uint16() == 3 else 8
        palette_length = rdr.read_uint32()

        # import the images
        self.images = []
        for img_i in range(n_images):
            img_w = rdr.read_uint16()
            img_h = rdr.read_uint16()
            n_parts = rdr.read_uint16()

            img = np.zeros((img_h, img_w), np.uint8)

            rdr.seek(2, SEEK_CUR)
            for part_i in range(n_parts):
                _part_glb_x = rdr.read_uint16()
                _part_glb_y = rdr.read_uint16()
                part_x = rdr.read_uint16()
                part_y = rdr.read_uint16()
                part_w = 2 ** (3 + rdr.read_uint16())
                part_h = 2 ** (3 + rdr.read_uint16())
                part: np.ndarray
                if self.colordepth == 8:
                    part = np.frombuffer(rdr.read(part_h * part_w), np.uint8)
                else:
                    bufpart = np.frombuffer(rdr.read(part_h * part_w // 2), np.uint8)
                    part = np.zeros((part_w * part_h), np.uint8)
                    part[0::2] = bufpart & 0xf
                    part[1::2] = bufpart >> 4
                    part = part.reshape((part_h, part_w))
                part.resize((part_h // 8, part_w // 8, 8, 8))
                part_w = min(img_w - part_x, part_w)
                part_h = min(img_h - part_y, part_h)
                for yt, yslice in enumerate(part):
                    for xt, xslice in enumerate(yslice):
                        offset_y = part_y + yt * 8
                        offset_x = part_x + xt * 8
                        end_y = min(part_y + yt * 8 + 8, part_y + part_h)
                        end_x = min(part_x + xt * 8 + 8, part_x + part_w)
                        copy_h = max(end_y - offset_y, 0)
                        copy_w = max(end_x - offset_x, 0)
                        img[offset_y:end_y,
                            offset_x:end_x] = \
                            xslice[:copy_h, :copy_w]

            self.images.append(img)

        self.palette = np.zeros((256, 4), np.uint8)
        for color_i in range(palette_length):
            self.palette[color_i] = ndspy.color.unpack255(rdr.read_uint16())
            if color_i:
                self.palette[color_i, 3] = 255

        rdr.seek(0x1E, SEEK_CUR)
        n_animations = rdr.read_uint32()
        animation_names = rdr.read_string_array(n_animations, 0x1e)
        animation_frame_sets = []
        for i in range(n_animations):
            n_frames = rdr.read_uint32()
            frame_indexes = rdr.read_uint32_array(n_frames)
            frame_durations = rdr.read_uint32_array(n_frames)
            image_indexes = rdr.read_uint32_array(n_frames)
            animation_frame_sets.append([
                AnimationFrame(index=frame_indexes[i], duration=frame_durations[i],
                               image_index=image_indexes[i])
                for i in range(n_frames)])
        self.animations = [Animation(name=animation_names[i], frames=animation_frame_sets[i])
                           for i in range(n_animations)]

        if rdr.read_uint16() != 0x1234:
            return  # We hit end of stream

        variable_labels = rdr.read_string_array(16, 16)
        variable_data = [[] for _ in range(16)]
        for _ in range(8):
            for var_i in range(16):
                variable_data[var_i].append(rdr.read_int16())

        self.variables = {variable_labels[i]: variable_data[i] for i in range(16)}

        for anim in self.animations:
            anim.child_image_x = rdr.read_int16()
        for anim in self.animations:
            anim.child_image_y = rdr.read_int16()
        for anim in self.animations:
            anim.child_spr_index = rdr.read_uint8()

        self.child_image = rdr.read_string(128)

    def write_stream(self, stream=None):
        wtr = stream if isinstance(stream, BinaryWriter) else BinaryWriter(stream)

        wtr.write_uint16(len(self.images))
        wtr.write_uint16(3 if self.colordepth == 4 else 4)
        wtr.write_uint32(256 if self.colordepth == 8 else 16)

        for img in self.images:
            img_h, img_w = img.shape
            wtr.write_uint16(img_w)
            wtr.write_uint16(img_h)

            # number of parts
            wtr.write_uint16(calculate_power_of_2_steps(img_w) *
                             calculate_power_of_2_steps(img_h))
            wtr.write_zeros(2)

            w_left, h_left = img_w, img_h
            part_x, part_y = 0, 0
            while h_left > 0:
                part_h = get_nearest_power_of_2(h_left)
                good_h = part_h
                h_left -= part_h
                w_left = img_w
                part_x = 0
                while w_left > 0:
                    part_w = get_nearest_power_of_2(w_left)
                    w_left -= part_w
                    part_h = good_h

                    wtr.write_uint16(part_x)  # TODO: THIS
                    wtr.write_uint16(part_y)
                    wtr.write_uint16(part_x)
                    wtr.write_uint16(part_y)
                    wtr.write_uint16(int(log(part_w, 2)) - 3)
                    wtr.write_uint16(int(log(part_h, 2)) - 3)

                    part = np.zeros((part_h // 8, part_w // 8, 8, 8), np.uint8)

                    if part_x + part_w > img_w:
                        part_w += img_w - part_x - part_w
                    if part_y + part_h > img_h:
                        part_h += img_h - part_y - part_h

                    for yt, yslice in enumerate(part):
                        for xt, xslice in enumerate(yslice):
                            xslice[:part_h - 8 * yt, :part_w - 8 * xt] = \
                                img[part_y + yt * 8:min(part_y + yt * 8 + 8, part_y + part_h),
                                    part_x + xt * 8:min(part_x + xt * 8 + 8, part_x + part_w)]

                    if self.colordepth == 8:
                        wtr.write(part.tobytes())
                    else:
                        _, hw = part.shape
                        part_4bit: np.ndarray = part[:hw // 2] << 4 | part[hw // 2:]
                        wtr.write(part_4bit.tobytes())

                    part_x += part_w
                part_y += part_h

        for color_i in range(256 if self.colordepth == 8 else 16):
            self.palette[color_i]: np.ndarray
            wtr.write_uint16(ndspy.color.pack255(*self.palette[color_i]))

        wtr.write_zeros(0x1e)
        wtr.write_uint32(len(self.animations))

        for anim in self.animations:
            wtr.write_string(anim.name, 0x1e)
        for anim in self.animations:
            wtr.write_uint32(len(anim.frames))
            wtr.write_uint32_array([frame.index for frame in anim.frames])
            wtr.write_uint32_array([frame.duration for frame in anim.frames])
            wtr.write_uint32_array([frame.image_index for frame in anim.frames])

        wtr.write_uint16(0x1234)  # magic number probably

        variable_labels = list(self.variables)
        assert len(variable_labels) == 16
        wtr.write_string_array(variable_labels, 16)
        for dat_i in range(8):
            for var_l in variable_labels:
                wtr.write_uint16(self.variables[var_l][dat_i])

        for anim in self.animations:
            wtr.write_int16(anim.child_image_x)
        for anim in self.animations:
            wtr.write_int16(anim.child_image_y)
        for anim in self.animations:
            wtr.write_uint8(anim.child_image_animation_index)

        wtr.write_string(self.child_image, 128)

        return BinaryReader.data
