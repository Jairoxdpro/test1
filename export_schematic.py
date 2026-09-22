#!/usr/bin/env python3
"""
Exporta la casa medieval a formato .schematic (WorldEdit) y .json
Compatible con Minecraft Java Edition 26.2
"""

import struct
import gzip
import io
import json


class NBTWriter:
    def __init__(self):
        self.buffer = io.BytesIO()

    def _write_header(self, tag_type, name):
        self.buffer.write(struct.pack('>B', tag_type))
        if name is not None:
            nb = name.encode('utf-8')
            self.buffer.write(struct.pack('>H', len(nb)))
            self.buffer.write(nb)

    def write_byte(self, name, value):
        self._write_header(1, name)
        self.buffer.write(struct.pack('>b', value))

    def write_short(self, name, value):
        self._write_header(2, name)
        self.buffer.write(struct.pack('>h', value))

    def write_int(self, name, value):
        self._write_header(3, name)
        self.buffer.write(struct.pack('>i', value))

    def write_string(self, name, value):
        self._write_header(8, name)
        vb = value.encode('utf-8')
        self.buffer.write(struct.pack('>H', len(vb)))
        self.buffer.write(vb)

    def begin_compound(self, name):
        self._write_header(10, name)

    def end_compound(self):
        self.buffer.write(b'\x00')

    def begin_list(self, name, tag_type, length):
        self._write_header(9, name)
        self.buffer.write(struct.pack('>bI', tag_type, length))

    def write_byte_array(self, name, data):
        self._write_header(7, name)
        self.buffer.write(struct.pack('>i', len(data)))
        self.buffer.write(data)

    def get_bytes(self):
        return self.buffer.getvalue()


# IDs legacy para formato .schematic
LEGACY_IDS = {
    'air':                    (0, 0),  'cobblestone':          (4, 0),
    'oak_planks':             (5, 0),  'spruce_planks':        (5, 1),
    'dark_oak_planks':        (5, 5),  'oak_log':             (17, 0),
    'stripped_oak_log':       (17, 0), 'spruce_log':          (17, 1),
    'oak_slab':              (44, 2),  'oak_slab_top':        (44, 10),
    'cinnabar_slab':         (44, 2),  'cinnabar_slab_top':   (44, 10),
    'sulfur_slab':           (44, 2),  'cinnabar_brick_slab': (44, 2),
    'stone_bricks':          (98, 0),  'mossy_stone_bricks':  (98, 1),
    'bricks':                (45, 0),  'glass':               (20, 0),
    'glass_pane':           (102, 0),  'oak_stairs_s':        (53, 0),
    'oak_stairs_n':          (53, 2),  'oak_stairs_w':        (53, 3),
    'oak_stairs_e':          (53, 1),  'spruce_stairs_s':    (134, 0),
    'spruce_stairs_n':      (134, 2),  'spruce_stairs_w':    (134, 3),
    'spruce_stairs_e':      (134, 1),  'cinnabar_stairs_s':   (53, 0),
    'cinnabar_stairs_n':     (53, 2),  'cinnabar_stairs_e':   (53, 1),
    'cinnabar_stairs_w':     (53, 3),  'cinnabar_brick_stairs_s': (53, 0),
    'polished_cinnabar_stairs_s': (53, 0), 'sulfur_stairs_s': (53, 0),
    'oak_door_lower_s':      (64, 1),  'oak_door_upper_s':    (64, 9),
    'oak_fence':             (85, 0),  'oak_fence_gate':     (107, 0),
    'torch':                 (50, 5),  'lantern':             (50, 5),
    'hanging_lantern':       (50, 5),  'chest':               (54, 2),
    'crafting_table':        (58, 0),  'furnace':             (61, 2),
    'bookshelf':             (47, 0),  'barrel':              (54, 2),
    'campfire':              (50, 5),  'flower_pot':         (140, 0),
    'red_tulip':             (38, 4),  'dandelion':           (37, 0),
    'golden_dandelion':      (37, 0),  'gravel':              (13, 0),
    'grass_block':            (2, 0),  'dirt_path':            (2, 0),
    'white_carpet':         (171, 0),  'white_bed_n':         (26, 0),
    'white_bed_s':           (26, 0),  'straw_bed_n':         (26, 0),
    'straw_bed_s':           (26, 0),  'cushion':            (171, 0),
    'ladder_s':              (65, 2),  'cobblestone_wall':   (139, 0),
    'cinnabar':               (1, 0),  'cinnabar_bricks':     (45, 0),
    'polished_cinnabar':      (1, 3),  'chiseled_cinnabar':   (98, 3),
    'sulfur':                 (1, 1),  'polished_sulfur':      (1, 2),
    'sulfur_bricks':         (98, 1),  'chiseled_sulfur':     (98, 3),
    'brick_wall':           (139, 0),
}


def export_schematic(blocks, filename, width, height, depth, min_x, min_y, min_z):
    total = width * height * depth
    block_bytes = bytearray(total)
    data_bytes = bytearray(total)

    for (bx, by, bz), block_key in blocks.items():
        x, y, z = bx - min_x, by - min_y, bz - min_z
        if 0 <= x < width and 0 <= y < height and 0 <= z < depth:
            idx = y * width * depth + z * width + x
            bid, bdata = LEGACY_IDS.get(block_key, (0, 0))
            block_bytes[idx] = bid & 0xFF
            data_bytes[idx] = bdata & 0xFF

    w = NBTWriter()
    w.begin_compound('')
    w.write_string('Materials', 'Alpha')
    w.write_short('Width', width)
    w.write_short('Height', height)
    w.write_short('Length', depth)
    w.write_short('WEOffsetX', 0)
    w.write_short('WEOffsetY', 0)
    w.write_short('WEOffsetZ', 0)
    w.write_byte_array('Blocks', bytes(block_bytes))
    w.write_byte_array('Data', bytes(data_bytes))
    w.begin_list('Entities', 10, 0)
    w.begin_list('TileEntities', 10, 0)
    w.end_compound()

    raw = w.get_bytes()
    with gzip.open(filename, 'wb') as f:
        f.write(raw)


def main():
    from generate_house import HouseBuilder, BLOCKS

    print("📦 Exportando casa medieval para Minecraft Java 26.2...")

    house = HouseBuilder(width=17, height=13, depth=15)
    house.build()

    min_x = min(b[0] for b in house.blocks)
    max_x = max(b[0] for b in house.blocks)
    min_y = min(b[1] for b in house.blocks)
    max_y = max(b[1] for b in house.blocks)
    min_z = min(b[2] for b in house.blocks)
    max_z = max(b[2] for b in house.blocks)

    w, h, d = max_x - min_x + 1, max_y - min_y + 1, max_z - min_z + 1

    # .schematic
    export_schematic(house.blocks, 'medieval_house.schematic', w, h, d,
                     min_x, min_y, min_z)
    print(f"✅ medieval_house.schematic ({w}x{h}x{d}, {len(house.blocks)} bloques)")

    # .json
    data = {
        'name': 'Casa Medieval Bonita',
        'minecraft_version': '26.2',
        'data_version': 4903,
        'dimensions': {'width': w, 'height': h, 'depth': d},
        'total_blocks': len(house.blocks),
        'blocks': [
            {'x': x - min_x, 'y': y - min_y, 'z': z - min_z, 'block': b}
            for (x, y, z), b in sorted(house.blocks.items())
        ]
    }
    with open('medieval_house_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ medieval_house_data.json")

    print()
    print("📁 Archivos para Minecraft Java 26.2 (DataVersion 4903):")
    print("  • medieval_house.nbt        → Structure Block")
    print("  • medieval_house.schematic   → WorldEdit / Litematica")
    print("  • medieval_house_data.json   → Datos JSON")
    print("  • guia_casa_medieval.txt     → Guía de uso")


if __name__ == "__main__":
    main()
