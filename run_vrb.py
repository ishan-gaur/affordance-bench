import sys
from pathlib import Path
import subprocess
from tqdm import tqdm
import subprocess
vrb_repo = Path("~/vrb").expanduser()
giga_repo = Path("~/GIGA").expanduser()
overwrite = True
debug = False

def run_command_on_subdirectories(directory_path):
    directory = Path(directory_path)
    rgb_images_list = []

    for subdirectory in tqdm(directory.iterdir(), desc="Processing subdirectories"):
        if subdirectory.is_dir():
            rgb_images_folder = subdirectory / "rgb_images"
            vrb_folder = subdirectory / "vrb"
            
            if not rgb_images_folder.exists():
                raise FileNotFoundError(f"rgb_images folder not found in {subdirectory}")
            
            if vrb_folder.exists() and not overwrite:
                rgb_images_count = len(list(rgb_images_folder.glob("*")))
                vrb_count = len(list(vrb_folder.glob("*")))
                
                if rgb_images_count != vrb_count:
                    for file in vrb_folder.glob("*"):
                        file.unlink()
                else:
                    continue
            elif not vrb_folder.exists():
                vrb_folder.mkdir()
    
            for file in rgb_images_folder.glob("*.png"):
                rgb_images_list.append(file)
    
    image_list_file = Path.cwd() / "image_list.txt"
    
    with open(image_list_file, "w") as f:
        for rgb_image in rgb_images_list:
            subdirectory = rgb_image.parent.parent
            vrb_folder = subdirectory / "vrb"
            output_image = vrb_folder / rgb_image.name
            f.write(f"{rgb_image},{output_image}\n")
    
    program = f"""
    python {vrb_repo}/aff_bench_inference.py --image_list {image_list_file} \
    --obj_list {giga_repo}/object_list.txt \
    --model_path {vrb_repo}/models/model_checkpoint_1249.pth.tar \
    --max_box 1 {'--debug' if debug else ''}
    """
    command = program
    subprocess.run(command, shell=True)

# Example usage
if len(sys.argv) != 2:
    print("Usage: python run_vrb.py <path/to/giga/experiments>")
    sys.exit(1)

directory_path = sys.argv[1]
run_command_on_subdirectories(directory_path)
