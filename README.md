# affordance-bench
## Setup
Used VRB Conda environment as base but got rid of the build hashes. 
Then I added all the named versions from the VRB requirements.txt into the one
from GIGA and tried to pip install.
The gdown install threw an error saying that the named version of open3d isn't
compatible with the current python version.Open3d is from GIGA and gdown is
from VRB so it looks like GIGA was python3.7 or earlier. Going to try to
resolve by upgrading to 0.14.1.

The torch and torchvision versions conflict, not to mention that 1.7 isn't
compatible with python3.9. Going to try 1.7.1 using CUDA toolkit 11.0. Just
going to do the install with conda though.

Well, installing lang-sam overwrote a ton of all this so let's see what
happens. Mb I'll start with testing GIGA now.

Also it looks like torch-scatter is on conda for torch>=1.8 so maybe at least
updating torch is a good idea.

Actually, now I have two versions of torch, cpu and gpu and it's all getting
a bit wierd so I'm going to just run with two different environments. Just will
have to generate images first, then send over to VRB, and then switch back
maybe.

Ended up doing the GIGA install with a few tweaks:
python 3.8, torch 1.8 (to make installing torch-scatter more convenient), open3d
1.14 (last is because it uses a deprecated pip install for sklearn instead of
scikit-learn)

Acutally you need open3d 0.12.0 otherwise there is a segfault with their code.
Need to install the package with `SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True pip install open3d==0.12.0`

Along with the GIGA issues, the [VGN repo
README](https://github.com/ethz-asl/vgn) is quite helpful.

Ended up doing the fix ishikaa did on the vgn clutter removal to save grasps
and then I downloaded the obj files and opened locally on my mac to take
images. however, I did have to install scipy and networkx in addition to
pyglet<2, and run defaults write org.python.python ApplePersistenceIgnoreState NO
Then I needed to get rid of the cocoa error by disabling the alternate event
controller backend in pyglet, which I documented on a recent issue on the repo

Key Commands:
```
python scripts/sim_grasp_table.py --num-view 1 --num-rounds 1 --object-set pile/test --scene pile  --view horizontal --force --best --model data/models/giga_pile.pt --type giga --result-path data/experiments/result.json --vis --seeds 10 --logdir data/horizontal_exp --zoom 2
```
```
python run_vrb.py ../GIGA/data/single_exp/
```
