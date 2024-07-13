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
    spec_lib_files = st.file_uploader(label="Upload Spectral Library", type=[".txt", ".csv", ".tsv", ".xls", ".speclib", ".sptxt", ".msp"], accept_multiple_files=True)
    column1, column2 = st.columns(2)
    with column1:
        if st.button("Add", use_container_width=True, type='primary'):
            for file in spec_lib_files:
                fs.add_spec_lib(selected_project, file.name, file.getvalue().decode("utf-8"))
            st.rerun()
    with column2:
        if st.button("Cancel", use_container_width=True, type='secondary'):
            st.rerun()

if st.button("Upload Spectral Library", use_container_width=True, type='primary'):
    upload_prompt()