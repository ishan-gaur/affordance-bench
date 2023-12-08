import numpy as np
from PIL import Image
import trimesh
from pathlib import Path
import sys
import math

if len(sys.argv) != 3:
    print("Usage: python render_giga.py <path/to/experiment/directory/> {side, top, horizontal}")
    sys.exit(1)

exp_folder = Path(sys.argv[1]).resolve()
view = sys.argv[2]
print(view)
assert view in ['side', 'top', 'horizontal'], "View must be one of side, top, horizontal"

for trial_folder in exp_folder.iterdir():
    if not trial_folder.is_dir():
        continue
    grasps_folder = trial_folder / 'grasps'
    image_folder = trial_folder / 'grasp_images'
    if not image_folder.exists():
        image_folder.mkdir()

    sizes = []
    for grasp_path in grasps_folder.iterdir():
        if grasp_path.suffix != '.obj':
            continue
        grasp_mesh = trimesh.load_mesh(grasp_path)
        sizes.extend(grasp_mesh.bounding_box.extents[:2])

    scene_size = max(sizes)
    for grasp_path in grasps_folder.iterdir():
        if grasp_path.suffix != '.obj':
            continue
        grasp_mesh = trimesh.load_mesh(grasp_path)
        scene = trimesh.Scene()
        scene.add_geometry(grasp_mesh)
        if view == "side":
            scene.set_camera(distance=2.0 * scene_size, angles=[np.pi / 3, 0, 0])
        elif view == "top":
            scene.set_camera(distance=2.0 * scene_size, angles=[0, 0, 0])
        elif view == "horizontal":
            scene.set_camera(distance=2.0 * scene_size, angles=[np.pi / 2.1, 0, 0])
        png = scene.save_image()

        image_path = image_folder / grasp_path.stem
        image_path = image_path.with_suffix('.png')
        with open(image_path, 'wb') as f:
            f.write(png)

        img = Image.open(image_path)
        width, height = img.size
        t, b = 0, height
        l, r = int(math.floor(width / 4)), int(math.ceil(width / 4 * 3))
        img.crop((l, t, r, b)).save(image_path)
