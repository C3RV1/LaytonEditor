from formats.binary import BinaryReader, BinaryWriter
from typing import *


class HuffTreeNode:
    def __init__(self, is_data: bool, data: Optional[int] = None, parent=None, child0=None, child1=None):
        self.is_data: bool = is_data
        self.data: Optional[int] = data
        self.parent: Optional[HuffTreeNode] = parent
        self.child0: Optional[HuffTreeNode] = child0
        self.child1: Optional[HuffTreeNode] = child1
        if self.child0:
            self.child0.parent = self
        if self.child1:
            self.child1.parent = self

    @classmethod
    def from_rdr(cls, rdr: BinaryReader, is_data: bool, relative_offset, max_stream_pos, parent=None):
        self = cls(is_data, parent=parent)
        if rdr.c >= max_stream_pos:
            return
        self.data = rdr.read_uint8()
        if not is_data:
            offset = self.data & 0x3F
            zero_is_data = (self.data & 0x80) > 0
            one_is_data = (self.data & 0x40) > 0

            # off AND NOT == off XOR (off AND 1)
            zero_rel_offset = (relative_offset ^ (relative_offset & 1)) + offset * 2 + 2

            curr_stream_pos = rdr.c

            rdr.c += (zero_rel_offset - relative_offset) - 1

            # Node after 0
            self.child0 = HuffTreeNode.from_rdr(
                rdr, zero_is_data, zero_rel_offset, max_stream_pos, parent=self)
            # Node after 1 directly located after the node after 0
            self.child1 = HuffTreeNode.from_rdr(
                rdr, one_is_data, zero_rel_offset + 1, max_stream_pos, parent=self)

            # reset stream
            rdr.c = curr_stream_pos
        return self

    def to_wtr(self, wtr: BinaryWriter):
        queue: List[HuffTreeNode] = [self]
        while len(queue):
            node: HuffTreeNode = queue[0]
            queue = queue[1:]
            if node.is_data:
                wtr.write_ubyte(node.data)
            else:
                data = (len(queue) // 2) & 0x3f
                if node.child0.is_data:
                    data |= 0x80
                if node.child1.is_data:
                    data |= 0x40
                wtr.write_ubyte(data)
                queue.append(node.child0)
                queue.append(node.child1)

    @property
    def depth(self):
        if self.parent:
            return self.parent.depth + 1
        return 0

    @property
    def is_child1(self) -> bool:
        return self.parent.child1 == self

    @property
    def is_filled(self):
        return self.data is None


def compress(input_data: bytes, datablock_size=None) -> bytes:
    if datablock_size is None:
        # Return the smallest we can
        return min(compress(input_data, 4), compress(input_data, 8), key=lambda x: len(x))

    assert datablock_size in [4, 8]

    wtr = BinaryWriter()

    wtr.write_uint8(0x20 | datablock_size)  # huffman identifier

    wtr.write_uint24(len(input_data) if len(input_data) < 0xffffff else 0)
    if len(input_data) > 0xffffff:
        wtr.write_uint32(len(input_data))

    # build frequency table
    frequencies = [0 for _ in range(0x100 if datablock_size == 8 else 0x10)]
    for b in input_data:
        if datablock_size == 8:
            frequencies[b] += 1
        else:
            b0, b1 = b & 0xf, b >> 4
            frequencies[b0] += 1
            frequencies[b1] += 1

    # build the huffman tree
    node_count = 0
    leaf_queue = []
    node_queue = []
    leaves: List[HuffTreeNode] = [None for _ in range(0x100 if datablock_size == 8 else 0x10)]
    for i in range(0x10 if datablock_size == 4 else 0x100):
        if frequencies[i] == 0:
            continue
        node = HuffTreeNode(True, data=i)
        leaves[i] = node
        leaf_queue.append((frequencies[i], node))
        node_count += 1

    if len(leaf_queue) < 2:  # Add an unused node to make it possible
        node = HuffTreeNode(True, data=0)
        leaves[0] = node
        leaf_queue.append((1, node))
        node_count += 1

    def take_lowest(queue0: List[Tuple[int, HuffTreeNode]],
                    queue1: List[Tuple[int, HuffTreeNode]]) -> Tuple[int, HuffTreeNode]:
        if queue0:
            lowest_queue0 = min(queue0, key=lambda x: x[0])
        elif queue1:
            lowest_queue1 = min(queue1, key=lambda x: x[0])
            queue1.remove(lowest_queue1)
            return lowest_queue1
        else:
            raise ValueError("take_lowest() arg are empty sequences")
        if queue1:
            lowest_queue1 = min(queue1, key=lambda x: x[0])
        else:
            queue0.remove(lowest_queue0)
            return lowest_queue0
        if lowest_queue0[0] < lowest_queue1[0]:
            queue0.remove(lowest_queue0)
            return lowest_queue0
        else:
            queue1.remove(lowest_queue1)
            return lowest_queue1

    while len(leaf_queue) + len(node_queue) > 1:
        one_prio, one = take_lowest(leaf_queue, node_queue)
        two_prio, two = take_lowest(leaf_queue, node_queue)

        newnode = HuffTreeNode(False, child0=one, child1=two)
        node_queue.append((one_prio + two_prio, newnode))
        node_count += 1

    root: HuffTreeNode = node_queue[0][1]

    # write the huffman tree
    wtr.write_uint8((node_count - 1) // 2)
    root.to_wtr(wtr)

    datablock = 0
    bits_left = 32
    cached_byte = 0
    for i in range(len(input_data) * (2 if datablock_size == 4 else 1)):
        if datablock_size == 4:
            if i & 1 == 0:
                cached_byte = input_data[i // 2]
                data = cached_byte & 0xf
            else:
                data = cached_byte >> 4
        else:
            data = input_data[i]

        node = leaves[data]
        depth = node.depth
        path: List[bool] = [False for _ in range(depth)]
        for d in range(depth):
            path[depth - d - 1] = node.is_child1
            node = node.parent
        for p in path:
            if bits_left == 0:
                wtr.write_uint32(datablock)
                datablock = 0
                bits_left = 32
            bits_left -= 1
            if p:
                datablock |= 1 << bits_left
    if bits_left != 32:
        wtr.write_uint32(datablock)
    return wtr.getvalue()


def decompress(data: bytes) -> bytes:
    rdr = BinaryReader(data)
    wtr = BinaryWriter()
    compression_type = rdr.read_uint8()
    if compression_type == 0x24:
        blocksize = 4
    elif compression_type == 0x28:
        blocksize = 8
    else:
        raise Exception("Tried to decompress something as huffman that isn't huffman")
    ds = rdr.read_uint24()
    if ds == 0:
        rdr.read_uint32()

    # Read the tree
    treesize = (rdr.read_uint8() + 1) * 2
    tree_end = (rdr.c - 1) + treesize
    root_node = HuffTreeNode.from_rdr(rdr, False, 5, tree_end)
    rdr.c = tree_end

    # Decompress with the tree
    bitsleft = 0  # amount of bits left to read from {commands}
    current_size = 0
    current_node = root_node

    cashedbyte = -1

    while current_size < ds:
        # Find next reference to commands node
        while not current_node.is_data:
            if bitsleft == 0:
                data = rdr.read_uint32()
                bitsleft = 32

            bitsleft -= 1
            next_is_one = (data & (1 << bitsleft)) != 0
            if next_is_one:
                current_node = current_node.child1
            else:
                current_node = current_node.child0

        if blocksize == 8:
            current_size += 1
            wtr.write_uint8(current_node.data)

        elif blocksize == 4:
            if cashedbyte < 0:
                cashedbyte = current_node.data
            else:
                cashedbyte |= current_node.data << 4
                wtr.write_uint8(cashedbyte)
                current_size += 1
                cashedbyte = -1
        current_node = root_node

    return wtr.data
