import streamlit as st
from pathlib import Path
import pickle as pkl
import random
from PIL import Image
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Setup Dataset
experiment_folder = [
    "./horizontal_exp",
    "./single_exp",
    "./top_exp",
    "./pile_exp"
]
experiment_folder = [Path(f).resolve() for f in experiment_folder]

handed = Path.cwd() / "handed.pkl"
if not handed.exists():
    all_trials = {}
else:
    all_trials = pkl.load(handed.open("rb"))

if 'all_trials' not in st.session_state:
    for folder_path in experiment_folder:
        experiment_directories = [d for d in folder_path.iterdir() if d.is_dir()]
        for experiment_directory in experiment_directories:
            grasp_images_dir = experiment_directory / "grasp_images"
            vrb_dir = experiment_directory / "vrb"
            grasp_images_files = [f.name for f in grasp_images_dir.iterdir() if f.is_file()]
            vrb_files = [f.name for f in vrb_dir.iterdir() if f.is_file()]
            for grasp_images_file in grasp_images_files:
                if grasp_images_file in vrb_files:
                    trial_id = f"{folder_path.name}_{experiment_directory.name}_{grasp_images_file}"
                    if trial_id not in all_trials:
                        all_trials[trial_id] = {
                            "grasp_images": str(grasp_images_dir / grasp_images_file),
                            "vrb": str(vrb_dir / grasp_images_file),
                            "handed": [[0, 0, 0], [0, 0, 0]]
                        }
    pkl.dump(all_trials, handed.open("wb"))

if 'random_trial_id' not in st.session_state:
    min_votes = min([sum(trial_info["handed"][0]) + sum(trial_info["handed"][1]) for trial_info in all_trials.values()])
    min_preference_trials = [trial_id for trial_id, trial_info in all_trials.items() if sum(trial_info["handed"][0]) + sum(trial_info["handed"][1]) == min_votes]
    st.session_state.random_trial_id = random.choice(min_preference_trials)
    st.session_state.all_trials = all_trials

# Load the images
giga_image_path = st.session_state.all_trials[st.session_state.random_trial_id]["grasp_images"]
vrb_image_path = st.session_state.all_trials[st.session_state.random_trial_id]["vrb"]
giga_image = Image.open(giga_image_path)
vrb_image = Image.open(vrb_image_path)

# Resize the images
resized_giga_image = giga_image.resize((400, 400))
resized_vrb_image = vrb_image.resize((400, 400))

# Display the images side by side in two columns
col1, col2 = st.columns(2)
with col1:
    st.image(resized_giga_image, caption="GIGA Image", width=400)
    giga_preference = st.radio("GIGA Preference", ["neutral", "right", "left"], key="giga_preference")

with col2:
    st.image(resized_vrb_image, caption="VRB Image", width=400)
    vrb_preference = st.radio("VRB Preference", ["neutral", "right", "left"], key="vrb_preference")

def update_handed():
    if 'giga_preference' in st.session_state:
        if st.session_state.giga_preference == "left":
            st.session_state.all_trials[st.session_state.random_trial_id]["handed"][0][0] += 1
        elif st.session_state.giga_preference == "neutral":
            st.session_state.all_trials[st.session_state.random_trial_id]["handed"][0][1] += 1
        elif st.session_state.giga_preference == "right":
            st.session_state.all_trials[st.session_state.random_trial_id]["handed"][0][2] += 1
    if 'vrb_preference' in st.session_state:
        if st.session_state.vrb_preference == "left":
            st.session_state.all_trials[st.session_state.random_trial_id]["handed"][1][0] += 1
        elif st.session_state.vrb_preference == "neutral":
            st.session_state.all_trials[st.session_state.random_trial_id]["handed"][1][1] += 1
        elif st.session_state.vrb_preference == "right":
            st.session_state.all_trials[st.session_state.random_trial_id]["handed"][1][2] += 1
    pkl.dump(st.session_state.all_trials, handed.open("wb"))
    del st.session_state.random_trial_id

st.button("Submit Preferences", on_click=update_handed)

# Show the bias results
st.write("Bias Results")

# Create a bar chart of the biases
bias_data = []
for trial_id, trial_info in st.session_state.all_trials.items():
    folder_name = trial_id.split("_")[0]
    giga_bias = trial_info["handed"][0]
    vrb_bias = trial_info["handed"][1]
    # Calculate the skewness for GIGA and VRB biases considering all three options
    giga_skew = (giga_bias[0] - giga_bias[2]) / sum(giga_bias) if sum(giga_bias) != 0 else 0
    vrb_skew = (vrb_bias[0] - vrb_bias[2]) / sum(vrb_bias) if sum(vrb_bias) != 0 else 0
    bias_data.append((folder_name, giga_skew, vrb_skew))

df = pd.DataFrame(bias_data, columns=["Experiment Directory", "GIGA Bias", "VRB Bias"])
df = df.melt("Experiment Directory", var_name="Model", value_name="Bias")
plot = sns.barplot(x="Experiment Directory", y="Bias", hue="Model", data=df)
plt.xlabel("Experiment Directory")
plt.ylabel("Model Bias")
plt.title("Model Bias Results")
plt.legend(["GIGA Bias", "VRB Bias"])
st.pyplot(plot.get_figure())
