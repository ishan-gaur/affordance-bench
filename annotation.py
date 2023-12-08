import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

# Need to add directional and positional modes
# Need to run experiments with more grasps for 

import utils
from config import ANNOTATED, GIGA_PREFIX, VRB_PREFIX, NUM_SAME, OBJ_MODES
import components

eval_df = utils.setup()

total_samples = len(eval_df)
annotated_samples = eval_df[ANNOTATED].sum()

st.write(eval_df)

st.header("Annotation Samples")
st.subheader(f"Remaining: {total_samples - annotated_samples}; Annotated: {annotated_samples}; Total: {total_samples}")

eval_sample = eval_df[~eval_df[ANNOTATED]].iloc[0]
col1, col2 = st.columns([1, 1])
submit = st.button('Submit')
with col1:
    st.image(str(eval_sample['giga_image']), caption='Giga Image')
    eval_sample = components.common_cols(eval_sample, submit, prefix=GIGA_PREFIX)
with col2:
    st.image(str(eval_sample['vrb_image']), caption='VRB Image')
    eval_sample = components.common_cols(eval_sample, submit, prefix=VRB_PREFIX)

if submit:
    try:
        giga_grasp = [int(s) for s in eval_sample[GIGA_PREFIX + OBJ_MODES].split(',')]
        vrb_grasp = [int(s) for s in eval_sample[VRB_PREFIX + OBJ_MODES].split(',')]
        if len(giga_grasp) != len(vrb_grasp):
            raise ValueError("Lengths of giga and vrb grasps are not the same")
        eval_sample[NUM_SAME] = sum([g > 0 and v > 0 for g, v in zip(giga_grasp, vrb_grasp)])
        eval_df = utils.update_eval_entry(eval_sample, overwrite=True)
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
    except Exception as e:
        st.error(f"An error occurred: {e}")