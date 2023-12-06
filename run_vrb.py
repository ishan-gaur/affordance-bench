import sys
from pathlib import Path
import subprocess

vrb_repo = Path("~/vrb").expanduser()
giga_repo = Path("~/GIGA").expanduser()

def run_command_on_subdirectories(directory_path):
    directory = Path(directory_path)
    conda_env = "vrb"

    for subdirectory in directory.iterdir():
        if subdirectory.is_dir():
            rgb_images_folder = subdirectory / "rgb_images"
            vrb_folder = subdirectory / "vrb"
            
            if not rgb_images_folder.exists():
                raise FileNotFoundError(f"rgb_images folder not found in {subdirectory}")
            
            if vrb_folder.exists():
                rgb_images_count = len(list(rgb_images_folder.glob("*")))
                vrb_count = len(list(vrb_folder.glob("*")))
                
                if rgb_images_count != vrb_count:
                    for file in vrb_folder.glob("*"):
                        file.unlink()
                else:
                    continue
            else:
                vrb_folder.mkdir()
    
            for file in rgb_images_folder.glob("*.png"):  # Iterate over .png files in rgb_images folder
                rgb_image = file.name
                
                program = f"""
                python {vrb_repo}/aff_bench_inference.py --image {subdirectory}/rgb_images/{rgb_image} \
                --output {subdirectory}/rgb_images/{rgb_image} --obj_list {giga_repo}/object_list.txt \
                --model_path {vrb_repo}/models/model_checkpoint_1249.pth.tar \
                --max_box 5
                """
                # command = f"conda init bash && conda activate {conda_env} && {program}"
                command = program
                subprocess.run(command, cwd=subdirectory, shell=True, executable="/bin/bash")

# Example usage
if len(sys.argv) != 2:
    print("Usage: python run_vrb.py <path/to/giga/experiments>")
    sys.exit(1)

directory_path = sys.argv[1]
run_command_on_subdirectories(directory_path)
