import pandas as pd
import streamlit as st

import utils
from config import ANNOTATED, GIGA_PREFIX, VRB_PREFIX
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
utils.update_eval_entry(eval_sample, overwrite=True)

# record number of objects identified by each
# record the number of objects with a grasp for each