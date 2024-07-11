import streamlit as st
import pandas as pd
import numpy as np
from hpc_manager import RemoteProjectFileSystem

from utils import get_fs

st.title("Upload Spectral Library")

fs = get_fs()

selected_project = st.selectbox("Select Project:", options=fs.list_projects())

@st.experimental_dialog("Upload Spectral Library")
def upload_prompt():
    data_file = st.file_uploader(label="Upload Spectral Library", type=[".txt", ".csv", ".tsv", ".xls", ".speclib", ".sptxt", ".msp"])
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Add", use_container_width=True, type='primary'):
            fs.add_spec_lib(selected_project, data_file.name, data_file.getvalue().decode("utf-8"))
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary'):
            st.rerun()

if st.button("Upload Spectral Library", use_container_width=True, type='primary'):
    upload_prompt()