import bpy, sys
from pathlib import Path
args = sys.argv[sys.argv.index('--') + 1:]
out = Path(args[0]).resolve()
# Exporta a cena inteira aberta pelo Blender para GLB.
bpy.ops.export_scene.gltf(filepath=str(out), export_format='GLB', export_apply=True)
print('GLB criado:', out)
