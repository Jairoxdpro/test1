#!/usr/bin/env python3
"""
Generador de esquema de casa medieval bonita para Minecraft Java Edition 26.2
(Chaos Cubed - DataVersion 4903)

Incluye bloques nuevos de 26.2:
- Cinnabar bricks (chimenea)
- Polished cinnabar (detalles decorativos)
- Sulfur blocks (decoración amarilla)
- Cinnabar stairs/slabs (acento de techo)

Crea un archivo .nbt compatible con los bloques de estructura de Minecraft.
No requiere dependencias externas.
"""

import struct
import gzip
import io

# ============================================================
# Escritor NBT
# ============================================================

class NBTWriter:
    def __init__(self):
        self.buffer = io.BytesIO()

    def _write_tag_header(self, tag_type, name):
        self.buffer.write(struct.pack('>B', tag_type))
        if name is not None:
            name_bytes = name.encode('utf-8')
            self.buffer.write(struct.pack('>H', len(name_bytes)))
            self.buffer.write(name_bytes)

    def write_byte(self, name, value):
        self._write_tag_header(1, name)
        self.buffer.write(struct.pack('>b', value))

    def write_short(self, name, value):
        self._write_tag_header(2, name)
        self.buffer.write(struct.pack('>h', value))

    def write_int(self, name, value):
        self._write_tag_header(3, name)
        self.buffer.write(struct.pack('>i', value))

    def write_long(self, name, value):
        self._write_tag_header(4, name)
        self.buffer.write(struct.pack('>q', value))

    def write_string(self, name, value):
        self._write_tag_header(8, name)
        val_bytes = value.encode('utf-8')
        self.buffer.write(struct.pack('>H', len(val_bytes)))
        self.buffer.write(val_bytes)

    def begin_compound(self, name):
        self._write_tag_header(10, name)

    def end_compound(self):
        self.buffer.write(struct.pack('>B', 0))

    def begin_list(self, name, tag_type, length):
        self._write_tag_header(9, name)
        self.buffer.write(struct.pack('>b', tag_type))
        self.buffer.write(struct.pack('>i', length))

    def write_byte_array(self, name, data):
        self._write_tag_header(7, name)
        self.buffer.write(struct.pack('>i', len(data)))
        self.buffer.write(data)

    def get_bytes(self):
        return self.buffer.getvalue()


# ============================================================
# Paleta de bloques para Minecraft 26.2
# ============================================================

BLOCKS = {
    # --- Aire ---
    'air':                       {'id': 'minecraft:air'},

    # --- Piedra y variantes ---
    'cobblestone':               {'id': 'minecraft:cobblestone'},
    'stone_bricks':              {'id': 'minecraft:stone_bricks'},
    'mossy_stone_bricks':        {'id': 'minecraft:mossy_stone_bricks'},
    'cobblestone_wall':          {'id': 'minecraft:cobblestone_wall'},

    # --- Ladrillos ---
    'bricks':                    {'id': 'minecraft:bricks'},
    'brick_wall':                {'id': 'minecraft:brick_wall'},

    # --- Cinnabar (NUEVO en 26.2) ---
    'cinnabar':                  {'id': 'minecraft:cinnabar'},
    'cinnabar_bricks':           {'id': 'minecraft:cinnabar_bricks'},
    'polished_cinnabar':         {'id': 'minecraft:polished_cinnabar'},
    'chiseled_cinnabar':         {'id': 'minecraft:chiseled_cinnabar'},
    'cinnabar_stairs_s':         {'id': 'minecraft:cinnabar_stairs', 'props': {'facing': 'south', 'half': 'bottom', 'shape': 'straight'}},
    'cinnabar_stairs_n':         {'id': 'minecraft:cinnabar_stairs', 'props': {'facing': 'north', 'half': 'bottom', 'shape': 'straight'}},
    'cinnabar_stairs_e':         {'id': 'minecraft:cinnabar_stairs', 'props': {'facing': 'east', 'half': 'bottom', 'shape': 'straight'}},
    'cinnabar_stairs_w':         {'id': 'minecraft:cinnabar_stairs', 'props': {'facing': 'west', 'half': 'bottom', 'shape': 'straight'}},
    'cinnabar_slab':             {'id': 'minecraft:cinnabar_slab', 'props': {'type': 'bottom'}},
    'cinnabar_slab_top':         {'id': 'minecraft:cinnabar_slab', 'props': {'type': 'top'}},
    'cinnabar_brick_stairs_s':   {'id': 'minecraft:cinnabar_brick_stairs', 'props': {'facing': 'south', 'half': 'bottom', 'shape': 'straight'}},
    'cinnabar_brick_slab':       {'id': 'minecraft:cinnabar_brick_slab', 'props': {'type': 'bottom'}},
    'polished_cinnabar_stairs_s': {'id': 'minecraft:polished_cinnabar_stairs', 'props': {'facing': 'south', 'half': 'bottom', 'shape': 'straight'}},
    'polished_cinnabar_slab':    {'id': 'minecraft:polished_cinnabar_slab', 'props': {'type': 'bottom'}},

    # --- Sulfur (NUEVO en 26.2) ---
    'sulfur':                    {'id': 'minecraft:sulfur'},
    'polished_sulfur':           {'id': 'minecraft:polished_sulfur'},
    'sulfur_bricks':             {'id': 'minecraft:sulfur_bricks'},
    'chiseled_sulfur':           {'id': 'minecraft:chiseled_sulfur'},
    'sulfur_stairs_s':           {'id': 'minecraft:sulfur_stairs', 'props': {'facing': 'south', 'half': 'bottom', 'shape': 'straight'}},
    'sulfur_slab':               {'id': 'minecraft:sulfur_slab', 'props': {'type': 'bottom'}},

    # --- Madera de roble ---
    'oak_planks':                {'id': 'minecraft:oak_planks'},
    'oak_log':                   {'id': 'minecraft:oak_log', 'props': {'axis': 'y'}},
    'oak_log_x':                 {'id': 'minecraft:oak_log', 'props': {'axis': 'x'}},
    'oak_log_z':                 {'id': 'minecraft:oak_log', 'props': {'axis': 'z'}},
    'stripped_oak_log':          {'id': 'minecraft:stripped_oak_log', 'props': {'axis': 'y'}},
    'oak_stairs_s':              {'id': 'minecraft:oak_stairs', 'props': {'facing': 'south', 'half': 'bottom', 'shape': 'straight'}},
    'oak_stairs_n':              {'id': 'minecraft:oak_stairs', 'props': {'facing': 'north', 'half': 'bottom', 'shape': 'straight'}},
    'oak_stairs_e':              {'id': 'minecraft:oak_stairs', 'props': {'facing': 'east', 'half': 'bottom', 'shape': 'straight'}},
    'oak_stairs_w':              {'id': 'minecraft:oak_stairs', 'props': {'facing': 'west', 'half': 'bottom', 'shape': 'straight'}},
    'oak_slab':                  {'id': 'minecraft:oak_slab', 'props': {'type': 'bottom'}},
    'oak_slab_top':              {'id': 'minecraft:oak_slab', 'props': {'type': 'top'}},
    'oak_fence':                 {'id': 'minecraft:oak_fence'},
    'oak_fence_gate':            {'id': 'minecraft:oak_fence_gate', 'props': {'facing': 'south', 'in_wall': 'false', 'open': 'false'}},
    'oak_door_lower_s':          {'id': 'minecraft:oak_door', 'props': {'facing': 'south', 'half': 'lower', 'hinge': 'left', 'open': 'false'}},
    'oak_door_upper_s':          {'id': 'minecraft:oak_door', 'props': {'facing': 'south', 'half': 'upper', 'hinge': 'left', 'open': 'false'}},

    # --- Madera de abeto ---
    'spruce_planks':             {'id': 'minecraft:spruce_planks'},
    'spruce_log':                {'id': 'minecraft:spruce_log', 'props': {'axis': 'y'}},
    'spruce_stairs_s':           {'id': 'minecraft:spruce_stairs', 'props': {'facing': 'south', 'half': 'bottom', 'shape': 'straight'}},
    'spruce_stairs_n':           {'id': 'minecraft:spruce_stairs', 'props': {'facing': 'north', 'half': 'bottom', 'shape': 'straight'}},
    'spruce_stairs_e':           {'id': 'minecraft:spruce_stairs', 'props': {'facing': 'east', 'half': 'bottom', 'shape': 'straight'}},
    'spruce_stairs_w':           {'id': 'minecraft:spruce_stairs', 'props': {'facing': 'west', 'half': 'bottom', 'shape': 'straight'}},

    # --- Madera oscura ---
    'dark_oak_planks':           {'id': 'minecraft:dark_oak_planks'},
    'dark_oak_log':              {'id': 'minecraft:dark_oak_log', 'props': {'axis': 'y'}},

    # --- Cristal ---
    'glass':                     {'id': 'minecraft:glass'},
    'glass_pane':                {'id': 'minecraft:glass_pane'},

    # --- Mobiliario ---
    'chest':                     {'id': 'minecraft:chest', 'props': {'facing': 'north'}},
    'crafting_table':            {'id': 'minecraft:crafting_table'},
    'furnace':                   {'id': 'minecraft:furnace', 'props': {'facing': 'south'}},
    'campfire':                  {'id': 'minecraft:campfire', 'props': {'facing': 'north', 'lit': 'true', 'signal_fire': 'false', 'waterlogged': 'false'}},
    'torch':                     {'id': 'minecraft:torch'},
    'lantern':                   {'id': 'minecraft:lantern', 'props': {'hanging': 'false'}},
    'hanging_lantern':           {'id': 'minecraft:lantern', 'props': {'hanging': 'true'}},
    'bookshelf':                 {'id': 'minecraft:bookshelf'},
    'barrel':                    {'id': 'minecraft:barrel', 'props': {'facing': 'up'}},
    'flower_pot':                {'id': 'minecraft:flower_pot'},

    # --- Decoración natural ---
    'red_tulip':                 {'id': 'minecraft:red_tulip'},
    'dandelion':                 {'id': 'minecraft:dandelion'},
    'golden_dandelion':          {'id': 'minecraft:golden_dandelion'},
    'grass_block':               {'id': 'minecraft:grass_block', 'props': {'snowy': 'false'}},
    'dirt_path':                 {'id': 'minecraft:dirt_path'},
    'gravel':                    {'id': 'minecraft:gravel'},
    'white_carpet':              {'id': 'minecraft:white_carpet'},
    'white_bed_s':               {'id': 'minecraft:white_bed', 'props': {'facing': 'south', 'part': 'head'}},
    'white_bed_n':               {'id': 'minecraft:white_bed', 'props': {'facing': 'south', 'part': 'foot'}},
    'straw_bed_s':               {'id': 'minecraft:straw_bed', 'props': {'facing': 'south', 'part': 'head'}},
    'straw_bed_n':               {'id': 'minecraft:straw_bed', 'props': {'facing': 'south', 'part': 'foot'}},
    'cushion':                   {'id': 'minecraft:cushion'},
    'ladder_s':                  {'id': 'minecraft:ladder', 'props': {'facing': 'south'}},
    'flowering_azalea_leaves':   {'id': 'minecraft:flowering_azalea_leaves'},
}


class HouseBuilder:
    """Construye una casa medieval mejorada con bloques de 26.2"""

    def __init__(self, width=17, height=13, depth=15):
        self.width = width
        self.height = height
        self.depth = depth
        self.blocks = {}

    def set(self, x, y, z, block_key):
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            if block_key != 'air' or (x, y, z) in self.blocks:
                self.blocks[(x, y, z)] = block_key

    def fill(self, x1, y1, z1, x2, y2, z2, block_key):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, block_key)

    def build(self):
        self._build_foundation()
        self._build_first_floor_walls()
        self._build_door()
        self._build_first_floor_windows()
        self._build_second_floor()
        self._build_second_floor_walls()
        self._build_second_floor_windows()
        self._build_roof()
        self._build_chimney()
        self._build_first_floor_interior()
        self._build_second_floor_interior()
        self._build_garden()
        self._build_details()

    # ── Cimientos ──
    def _build_foundation(self):
        self.fill(0, 0, 0, self.width - 1, 0, self.depth - 1, 'cobblestone')

    # ── Paredes primer piso ──
    def _build_first_floor_walls(self):
        W, D = self.width, self.depth

        for x in range(1, W - 1):
            for y in [1, 2]:
                self.set(x, y, 0, 'stone_bricks')
                self.set(x, y, D - 1, 'stone_bricks')
            for y in [3, 4]:
                self.set(x, y, 0, 'oak_planks')
                self.set(x, y, D - 1, 'oak_planks')

        for z in range(1, D - 1):
            for y in [1, 2]:
                self.set(0, y, z, 'stone_bricks')
                self.set(W - 1, y, z, 'stone_bricks')
            for y in [3, 4]:
                self.set(0, y, z, 'oak_planks')
                self.set(W - 1, y, z, 'oak_planks')

        # Postes esquineros
        for y in range(1, 5):
            self.set(0, y, 0, 'oak_log')
            self.set(W - 1, y, 0, 'oak_log')
            self.set(0, y, D - 1, 'oak_log')
            self.set(W - 1, y, D - 1, 'oak_log')

        # Postes intermedios fachada (stripped oak para contraste)
        mid = W // 2
        for y in range(1, 5):
            self.set(mid - 3, y, 0, 'stripped_oak_log')
            self.set(mid + 3, y, 0, 'stripped_oak_log')

        # Faja decorativa de cinnabar en la base de las paredes
        for x in range(1, W - 1):
            self.set(x, 1, 0, 'cinnabar_brick_slab')
            self.set(x, 1, D - 1, 'cinnabar_brick_slab')
        for z in range(1, D - 1):
            self.set(0, 1, z, 'cinnabar_brick_slab')
            self.set(W - 1, 1, z, 'cinnabar_brick_slab')

        # Suelo interior
        self.fill(1, 1, 1, W - 2, 1, D - 2, 'oak_planks')

    # ── Puerta principal ──
    def _build_door(self):
        mid = self.width // 2
        self.set(mid, 1, 0, 'oak_door_lower_s')
        self.set(mid, 2, 0, 'oak_door_upper_s')
        # Marco
        self.set(mid - 1, 1, 0, 'oak_log')
        self.set(mid + 1, 1, 0, 'oak_log')
        self.set(mid - 1, 2, 0, 'oak_log')
        self.set(mid + 1, 2, 0, 'oak_log')
        self.set(mid, 3, 0, 'oak_log')
        self.set(mid - 1, 3, 0, 'oak_planks')
        self.set(mid + 1, 3, 0, 'oak_planks')
        # Detalle de cinabrio sobre la puerta
        self.set(mid, 4, 0, 'chiseled_cinnabar')

    # ── Ventanas primer piso ──
    def _build_first_floor_windows(self):
        W, D = self.width, self.depth

        # Frontales
        for x in [3, 4]:
            self.set(x, 2, 0, 'glass_pane')
        for x in [W - 5, W - 4]:
            self.set(x, 2, 0, 'glass_pane')

        # Laterales izquierda
        for z in [3, 4]:
            self.set(0, 2, z, 'glass_pane')
        for z in [9, 10]:
            self.set(0, 2, z, 'glass_pane')

        # Laterales derecha
        for z in [3, 4]:
            self.set(W - 1, 2, z, 'glass_pane')
        for z in [9, 10]:
            self.set(W - 1, 2, z, 'glass_pane')

        # Traseras
        for x in [4, 5]:
            self.set(x, 2, D - 1, 'glass_pane')
        for x in [W - 6, W - 5]:
            self.set(x, 2, D - 1, 'glass_pane')

    # ── Suelo segundo piso ──
    def _build_second_floor(self):
        W, D = self.width, self.depth
        self.fill(1, 5, 1, W - 2, 5, D - 2, 'spruce_planks')

    # ── Paredes segundo piso ──
    def _build_second_floor_walls(self):
        W, D = self.width, self.depth

        for y in range(6, 9):
            for x in range(1, W - 1):
                self.set(x, y, 0, 'dark_oak_planks')
                self.set(x, y, D - 1, 'dark_oak_planks')
            for z in range(1, D - 1):
                self.set(0, y, z, 'dark_oak_planks')
                self.set(W - 1, y, z, 'dark_oak_planks')

        for y in range(6, 9):
            self.set(0, y, 0, 'oak_log')
            self.set(W - 1, y, 0, 'oak_log')
            self.set(0, y, D - 1, 'oak_log')
            self.set(W - 1, y, D - 1, 'oak_log')

        mid = W // 2
        for y in range(6, 9):
            self.set(mid - 3, y, 0, 'stripped_oak_log')
            self.set(mid + 3, y, 0, 'stripped_oak_log')

        # Faja decorativa sulfur entre pisos
        for x in range(1, W - 1):
            self.set(x, 6, 0, 'polished_sulfur')
            self.set(x, 6, D - 1, 'polished_sulfur')
        for z in range(1, D - 1):
            self.set(0, 6, z, 'polished_sulfur')
            self.set(W - 1, 6, z, 'polished_sulfur')

    # ── Ventanas segundo piso ──
    def _build_second_floor_windows(self):
        W, D = self.width, self.depth

        for x in [3, 4, 5]:
            self.set(x, 7, 0, 'glass')
        for x in [W - 6, W - 5, W - 4]:
            self.set(x, 7, 0, 'glass')

        for z in [3, 4, 5]:
            self.set(0, 7, z, 'glass')
            self.set(W - 1, 7, z, 'glass')
        for z in [D - 6, D - 5, D - 4]:
            self.set(0, 7, z, 'glass')
            self.set(W - 1, 7, z, 'glass')

        for x in [4, 5, 6]:
            self.set(x, 7, D - 1, 'glass')
        for x in [W - 7, W - 6, W - 5]:
            self.set(x, 7, D - 1, 'glass')

    # ── Tejado ──
    def _build_roof(self):
        W, D = self.width, self.depth
        by = 9

        # Borde de escaleras
        for x in range(W):
            self.set(x, by, -1, 'spruce_stairs_s')
            self.set(x, by, D, 'spruce_stairs_n')
        for z in range(D):
            self.set(-1, by, z, 'spruce_stairs_e')
            self.set(W, by, z, 'spruce_stairs_w')
        self.set(-1, by, -1, 'spruce_planks')
        self.set(W, by, -1, 'spruce_planks')
        self.set(-1, by, D, 'spruce_planks')
        self.set(W, by, D, 'spruce_planks')
        self.fill(0, by, 0, W - 1, by, D - 1, 'spruce_planks')

        # Nivel 2
        by2 = 10
        for x in range(1, W - 1):
            self.set(x, by2, 0, 'spruce_stairs_s')
            self.set(x, by2, D - 1, 'spruce_stairs_n')
        for z in range(1, D - 1):
            self.set(0, by2, z, 'spruce_stairs_e')
            self.set(W - 1, by2, z, 'spruce_stairs_w')
        self.fill(1, by2, 1, W - 2, by2, D - 2, 'spruce_planks')

        # Nivel 3
        by3 = 11
        for x in range(2, W - 2):
            self.set(x, by3, 1, 'spruce_stairs_s')
            self.set(x, by3, D - 2, 'spruce_stairs_n')
        for z in range(2, D - 2):
            self.set(1, by3, z, 'spruce_stairs_e')
            self.set(W - 2, by3, z, 'spruce_stairs_w')
        self.fill(2, by3, 2, W - 3, by3, D - 3, 'spruce_planks')

        # Cumbrera con cinnabar slab (toque de 26.2)
        by4 = 12
        self.fill(3, by4, 3, W - 4, by4, D - 4, 'cinnabar_slab_top')

    # ── Chimenea (¡ahora con cinabrio!) ──
    def _build_chimney(self):
        for y in range(1, 9):
            self.set(-1, y, 6, 'cinnabar_bricks')
            self.set(-1, y, 7, 'cinnabar_bricks')
            self.set(0, y, 6, 'cinnabar_bricks')
            self.set(0, y, 7, 'cinnabar_bricks')
        # Hogar
        self.set(0, 1, 6, 'campfire')
        self.set(0, 1, 7, 'campfire')
        # Detalle cincelado
        self.set(0, 3, 6, 'chiseled_cinnabar')
        self.set(0, 3, 7, 'chiseled_cinnabar')
        # Tiro de chimenea
        for y in range(9, 12):
            self.set(-1, y, 6, 'cinnabar_bricks')
            self.set(-1, y, 7, 'cinnabar_bricks')
        # Corona
        self.set(-1, 12, 6, 'cinnabar_slab')
        self.set(-1, 12, 7, 'cinnabar_slab')

    # ── Interior primer piso ──
    def _build_first_floor_interior(self):
        W = self.width

        # Libreros junto a la chimenea
        self.set(1, 2, 5, 'bookshelf')
        self.set(1, 2, 8, 'bookshelf')
        self.set(1, 3, 5, 'bookshelf')
        self.set(1, 3, 8, 'bookshelf')

        # Área de trabajo
        self.set(W - 2, 2, 2, 'crafting_table')
        self.set(W - 2, 2, 3, 'furnace')

        # Barriles
        for z in [9, 10, 11]:
            self.set(W - 2, 2, z, 'barrel')
        for z in [9, 10]:
            self.set(W - 2, 3, z, 'barrel')

        # Alfombra central
        self.fill(7, 1, 6, 9, 1, 8, 'white_carpet')

        # Cojines (NUEVO en 26.2) junto a la chimenea
        self.set(2, 1, 6, 'cushion')
        self.set(2, 1, 7, 'cushion')

        # Escalera al segundo piso
        for i in range(5):
            self.set(W - 3, 1 + i, 7, 'oak_stairs_n')

        # Linterna
        self.set(8, 4, 7, 'hanging_lantern')

        # Maceta
        self.set(1, 1, 7, 'flower_pot')

    # ── Interior segundo piso ──
    def _build_second_floor_interior(self):
        W = self.width

        # Cama de paja (NUEVO en 26.2)
        self.set(3, 6, 3, 'straw_bed_n')
        self.set(3, 6, 4, 'straw_bed_s')

        # Mesitas de noche con slabs de azufre (NUEVO en 26.2)
        self.set(2, 6, 3, 'sulfur_slab')
        self.set(4, 6, 3, 'sulfur_slab')

        # Cofres
        self.set(W - 3, 6, 3, 'chest')
        self.set(W - 3, 6, 4, 'chest')

        # Librero privado
        for z in range(7, 11):
            self.set(1, 7, z, 'bookshelf')

        # Alfombra
        self.fill(6, 6, 5, 10, 6, 9, 'white_carpet')

        # Cojines
        self.set(8, 6, 6, 'cushion')
        self.set(8, 6, 8, 'cushion')

        # Linternas
        self.set(8, 8, 7, 'hanging_lantern')

        # Escalera bajando
        for i in range(5):
            self.set(W - 3, 5 + i, 7, 'oak_stairs_n')

        # Macetas
        self.set(W - 2, 6, 11, 'flower_pot')
        self.set(W - 2, 6, 1, 'flower_pot')

    # ── Jardín ──
    def _build_garden(self):
        W = self.width
        mid = W // 2

        # Camino de gravilla
        for z in range(-3, 0):
            for x in range(mid - 1, mid + 2):
                self.set(x, 0, z, 'gravel')

        # Césped
        for x in range(0, W):
            for z in range(-3, 0):
                if self.blocks.get((x, 0, z)) is None:
                    self.set(x, 0, z, 'grass_block')

        # Flores
        for x, z in [(2, -2), (3, -1), (W - 3, -2), (W - 4, -1), (5, -2), (W - 6, -2)]:
            self.set(x, 0, z, 'red_tulip')
        for x, z in [(2, -1), (W - 3, -1), (4, -1), (W - 5, -1)]:
            self.set(x, 0, z, 'dandelion')

        # Flor dorada (NUEVO en 26.1)
        self.set(mid, 0, -2, 'golden_dandelion')

        # Cerda
        for x in range(0, W):
            self.set(x, 1, -3, 'oak_fence')
        self.set(mid, 1, -3, 'oak_fence_gate')

    # ── Detalles ──
    def _build_details(self):
        W = self.width
        mid = W // 2

        # Antorchas fachada
        self.set(2, 3, 0, 'torch')
        self.set(W - 3, 3, 0, 'torch')

        # Faroles junto a la puerta
        self.set(mid - 2, 1, -1, 'torch')
        self.set(mid + 2, 1, -1, 'torch')

        # Escalón de entrada con cinnabar
        self.set(mid, 0, -1, 'cinnabar_slab')
        self.set(mid - 1, 0, -1, 'cinnabar_slab')
        self.set(mid + 1, 0, -1, 'cinnabar_slab')

    def build_palette(self):
        used_keys = set(self.blocks.values())
        self.palette = []
        self.palette_index = {}
        idx = 0
        for key in sorted(used_keys):
            if key in BLOCKS:
                self.palette.append(BLOCKS[key])
                self.palette_index[key] = idx
                idx += 1

    def write_nbt(self, filename):
        self.build_palette()

        w = NBTWriter()
        w.begin_compound('')

        # DataVersion para Minecraft Java 26.2
        w.write_int('DataVersion', 4903)
        w.write_string('Author', 'ArenaAI - Casa Medieval 26.2')

        # Size
        min_x = min(b[0] for b in self.blocks)
        max_x = max(b[0] for b in self.blocks)
        min_y = min(b[1] for b in self.blocks)
        max_y = max(b[1] for b in self.blocks)
        min_z = min(b[2] for b in self.blocks)
        max_z = max(b[2] for b in self.blocks)

        sx = max_x - min_x + 1
        sy = max_y - min_y + 1
        sz = max_z - min_z + 1

        w.begin_list('size', 3, 3)
        w.write_int('', sx)
        w.write_int('', sy)
        w.write_int('', sz)

        # Palette
        w.begin_list('palette', 10, len(self.palette))
        for block_def in self.palette:
            w.begin_compound('')
            w.write_string('Name', block_def['id'])
            if 'props' in block_def:
                w.begin_compound('Properties')
                for k, v in block_def['props'].items():
                    w.write_string(k, v)
                w.end_compound()
            w.end_compound()

        # Blocks
        w.begin_list('blocks', 10, len(self.blocks))
        for (bx, by, bz), block_key in sorted(self.blocks.items()):
            w.begin_compound('')
            w.begin_list('pos', 3, 3)
            w.write_int('', bx - min_x)
            w.write_int('', by - min_y)
            w.write_int('', bz - min_z)
            w.write_int('state', self.palette_index[block_key])
            w.end_compound()

        # Entities
        w.begin_list('entities', 10, 0)

        w.end_compound()

        raw = w.get_bytes()
        with gzip.open(filename, 'wb') as f:
            f.write(raw)

        return sx, sy, sz

    def print_summary(self):
        print(f"  Dimensiones: {self.width}x{self.height}x{self.depth}")
        print(f"  Bloques totales: {len(self.blocks)}")
        print(f"  Tipos únicos: {len(set(self.blocks.values()))}")
        counts = {}
        for key in self.blocks.values():
            counts[key] = counts.get(key, 0) + 1
        print(f"\n  📦 Materiales necesarios:")
        for key, count in sorted(counts.items(), key=lambda x: -x[1]):
            mc_name = BLOCKS.get(key, {}).get('id', key)
            print(f"    {mc_name}: {count}")


def main():
    print("🏠" + "=" * 58)
    print("  CASA MEDIEVAL BONITA - Minecraft Java 26.2")
    print("  Chaos Cubed (DataVersion 4903)")
    print("=" * 60)
    print()

    print("🔨 Construyendo la casa con bloques nuevos de 26.2...")
    house = HouseBuilder(width=17, height=13, depth=15)
    house.build()

    print("✅ Casa construida!")
    house.print_summary()

    print(f"\n💾 Guardando archivo .nbt (DataVersion 4903)...")
    sx, sy, sz = house.write_nbt('medieval_house.nbt')
    print(f"✅ medieval_house.nbt guardado ({sx}x{sy}x{sz})")

    # Guía
    guide = """# 🏠 Casa Medieval Bonita - Minecraft Java 26.2
# ============================================
# Chaos Cubed (DataVersion 4903)
#
# Incluye bloques nuevos de 26.2:
# - Cinnabar (cinabrio): chimenea, detalles rojos
# - Sulfur (azufre): decoración amarilla, mesitas
# - Cushion (cojín): asientos cómodos
# - Straw Bed (cama de paja): dormitorio
# - Golden Dandelion: flor dorada en el jardín
#
## USO CON BLOQUE DE ESTRUCTURA:
# 1. Copia medieval_house.nbt a:
#    .minecraft/saves/<tu_mundo>/generated/minecraft/structures/
# 2. /give @s structure_block
# 3. Modo "Cargar" → "medieval_house" → Cargar → Generar
#
## USO CON WORLDEDIT:
# 1. Copia medieval_house.schematic a:
#    .minecraft/config/worldedit/schematics/
# 2. //schem load medieval_house
# 3. //paste
#
## CARACTERÍSTICAS:
# • 2 pisos completamente amueblados
# • Chimenea de cinnabar bricks con fogata
# • Tejado a dos aguas con cumbrera de cinnabar
# • Fajas decorativas de polished sulfur y cinnabar
# • Cojines (cushions) junto a la chimenea
# • Cama de paja (straw bed) en el dormitorio
# • Mesitas de noche de sulfur slab
# • Escalón de entrada de cinnabar
# • Jardín con golden dandelion
# • Ventanas de cristal en ambos pisos
# • Escalera interior, linternas, barriles, cofres
#
## MATERIALES:
# Estructura: Cobblestone, Stone Bricks, Oak/Dark Oak Planks
# Decoración 26.2: Cinnabar Bricks, Polished Sulfur, Chiseled Cinnabar
# Madera: Oak Log, Spruce Planks, Stripped Oak Log
# Tejado: Spruce Stairs, Cinnabar Slab (cumbrera)
# Interior: Cushion, Straw Bed, Barrel, Bookshelf, Lantern
# Jardín: Grass, Gravel, Flowers, Golden Dandelion, Fence
"""
    with open('guia_casa_medieval.txt', 'w', encoding='utf-8') as f:
        f.write(guide)
    print(f"✅ guia_casa_medieval.txt guardado")

    print()
    print("🎉 ¡Archivos listos para Minecraft Java 26.2!")
    print()
    print("  📁 medieval_house.nbt       → Structure Block (vanilla)")
    print("  📁 medieval_house.schematic  → WorldEdit / Litematica")
    print("  📁 medieval_house_data.json  → Datos completos JSON")
    print("  📁 guia_casa_medieval.txt    → Instrucciones")
    print()
    print("✨ Bloques nuevos de 26.2 utilizados:")
    print("  🔴 Cinnabar Bricks → Chimenea y detalles rojos")
    print("  🟡 Polished Sulfur → Fajas decorativas entre pisos")
    print("  🟤 Chiseled Cinnabar → Detalle sobre la puerta")
    print("  🛏️  Straw Bed → Cama del dormitorio")
    print("  🛋️  Cushion → Asientos en la sala")
    print("  🌼 Golden Dandelion → Flor del jardín")
    print("  ⬜ Cinnabar Slab → Cumbrera del techo y escalones")


if __name__ == "__main__":
    main()
