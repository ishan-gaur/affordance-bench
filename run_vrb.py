import sys
from pathlib import Path
import subprocess
from tqdm import tqdm
import subprocess
vrb_repo = Path("~/vrb").expanduser()
giga_repo = Path("~/GIGA").expanduser()

def run_command_on_subdirectories(directory_path):
    directory = Path(directory_path)
    conda_env = "vrb"
    rgb_images_list = []

    for subdirectory in tqdm(directory.iterdir(), desc="Processing subdirectories"):
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
    
            for file in rgb_images_folder.glob("*.png"):
                rgb_images_list.append(file)
    
    for rgb_image in tqdm(rgb_images_list, desc="Processing images"):
        rgb_image_path = rgb_image.resolve()
        subdirectory = rgb_image_path.parent.parent
        
        program = f"""
        python {vrb_repo}/aff_bench_inference.py --image {rgb_image_path} \
        --output {subdirectory}/vrb/{rgb_image.name} --obj_list {giga_repo}/object_list.txt \
        --model_path {vrb_repo}/models/model_checkpoint_1249.pth.tar \
        --max_box 5
        """
        command = program

        def run_command(command):
            process = subprocess.Popen(command, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, _ = process.communicate()
            stdout = stdout.decode("utf-8")
            return stdout

        stdout = run_command(command)
        if "All done !" not in stdout:
            print(f"Failed image: {rgb_image_path}")
            print(f"Associated stdout: {stdout}")
        else:
            print(f"Processed image: {rgb_image_path}")

# Example usage
if len(sys.argv) != 2:
    print("Usage: python run_vrb.py <path/to/giga/experiments>")
    sys.exit(1)

directory_path = sys.argv[1]
run_command_on_subdirectories(directory_path)
