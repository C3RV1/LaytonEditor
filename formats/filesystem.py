import io
import os
import re

import ndspy.rom
from ndspy.fnt import *

from formats.binary import *
from .compression import *


class Archive:
    files: List[bytes] = []
    opened_files: list = []

    def open(self, file: Union[AnyStr, int], mode: str = "rb") -> Union[io.BytesIO, io.TextIOWrapper]:
        pass


class RomFile(io.BytesIO):
    def __init__(self, archive, index: int, opperation: str = "w"):
        if opperation not in ["r", "w", "a"]:
            raise NotImplementedError(f"opperation: {opperation}")
        self.archive = archive
        self.id = index
        self.opp = opperation
        if self not in self.archive.opened_files:
            self.archive.opened_files.append(self)
        super().__init__(self.archive.files[index] if opperation in ["r", "a"] else b"")
        if opperation == "a":
            self.read()

    def writable(self) -> bool:
        return self.opp in ["w", "a"]

    def close(self):
        self.flush()
        super().close()
        if self in self.archive.opened_files:
            self.archive.opened_files.remove(self)

    def fileno(self) -> int:
        return self.id

    def flush(self):
        if not self.closed:
            if self.opp != "r":
                self.archive.files[self.id] = self.getvalue()
            super().flush()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, *args):
        self.close()
        super().__exit__(*args)

    def __del__(self):
        self.close()


class CompressedIOWrapper(io.BytesIO):
    def __init__(self, stream, double_typed: Optional[bool] = None):
        self.stream = stream

        current, self.double_typed = decompress(stream.read(), double_typed)

        super().__init__(current)

    def close(self):
        self.flush()
        super().close()
        self.stream.close()

    def flush(self):
        if self.stream.writable():
            self.stream.truncate(0)
            self.stream.seek(0)
            self.stream.write(compress(self.getvalue(), double_typed=self.double_typed))
        super().flush()
        self.stream.flush()

    def __enter__(self):
        super().__enter__()
        return self


class NintendoDSRom(ndspy.rom.NintendoDSRom, Archive):
    opened_files: List[RomFile]
    _loaded_archives: dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._opened_files = []
        self._loaded_archives: Dict[str, PlzArchive] = {}

    def get_archive(self, path):
        if path not in self._loaded_archives:
            self._loaded_archives[path] = PlzArchive(path, rom=self)
        return self._loaded_archives[path]

    def save(self, *args, **kwargs):
        for arch in self._loaded_archives:
            self._loaded_archives[arch].save()
        return super(NintendoDSRom, self).save(*args, **kwargs)

    # TODO: Unify archive opening and make sure archive are opened only once
    def open(self, file: Union[AnyStr, int], mode: str = "rb") -> Union[io.BytesIO, io.TextIOWrapper]:
        match = re.findall(r"^([rwa])(b?)(\+?)$", mode)
        if not match:
            raise ValueError(f"invalid mode: '{mode}'")
        create = False
        text = True
        if match:
            if match[0][1] == "b":
                text = False
            if match[0][2] == "+":
                create = True

        if isinstance(file, int):
            fileid = file
        else:
            fileid = self.filenames.idOf(file)
            if not fileid and create:
                fileid = self.add_file(file)
                if not fileid:
                    raise FileNotFoundError(f"file '{file}' could not be opened nor created")
            if not fileid:
                raise FileNotFoundError(f"file '{file}' could not be opened")

        romfile = RomFile(self, fileid, match[0][0])
        if text:
            return io.TextIOWrapper(romfile)
        return romfile

    def add_file(self, file: str) -> Optional[int]:
        foldername, filename = os.path.split(file)
        folder_add = self.filenames[foldername]
        new_file_id = folder_add.firstID + len(folder_add.files)

        # Insert our new file into this ID
        self.files.insert(new_file_id, b"")

        # Add our file to the folder
        folder_add.files.append(filename)

        # Change the firstID of all the folders after our base folder.
        def increment_first_index_if_needed(new_id, root: Folder):
            if root.firstID >= new_id and root != folder_add:
                root.firstID += 1

            for fd in root.folders:
                increment_first_index_if_needed(new_id, fd[1])

        increment_first_index_if_needed(new_file_id, self.filenames)

        # increment the id of loaded files after our base id
        for fp in self._opened_files:
            if fp.id > new_file_id:
                fp.id += 1

            if fp.id == new_file_id:
                fp.close()

        return new_file_id

    def remove_file(self, file: str):
        foldername, filename = os.path.split(file)
        folder: Folder = self.filenames[foldername]
        fileid = self.filenames.idOf(file)
        folder.files.remove(filename)
        del self.files[fileid]

        def decrement_first_index_if_needed(removed_id, root: Folder):
            if root.firstID > removed_id:
                root.firstID -= 1

            for fd in root.folders:
                decrement_first_index_if_needed(removed_id, fd[1])

        decrement_first_index_if_needed(fileid, self.filenames)
        for fp in self._opened_files:
            if fp.id > fileid:
                fp.id -= 1

            if fp.id == fileid:
                fp.close()

    def rename_file(self, old, new):
        with self.open(old, "rb") as f:
            data = f.read()
        self.remove_file(old)
        with self.open(new, "wb+") as f:
            f.write(data)

    @staticmethod
    def folder_split(path) -> List[str]:
        return [x for x in path.split("/") if x]

    def folder_get_parent(self, path) -> Folder:
        *basedirs, subdir = self.folder_split(path)
        if basedirs:
            base_path = "/".join(basedirs) + "/"
            return self.filenames[base_path]
        else:  # The folder is located at the root.
            return self.filenames

    def add_folder(self, path):
        parent = self.folder_get_parent(path)
        new_folder = Folder(firstID=len(self.files))
        parent.folders.append((self.folder_split(path)[-1], new_folder))

    def remove_folder(self, path):
        folder = self.filenames[path]
        if not folder:
            raise Exception(f"Directory {path} does not exist.")
        if folder.files or folder.folders:
            raise Exception(f"Directory {path} not empty.")

        parent = self.folder_get_parent(path)

        parent.folders.remove((self.folder_split(path)[-1], folder))

    def rename_folder(self, oldpath, newpath):
        folder = self.filenames[oldpath]

        # get parents
        oldparent = self.folder_get_parent(oldpath)
        newparent = self.folder_get_parent(newpath)

        # generate folder items.
        oldfolderitem = (self.folder_split(oldpath)[-1], folder)
        newfolderitem = (self.folder_split(newpath)[-1], folder)

        if oldparent != newparent:
            oldparent.folders.remove(oldfolderitem)
            newparent.folders.append(newfolderitem)
        else:  # same parent, keep the folder index
            index = oldparent.folders.index(oldfolderitem)
            newparent.folders[index] = newfolderitem


class FileFormat:
    _compressed_default = False

    _last_compressed = _compressed_default
    _last_filename: Optional[str] = None
    _last_rom: Archive = None

    def __init__(self, filename: str = None, file=None, compressed=None, rom: NintendoDSRom = None, **kwargs):
        if filename is not None:
            self._last_filename = filename
            self._last_rom = rom
            file = rom.open(filename, "rb") if rom else open(filename, "rb")

        if compressed is None:
            compressed = self._compressed_default
        if compressed:
            file = CompressedIOWrapper(file, double_typed=(compressed == 2))
        self._last_compressed = compressed

        if file is not None:
            self.read_stream(file)

        for kwarg in kwargs:
            self.__dict__[kwarg] = kwargs[kwarg]

        if filename is not None:
            file.close()  # we opened the file here, we close the file here

    def save(self, filename=None, file=None, compressed=None, rom: NintendoDSRom = None):
        should_close = False
        if not file:
            should_close = True
            if filename:
                file = rom.open(filename, "wb+") if rom else open(filename, "wb+")
                self._last_filename = filename
                self._last_rom = rom
            elif self._last_filename:
                if self._last_rom:
                    file = self._last_rom.open(self._last_filename, "wb+")
                else:
                    open(self._last_filename, "wb+")

        if compressed is None:
            compressed = self._last_compressed
        if compressed:
            file = CompressedIOWrapper(file, double_typed=(compressed == 2))

        self.write_stream(file)

        # Close file if we opened it here
        if should_close:
            file.close()

    def read_stream(self, stream):
        pass

    def write_stream(self, stream):
        pass


class PlzArchive(Archive, FileFormat):
    # for saving
    last_filename: Optional[str] = None
    last_rom: Optional[NintendoDSRom] = None

    _compressed_default = 1

    filenames: List[str] = []
    files: List[bytes] = []

    def read_stream(self, stream):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)

        self.filenames = []
        self.files = []

        headersize = rdr.read_uint32()
        filesize = rdr.read_uint32()
        assert rdr.read(4) == b"PCK2"
        rdr.seek(headersize)

        while rdr.c < filesize:
            start_pos = rdr.c

            fileheader_size = rdr.read_uint32()
            filetotal_size = rdr.read_uint32()
            rdr.seek(4, io.SEEK_CUR)
            file_size = rdr.read_uint32()

            filename = rdr.read_string(encoding="shift-jis")

            rdr.seek(start_pos + fileheader_size)
            file = rdr.read(file_size)
            rdr.seek(start_pos + filetotal_size)

            self.filenames.append(filename)
            self.files.append(file)

    def write_stream(self, stream):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        wtr.write_uint32(16)
        wtr.write_uint32(0)  # placeholder filesize
        wtr.write(b"PCK2")
        wtr.write_uint32(0)

        for i in range(len(self.files)):
            headersize = 16 + len(self.filenames[i]) + 1
            headersize += 4 - headersize % 4

            totalsize = headersize + len(self.files[i])
            totalsize += 4 - totalsize % 4
            c = wtr.c
            wtr.write_uint32(headersize)
            wtr.write_uint32(totalsize)
            wtr.write_uint32(0)
            wtr.write_uint32(len(self.files[i]))

            wtr.write_string(self.filenames[i])
            wtr.seek(c + headersize)
            wtr.write(self.files[i])
            # Seek while adding bytes
            while wtr.c != c + totalsize:
                wtr.write_uint8(0)

        filesize = len(wtr)
        wtr.seek(4)
        wtr.write_uint32(filesize)

    def open(self, file: Union[AnyStr, int], mode: str = "rb") -> Union[io.BytesIO, io.TextIOWrapper]:
        match = re.findall(r"^([rwa])(b?)(\+?)$", mode)
        if not match:
            raise ValueError(f"invalid mode: '{mode}'")
        create = False
        text = True
        if match:
            if match[0][1] == "b":
                text = False
            if match[0][2] == "+":
                create = True

        if isinstance(file, int):
            fileid = file
        else:
            try:
                fileid = self.filenames.index(file)
            except:
                fileid = None
            if fileid is None and create:
                fileid = self.add_file(file)
                if not fileid:
                    raise FileNotFoundError(f"file '{file}' could not be opened nor created")
            if fileid is None:
                raise FileNotFoundError(f"file '{file}' could not be opened")

        romfile = RomFile(self, fileid, match[0][0])
        if text:
            return io.TextIOWrapper(romfile)
        return romfile

    def add_file(self, filename: str):
        new_file_id = len(self.files)
        self.files.append(b"")
        self.filenames.append(filename)

        return new_file_id

    def remove_file(self, filename: str):
        if filename not in self.filenames:
            return
        index = self.filenames.index(filename)
        self.files.pop(index)
        self.filenames.pop(index)

    def rename_file(self, old, new):
        with self.open(old, "rb") as f:
            data = f.read()
        self.remove_file(old)
        with self.open(new, "wb+") as f:
            f.write(data)
