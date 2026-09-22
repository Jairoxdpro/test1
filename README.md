# 🏠 Casa Medieval Bonita - Minecraft Java 26.2

Esquema de una hermosa casa medieval para **Minecraft Java Edition 26.2** (Chaos Cubed).

DataVersion: **4903**

## ✨ Novedades de 26.2 incluidas

| Bloque | Uso en la casa |
|--------|----------------|
| 🔴 **Cinnabar Bricks** | Chimenea y detalles decorativos |
| 🟡 **Polished Sulfur** | Fajas decorativas entre pisos |
| 🟤 **Chiseled Cinnabar** | Detalle sobre la puerta principal |
| 🛏️ **Straw Bed** | Cama del dormitorio |
| 🛋️ **Cushion** | Asientos junto a la chimenea |
| 🌼 **Golden Dandelion** | Flor en el jardín |
| ⬜ **Cinnabar Slab** | Cumbrera del techo y escalones |

## 📐 Dimensiones

- **17 × 13 × 15 bloques** (ancho × alto × profundo)
- **1,919 bloques** totales
- **35 tipos de bloques** únicos

## 🏠 Características

- **2 pisos** completamente amueblados
- **Chimenea** de cinnabar bricks con fogata
- **Techo** a dos aguas con cumbrera de cinnabar slab
- **Jardín** con flores, golden dandelion, cercas y camino de gravilla
- **Ventanas** de cristal en ambos pisos
- **Puerta principal** con marco de madera y detalle de chiseled cinnabar
- **Escalera interior** al segundo piso
- **Iluminación** con linternas y antorchas
- **Interior**: straw bed, cushion, cofres, libreros, mesa de trabajo, horno, barriles

## 📁 Archivos

| Archivo | Descripción |
|---------|-------------|
| `medieval_house.nbt` | Estructura para Structure Block (vanilla) |
| `medieval_house.schematic` | Formato WorldEdit / Litematica |
| `medieval_house_data.json` | Datos completos en JSON |
| `guia_casa_medieval.txt` | Instrucciones de uso |
| `generate_house.py` | Script generador de la estructura |
| `export_schematic.py` | Script exportador a .schematic y .json |

## 🎮 Cómo usar

### Opción 1: Structure Block (vanilla, sin mods)

1. Copia `medieval_house.nbt` a:
   ```
   .minecraft/saves/<tu_mundo>/generated/minecraft/structures/
   ```
2. En Minecraft:
   ```
   /give @s structure_block
   ```
3. Modo **"Cargar"** → escribe `medieval_house` → **Cargar** → **Generar**

### Opción 2: WorldEdit

1. Copia `medieval_house.schematic` a:
   ```
   .minecraft/config/worldedit/schematics/
   ```
2. En Minecraft:
   ```
   //schem load medieval_house
   //paste
   ```

### Opción 3: Litematica

1. Copia `medieval_house.schematic` a:
   ```
   .minecraft/schematics/
   ```
2. Usa el mod Litematica para cargar y colocar

## 🏗️ Diseño Interior

### Primer Piso
- Sala principal con chimenea de cinnabar bricks y fogata
- Cojines (cushion) junto al fuego
- Área de trabajo: mesa de crafting + horno
- Bodega con barriles
- Libreros
- Alfombra central blanca
- Escalera al segundo piso

### Segundo Piso
- Dormitorio con straw bed
- Mesitas de noche de sulfur slab
- Cofres de almacenamiento
- Biblioteca privada con libreros
- Alfombras y cojines
- Linternas colgantes

### Exterior
- Camino de gravilla
- Cerda de roble con puerta
- Flores: tulipanes rojos, dientes de león y golden dandelion
- Escalón de entrada de cinnabar slab

## 🔧 Regenerar / Modificar

```bash
python3 generate_house.py     # Genera medieval_house.nbt
python3 export_schematic.py   # Genera .schematic y .json
```

## 📜 Licencia

MIT License - Consulta el archivo LICENSE para más detalles.
